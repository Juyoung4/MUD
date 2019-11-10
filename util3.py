from konlpy.tag import Mecab
import csv
import os
import re
import numpy as np
from collections import Counter
#stopword
stopwords = ['가운데', '대체로', '간의', '크게', '같', '아니', '있', '되', '두', '받', '많', '크', '좋', '따르', '만들', '시키', '그러', '하나','모르', '데', '자신', '어떤', '명', '앞', '번', '보이', '나', '어떻', '월', '들', '이렇', '점', '싶', '좀', '잘', '통하', '놓','란', '이나', '것', '이', '그', '수', '등', '의', '때', '경우', '및', '를', '대한', '사용', '위', '때문', '약', '제', '후','다른', '중', '이상', '일', '은', '위해', '가지', '시', '로', '세', '과', '다음', '두', '더', '또한', '함', '하나', '우리', '개','관', '속', '가장', '모두', '점', '곳', '전', '또', '통해', '여러', '대해', '안', '즉', '모든', '내', '뒤', '보고', '이후', '데','로서', '다시', '관련', '알', '비', '그것', '나', '일반', '각', '뜻', '정도', '사이', '사실', '도', '따라서', '고', '못', '예', '간', '동안', '매우', '정', '지금', '증', '임', '공', '해', '음', '앞', '번', '볼', '여기', '거나', '자', '부', '인', '날','바로', '대부분', '기', '바', '주로', '뿐', '직접', '부터', '계속', '일부', '주', '재', '아래', '더욱', '초', '각각', '동시', '권','년', '곧', '온', '거의', '먼저', '비롯', '역시', '몇', '반드시', '거', '보', '단', '듯', '가장', '서로', '모든', '에 대한 ',' 수 ', '모두', '의', '에', '대해', '그런데', '으로', '이것', '대로', '것', '그대로', '그리고', '것도', '수가', '이 ', '해야', '지금','할 수가', '할 수', '각종', '요게', '여기', '혹시', '우리', '한번', '이번', '당신', '이렇게', '차고', '어떻게', '뭐', '깜짝', '거지','싶어서', '그래서', '정말', '이런', '도저히', '거죠', '하면은', '이제', '그렇게', '그럼', '많이', '이거', '그거', '저거', '누가', '그래', '그냥', '바로', '누가', '다시', '그래도', '간단히', '거야', '이따', '00', '근데', '결국', '이때', '누가', '그런', '딱', '일단', '보면','하나', '어디', '부터', '원', '위하', '나오', '중', '못하', '그렇', '오', '대하', '한', '지', '하']

def normalize(datapath):
    #csv file save
    os.chdir("./")
    doc_ko=open('merge12.csv','w',encoding='utf_8_sig', newline="")
    wcsv = csv.writer(doc_ko)

    #mecab tokenize
    m = Mecab()

    #file1 = open('merge10.csv','r',encoding='utf_8_sig')
    file1 = open(datapath,'r',encoding='utf_8_sig')
    line = csv.reader(file1)

    title,content,title1,content1,title2,content2=[],[],[],[],[],[]
    m_title,m_content=[],[]
    count=1
    temp=''
    for i in line:
        hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')
        i[0] = hangul.sub('',i[0])
        i[1] = hangul.sub('',i[1])

        m_title.append(m.morphs(i[0]))
        m_content.append(m.morphs(i[1]))
        #stop word delete
        for w in m_title:
            if w not in stopwords:
                title.append(w)
        for p in m_content:
            if p not in stopwords:
                content.append(p)

        title1 = ' '.join(title[0])
        title2.append(title1)
        content1 = ' '.join(content[0])
        content2.append(content1)
        temp=content1
        wcsv.writerow([title1,content1])

        title1,content1='',''
        title,content,title1,content1,=[],[],[],[]
        m_title,m_content=[],[] 

        if count == 20000:
            break
        else:
            count += 1
    len(title2+content2)
    return title2,content2

# word_to_ix, ix_to_word 생성
def make_dict(contents):
    content=[]
    for i in contents:
        for word in i.split():
            content.append(word)
    #print(content[:3])
    vocab=Counter(content)
    #print(vocab)
    vocab = Counter(content)
    maxn = max(vocab.values())
    vocab['<PAD>']=maxn+1
    vocab['<S>'] = maxn + 2
    vocab['<E>'] = maxn + 3
    vocab['<UNK>'] = maxn + 4
    #print(vocab['<PAD>'])
    ix_to_word = {ch: i for i, ch in vocab.items()}

    word_to_ix = vocab
    counte=0
    for i,k in ix_to_word.items():
        if counte == 5:break
        counte += 1
        print("ix_to_word: {",i,": ",k,"}")
    counte=0
    for i,k in word_to_ix.items():
        if counte == 5: break
        counte += 1
        print("word_to_ix: {",i,": ",k,"}")

    print('contents number: %s, voca numbers: %s' %(len(contents),len(ix_to_word)))
    return word_to_ix,ix_to_word

def make_suffle(rawinputs, rawtargets, word_to_ix, encoder_size, decoder_size, shuffle=True):
    rawinputs = np.array(rawinputs)
    rawtargets = np.array(rawtargets)
    if shuffle:
        shuffle_indices = np.random.permutation(np.arange(len(rawinputs)))
        rawinputs = rawinputs[shuffle_indices]
        rawtargets = rawtargets[shuffle_indices]
    encoder_input = []
    decoder_input = []
    targets = []
    target_weights = []
    for rawinput, rawtarget in zip(rawinputs, rawtargets):
        tmp_encoder_input = [word_to_ix[v] for idx, v in enumerate(rawinput.split()) if idx < encoder_size and v in word_to_ix]
        encoder_padd_size = max(encoder_size - len(tmp_encoder_input), 0)
        encoder_padd = [word_to_ix['<PAD>']] * encoder_padd_size
        encoder_input.append(list(reversed(tmp_encoder_input + encoder_padd)))
        tmp_decoder_input = [word_to_ix[v] for idx, v in enumerate(rawtarget.split()) if idx < decoder_size - 1 and v in word_to_ix]
        decoder_padd_size = decoder_size - len(tmp_decoder_input) - 1
        decoder_padd = [word_to_ix['<PAD>']] * decoder_padd_size
        decoder_input.append([word_to_ix['<S>']] + tmp_decoder_input + decoder_padd)
        targets.append(tmp_decoder_input + [word_to_ix['<E>']] + decoder_padd)
        tmp_targets_weight = np.ones(decoder_size, dtype=np.float32)
        tmp_targets_weight[-decoder_padd_size:] = 0
        target_weights.append(list(tmp_targets_weight))
    return encoder_input, decoder_input, targets, target_weights

def doclength(docs,sep=True):
    max_document_length = 0
    for doc in docs:
        if sep:
            words = doc.split()
            document_length = len(words)
        else:
            document_length = len(doc)
        if document_length > max_document_length:
            max_document_length = document_length
    return max_document_length

def make_batch(encoder_inputs, decoder_inputs, targets, target_weights):
    encoder_size = len(encoder_inputs[0])
    decoder_size = len(decoder_inputs[0])
    encoder_inputs, decoder_inputs, targets, target_weights = np.array(encoder_inputs), np.array(decoder_inputs), np.array(targets), np.array(target_weights)
    result_encoder_inputs = []
    result_decoder_inputs = []
    result_targets = []
    result_target_weights = []
    for i in range(encoder_size):
        result_encoder_inputs.append(encoder_inputs[:, i])
    for j in range(decoder_size):
        result_decoder_inputs.append(decoder_inputs[:, j])
        result_targets.append(targets[:, j])
        result_target_weights.append(target_weights[:, j])
    return result_encoder_inputs, result_decoder_inputs, result_targets, result_target_weights

