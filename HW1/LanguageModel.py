#!/usr/bin/env python
# coding: utf-8

import math, re
from collections import Counter


def bigram2freqdict(text):
    mydict=dict()
    for (ch1,ch2) in text:
        mydict[(ch1,ch2)]=mydict.get((ch1,ch2),0)+1
    return mydict
    
# tokenize text and get words list
def words(text): return re.findall(r'\w+', text.lower())

# get all bigrams
def bigrams(text):
    splited_text = text.split()
    return [splited_text[i:i+2] for i in range(0,len(splited_text)-1)]
    #return [text[i:i+2] for i in range(0,len(text)-1)]
    #pass

# these are word-level 1-grams(unigram) and 2-grams(bigram)
# count of the number of times they appeared
data_text = open('big.txt').read()
data_text = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）：]+", ' ', data_text)
bi_count = bigram2freqdict(bigrams(data_text.lower()))
uni_count = Counter(words(open('big.txt').read()))
#bi_count = Counter(bigrams(open('big.txt').read()))



# ==Format==
# call add1_smooth("He is") or add1_smooth(("He", "is")) something like that...
# retrun 1.306 (probability with add one smooth)
V = len(list(uni_count.keys()))
V2 = len(list(bi_count.keys()))

def add1_smooth(bigram):
    #P = math.log((sentence_list[wordnum] + 1 )/(sentence_list[wordnum][0] + V )) 
    try:
        return bi_count[bigram]
    except KeyError:
        return 1 
    #pass

# ==Format==
# call sentence_prob("He is looking a new job.")
# retrun -33.306 (sentence probability)

def sentence_prob(sentence):
    sentence = sentence.lower()
    sentence = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）：]+", ' ', sentence)
    sentence_list = list(bigram2freqdict(bigrams(sentence))) #字典表化
    totalP=0
    for wordnum in range(0,len(sentence_list)):
        P = math.log((add1_smooth(sentence_list[wordnum]) + 1 )/(uni_count[sentence_list[wordnum][0]] + V )) 
        totalP = totalP + P
        print(P)
    
    return totalP
    #pass


if __name__ == "__main__":
    lm = sentence_prob("He is looking a new job.")
    print(lm)
    
    
    
"""
"""

