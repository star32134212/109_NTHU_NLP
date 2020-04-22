import sys, fileinput, itertools
from collections import defaultdict
import nltk
import spacy
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import word_tokenize
import pandas as pd
import re
path = '/Users/user/Desktop/大四下/NLP/HW8/Week8'

#nlp = spacy.load('en', disable=["ner"])
lmtzr = WordNetLemmatizer()
ngram_sentence = defaultdict(list)
high_freq_words = set([line.strip() for line in fileinput.input(path+'/high_freq_words.txt')])
prons = set([line.strip() for line in fileinput.input(path+'/prons.txt')])
collocation = set([(tk[0], tk[2]) for line in fileinput.input(path+'/collocation.txt') for tk in [line.strip().split('\t')]])
"""
f = open(path+'/result2.txt')
data = []
for l in f:
    data.append(l)
"""
f = open(path+'/mp.collocation.sort.txt')
collocation = []
for line in f:
    collocation.append(line)

collocation = pd.read_csv(path+'/mp.collocation.sort.txt',header=None,sep='\t')
collocation.rename(columns={0:"collocation1",1:"pos1",2:"collocation2",3:"pos2",4:"relation",5:"count",6:"score"},inplace=True)
mean_score = collocation["score"].mean()
setA = set(collocation["collocation1"])
setB = set(collocation["collocation2"])

def lemmatize_sent(sentence): #list
    sentence = [lmtzr.lemmatize(word) for word in sentence]
    return sentence

def tokens(s): return(nltk.word_tokenize(s))

#用來算平均的
c1 = []
c2 = []
c3 = []
loc = []
#count1:5.8 count2=1.X count3=5.6
def calculate_score(ngram, sentence):
    ##### YOUR CODE HERE #####
    count1 = 0 #(word ∈ S & word ∉ high_freq_words.txt)
    count2 = 0 #(word ∈ S & word ∈ prons.txt)
    count3 = 0 #(collocation ∈ S & collocation ∈ collocation.txt)
    ngram = ngram.lower()
    sentence = sentence.lower()
    sentence2 = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）：]+", ' ', sentence)
    words = tokens(sentence2)
    words2 = lemmatize_sent(words) #words is list
    location = words.index(ngram.split(" ")[0])
    loc.append(location)
    for w in words2:
        if(w not in high_freq_words):
            count1 = count1 + 1
            c1.append(count1)
        if(w in prons):
            count2 = count2 + 1
            c2.append(count2)

        if(w in setA):
            for w2 in words2:
                if(w2 in setB):
                    count3 = count3 + 1
            c3.append(count3)
    score = 0.25*location - 0.25*count1 - 0.5*count2 + 0.25*count3
    #print(count)
    return(score)


for line in fileinput.input():
    ngram, sentence = line.strip().split('\t')
    ngram_sentence[ngram].append(sentence)
"""
for line in data:
    ngram, sentence = line.strip().split('\t')
    ngram_sentence[ngram].append(sentence)
 """   
for ngram, sentences in ngram_sentence.items():
    #break
    best_sentence = sorted(sentences, key=lambda s: calculate_score(ngram, s), reverse=True)[:3]
    for bs in best_sentence:
        idx = sentences.index(bs)
        value = calculate_score(ngram,bs)
        print(str(idx)+','+str(value)+'/',end='')
    print("")
    print("========================")
    print(ngram + ':'+'\t'.join(best_sentence))
    print("")


