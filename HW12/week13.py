#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 26 16:22:00 2020

@author: user
"""


import math 
from collections import defaultdict
import numpy as np


def takesecond(elem):
    return elem[1]

def cal_er(two_word):
    word = two_word.split(' ')
    w1 = list(bigram[word[0]].values())
    m1 = np.mean(w1)
    w2 = list(bigram_reverse[word[1]].values())
    m2 = np.mean(w2)
    return math.sqrt(m1 * m2 )

def cal_RR(two_word):
    ar = bigram_2[two_word]
    er = cal_er(two_word)
    return er/ar

path = 'count_1w.txt'
print('preparing the data1 ...')
with open(path, 'r', encoding='utf8') as f:
    data1 = f.read().split('\n')

path = 'count_2w.txt'
print('preparing the data2 ...')
with open(path, 'r', encoding='utf8') as f:
    data2 = f.read().split('\n')



dic = defaultdict(lambda: 0.0)
for d in data2:
    try:
        gram,count = d.split('\t')
        gram = gram.lower()
        dic[gram] = dic[gram.lower()] + int(count)
    except ValueError:
        continue
w = [(k, v) for k, v in dic.items()]
w.sort(key=takesecond,reverse=True)

bigram = defaultdict(lambda: defaultdict(lambda: 0.0))
bigram_reverse = defaultdict(lambda: defaultdict(lambda: 0.0))
bigram_2 = defaultdict(lambda: 0.0)
bigram_p = defaultdict(lambda: defaultdict(lambda: 0.0))
#bigram_list = []
rank = 1
for line in w:
    try:
        word = line[0].split(' ')
        bigram[word[0]][word[1]] = rank#int(text[1])
        bigram_reverse[word[1]][word[0]] = rank#int(text[1])
        bigram_2[line[0]] = rank#int(text[1]) 
        rank = rank + 1
        bigram_p[word[0]][word[1]] = line[1]
        #bigram_list.append((text[0],text[1]))
    except IndexError:
        print('Finish')
        #continue
        
unigram = defaultdict(lambda: 0.0)
for line in data1:
    try:
        word_count = line.split('\t')
        word = word_count[0].lower()
        count = word_count[1]
        unigram[word] = count#int(text[1])
    except IndexError:
        print('Finish')
        #continue

    
bigram_2_sort = sorted(bigram_2.items(), key=lambda d: d[1], reverse = True)
print(bigram_2_sort[:10]) #最大10
print(bigram_2_sort[-10:]) #最小10


"""
Rank Ratio
"""
RR = []
for pair in w:
    try:
        bg = pair[0]
        ar = bigram_2[bg]
        er = cal_er(bg)
        rr = er / ar
        RR.append((bg,rr))
    except IndexError:
        print('Finish')
        #continue   

result  = RR
result.sort(key=takesecond,reverse=True)
print(result[:10]) #最大10
print("=============")
print(result[-10:]) #最小10

cal_RR('hot dog')
#3.532345610794304


"""
MutInfo
"""
MI = []
for pair in w:
    try:
        bg = pair[0]
        word = bg.split(' ')
        p = bigram_p[word[0]][word[1]]
        p1 = int(unigram[word[0]])
        p2 = int(unigram[word[1]])
        if(p1*p2 != 0):
            I = p / (p1 * p2)
            MI.append((bg,I))
        #bigram_list.append((text[0],text[1]))
    except IndexError:
        print('Finish')
        #continue
        
MI.sort(key=takesecond,reverse=True)
print(MI[:10]) #最大10
print("=============")
print(MI[-10:]) #最小10   