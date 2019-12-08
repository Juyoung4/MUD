import tensorflow as tf
import numpy as np
import time
import os
import pickle

from normalizing import normalize
import tensorflow as tf
import numpy as np


def make_suffle(content,word_to_ix,encoder_size=100,decoder_size=18):
    tmp=[] 
    content=normalize(content)
    tmp.append(content)
    content = np.array(tmp)
    
     
    encoder_input=[]
    
    tmp_encoder_input=[word_to_ix[v] for idx,v in enumerate(content[0].split()) if idx < encoder_size and v in word_to_ix]
    encoder_padd_size=max(encoder_size - len(tmp_encoder_input),0)
    encoder_padd = [word_to_ix['<PAD>']] * encoder_padd_size
    encoder_input.append(list(reversed(tmp_encoder_input+encoder_padd)))

    return encoder_input
    

def make_batch(encoder_inputs, decoder_inputs, targets, target_weights):
    
    
    encoder_size = len(encoder_inputs[0])
    decoder_size = len(decoder_inputs[0])
    
    encoder_inputs = np.array(encoder_inputs)
    result_encoder_inputs = []
    result_decoder_inputs = []
    result_targets = []
    result_target_weights = []
    encoder_inputs, decoder_inputs, targets, target_weights = np.array(encoder_inputs), np.array(decoder_inputs), np.array(targets), np.array(target_weights)
    for i in range(encoder_size):
        result_encoder_inputs.append(encoder_inputs[:, i])
    
    for j in range(decoder_size):
        result_decoder_inputs.append(decoder_inputs[:, j])
        result_targets.append(targets[:, j])
        result_target_weights.append(target_weights[:, j])
    return result_encoder_inputs, result_decoder_inputs, result_targets, result_target_weights


class seq2seq_attention(object):

    def __init__(self, multi, hidden_size, num_layers, forward_only,learning_rate, batch_size,vocab_size, encoder_size, decoder_size):

        # variables
        self.source_vocab_size = vocab_size
        self.target_vocab_size = vocab_size
        self.batch_size = batch_size
        self.encoder_size = encoder_size
        self.decoder_size = decoder_size
        self.learning_rate = tf.Variable(float(learning_rate), trainable=False)
        self.global_step = tf.Variable(0, trainable=False)

        # networks
        W = tf.Variable(tf.random.normal([hidden_size, vocab_size]))
        #W = tf.Variable(tf.random_normal([hidden_size, vocab_size]))
        #b = tf.Variable(tf.random_normal([vocab_size]))
        b = tf.Variable(tf.random.normal([vocab_size]))
        output_projection = (W, b)
        #tf.placeholder(tf.int32, [batch_size]) 
        self.encoder_inputs = [tf.compat.v1.placeholder(tf.int32, [batch_size]) for _ in range(encoder_size)]  # 인덱스만 있는 데이터 (원핫 인코딩 미시행)
        self.decoder_inputs = [tf.compat.v1.placeholder(tf.int32, [batch_size]) for _ in range(decoder_size)]
        self.targets = [tf.compat.v1.placeholder(tf.int32, [batch_size]) for _ in range(decoder_size)]
        self.target_weights = [tf.compat.v1.placeholder(tf.float32, [batch_size]) for _ in range(decoder_size)]

        # models
        if multi:
            rnn_cells=[]
            #warning two cells provided to MutltiRNNCell are the same object
            for _ in range(num_layers):
                #single_cell = tf.nn.rnn_cell.GRUCell(num_units=hidden_size)
                #tf.compat.v1.nn.rnn_cell.LSTMCell
                single_cell = tf.compat.v1.nn.rnn_cell.GRUCell(num_units=hidden_size)
                rnn_cells.append(single_cell)
                #tf.compat.v1.nn.rnn_cell.MultiRNNCell
            cell = tf.compat.v1.nn.rnn_cell.MultiRNNCell(rnn_cells)
        else:
            cell = tf.compat.v1.nn.rnn_cell.GRUCell(num_units=hidden_size)
            #cell = tf.keras.layers.LSTMCell(units=hidden_size)

        if not forward_only:
            #tf.nn.seq2seq.embedding_attention_seq2seq(
            self.outputs, self.states = tf.contrib.legacy_seq2seq.embedding_attention_seq2seq(
                self.encoder_inputs, self.decoder_inputs, cell,
                num_encoder_symbols=vocab_size,
                num_decoder_symbols=vocab_size,
                embedding_size=hidden_size,
                output_projection=output_projection,
                feed_previous=False)

            self.logits = [tf.matmul(output, output_projection[0]) + output_projection[1] for output in self.outputs]
            self.loss = []
            for logit, target, target_weight in zip(self.logits, self.targets, self.target_weights):
                crossentropy = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=logit, labels=target)
                self.loss.append(crossentropy * target_weight)
            self.cost = tf.add_n(self.loss)#tf.train.AdamOptimizer(learning_rate)
            self.train_op = tf.compat.v1.train.AdamOptimizer(learning_rate).minimize(self.cost)


        else:
            self.outputs, self.states = tf.contrib.legacy_seq2seq.embedding_attention_seq2seq(
                self.encoder_inputs, self.decoder_inputs, cell,
                num_encoder_symbols=vocab_size,
                num_decoder_symbols=vocab_size,
                embedding_size=hidden_size,
                output_projection=output_projection,
                feed_previous=True)
            self.logits = [tf.matmul(output, output_projection[0]) + output_projection[1] for output in self.outputs]

    def step(self, session, encoderinputs, decoderinputs, targets, targetweights, forward_only):
        input_feed = {}
        for l in range(len(encoderinputs)):
            input_feed[self.encoder_inputs[l].name] = encoderinputs[l]
            for l in range(len(decoderinputs)):
                input_feed[self.decoder_inputs[l].name] = decoderinputs[l]
                input_feed[self.targets[l].name] = targets[l]
                input_feed[self.target_weights[l].name] = targetweights[l]
        if not forward_only:
            output_feed = [self.train_op, self.cost]
        else:
            output_feed = []
            for l in range(len(decoderinputs)):
                output_feed.append(self.logits[l])
        output = session.run(output_feed,input_feed)
        if not forward_only:
            return output[1] # loss
        else:
            return output[0:] # outputs


if __name__ == '__main__':
    with open("ix_to_word.pickle", "rb") as f:
        ix_to_word = pickle.load(f)
    with open("word_to_ix.pickle", "rb") as t:
        word_to_ix = pickle.load(t)
    
    multi = True
    
    hidden_size = 300
    vocab_size = len(ix_to_word)+1#voca_size error
    num_layers = 3
    learning_rate = 0.001
    batch_size = 1
    encoder_size = 100
    decoder_size = 18
    
    content="박근혜 정부 시절 우병우 전 청와대 민정수석비서관과 함께 국가정보원의 불법사찰에 관여한 혐의를 받는 최윤수 50 전 국정원 2차장의 구속 여부가 이르면 1일 밤 결정된다. 우 전 수석은 30일 새벽 검찰 소환 조사를 마치고 나오는 길에 최 전 차장의 구속영장 청구 소식과 관련한 질문을 받고 가슴이 아프다 며 잘되기를 바란다 고 말하기도 했다. 한편 검찰은 최 전 차장의 구속 여부가 판가름나는 대로 조만간 우 전 수석의 혐의 내용을 보강 조사해 이르면 내주 초 우 전 수석의 구속영장을 청구한다는 방침이다."
    end = 1
    encoderinputs=make_suffle(content,word_to_ix) # padding 
    print(encoderinputs)
    print(type(encoderinputs))
    with tf.compat.v1.Session() as sess:
        print("Loading saved model")
        model = seq2seq_attention(multi=True, hidden_size=300, num_layers=3,learning_rate=0.001, batch_size=1,vocab_size=vocab_size,encoder_size=100,decoder_size=15,forward_only=True)
        sess.run(tf.compat.v1.global_variables_initializer())
        saver = tf.train.Saver()
        ckpt = tf.train.get_checkpoint_state("./model/")
        saver.restore(sess, ckpt.model_checkpoint_path)
        d=[]
        print([0]*15)
        d.append([0]*15)
        print(d)
        encoder_inputs, decoder_inputs, targets, target_weights = make_batch(encoderinputs[0:end],d,d,d)
        print(encoder_inputs)
        
        
        output_logits = model.step(sess,encoder_inputs,decoder_inputs,targets,target_weights,True)
        predict = [np.argmax(logit,axis=1)[0] for logit in output_logits]
        predict = ' '.join(ix_to_word[ix] for ix in predict)
        print(predict)

