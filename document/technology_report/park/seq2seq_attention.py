# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function, division
from io import open
import unicodedata
import string
import re
import random

import torch
import torch.nn as nn
from torch.autograd import Variable
from torch import optim
import torch.nn.functional as F

use_cuda = torch.cuda.is_available()

SOS_token = "\t"
EOS_token = "\n"


class Lang:
    def __init__(self, name):
        self.name = name
        self.word2index = {}
        self.word2count = {}
        self.index2word = {"\t": "SOS", "\n": "EOS"}
        self.n_words = 2  #  SOS 와 EOS 단어 숫자 포함

    def addSentence(self, sentence):
        for word in sentence.split(' '):
            self.addWord(word)

    def addWord(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.n_words
            self.word2count[word] = 1
            self.index2word[self.n_words] = word
            self.n_words += 1
        else:
            self.word2count[word] += 1


######################################################################
# 파일은 모두 유니 코드로 되어있어 간단하게하기 위해 유니 코드 문자를
# ASCII로 변환하고, 모든 문자를 소문자로 만들고, 대부분의 구두점을
# 지워줍니다.
#

# 유니 코드 문자열을 일반 ASCII로 변환하십시오.
# http://stackoverflow.com/a/518232/2809427 에 감사드립니다.
def unicodeToAscii(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )

# 소문자, 다듬기, 그리고 문자가 아닌 문자 제거


def normalizeString(s):
    s = unicodeToAscii(s.lower().strip())
    s = re.sub(r"([.!?])", r" \1", s)
    s = re.sub(r"[^a-zA-Z.!?]+", r" ", s)
    return s


######################################################################
# 데이터 파일을 읽으려면 파일을 줄로 나누고 줄을 쌍으로 나눕니다.
# 파일은 모두 영어 → 기타 언어이므로 만약 다른 언어 → 영어로
# 번역한다면 쌍을 뒤집도록 ``reverse`` 플래그를 추가했습니다.
#

def readLangs(lang1, lang2, reverse=False):
    print("Reading lines...")

    # Read the file and split into lines
    lines = open('data/%s-%s.txt' % (lang1, lang2), encoding='utf-8').\
        read().strip().split('\n')

    # 모든 줄을 쌍으로 분리하고 정규화 하십시오
    pairs = [[normalizeString(s) for s in l.split('\t')] for l in lines]

    # 쌍을 뒤집고, Lang 인스턴스를 만드십시오
    if reverse:
        pairs = [list(reversed(p)) for p in pairs]
        input_lang = Lang(lang2)
        output_lang = Lang(lang1)
    else:
        input_lang = Lang(lang1)
        output_lang = Lang(lang2)

    return input_lang, output_lang, pairs


######################################################################
# *많은* 예제 문장이 있고 신속하게 학습하기를 원하기 때문에
# 비교적 짧고 간단한 문장으로만 데이터 셋을 정리할 것입니다. 여기서
# 최대 길이는 10 단어 (종료 문장 부호 포함)이며 "I am" 또는
# "He is" 등의 형태로 번역되는 문장으로 필터링됩니다.(이전에
# 아포스트로피는 대체 됨)
#

MAX_LENGTH = 10

eng_prefixes = (
    "i am ", "i m ",
    "he is", "he s ",
    "she is", "she s",
    "you are", "you re ",
    "we are", "we re ",
    "they are", "they re "
)


def filterPair(p):
    return len(p[0].split(' ')) < MAX_LENGTH and \
        len(p[1].split(' ')) < MAX_LENGTH and \
        p[1].startswith(eng_prefixes)


def filterPairs(pairs):
    return [pair for pair in pairs if filterPair(pair)]


######################################################################
# 데이터 준비를 위한 전체 과정:
#
# -  텍스트 파일을 읽고 줄로 분리하고, 줄을 쌍으로 분리합니다.
# -  텍스트를 정규화 하고 길이와 내용으로 필터링 합니다.
# -  쌍의 문장들에서 단어 리스트를 생성합니다.
#

def prepareData(lang1, lang2, reverse=False):
    input_lang, output_lang, pairs = readLangs(lang1, lang2, reverse)
    print("Read %s sentence pairs" % len(pairs))
    pairs = filterPairs(pairs)
    print("Trimmed to %s sentence pairs" % len(pairs))
    print("Counting words...")
    for pair in pairs:
        input_lang.addSentence(pair[0])
        output_lang.addSentence(pair[1])
    print("Counted words:")
    print(input_lang.name, input_lang.n_words)
    print(output_lang.name, output_lang.n_words)
    return input_lang, output_lang, pairs


input_lang, output_lang, pairs = prepareData('eng', 'fra', True)
print(random.choice(pairs))

######################################################################
# 인코더
# -----------
#
# seq2seq 네트워크의 인코더는 입력 문장의 모든 단어에 대해 어떤 값을
# 출력하는 RNN입니다. 모든 입력 단어에 대해 인코더는 벡터와
# hidden state 를 출력하고 다음 입력 단어에 hidden state를 사용합니다.


class EncoderRNN(nn.Module):
    def __init__(self, input_size, hidden_size):
        super(EncoderRNN, self).__init__()
        self.hidden_size = hidden_size

        self.embedding = nn.Embedding(input_size, hidden_size)
        self.gru = nn.GRU(hidden_size, hidden_size)

    def forward(self, input, hidden):
        embedded = self.embedding(input).view(1, 1, -1)
        output = embedded
        output, hidden = self.gru(output, hidden)
        return output, hidden

    def initHidden(self):
        result = Variable(torch.zeros(1, 1, self.hidden_size))
        if use_cuda:
            return result.cuda()
        else:
            return result

######################################################################
# 어텐션 디코더

#
# 문맥 벡터만 인코더와 디코더 사이로 전달 된다면, 단일 벡터가 전체 문장의
# 인코딩 부담을 가지게 됩니다.
# 어텐션은 디코더 네트워크가 자기 출력의 모든 단계에서 인코더 출력의
# 다른 부분에 "집중" 할 수 있게 합니다. 첫째 *어텐션 웨이트* 의 셋을
# 계산합니다. 이것은 가중치 조합을 만들기 위해서 인코더 출력 벡터와
# 곱해집니다. 그 결과 (코드에서 ``attn_applied``)는 입력 시퀀스의
# 특정 부분에 관한 정보를 포함해야하고 따라서 디코더가 알맞은 출력
# 단어를 선택하는 것을 도와줍니다.

# 어텐션 가중치 계산은 디코더의 입력 및 Hidden State를 입력으로
# 사용하는 다른 feed-forwad layer 인 ``attn`` 으로 수행됩니다.
# 학습 데이터에는 모든 크기의 문장이 있기 때문에 이 계층을 실제로
# 만들고 학습시키려면 적용 할 수 있는 최대 문장 길이 (인코더 출력의 입력 길이)를
# 선택해야 합니다. 최대 길이의 문장은 모든 어텐션 가중치를 사용하지만
# 더 짧은 문장은 처음 몇 개만 사용합니다.


class AttnDecoderRNN(nn.Module):
    def __init__(self, hidden_size, output_size, dropout_p=0.1, max_length=MAX_LENGTH):
        super(AttnDecoderRNN, self).__init__()
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.dropout_p = dropout_p
        self.max_length = max_length

        self.embedding = nn.Embedding(self.output_size, self.hidden_size)
        self.attn = nn.Linear(self.hidden_size * 2, self.max_length)
        self.attn_combine = nn.Linear(self.hidden_size * 2, self.hidden_size)
        self.dropout = nn.Dropout(self.dropout_p)
        self.gru = nn.GRU(self.hidden_size, self.hidden_size)
        self.out = nn.Linear(self.hidden_size, self.output_size)

    def forward(self, input, hidden, encoder_outputs):
        embedded = self.embedding(input).view(1, 1, -1)
        embedded = self.dropout(embedded)

        attn_weights = F.softmax(
            self.attn(torch.cat((embedded[0], hidden[0]), 1)), dim=1)
        attn_applied = torch.bmm(attn_weights.unsqueeze(0),
                                 encoder_outputs.unsqueeze(0))

        output = torch.cat((embedded[0], attn_applied[0]), 1)
        output = self.attn_combine(output).unsqueeze(0)

        output = F.relu(output)
        output, hidden = self.gru(output, hidden)

        output = F.log_softmax(self.out(output[0]), dim=1)
        return output, hidden, attn_weights

    def initHidden(self):
        result = Variable(torch.zeros(1, 1, self.hidden_size))
        if use_cuda:
            return result.cuda()
        else:
            return result


######################################################################
# .. Note:: 상대 위치 접근을 이용한 길이 제한을 하는 다른 형태의 어텐션
#   이 있습니다. "local attention"에 관한 자료
#   `Effective Approaches to Attention-based Neural Machine Translation <https://arxiv.org/abs/1508.04025>`__
#   를 읽으십시오
#
# 학습
# ========
#
# 학습 데이터 준비
# -----------------------
#
# 학습을 위해서, 각 쌍마다 입력 Tensor (입력 문장의 단어 주소)와
# 목표 Tensor (목표 문장의 단어 주소)가 필요합니다. 이 벡터들을
# 생성하는 동안 두 시퀀스에 EOS 토큰을 추가 합니다.
#

def indexesFromSentence(lang, sentence):
    return [lang.word2index[word] for word in sentence.split(' ')]


def variableFromSentence(lang, sentence):
    indexes = indexesFromSentence(lang, sentence)
    indexes.append(EOS_token)
    result = Variable(torch.LongTensor(indexes).view(-1, 1))
    if use_cuda:
        return result.cuda()
    else:
        return result


def variablesFromPair(pair):
    input_variable = variableFromSentence(input_lang, pair[0])
    target_variable = variableFromSentence(output_lang, pair[1])
    return (input_variable, target_variable)


######################################################################
# 모델 학습
# ------------------
#
# 학습을 위해서 인코더에 입력 문장을 넣고 모든 출력과 최신 hidden state를
# 추적합니다. 그런 다음 디코더에 첫 번째 입력으로 ``<SOS>`` 토큰과
# 인코더의 마지막 Hidden state가 첫번쩨 Hidden state로 제공됩니다.
#
# "Teacher forcing"은 다음 입력으로 디코더의 예측을 사용하는 대신
# 실제 목표 출력을 다음 입력으로 사용하는 컨셉입니다.
# "Teacher forcing"을 사용하면 수렴이 빨리되지만 `학습된 네트워크가
# 잘못 사용될 때 불안정성을 보입니다
# <http://minds.jacobs-university.de/sites/default/files/uploads/papers/ESNTutorialRev.pdf>`__
#
# teacher-forced 네트워크의 출력이 일관된 문법으로 읽지만 정확한
# 번역과는 거리가 멀다는 것을 볼 수 있습니다. - 직관적으로 출력 문법을
# 표현하는 법을 배우고 교사가 처음 몇 단어를 말하면 의미를 "선택할" 수 있지만
# 번역에서 처음으로 문장을 만드는 법을 잘 배우지 못했습니다.
#
# PyTorch의 autograd 가 제공하는 자유 덕분에 간단한 if 문으로
# teacher forcing 을 사용할지 아니면 사용하지 않을지를 선택할 수 있습니다.
# 더 많은 것을 사용하려면 ``teacher_forcing_ratio`` 를 확인하십시오.
#

teacher_forcing_ratio = 0.5


def train(input_variable, target_variable, encoder, decoder, encoder_optimizer, decoder_optimizer, criterion, max_length=MAX_LENGTH):
    encoder_hidden = encoder.initHidden()

    encoder_optimizer.zero_grad()
    decoder_optimizer.zero_grad()

    input_length = input_variable.size()[0]
    target_length = target_variable.size()[0]

    encoder_outputs = Variable(torch.zeros(max_length, encoder.hidden_size))
    encoder_outputs = encoder_outputs.cuda() if use_cuda else encoder_outputs

    loss = 0

    for ei in range(input_length):
        encoder_output, encoder_hidden = encoder(
            input_variable[ei], encoder_hidden)
        encoder_outputs[ei] = encoder_output[0][0]

    decoder_input = Variable(torch.LongTensor([[SOS_token]]))
    decoder_input = decoder_input.cuda() if use_cuda else decoder_input

    decoder_hidden = encoder_hidden

    use_teacher_forcing = True if random.random() < teacher_forcing_ratio else False

    if use_teacher_forcing:
        # Teacher forcing: 목표를 다음 입력으로 전달
        for di in range(target_length):
            decoder_output, decoder_hidden, decoder_attention = decoder(
                decoder_input, decoder_hidden, encoder_outputs)
            loss += criterion(decoder_output, target_variable[di])
            decoder_input = target_variable[di]  # Teacher forcing

    else:
        # teacher forcing 없이: 자신의 예측을 다음 입력으로 사용
        for di in range(target_length):
            decoder_output, decoder_hidden, decoder_attention = decoder(
                decoder_input, decoder_hidden, encoder_outputs)
            topv, topi = decoder_output.data.topk(1)
            ni = topi[0][0]

            decoder_input = Variable(torch.LongTensor([[ni]]))
            decoder_input = decoder_input.cuda() if use_cuda else decoder_input

            loss += criterion(decoder_output, target_variable[di])
            if ni == EOS_token:
                break

    loss.backward()

    encoder_optimizer.step()
    decoder_optimizer.step()
    #ll=loss.data[0]
    return loss.data.item() / target_length


######################################################################
# 이것은 현재 시간과 진행률%을 고려하여 경과된 시간과 남은 예상
# 시간을 출력하는 헬퍼 함수입니다.
#

import time
import math


def asMinutes(s):
    m = math.floor(s / 60)
    s -= m * 60
    return '%dm %ds' % (m, s)


def timeSince(since, percent):
    now = time.time()
    s = now - since
    es = s / (percent)
    rs = es - s
    return '%s (- %s)' % (asMinutes(s), asMinutes(rs))


######################################################################
# 전체 학습 과정
#
# -  타이머 시작
# -  optimizers와 criterion 초기화
# -  학습 쌍의 세트 생성,여러 번 ``train`` 을 호출하며 때로는 진행률
# (예제의 %, 현재까지의 예상 시간)과 평균 손실을 출력합니다.
#

def trainIters(encoder, decoder, n_iters, print_every=1000, plot_every=100, learning_rate=0.01):
    start = time.time()
    plot_losses = []
    print_loss_total = 0  # 매 print_every 마다 초기화
    plot_loss_total = 0   # 매 plot_every 마다 초기화

    encoder_optimizer = optim.SGD(encoder.parameters(), lr=learning_rate)
    decoder_optimizer = optim.SGD(decoder.parameters(), lr=learning_rate)
    training_pairs = [variablesFromPair(random.choice(pairs))
                      for i in range(n_iters)]
    criterion = nn.NLLLoss()

    for iter in range(1, n_iters + 1):
        training_pair = training_pairs[iter - 1]
        input_variable = training_pair[0]
        target_variable = training_pair[1]

        loss = train(input_variable, target_variable, encoder,
                     decoder, encoder_optimizer, decoder_optimizer, criterion)
        print_loss_total += loss
        plot_loss_total += loss

        if iter % print_every == 0:
            print_loss_avg = print_loss_total / print_every
            print_loss_total = 0
            print('%s (%d %d%%) %.4f' % (timeSince(start, iter / n_iters),
                                         iter, iter / n_iters * 100, print_loss_avg))

        if iter % plot_every == 0:
            plot_loss_avg = plot_loss_total / plot_every
            plot_losses.append(plot_loss_avg)
            plot_loss_total = 0


######################################################################
# 평가
# ==========
#
# 평가는 대부분 학습과 동일하지만 목표가 없으므로 각 단계마다 디코더의예측을 되돌려 전달합니다.
# 단어를 예측할 때마다 그 단어를 출력 문자열에 추가합니다.
# 만약 EOS 토큰을 예측하면 거기에서 멈춥니다.


def evaluate(encoder, decoder, sentence, max_length=MAX_LENGTH):
    input_variable = variableFromSentence(input_lang, sentence)
    input_length = input_variable.size()[0]
    encoder_hidden = encoder.initHidden()

    encoder_outputs = Variable(torch.zeros(max_length, encoder.hidden_size))
    encoder_outputs = encoder_outputs.cuda() if use_cuda else encoder_outputs

    for ei in range(input_length):
        encoder_output, encoder_hidden = encoder(input_variable[ei],
                                                 encoder_hidden)
        encoder_outputs[ei] = encoder_outputs[ei] + encoder_output[0][0]

    decoder_input = Variable(torch.LongTensor([[SOS_token]]))  # SOS
    decoder_input = decoder_input.cuda() if use_cuda else decoder_input

    decoder_hidden = encoder_hidden

    decoded_words = []
    decoder_attentions = torch.zeros(max_length, max_length)

    for di in range(max_length):
        decoder_output, decoder_hidden, decoder_attention = decoder(
            decoder_input, decoder_hidden, encoder_outputs)
        decoder_attentions[di] = decoder_attention.data
        topv, topi = decoder_output.data.topk(1)
        ni = topi[0][0]
        if ni == EOS_token:
            decoded_words.append('<EOS>')
            break
        else:
            decoded_words.append(output_lang.index2word[ni])

        decoder_input = Variable(torch.LongTensor([[ni]]))
        decoder_input = decoder_input.cuda() if use_cuda else decoder_input

    return decoded_words, decoder_attentions[:di + 1]


######################################################################
# 학습 세트에 있는 임의의 문장을 평가하고
# 입력, 목표 및 출력을 출력하여 주관적인 품질 판단을 내릴 수 있습니다::

def evaluateRandomly(encoder, decoder, n=10):
    for i in range(n):
        pair = random.choice(pairs)
        print('>', pair[0])
        print('=', pair[1])
        output_words, attentions = evaluate(encoder, decoder, pair[0])
        output_sentence = ' '.join(output_words)
        print('<', output_sentence)
        print('')


######################################################################
# 학습과 평가

# 이러한 모든 헬퍼 함수를 이용해서 (추가 작업처럼 보이지만 여러 실험을
# 더 쉽게 수행 할 수 있음) 실제로 네트워크를 초기화하고 학습을
# 시작할 수 있습니다.

# 입력 문장은 많이 필터링되었음을 기억하십시오. 이 작은 데이터 세트의
# 경우 256 개의 hidden node

hidden_size = 256
encoder1 = EncoderRNN(input_lang.n_words, hidden_size)
attn_decoder1 = AttnDecoderRNN(hidden_size, output_lang.n_words, dropout_p=0.1)


if use_cuda:
    encoder1 = encoder1.cuda()
    attn_decoder1 = attn_decoder1.cuda()

trainIters(encoder1, attn_decoder1, 75000, print_every=5000)

######################################################################
#

evaluateRandomly(encoder1, attn_decoder1)

