import tensorflow as tf
import numpy as np
import util3
import time

datapath = 'merge10.csv'
title,content = util3.normalize(datapath)
word_to_ix,ix_to_word = util3.make_dict(title + content)

multi = True
forward_only = False
hidden_size = 300
vocab_size = len(ix_to_word)+1#voca_size error
num_layers = 3
learning_rate = 0.001
batch_size = 16
encoder_size = 100
decoder_size = util3.doclength(title, sep=True) # (Maximum) number of time steps in this batch
steps_per_checkpoint = 10

# transform data
encoderinputs, decoderinputs, targets_, targetweights = util3.make_suffle(content, title, word_to_ix, encoder_size=encoder_size, decoder_size=decoder_size, shuffle=False)

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
        self.decoder_inputs = [tf.placeholder(tf.int32, [batch_size]) for _ in range(decoder_size)]
        self.targets = [tf.placeholder(tf.int32, [batch_size]) for _ in range(decoder_size)]
        self.target_weights = [tf.placeholder(tf.float32, [batch_size]) for _ in range(decoder_size)]

        # models
        if multi:
            rnn_cells=[]
            #warning two cells provided to MutltiRNNCell are the same object
            for _ in range(num_layers):
                #single_cell = tf.nn.rnn_cell.GRUCell(num_units=hidden_size)
                single_cell = tf.compat.v1.nn.rnn_cell.LSTMCell(num_units=hidden_size)
                rnn_cells.append(single_cell)
            cell = tf.compat.v1.nn.rnn_cell.MultiRNNCell(rnn_cells)
        else:
            #cell = tf.nn.rnn_cell.GRUCell(num_units=hidden_size)
            cell = tf.compat.v1.nn.rnn_cell.LSTMCell(num_units=hidden_size)

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

sess = tf.Session()
model = seq2seq(multi=multi, hidden_size=hidden_size, num_layers=num_layers,
                    learning_rate=learning_rate, batch_size=batch_size,
                    vocab_size=vocab_size,
                    encoder_size=encoder_size, decoder_size=decoder_size,
                    forward_only=forward_only)
sess.run(tf.compat.v1.global_variables_initializer())#global_variables_initializer()
step_time, loss = 0.0, 0.0
current_step = 0
start = 0
end = batch_size
while current_step < 10000001:

    if end > len(title):
        start = 0
        end = batch_size

    # Get a batch and make a step
    start_time = time.time()
    encoder_inputs, decoder_inputs, targets, target_weights = util3.make_batch(encoderinputs[start:end],decoderinputs[start:end],targets_[start:end],targetweights[start:end])

    if current_step % steps_per_checkpoint == 0:
        for i in range(decoder_size - 2):
            decoder_inputs[i + 1] = np.array([word_to_ix['<PAD>']] * batch_size)
        output_logits = model.step(sess, encoder_inputs, decoder_inputs, targets, target_weights, True)
        predict = [np.argmax(logit, axis=1)[0] for logit in output_logits]
        predict = ' '.join(ix_to_word[ix][0] for ix in predict)
        real = [word[0] for word in targets]
        real = ' '.join(ix_to_word[ix][0] for ix in real)
        print('\n----\n step : %s \n time : %s \n LOSS : %s \n prediction : %s \n edit result : %s \n actual result : %s \n----' %
              (current_step, step_time, loss, predict, real, title[start]))
        loss, step_time = 0.0, 0.0

    step_loss = model.step(sess, encoder_inputs, decoder_inputs, targets, target_weights, False)
    step_time += time.time() - start_time / steps_per_checkpoint
    loss += np.mean(step_loss) / steps_per_checkpoint
    current_step += 1
    start += batch_size
    end += batch_size



