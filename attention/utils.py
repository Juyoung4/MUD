import re
import numpy as np
import pickle


from gensim.models.keyedvectors import KeyedVectors
from gensim.test.utils import get_tmpfile
from gensim.scripts.glove2word2vec import glove2word2vec

import operator
from collections import defaultdict
import collections
import os
import csv
from konlpy.tag import Twitter;t=Twitter()#tokens_ko=t.morphs(doc_ko)
from normalizing import normalize

#각 파일 불러오기
train_content_path= '../content.csv'
train_title_path = '../title.csv'
valid_content_path ='../test_content.csv'
valid_title_path ='../test_title.csv'

def clean_str(sentence):
    sentence = re.sub("[#.]+", "#", sentence)
    return sentence

def get_text_list(data_path,toy):
    with open (data_path, "r", encoding="utf-8") as f:
        if not toy:
            return [clean_str(x.strip()) for x in f.readlines()]
        else:
            return [clean_str(x.strip()) for x in f.readlines()]
            
def build_dict(step, toy=False):
    if step == "train":
      
        if not os.path.isfile("word_dict.pickle"):
            train_article_list = get_text_list(train_content_path, toy)
            train_title_list = get_text_list(train_title_path,toy)

            count = 0
            dict = defaultdict(lambda: [])
            for sentence in train_article_list + train_title_list:
                #for word in t.pos(sentence):
                #    words.append(word[0])
                #if count <= 5:
                #    print(words)
                #    count += 1
            #sentence = ' '.join(t.morphs(sentence))
                sentence = normalize(sentence,english=False)
                for idx, word in enumerate(sentence.split()):
                    if len(word) >0:
                        normalizedword = word[:3]
                        tmp=[]
                        for char in normalizedword:
                            if ord(char) < 12593 or ord(char) > 12643:
                                tmp.append(char)
                        normalizedword = ''.join(char for char in tmp)
                        if word not in dict[normalizedword]:
                            dict[normalizedword].append(word)
            dict = sorted(dict.items(), key=operator.itemgetter(0))[1:]
            words = []
            for i in range(len(dict)):
                word = []
                word.append(dict[i][0])
                for w in dict[i][1]:
                    if w not in word:
                        word.append(w)
                words.append(word)

            words.append(['<padding>'])
            words.append(['<unk>'])
            words.append(['<s>'])
            words.append(['</s>'])
            
            reversed_dict = {i: ch[0] for i, ch in enumerate(words)}
            with open("ix_to_word.pickle", "wb") as t:
                pickle.dump(reversed_dict, t)
            #word_counter = collections.Counter(words).most_common()
            word_dict = {}
            #word_dict["<padding>"] = 0
            #word_dict["<unk>"] = 1
            #word_dict["<s>"] = 2
            #word_dict["</s>"] = 3
            #for word, _ in word_counter:
            #    word_dict[word] = len(word_dict)
        
            for idx, words in enumerate(words):
                for word in words:
                    word_dict[word] = idx

            with open("word_dict.pickle", "wb") as f:
                pickle.dump(word_dict, f)
        else:
                with open("word_dict.pickle", "rb") as f:
                    word_dict = pickle.load(f)
                    
    elif step == "valid":
        with open("word_dict.pickle", "rb") as f:
            word_dict = pickle.load(f)

    #reversed_dict = dict(zip(word_dict.values(), word_dict.keys()))
    #reversed_dict = {i: ch[0] for i, ch in enumerate(words)}

    article_max_len = 120
    summary_max_len = 18
    print(len(word_dict))
    
    return word_dict, reversed_dict, article_max_len, summary_max_len

def build_dataset(step, word_dict, article_max_len, summary_max_len, toy=False):
    if step == "train":
        article_list = get_text_list(train_content_path,toy)
        title_list = get_text_list(train_title_path,toy)
    elif step == "valid":
        article_list = get_text_list(valid_content_path,toy)
    else:
        raise NotImplementedError
    
    x = [normalize(d,english=False).split() for d in article_list]
    x = [[word_dict.get(w, word_dict["<unk>"]) for w in d] for d in x]
    x = [d[:article_max_len] for d in x]
    x = [d + (article_max_len - len(d)) * [word_dict["<padding>"]] for d in x]
    
    if step == "valid":
        return x
    else:
               
        y = [normalize(d,english=False).split() for d in title_list]
        y = [[word_dict.get(w, word_dict["<unk>"]) for w in d] for d in y]
        y = [d[:(summary_max_len - 1)] for d in y]
        print(len(x),len(y))
        return x, y
        
def batch_iter(inputs, outputs, batch_size, num_epochs):
    inputs = np.array(inputs)
    outputs = np.array(outputs)

    num_batches_per_epoch = (len(inputs) - 1) // batch_size + 1
    for epoch in range(num_epochs):
        for batch_num in range(num_batches_per_epoch):
            start_index = batch_num * batch_size
            end_index = min((batch_num + 1) * batch_size, len(inputs))
            yield inputs[start_index:end_index], outputs[start_index:end_index]

def get_init_embedding(reversed_dict, embedding_size):
    glove_file = "glove/glove.42B.300d.txt"
    word2vec_file = get_tmpfile("word2vec_format.vec")
    glove2word2vec(glove_file, word2vec_file)
    print("Loading Glove vectors...")
    word_vectors = KeyedVectors.load_word2vec_format(word2vec_file)

    word_vec_list = list()
    for _, word in sorted(reversed_dict.items()):
        try:
            word_vec = word_vectors.word_vec(word)
        except KeyError:
            word_vec = np.zeros([embedding_size], dtype=np.float32)

        word_vec_list.append(word_vec)
    print(len(word_vec_list))


    # Assign random vector to <s>, </s> token
    word_vec_list[2] = np.random.normal(0, 1, embedding_size)
    word_vec_list[3] = np.random.normal(0, 1, embedding_size)

    return np.array(word_vec_list)
      
        
