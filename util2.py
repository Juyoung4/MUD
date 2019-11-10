# word_to_ix, ix_to_word 생성
def make_dict(contents):
    words=[]
    for j in contents:
        for idx, word in enumerate(j.split()):
            words.append(word)
            words.append(['<PAD>'])
    words.append(['<S>'])
    words.append(['<E>'])
    words.append(['<UNK>'])

    ix_to_word = {i: ch[0] for i, ch in enumerate(words)}
    word_to_ix = {}
    for idx,words in enumerate(words):
        for word in words:
            word_to_ix[word] = idx
    print('contents number: %s, voca numbers: %s' %(len(contents),len(ix_to_word)))
    return word_to_ix,ix_to_word
