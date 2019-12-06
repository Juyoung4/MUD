import tensorflow as tf
import numpy as np
import os
#import import_ipynb
#from utils import loading,make_dict,make_suffle,doclength,make_batch
#from test import load
import time
class seq2seq(object):

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
        for l in range(len(encoder_inputs)):
            input_feed[self.encoder_inputs[l].name] = encoderinputs[l]
        for l in range(len(decoder_inputs)):
            input_feed[self.decoder_inputs[l].name] = decoderinputs[l]
            input_feed[self.targets[l].name] = targets[l]
            input_feed[self.target_weights[l].name] = targetweights[l]
        if not forward_only:
            output_feed = [self.train_op, self.cost]
        else:
            output_feed = []
            for l in range(len(decoder_inputs)):
                output_feed.append(self.logits[l])
        output = session.run(output_feed, input_feed)
        if not forward_only:
            return output[1] # loss
        else:
            return output[0:] # outputs
 ########################       
import import_ipynb
import tensorflow as tf
import numpy as np
import time
import os
import pickle

import import_ipynb
from normalizing import normalize
import tensorflow as tf
import numpy as np

def make_3word(content):
    raw_content=""
    for word in content.split():
        if len(word) > 0:
            normalizedword = word[:3]
            tmp = []
            for char in normalizedword:
                if ord(char) < 12593 or ord(char) > 12643:
                    tmp.append(char)
            normalizedword = ''.join(char for char in tmp)
            raw_content += normalizedword+" "
    return raw_content

def make_suffle2(content,word_to_ix,encoder_size=100,decoder_size=18):
    tmp=[] 
    tmp.append(content)
    content = np.array(tmp)
    
     
    encoder_input=[]
    
    tmp_encoder_input=[word_to_ix[v] for idx,v in enumerate(content[0].split()) if idx < encoder_size and v in word_to_ix]
    encoder_padd_size=max(encoder_size - len(tmp_encoder_input),0)
    encoder_padd = [word_to_ix['<PAD>']] * encoder_padd_size
    encoder_input.append(list(reversed(tmp_encoder_input+encoder_padd)))

    return encoder_input
#############################################
if __name__ == "__main__":
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    #sess = tf.compat.v1.Session()
    args1=input("input train or test:")

    ########test#########################
    if args1 == "test":
        tf.reset_default_graph()
        multi = True
        forward_only = False
        hidden_size = 150
        num_layers = 3
        learning_rate = 0.001
        batch_size = 16
        encoder_size = 100
        decoder_size = 15
        
    #     with open("ix_to_word.pickle", "rb") as f:
    #         ix_to_word = pickle.load(f)
        with open("word_to_ix.pickle", "rb") as t:
            word_to_ix = pickle.load(t)
        content = """6일 통신업계에 따르면 이동통신사들이 '구독형 유료 멤버십' 형태로 자사 가입고객에게 추가 혜택을 제공하는 상품을 출시하고 있다. 
        이통사들은 통신서비스 외에 쇼핑, 여행 등 이용시 다양한 할인 등 추가적인 혜택을 제공하는 멤버십을 운영해 왔다. 
        이통 가입자 1위 사업자인 SK텔레콤의 마케팅비용은 지난 3분기 7천878억원에 달했다"""
        end = 1
        content=normalize(content)
        content=make_3word(content)
        vocab_size = len(content.split())+1
        encoderinputs=make_suffle2(content,word_to_ix) # padding
        
        if not os.path.exists("mm/copy_model"):
            os.mkdir("mm/copy_model")
        else:
            if os.path.exists("mm/copy_model/checkpoint"):
                old_model_checkpoint_path = open('mm/copy_model/checkpoint','r')
                old_model_checkpoint_path = "".join(["model/",old_model_checkpoint_path.read().splitlines()[0].split('"')[1]]) 
        
        with tf.compat.v1.Session() as sess:

            print("continuing from previous trained model: ",old_model_checkpoint_path, "...")
            #saver.restore(sess, old_model_checkpoint_path)
            model = seq2seq(multi=multi, hidden_size=hidden_size, num_layers=num_layers,
                        learning_rate=learning_rate, batch_size=batch_size,
                        vocab_size=vocab_size,
                        encoder_size=encoder_size, decoder_size=decoder_size,
                        forward_only=True)

            saver = tf.train.Saver(tf.global_variables())
            ckpt = tf.train.get_checkpoint_state("./mm/copy_model/")
            saver.restore(sess, ckpt.model_checkpoint_path)
            d=[]
            print([0]*15)
            d.append([0]*15)
            print(d)
            encoder_inputs, decoder_inputs, targets, target_weights = make_batch(encoderinputs[0:end],d,d,d)
            print(encoder_inputs)

            sess.run()
            output_logits = model.step(sess,encoder_inputs,decoder_inputs,targets,target_weights,True)
            predict = [np.argmax(logit,axis=1)[0] for logit in output_logits]
            predict = ' '.join(ix_to_word[ix] for ix in predict)
            print(predict)
    #######train################
    elif args1 == "train":
        data_path = './jp1.csv'
        title,content = loading(data_path,eng=False, num=True, punc=False)
        word_to_ix,ix_to_word = make_dict(title + content, minlength=0, maxlength=3,jamo_delete=True)
        
        multi = True
        forward_only = False
        hidden_size = 150
        vocab_size = len(ix_to_word)+1
        num_layers = 3
        learning_rate = 0.001
        batch_size = 16
        encoder_size = 100
        decoder_size = doclength(title, sep=True)
        #decoder_size = util3.doclength(title, sep=True) # (Maximum) number of time steps in this batch
        steps_per_checkpoint = 500
        
        # transform data
        encoderinputs, decoderinputs, targets_, targetweights = make_suffle(content, title, word_to_ix, encoder_size=encoder_size, decoder_size=decoder_size, shuffle=False)
           
        if not os.path.exists("mm/copy_model"):
            os.mkdir("mm/copy_model")
        else:
            if os.path.exists("mm/copy_model/checkpoint"):
                old_model_checkpoint_path = open('mm/copy_model/checkpoint','r')
                old_model_checkpoint_path = "".join(["model/",old_model_checkpoint_path.read().splitlines()[0].split('"')[1]]) 
        
        with tf.compat.v1.Session(config=config) as sess:
            model = seq2seq(multi=multi, hidden_size=hidden_size, num_layers=num_layers,
                        learning_rate=learning_rate, batch_size=batch_size,
                        vocab_size=vocab_size,
                        encoder_size=encoder_size, decoder_size=decoder_size,
                        forward_only=forward_only)

            sess.run(global_variables_initializer())#global_variables_initializer()
            saver = tf.compat.v1.train.Saver(tf.compat.v1.global_variables())
            step_time, loss = 0.0, 0.0
            current_step = 0
            start = 0
            end = batch_size
            while current_step < 200001:

                if end > len(title):
                    start = 0
                    end = batch_size

                # Get a batch and make a step
                start_time = time.time()
                encoder_inputs, decoder_inputs, targets, target_weights = make_batch(encoderinputs[start:end],decoderinputs[start:end],targets_[start:end],targetweights[start:end])

                if current_step % steps_per_checkpoint == 0:
                    for i in range(decoder_size - 2):
                        decoder_inputs[i + 1] = np.array([word_to_ix['<PAD>']] * batch_size)
                    output_logits = model.step(sess, encoder_inputs, decoder_inputs, targets, target_weights, True)
                    predict = [np.argmax(logit, axis=1)[0] for logit in output_logits]
                    predict = ' '.join(ix_to_word[ix] for ix in predict)
                    real = [word[0] for word in targets]
                    real = ' '.join(ix_to_word[ix][0] for ix in real)
                    saver.save(sess, "./mm/copy_model/model.ckpt",global_step=current_step)
                    print('\n----\n step : %s \n time : %s \n LOSS : %s \n prediction : %s \n edit result : %s \n actual result : %s \n----' %
                          (current_step, step_time, loss, predict, real, title[start]))
                    loss, step_time = 0.0, 0.0

                step_loss = model.step(sess, encoder_inputs, decoder_inputs, targets, target_weights, False)
                step_time += time.time() - start_time / steps_per_checkpoint
                loss += np.mean(step_loss) / steps_per_checkpoint
                current_step += 1
                start += batch_size
                end += batch_size
             save_path = saver.save(sess, 'model.pd')    

