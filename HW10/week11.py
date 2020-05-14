#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 12 16:27:32 2020

@author: user
"""

from collections import defaultdict
from typing import List, Tuple
import csv
import tqdm #for迴圈看進度
from copy import deepcopy
from math import log, isclose

parallel_tokens_path = '/Users/user/Desktop/4down/NLP/HW10/cambridge_parallel_tokens.tsv'
parallel_tokens = []
with open(parallel_tokens_path, 'r', encoding='utf8') as f:
    for en_tokens, ch_tokens in csv.reader(f, delimiter='\t'):
        parallel_tokens.append([en_tokens.split('#sep#'),
                                ch_tokens.split('#sep#')])
                                                
for x in parallel_tokens[:3]:
    print(x)
    
def compute_normalization_term(en_token_list: List[str], ch_token_list: List[str],t_ef: defaultdict) -> defaultdict:
    total_e = defaultdict(lambda: 0)
    #### YOUR CODE HERE ####
    total = 0
    for en in en_token_list:
        for ch in ch_token_list:    
            total = total + t_ef[en][ch]
        total_e[en] = total
        total = 0
    return total_e

example_ch = ['[NULL]', '我', '愛', '你', '愛', '我']
example_en = ['i', 'love', 'that', 'you', 'love', 'me']

for x in compute_normalization_term(example_en, example_ch,
                                    defaultdict(lambda: defaultdict(lambda: 0.1))).items():
    print(x)
    
""" result
('i', 0.6)
('love', 0.6)
('that', 0.6)
('you', 0.6)
('me', 0.6)
"""    
def collect_ef_count(en_token_list: List[str], ch_token_list: List[str],
                     t_ef: defaultdict, total_e: defaultdict) -> defaultdict:
    count_of_sent = defaultdict(lambda: defaultdict(lambda: 0.0))
    #### YOUR CODE HERE ####
    for en in en_token_list:
        for ch in ch_token_list:
            count_of_sent[en][ch] = count_of_sent[en][ch] + t_ef[en][ch] / total_e[en]
    return count_of_sent

for x, d in collect_ef_count(example_en, example_ch, 
                             defaultdict(lambda: defaultdict(lambda: 0.1)),
                             defaultdict(lambda: 10.0)).items():
    for y, z in d.items():
        print((x, y, z))
        
"""result
('i', '[NULL]', 0.01)
('i', '我', 0.02)
('i', '愛', 0.02)
('i', '你', 0.01)
('love', '[NULL]', 0.02)
('love', '我', 0.04)
('love', '愛', 0.04)
('love', '你', 0.02)
('that', '[NULL]', 0.01)
('that', '我', 0.02)
('that', '愛', 0.02)
('that', '你', 0.01)
('you', '[NULL]', 0.01)
('you', '我', 0.02)
('you', '愛', 0.02)
('you', '你', 0.01)
('me', '[NULL]', 0.01)
('me', '我', 0.02)
('me', '愛', 0.02)
('me', '你', 0.01)
"""

def ibm_model_1(parallel_corpus_list: List, n_iters: int) -> defaultdict:
    en_vocab = set(en_token.lower() for en_token_list, _ in parallel_corpus_list
                            for en_token in en_token_list)
    ch_vocab = set(ch_token for _, ch_token_list in parallel_corpus_list
                            for ch_token in ch_token_list)
    print(f'length of en_vocab: {len(en_vocab)}')
    print(f'lenght of ch_vocab: {len(ch_vocab)}')
    
    null_token = '[NULL]'
    # Add the Null token
    ch_vocab.add(null_token)
    
    # ptotal_edistribution is uniform.
    init_prob = 1 / len(en_vocab)
    # t_ef[e][f] means t(e|f)
    t_ef = defaultdict(lambda: defaultdict(lambda: init_prob))
    
    
    # EM process
    for i in tqdm.tqdm(range(n_iters)):
        # initialize
        # total_ef_count[e][f] is the numerator ot new t(e|f)
        total_ef_count = defaultdict(lambda: defaultdict(lambda: 0.0)) #分子
        # total_f[f] is the Denominator ot new t(e|f)
        total_f = defaultdict(lambda: 0.0) 
        token_pair_set = set()
        perp = 0
        # collect the evidence from corpus
        for en_token_list, ch_token_list in parallel_corpus_list:
            ch_token_list = [null_token] + ch_token_list
            perp += compute_perp(en_token_list, ch_token_list, t_ef)
            
            total_e = compute_normalization_term(en_token_list, ch_token_list, t_ef)
            ef_count_of_sent = collect_ef_count(en_token_list, ch_token_list, t_ef, total_e)
            
            cur_token_pair_set = set((e, f) for e in en_token_list
                                            for f in ch_token_list)
            for e, f in cur_token_pair_set:
                #### You should write two lines of code here.  ####
                #### Update total_ef_count and total_f with ef_count_of_sent ####
                total_ef_count[e][f] = total_ef_count[e][f] + ef_count_of_sent[e][f]
                total_f[f] = total_f[f] + ef_count_of_sent[e][f]
            token_pair_set.update(cur_token_pair_set)
            
        print(f'perplexity: {round(perp, 2)}')
        # estimate probabilities
        t_ef = defaultdict(lambda: defaultdict(lambda: 0))
        for e, f in token_pair_set:
            #### You should write a line of code here. Update t_ef ####
            ##分子分母除就ok
            t_ef[e][f] = total_ef_count[e][f] / total_f[f]
    return t_ef

def compute_perp(en_token_list, ch_token_list, t_ef):
    l_e = len(en_token_list)
    l_f = len(ch_token_list)    
    p_EF = 0.
    for e in en_token_list:
        s = 0.
        for f in ch_token_list:
            s += t_ef[e][f]
        p_EF += -log(s)
    p_EF += log(l_f**l_e)
    return p_EF

t_ef = ibm_model_1(parallel_tokens, 10)


def get_conditional_prob(token_ch, translation_dict):
    prob_dict = {}
    for token_en, sub_dict in translation_dict.items():
        if token_ch in sub_dict:
            prob_dict[token_en] = sub_dict[token_ch]
    return prob_dict

def check_top_k_prob(token_ch, k, translation_dict):
    prob_dict = get_conditional_prob(token_ch, translation_dict)
    prob_list = list(prob_dict.items())
    prob_sum = sum(prob_dict.values())
    prob_list.sort(key=lambda x:x[1], reverse=True)
    
    if not isclose(prob_sum, 1.):
        print(f"Warning. sum of p( e | {token_ch}) = {prob_sum}, not close to 1.")
    
    for token_en, prob in prob_list[:k]:
        print(f"p({token_en} | {token_ch}) = {prob}")
        
check_top_k_prob('學校', 5, t_ef)
check_top_k_prob('企業', 5, t_ef)
check_top_k_prob('預算', 5, t_ef)
##================================

def compute_alg_normalization_term(en_token_list: List[str], ch_token_list: List[str],
                                   t_ef: defaultdict, q_alg: defaultdict) -> defaultdict:
    total_e = defaultdict(lambda: defaultdict(lambda: 0))
    l_e = len(en_token_list)
    # the lenth of foreign sentence does not take NULL token into account
    l_f = len(ch_token_list) - 1
    total = 0
    for j in range(1, l_e + 1):
        en_word = en_token_list[j - 1]
        for i in range(l_f + 1):
            ch_word = ch_token_list[i]
            #### YOUR CODE HERE ####
            total = total + t_ef[en_word][ch_word] * q_alg[i][j][l_e][l_f]
        total_e[en_word][j] = total 
        total = 0
    return total_e

print(example_ch, example_en)
for x, d in compute_alg_normalization_term(example_en, example_ch,
                                           defaultdict(lambda: defaultdict(lambda: 0.1)),
                                           defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.2))))
                                          ).items():
    for y, z in d.items():
        print((x, y, z))

"""
('i', 1, 0.12000000000000002)
('love', 2, 0.12000000000000002)
('love', 5, 0.12000000000000002)
('that', 3, 0.12000000000000002)
('you', 4, 0.12000000000000002)
('me', 6, 0.12000000000000002)
"""
        
def collect_count(en_token_list: List[str], ch_token_list: List[str],
                    t_ef: defaultdict, q_alg: defaultdict,
                    total_e: defaultdict) -> defaultdict:
    ef_count = defaultdict(lambda: defaultdict(lambda: 0))
    alg_count = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0))))
    l_e = len(en_token_list)
    # the lenth of foreign sentence does not take NULL token into account
    l_f = len(ch_token_list) - 1
    
    for j in range(1, l_e + 1):
        en_word = en_token_list[j - 1]
        for i in range(l_f + 1):
            ch_word = ch_token_list[i]
            #### YOUR CODE HERE ####
            ef_count[en_word][ch_word] =  ef_count[en_word][ch_word] + (t_ef[en_word][ch_word]  * q_alg[i][j][l_e][l_f] )/ total_e[en_word][j]
            alg_count[i][j][l_e][l_f] = (t_ef[en_word][ch_word]  * q_alg[i][j][l_e][l_f] )/ total_e[en_word][j]
            #count_of_sent[en][ch] = count_of_sent[en][ch] + t_ef[en][ch] / total_e[en]

    return (ef_count, alg_count)

example_ef, example_alg = collect_count(example_en, example_ch,
                                        defaultdict(lambda: defaultdict(lambda: 0.1)),
                                        defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.2)))),
                                        defaultdict(lambda: defaultdict(lambda: 0.1))
                                       )
for x, d in example_ef.items():
    for y, z in d.items():
        print((x, y, z))
print()
"""
('i', '[NULL]', 0.20000000000000004)
('i', '我', 0.4000000000000001)
('i', '愛', 0.4000000000000001)
('i', '你', 0.20000000000000004)
('love', '[NULL]', 0.4000000000000001)
('love', '我', 0.8000000000000002)
('love', '愛', 0.8000000000000002)
('love', '你', 0.4000000000000001)
('that', '[NULL]', 0.20000000000000004)
('that', '我', 0.4000000000000001)
('that', '愛', 0.4000000000000001)
('that', '你', 0.20000000000000004)
('you', '[NULL]', 0.20000000000000004)
('you', '我', 0.4000000000000001)
('you', '愛', 0.4000000000000001)
('you', '你', 0.20000000000000004)
('me', '[NULL]', 0.20000000000000004)
('me', '我', 0.4000000000000001)
('me', '愛', 0.4000000000000001)
('me', '你', 0.20000000000000004)
"""
for x, d in example_alg.items():
    for y, z in d.items():
        print((x, y, z[len(example_en)][len(example_ch)-1]))
print()
"""
(0, 1, 0.20000000000000004)
(0, 2, 0.20000000000000004)
....
(5, 5, 0.20000000000000004)
(5, 6, 0.20000000000000004)
"""

def ibm_model_2(parallel_corpus_list: List, n_iters: int,
                init_t_ef: defaultdict) -> Tuple[defaultdict, defaultdict]:
    en_vocab = set(en_token.lower() for en_token_list, _ in parallel_corpus_list
                            for en_token in en_token_list)
    ch_vocab = set(ch_token for _, ch_token_list in parallel_corpus_list
                            for ch_token in ch_token_list)
    print(f'length of en_vocab: {len(en_vocab)}')
    print(f'lenght of ch_vocab: {len(ch_vocab)}')
    null_token = '[NULL]'
    # Add the Null token
    ch_vocab.add(null_token)
    
    t_ef = deepcopy(init_t_ef)
    q_alg = get_initial_q_alg(parallel_corpus_list) # q_alg[i][j][l_e][l_f] means a(i | j, l_e, l_f)
    
    for i in tqdm.tqdm(range(n_iters)):
        total_ef_count = defaultdict(lambda: defaultdict(lambda: 0.0))
        total_f = defaultdict(lambda: 0.0)

        # total_alg_count[i][j][l_e][l_f] is the numerator of new a(i | j, l_e, l_f)
        total_alg_count = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0))))
        # total_alg_count[j][l_e][l_f] is the denominator of new a(i | j, l_e, l_f)
        total_alg = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))

        token_pair_set = set()
        perp = 0
        # collect the evidence from corpus
        for en_token_list, ch_token_list in parallel_corpus_list:
            ch_token_list = [null_token] + ch_token_list
            perp += compute_perp_2(en_token_list, ch_token_list, t_ef, q_alg)
            # the lenth of foreign sentence does not take NULL token into account
            l_f = len(ch_token_list) - 1
            l_e = len(en_token_list)

            total_e = compute_alg_normalization_term(en_token_list, ch_token_list, t_ef, q_alg)
            ef_count_of_sent, alg_count_of_sent = collect_count(en_token_list, ch_token_list,
                                                                t_ef, q_alg, total_e)
            
            cur_token_pair_set = set((e, f) for e in en_token_list
                                            for f in ch_token_list)
            token_pair_set.update(cur_token_pair_set)
            for e, f in cur_token_pair_set:
                #### You should write two lines of code here.  ####
                #### Update total_ef_count and total_f with ef_count_of_sent####
                total_ef_count[e][f] = total_ef_count[e][f] + ef_count_of_sent[e][f]
                total_f[f] = total_f[f] + ef_count_of_sent[e][f]                
                
            # collect counts
            for j in range(1, l_e+1):
                for i in range(l_f+1):
                    #### You should write two lines of code here.  ####
                    #### Update total_alg_count, total_alg with alg_count_of_sent ####
                    total_alg_count[i][j][l_e][l_f] = total_alg_count[i][j][l_e][l_f] + alg_count_of_sent[i][j][l_e][l_f]
                    total_alg[i][l_e][l_f] = total_alg[i][l_e][l_f] + alg_count_of_sent[i][j][l_e][l_f]
        print(f'perplexity: {round(perp, 2)}')
        
        # Estimate the new lexical translation probabilities
        t_ef = defaultdict(lambda: defaultdict(lambda: 0))
        for e, f in token_pair_set:
            #### You should write a line of code here. Update t_ef ####
            t_ef[e][f] = total_ef_count[e][f] / total_f[f]
  
            
        # Estimate the new alignment probabilities
        q_alg = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0))))
        for en_token_list, ch_token_list in parallel_corpus_list:
            l_f = len(ch_token_list)
            l_e = len(en_token_list)
            for i in range(l_f + 1):
                for j in range(1, l_e + 1):
                    #### You should write a line of code here. Update q_alg ####
                    q_alg[i][j][l_e][l_f] = total_alg_count[i][j][l_e][l_f] / total_alg[j][l_e][l_f]
    return (t_ef, q_alg)

def get_initial_q_alg(parallel_corpus_list: List) -> defaultdict:
    q_alg = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0))))
    
    for en_token_list, ch_token_list in parallel_corpus_list:
        l_e = len(en_token_list)
        l_f = len(ch_token_list)
        q_initial = 1 / (l_f + 1)
        for i in range(0, l_f + 1): # 0 for NULL token
            for j in range(1, l_e + 1):
                q_alg[i][j][l_e][l_f] = q_initial
    return q_alg

def compute_perp_2(en_token_list, ch_token_list, t_ef, q_alg):
    perp = 0
    l_e = len(en_token_list)
    l_f = len(ch_token_list) - 1
    for j in range(1, l_e+1):
        en_word = en_token_list[j - 1]
        cur_perp = 0
        for i in range(l_f + 1):
            ch_word = ch_token_list[i]
            cur_perp += t_ef[en_word][ch_word] * q_alg[i][j][l_e][l_f]
        perp += -log(cur_perp)
    return perp


t_ef_2, q_alg = ibm_model_2(parallel_tokens, 15, t_ef)

def get_top_k_prob(token_ch, k, translation_dict):
    prob_dict = get_conditional_prob(token_ch, translation_dict)
    prob_list = list(prob_dict.items())
    prob_sum = sum(prob_dict.values())
    prob_list.sort(key=lambda x:x[1], reverse=True)
    if not isclose(prob_sum, 1.):
        print(f"Warning. sum of p( e | {token_ch}) = {prob_sum}, not close to 1.")
    
    return prob_list[:k]

def translate(ch_token_list: List[str], l_e: int, translation_dict, align):
    l_f = len(ch_token_list)
    null_token = '[NULL]'
    ch_token_list.insert(0, null_token)
    k = 3
    
    en_candidates = []
    for token_ch in ch_token_list:
        en_candidates.append(get_top_k_prob(token_ch, 10, translation_dict))

    for j in range(1, l_e+1):
        possible_list = []
        for i, ens in enumerate(en_candidates):
            for token_en, prob in ens:
                possible_list.append((token_en, align[i][j][l_e][l_f] * prob))
        possible_list.sort(key=lambda x:x[1], reverse=True)
        print(f"possible candidates for the {j}-th English word:")
        for token_en, prob in possible_list[:k]:
            print(f"{token_en}\t\tprobability:{prob}")
        print()

translate(['今天','天氣','很','好'], 5, t_ef_2, q_alg)