from train2 import seq2seq
import pickle

from normalizing import normalize
import tensorflow as tf
import numpy as np


def make_suffle(content,word_to_ix,encoder_size=100):
    content=normalize(content)
    content = np.array(content)
    encoder_input=[]
    tmp_encoder_size=[word_to_ix[v] for v in content.split() if idx < encdoer_size and v in word_to_ix]
    encdoer_padd_size=max(encoder_size - len(tmp_encoder_size),0)
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
    
    content="""대주주 심사시 공정거래법 위반을 삭제하는 인터넷전문은행법 개정안을 계기로 금융권 전체 대주주 적격성 심사를 재정비해야 한다는 지적이 나오기 시작했다.각 업권별로 대주주 적격성을 심사하는 근거법이 다르고 근거법마다 결격 사유가 되는 위반 법률도 통일성이 없기 때문이다. 또 인터넷은행법은 지속적으로 대주주 자격을 완화하는 반면 금융지배구조법은 강화되는 등 방향성도 엇갈리고 있다.2일 금융권에 따르면 국회 법제사법위원회에 계류 중인 인터넷은행법 개정안은 대주주 결격 사유 중 공정거래법 위반을 제외하는 내용이다. 개정안이 국회를 통과하면 인터넷은행법은 금융회사에 대한 대주주 적격성 심사시 '공정거래법 위반'을 보지 않는 유일한 법이 된다.현재 금융회사에 대한 대주주 적격성 심사는 업권별로 근거법이 다르다. 은행과 인터넷은행, 저축은행은 개별 업권법에 따라 진행되고 보험, 증권 등 나머지 금융업종은 금융지배구조법에 따른다. 각 법률에서 금융회사 대주주의 결격 사유가 되는 사유는 금융 관련 법, 조세범 처벌법, 공정거래법, '특정경제범죄 가중처벌 등에 관한 법률'(특경가법) 위반 등 4가지다.하지만 은행은 특경가법 위반을 보지 않고 인터넷은행과 저축은행은 이 법 위반도 대주주 결격 사유다. 금융지배구조법에도 특경가법은 없었지만 정부는 2018년 9월 '특경가법 위반'을 포함시키는 개정안을 제출해 둔 상태다.인터넷은행법 개정안과 금융지배구조법 개정안이 통과되면 인터넷은행은 공정거래법 위반이 제외되고 2금융권은 공정거래법은 유지되고 특경가법 위반이 추가된다. 은행은 대주주 결격사유에 '특경가법'이 없고 '공정거래법'은 있는 중간 형태가 된다. """
    
    encoderinputs=make_suffle(content,word_to_ix)
    
    with tf.compat.v1.Session() as sess:
        print("Loading saved model")
 
        model = seq2seq(multi=True, hidden_size=300, num_layers=3,learning_rate=0.001, batch_size=500,vocab_size=vocab_size,encoder_size=encoder_size,decoder_size=decoder_size,forward_only=forward_only)

        sess.run(tf.compat.v1.global_variables_initializer())

        saver = tf.train.Saver(tf.global_variables())
        ckpt = tf.train.get_checkpoint_state("./model/")
        saver.restore(sess, ckpt.model_checkpoint_path)
       
        encoder_inputs = make_batch(encoderinputs[0:batch_size])
        output_logits = model.step(sess,encoder_inputs,[],[],[],False)
        predict = [np.argmax(logit,axis=1)[0] for logit in output_logits]
        predict = ' '.join(ix_to_word[ix] for ix in predit)
        print(predict)
