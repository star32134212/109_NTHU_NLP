#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  5 15:03:16 2020

@author: user
"""
import numpy as np
from collections import defaultdict
from nltk.corpus import wordnet as wn
from itertools import product
import kenlm
import pandas as pd
import spacy
from spacy import displacy
from linggle_api import Linggle

deps = [ line.strip().split('\t') for line in open('bnc.vn.txt').readlines() ]
vo = [ (w1, w2, count) for w1, dep, w2, count in deps ]

#print ('All collocations counts =', len(vo))
#print (vo[:7])

vocount = defaultdict(lambda: defaultdict(lambda: 0))
ovcount = defaultdict(lambda: defaultdict(lambda: 0))

for v, obj, count in vo:
    vocount[v][obj] = int(count)
    ovcount[obj][v] = int(count)    
    ######### Your code here #########

"""
print (vocount['reach']['purpose'])
print ()
print (sorted(list(vocount['reach'].items()), key=lambda x: -x[1])[:10])
print ()
print (sorted(list(ovcount['purpose'].items()), key=lambda x: -x[1])[:10])
"""

N = sum( int(count) for _, _, count in vo)

def mi(v, o): #Mutual Information
    pvo = vocount[v][o] / N
    pv = sum(vocount[v].values()) / N
    po = sum(ovcount[o].values()) / N
    return np.log2( pvo / (pv * po) )
    ######### Your code here #########
"""    
print ('achieve', 'purpose', mi('achieve', 'purpose'))
"""
#pos 詞性
def wn_sim(w1, w2, pos):
    wn1 = wn.synsets(w1, pos)
    wn2 = wn.synsets(w2, pos)
    maxsim = 0
    for synset1 in wn1:
        for synset2 in wn2:
            similarity = synset1.path_similarity(synset2)
            if(similarity > maxsim):
                maxsim = similarity
                
    return maxsim
    ######### Your code here #########

""" 
print(wn_sim('dog','puppy','n'))
print(wn_sim('dog','cat','n'))
print(wn_sim('dog','book','n'))
"""

def n_cluster(v, o, sim):
    objs = sorted(list(vocount[v].items()), key=lambda x: -x[1])
    RES = [ (obj, mi(v, obj), sim(o, obj, 'n'))  for obj, count in objs ]
    RES = [ (obj, m, s)  for obj, m, s in RES if m > 1.5 and s > .4 ]
    return sorted(RES, key=lambda x: -x[2])

def v_cluster(v, o, sim):
    objs = sorted(list(ovcount[o].items()), key=lambda x: -x[1])
    RES = [ (obj, o, mi(obj, o), sim(v, obj, 'v'))  for obj, count in objs ]
    other_n = n_cluster(v, o, sim)
    for i in range(len(other_n)):
        o = other_n[i][0]
        objs = sorted(list(ovcount[o].items()), key=lambda x: -x[1])
        RES2 = [ (obj, o, mi(obj, o), sim(v, obj, 'v'))  for obj, count in objs ]
        
        RES = RES + RES2
    RES = [ (obj, o, m, s)  for obj, o, m, s in RES if m > 3.0 and s > .4 ]
    return sorted(RES, key=lambda x: -x[2])
    ######### Your code here #########

"""    
test = v_cluster('reach', 'purpose', wn_sim)
n_cluster('reach', 'purpose', wn_sim)
"""

test = v_cluster('reach', 'purpose', wn_sim)


#nlp = spacy.load('en_core_web_lg')
"""
model = kenlm.Model('bnc.bin')
print(model.score('this is an apple .', bos = True, eos = True))
"""

model = kenlm.Model('bnc.bin')
linggle = Linggle()

# Detect the miscollocations
# 透過Linggle查詢miscollocation，如果數量小於10000則判斷為error pair
def check_count(search):
    ######### Your code here #########
    count = linggle.search(search)
    if(len(count)>0):
        return count[0][1]
    else:
        return 0

    
def LM(vn_pair, sentence):
    search = ''
    for i in range(len(vn_pair[0])):
        search = search + vn_pair[0][i][0] + ' '
    pair_count = check_count(search)
    if(pair_count > 10000):
        print('Your sentence is correct.')
    else:
        ans = []
        print('========Candidate collocations========')
        candidate = v_cluster(vn_pair[0][0][0], vn_pair[0][1][0], wn_sim)
        print(candidate)
        for c in candidate:
            search = c[0] + ' ' +c[1]
            pair_count = check_count(search)
            if(pair_count > 10000):
                #print(c)
                str = ' '
                for l in range(len(vn_pair[0])):
                    sentence[vn_pair[0][l][1]] = c[l] #vn_pair的位置 = 
                output = str.join(sentence)
                #print("output: "+output)
                score = model.score(output, bos = True, eos = True)
                ans.append((output,score,pair_count))
        
        print(ans)
            ######### Your code here #########
            # 結果也要用Linggle查詢，如果數量小於10000則忽略
            
LM([[('reach', 1), ('dream', 3)]], "He reach his dream".split())