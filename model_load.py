
import pickle

from normalizing import normalize
import tensorflow as tf
import numpy as np


def make_suffle(content,word_to_ix,encoder_size=100):
    tmp=[] 
    content=normalize(content)
    tmp.append(content)
    content = np.array(tmp)
    
    encoder_input=[]
    
    tmp_encoder_input=[word_to_ix[v] for idx,v in enumerate(content[0].split()) if idx < encoder_size and v in word_to_ix]
    encoder_padd_size=max(encoder_size - len(tmp_encoder_input),0)
    encoder_padd = [word_to_ix['<PAD>']] * encoder_padd_size
    for i in range(len(256)):
        encoder_input.append(list(reversed(tmp_encoder_input+encoder_padd)))
    
    return encoder_input

def make_batch(encoder_inputs):
    encoder_size = len(encoder_inputs[0])
    encoder_inputs = np.array(encoder_inputs)
    result_encoder_inputs=[]
    for i in range(encoder_size):
        result_encoder_inputs.append(encoder_inputs[:,i])
    return result_encoder_inputs
    

if __name__ == '__main__':
   
    with open("ix_to_word.pickle", "rb") as f:
        ix_to_word = pickle.load(f)
    with open("word_to_ix.pickle", "rb") as t:
        word_to_ix = pickle.load(t)
    
    content="특정경제범죄 가중처벌 등에 관한 법률' 특경가법 위반 등 4가지다.하지만 은행은 특경가법 위반을 보지 않고 인터넷은행과 저축은행은 이 법 위반도 대주주 결격 사유다. 금융지배구조법에도 특경가법은 없었지만 정부는 2018년 9월 '특경가법 위반'을 포함시키는 개정안을 제출해 둔 상태다.인터넷은행법 개정안과 금융지배구조법 개정안이 통과되면 인터넷은행은 공정거래법 위반이 제외되고 2금융권은 공정거래법은 유지되고 특경가법 위반이 추가된다. 은행은 대주주 결격사유에 '특경가법'이 없고 '공정거래법'은 있는 중간 형태가 된다."
    end = 256
    encoderinputs=make_suffle(content,word_to_ix)
    vocab_size=len(ix_to_word)+1
    
    with tf.compat.v1.Session() as sess:
        print("Loading saved model")
        sess.run(tf.compat.v1.global_variables_initializer())

        model = seq2seq(multi=True, hidden_size=300, num_layers=3,learning_rate=0.001, batch_size=256,vocab_size=vocab_size,encoder_size=100,decoder_size=18,forward_only=False)
        saver = tf.train.Saver()
        ckpt = tf.train.get_checkpoint_state("./model/")
        saver.restore(sess, ckpt.model_checkpoint_path) 
       
        encoder_inputs = make_batch(encoderinputs[0:end])
        output_logits = model.step(sess,encoder_inputs,[],[],[],False)
        predict = [np.argmax(logit,axis=1)[0] for logit in output_logits]
        predict = ' '.join(ix_to_word[ix] for ix in predit)
        print(predict)
