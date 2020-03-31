#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 15:53:44 2020

@author: user
"""

import numpy as np
import math, re
from collections import defaultdict
import sys
import threading
from math import sqrt
import operator
# M:insert U:delete R:replace
PROBLEM_WORDS = [ line.strip() for line in open('/Users/user/Desktop/大四下/NLP/HW4/problem_word_list.txt') ]
corpus = open('/Users/user/Desktop/大四下/NLP/HW4/lang8.pos.m2.txt').read().split('\n\n')
corpus_list = [i.split('\n') for i in corpus]
corpus_list = [i for i in corpus_list if len(i) >=2]

def m2_to_wikiedit(row, edit):
    sent = [i.split('//')[0] for i in row.split()[1:]]
    index, pos, word, _, _, _ = edit.split('|||')
    start, end = [int(i) for i in index.split()[1:] ]
    if pos[0] == 'M': 
        sent.insert(start, '{+' + '_'.join(word.split()) + '+}')
    elif pos[0] == 'U':
        _del = '_'.join(sent[start:end])
        del sent[start:end]
        sent.insert(start, '[-' + _del + '-]' )
    else:
        _rep = '_'.join(sent[start:end])
        del sent[start:end]
        sent.insert(start, '[-' + _rep + '-]{+' + '_'.join(word.split()) + '+}' )
    return sent

def list_to_skipgram(row, maxdist = 5, problem_words = PROBLEM_WORDS):
    skip = []
    for edit in row[1:]:
        sent = m2_to_wikiedit(row[0], edit)
        #print(sent)
        for i in range(len(sent)):
            #print("i"+str(i))
            if('-]{+' in sent[i]):
                pos = i
            elif('[-' in sent[i]):
                pos = i
                #print("pos "+ str(pos))
            elif('{+' in sent[i]):
                pos = i
                #print("pos "+ str(pos))
        head = pos - maxdist + 1
        tail = pos + maxdist - 1
        if(head < 0):
            head = 0
        if(tail > len(sent) - 1):
            tail = len(sent) - 1
        for j in range(head,tail+1):
            if(sent[j] in PROBLEM_WORDS):
                #print('PRO: '+sent[j]+' j: '+str(j)+' edit: '+sent[pos])
                ans = []
                ans.append(sent[j])
                ans.append(sent[pos]) 
                ans.append(j - pos)
                skip.append(ans)
    return skip

rules = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
for row in corpus_list:
    skip = list_to_skipgram(row)
    for t in range(len(skip)):
        rules[skip[t][0]][skip[t][1]][skip[t][2]] = rules[skip[t][0]][skip[t][1]][skip[t][2]] + 1


def pad(vlist):
    vlist2 = [0,0,0,0,0,0,0,0,0,0]
    vlist += [0 for i in range(len(vlist2)-len(vlist))]
    return vlist


backup = rules

time = 0
skipbigram_static = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
for pro in rules:
    value_list2 = []
    for tag in rules[pro]:
        value_list = list(rules[pro][tag].values())
        for p in rules[pro][tag]:
            try:
                skipbigram_static[pro][tag]['avg_p'] = skipbigram_static[pro][tag]['avg_p'] + p*rules[pro][tag][p]   
            except TypeError:
                continue
        skipbigram_static[pro][tag]['freq'] = sum(value_list)
        skipbigram_static[pro][tag]['avg_p'] = skipbigram_static[pro][tag]['avg_p']/skipbigram_static[pro][tag]['freq']
        skipbigram_static[pro][tag]['spread'] = np.square(np.std(pad(value_list)))*(9/10)
        value_list2.append(skipbigram_static[pro][tag]['freq'])

    for tag3 in rules[pro]:
        skipbigram_static[pro][tag3]['strength'] = (skipbigram_static[pro][tag3]['freq'] - np.average(value_list2)) / np.std(value_list2)
    print(time)
    time = time + 1

backup3 = skipbigram_static

backup2 = skipbigram_static


def valid_collocation(key):
    K0 = 1
    U0 = 5
    K1 = 1
    for tag in skipbigram_static[key]:
        if(skipbigram_static[key][tag]['strength'] >= K0 and skipbigram_static[key][tag]['spread']*10/9 >= U0):
            for i in rules[key][tag]:
                if(rules[key][tag][i] >= skipbigram_static[key][tag]['freq']/10 + (K1 * np.sqrt(skipbigram_static[key][tag]['spread']))):
                    print(key + " " + tag + " " + "(" + str(-i) + ", " + str(rules[key][tag][i]) + ")" )
                    #print(skipbigram_static[key][tag].items())
        
valid_collocation('explain')

valid_collocation('discuss')
print()


