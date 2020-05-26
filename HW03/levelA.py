#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 16:23:32 2020

@author: user
"""

import re
import string
import random
import glob
import operator
import heapq
from collections import defaultdict, Counter, defaultdict
import math 
from functools import reduce
import csv
from pprint import pprint
from functools import lru_cache
from datetime import datetime

sentences = [
    "今天可能下雨",
    "中華民國於一九九五年三月一日開始實施全民健保",
    "孫中山先生推翻滿清建立中華民國",
    "教授應該要為辛苦的助教加薪",
    "火鍋是四川的特色",
    "波士頓茶葉事件促使美國革命",
    "羅馬帝國皇帝遭到殺害",
]


"""
WC
"""

mydict=dict()

def gramfreqdict(text):
    for word in text:
        word = word.split("|")[0]
        if type(mydict.get(word,0)) == "NoneType":
            mydict[word] = 1
        else :
            mydict[word]=mydict.get(word,0)+1
    #return mydict
    
file = open("COCT.small.txt", 'r', encoding='UTF-8')
while True:
    line = file.readline()
    if not line: break
    split_line = line.split()
    gramfreqdict(split_line)
    #print(line, end='', sep = ' ')
file.close()



"""
分詞
"""

def returnSum(myDict):   
    sum = 0
    for i in myDict: 
        sum = sum + myDict[i] 
    return sum

def splits(text, L):
    return [(text[:i+1], text[i+1:])
            for i in range(min(len(text), L))]
def getword(sentence,l,total):
    if l == 0 : 
        print(total)
        return 0
    exist = []
    sp_sentence = splits(sentence,l)
    h=0
    for i in sp_sentence:
        if i[0] in mydict:
            exist.append(1)
        elif i[0] not in mydict:
            exist.append(0)
    for j in range(l):
        if exist[j] == 1 :
            count = j
    print(sentence[h:h+count+1])
    voc = sentence[h:h+count+1]
    total = total + unigram(voc)
    #print(total)
    getword(sentence[h+count+1:l],l-count-1,total)
    
def my_word(sentence):
    l = len(sentence)
    getword(sentence,l,0)

    
def unigram(word):
    p = (mydict[word] + 1) / (len(mydict) + returnSum(mydict))
    return math.log(p)

#my_word(sentences[0])

for i in sentences:
    my_word(i)
