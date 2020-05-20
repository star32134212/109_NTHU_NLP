#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 19 16:47:12 2020

@author: user
"""

from alg_to_t import estimate_tef_and_tfe
import kenlm
import csv
from math import isclose, exp, log10
from collections import defaultdict
from typing import List
import copy #as cp
import operator
from collections import namedtuple

print('loading the language model ...')
lm = kenlm.Model('./bnc.bin')
print('You can use variable "lm" to score a sentence.')
print('\n' + '=' * 100 + '\n')


parallel_tokens_path = './cambridge_fast_align_corpus.txt'
parallel_tokens = []
print('preparing the data ...')
with open(parallel_tokens_path, 'r', encoding='utf8') as f:
    parallel_corpus = f.read().split('\n')
    for sent_pair in parallel_corpus:
        en_sent, ch_sent = sent_pair.split(' ||| ')
        en_tokens = en_sent.split(' ')
        ch_tokens = ch_sent.split(' ')
        parallel_tokens.append((en_tokens, ch_tokens))

print('Here are examples of the data.')
for x in parallel_tokens[:3]:
    print(x)
print('\n' + '=' * 100 + '\n')


with open('./cambridge_sym_en-ch.align', 'r') as f:
    en_ch_alignments = f.read().split('\n')[:-1]


# print('estimating t(e|f) and t(f|e) ...')
# t_ef, t_fe = estimate_tef_and_tfe(parallel_tokens, en_ch_alignments)
t_ef = defaultdict(lambda: defaultdict(lambda: 0.0))
t_fe = defaultdict(lambda: defaultdict(lambda: 0.0))
p_g_ef = defaultdict(lambda: defaultdict(lambda: 0.0))
p_g_fe = defaultdict(lambda: defaultdict(lambda: 0.0))
with open('word_table.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        w_e = row['ephrase']
        w_c = row['cphrase']
        t_ef[w_e][w_c] = float(row['pec'])
        t_fe[w_c][w_e] = float(row['pce'])
        p_g_fe[w_c][w_e] = row['pec']
        p_g_ef[w_e][w_c] = row['pce']
print('You can use variables "t_ef" denoting t(e|f) and "t_fe" denoting t(f|e).')

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
        
check_top_k_prob('遺憾', 10, t_ef)


# example
example_en_tokens = ["I", "suggest", "this", "method"]
example_ch_tokens = ["我", "建議", "這個", "方法"]
example_e1_idx = 1
example_e1 = example_en_tokens[example_e1_idx]
example_f_idx = 1
example_f = example_ch_tokens[example_f_idx]
example_e2 = 'proposed'

print(example_en_tokens)
print(example_ch_tokens)
print(example_e1_idx, example_e1)
print(example_f_idx, example_f)
print(example_e2)

test_idx = 1
e1_idx = 1
en_tokens, ch_tokens = example_en_tokens, example_ch_tokens
print(en_tokens, ch_tokens, sep="\n", end="\n\n")

test_paraphrasing_half(example_en_tokens, example_ch_tokens, e1_idx, example_f_idx, t_ef, t_fe)
#%%
def compute_paraphrase_prob(e1: str,
                            e2: str,
                            f: str,
                            t_ef: defaultdict,
                            t_fe: defaultdict):
    """
    Args:
        e1: 待替換的單字
        e2: 用來替換的單字
        f: e1 與 e2 替換用的 anchor，e1 => f => e2
        t_ef: t(e|f)
        t_fe: t(f|e)

    Returns:
        prob: e1 => f => e2 的 paraphrase probability
    """
    prob = 0.
    prob = t_fe[f][e1] * t_ef[e2][f] 
    
    return prob

""" result
.22497
"""
compute_paraphrase_prob(example_e1, example_e2, example_f, t_ef, t_fe)
#%%
def get_first_5_paraphrases(e1: str,
                            f: str,
                            t_ef: defaultdict,
                            t_fe: defaultdict):
    """
    Args:
        e1: 待替換的單字
        f: anchor
        t_ef: t(e|f)
        t_fe: t(f|e)

    Returns:
        candidates: paraphrase probability 前 5 高的其他英文單字，以及它們對應的
        paraphrase probability。

        example:
        [(c1, paraphrase_prob1),
         ... ,
         (c5, paraphrase_prob5)]
    """
    
    candidates = []#[('', 0.) for i in range(5)]
    candidates_wordlist = list(t_fe[f].items())
    for i in range(len(candidates_wordlist)):
        word = candidates_wordlist[i][0]
        prob = t_fe[f][e1] * t_ef[word][f] 
        candidates.append((word,prob))
    candidates.sort(key=lambda candidates: candidates[1],reverse=True)
    candidates = candidates[:5]
    #### YOUR CODE HERE ####
    
    return candidates

""" result
[('proposed', 0.22497118206479705),
 ('proposals', 0.1329054475991522),
 ('proposal', 0.11513612557416811),
 ('recommendations', 0.07940394719871861),
 ('propose', 0.045689473608494055)]
"""
get_first_5_paraphrases(example_e1, example_f, t_ef ,t_fe)
#%%
def rerank_paraphrases(en_tokens: List[str],
                       e1_idx: int,
                       candidates: List):
    """
    Args:
        en_tokens: 英文句子的 tokens (words)
        e1_idx: 待替換的單字在 en_tokens 中的 index
        candidates: get_first_5_paraphrases 的 output

    Returns:
        candidates_rerank: [c1, c2, ..., c5]，按照它們的 paraphrase probability 與
        exponential of sentence probability 的乘積排序，由高到低。
    """
    candidates_rerank = []
    new_sentence = ''
    en_tokens2 = en_tokens.copy()
    #### YOUR CODE HERE ####
    for w in candidates:
        en_tokens2[e1_idx] = w[0]
        new_sentence = " ".join(en_tokens2)
        #ew_sentence = new_sentence + '.'
        sc = lm.score(new_sentence,bos=False)
        sc2 = (10 ** sc) * w[1]
        #sc2 = -sc * w[1]
        print((w[0],sc2))
        candidates_rerank.append((w[0],sc2))
    candidates_rerank.sort(key=lambda candidates_rerank: candidates_rerank[1],reverse=True)
    candidates_rerank = [i[0] for i in candidates_rerank]
    return candidates_rerank

""" result
['proposed', 'propose', 'proposals', 'proposal', 'recommendations']
"""

example_candidates = get_first_5_paraphrases(example_e1, example_f, t_ef ,t_fe)
rerank_paraphrases(example_en_tokens, example_e1_idx, example_candidates)
#%%
def paraphrasing(en_tokens: List[str],
                 ch_tokens: List[str],
                 e1_idx: int,
                 f_idx: int,
                 t_ef: defaultdict,
                 t_fe: defaultdict):
    """
    Args:
        en_tokens: 英文句子的 tokens (words)
        ch_tokens: 對應的中文句子的 tokens (斷詞)
        e1_idx: 待替換的單字在 en_tokens 中的 index
        f_idx: 與 e1 align 的中文斷詞在 ch_tokens 中的 index
        t_ef: t(e|f)
        t_fe: t(f|e)

    Returns:
        e2: rerank 之後第一名的 candidate
    """
    e2 = ''
    #### YOUR CODE HERE ####
    rerank = []
    new_sentence = ''
    en_tokens3 = en_tokens.copy()
    f = ch_tokens[f_idx]
    e1 = en_tokens[e1_idx]
    candidates = get_first_5_paraphrases(e1, f, t_ef ,t_fe)
    for w,p in candidates:
        if(w == e1):
            continue
        #prob = t_fe[f][e1] * t_ef[w][f] 
        en_tokens3[e1_idx] = w
        new_sentence = " ".join(en_tokens3)
        #new_sentence = new_sentence + '.'
        sc = lm.score(new_sentence,bos=False)
        #print('sc',sc)
        sc2 = (10 ** sc) * p
        #sc2 = -sc * prob
        rerank.append((w,sc2))
        #print((word,sc2))
    rerank.sort(key=lambda rerank: rerank[1],reverse=True)
    rerank = [i[0] for i in rerank]
    e2 = rerank[0]
    return e2

""" result
'proposed'

"""

paraphrasing(example_en_tokens, example_ch_tokens, example_e1_idx, example_f_idx, t_ef, t_fe)
#%%
def test_paraphrasing_half(en_tokens, ch_tokens, e1_idx, f_idx, t_ef, t_fe):
    e2 = paraphrasing(en_tokens, ch_tokens, e1_idx, f_idx, t_ef, t_fe)
    print('before paraphrasing:', highlight_word(en_tokens, e1_idx))
    print('after paraphrasing:', highlight_word(en_tokens[:e1_idx] + [e2] + en_tokens[(e1_idx+1):],
                                                e1_idx))
    return

def test_paraphrasing(en_tokens, ch_tokens, e1_idx, alg_of_sent, t_ef, t_fe):
    idx_map = defaultdict(lambda: [])
    for en_ch_alg in alg_of_sent.split(' '):
        en_idx, ch_idx = list(map(lambda x: int(x), en_ch_alg.split('-')))
        idx_map[en_idx].append(ch_idx)
    f_idx = idx_map[e1_idx][0]
    e2 = paraphrasing(en_tokens, ch_tokens, e1_idx, f_idx, t_ef, t_fe)
    print('before paraphrasing:', highlight_word(en_tokens, e1_idx))
    print('after paraphrasing:', highlight_word(en_tokens[:e1_idx] + [e2] + en_tokens[(e1_idx+1):],
                                                e1_idx))
    return


def highlight_word(en_tokens, highlight_idx):
    word = f'```{en_tokens[highlight_idx]}```'
    sent = ' '.join(en_tokens[:highlight_idx] + [word] + en_tokens[(highlight_idx+1):])
    return sent

test_idx = 2001
e1_idx = 9
en_tokens, ch_tokens = copy.deepcopy(parallel_tokens[test_idx])
print(en_tokens, ch_tokens, sep="\n", end="\n\n")

test_paraphrasing(en_tokens, ch_tokens, e1_idx, en_ch_alignments[test_idx], t_ef, t_fe)
#%%
def get_e1_to_e2_prob_dict(e1, t_ef, t_fe):
    # update dict p such that p[e2] = t(e2 | e1) 
    # NOTE : p[e1] = t(e1 | e1) should NOT be zero
    p = defaultdict(lambda: 0.0) 
    #### CODE HERE ####
    candidates_e1 = list(t_ef[e1].items())
    for f,fp in candidates_e1:
        candidates_f = list(t_fe[f].items())
        for e2,ep in candidates_f:
            prop = compute_paraphrase_prob(e1,e2,f,t_ef,t_fe)
            p[e2] = p[e2] + prop
    #prob = t_fe[f][e1] * t_ef[e2][f] 
            
    return p

def general_paraphrasing(en_tokens, e1_idx, t_ef, t_fe):
    e2 = ''
    #### YOUR CODE HERE ####
    e1 = en_tokens[e1_idx]
    e1_dic = get_e1_to_e2_prob_dict(e1, t_ef, t_fe)
    e2 = sorted(e1_dic.items(), key=operator.itemgetter(1))[0]
    if(e2 == e1):
        e2 = sorted(e1_dic.items(), key=operator.itemgetter(1))[1]
        return e2

def test_general_paraphrasing(en_tokens, e1_idx, t_ef, t_fe):
    e2 = general_paraphrasing(en_tokens, e1_idx, t_ef, t_fe)
    print('before paraphrasing:', highlight_word(en_tokens, e1_idx))
    print('after paraphrasing:', highlight_word(en_tokens[:e1_idx] + [e2] + en_tokens[(e1_idx+1):],
                                                e1_idx))
    return

print(example_en_tokens, example_e1_idx)
general_paraphrasing(example_en_tokens, example_e1_idx, t_ef, t_fe)

print(example_en_tokens)
print(general_paraphrasing(example_en_tokens, example_e1_idx, t_ef, t_fe), end='\n\n')

test_general_paraphrasing(example_en_tokens[:], example_e1_idx, t_ef, t_fe)

#%%
class ParaphrasingModel():
    def __init__(self, t_ef, t_fe, prob_function):
        self.t_ef = t_ef
        self.t_fe = t_fe
        self.p_func = prob_function
        self.phrase_set = set(t_ef.keys())
        
    def __getitem__(self, phrase_in):
        # phase_in should be a tuple of words e.g. (word,)
        assert(type(phrase_in) == tuple)
        if len(phrase_in) == 1 and phrase_in not in self.phrase_set: # unknown word, OOV
            p = defaultdict(lambda: 0.0)
            p[phrase_in] = 1.
            return p
        
        return self.p_func(phrase_in, self.t_ef, self.t_fe)
    
# keys of t_ef and t_fe are words. We hope that the keys are tuples.
tt_ef = defaultdict(lambda:defaultdict(lambda:0.0))
for e in t_ef:
    for f in t_ef[e]:
        tt_ef[(e,)][(f,)] = t_ef[e][f]

tt_fe = defaultdict(lambda:defaultdict(lambda:0.0))
for f in t_fe:
    for e in t_fe[f]:
        tt_fe[(f,)][(e,)] = t_fe[f][e]
            
        
tm = ParaphrasingModel(tt_ef, tt_fe, get_e1_to_e2_prob_dict)

def noisy_channel_decode(sent_in, beam_size, tm, lm, verbose = False, bos=True):
    # The following code implements a monotone decoding
    # algorithm (one that doesn't permute the target phrases).
    # Hence all hypotheses in stacks[i] represent translations of 
    # the first i words of the input sentence. You should generalize
    # this so that they can represent translations of *any* i words.
    hypothesis = namedtuple("hypothesis", "logprob, lm_state, predecessor, phrase")
    state = kenlm.State()
    if bos:
        lm.BeginSentenceWrite(state) #Use <s> as context.  If you don't want <s>, use lm.NullContextWrite(state).
    else:
        lm.NullContextWrite(state)
    initial_hypothesis = hypothesis(0.0, state, None, None)
    # stacks = [{} for _ in sent_in] + [{}]
    # stacks[0][state] = initial_hypothesis
    stacks = [[] for _ in sent_in] + [[]]
    stacks[0].append(initial_hypothesis)
    for ii, stack in enumerate(stacks[:-1]):
    #     for h in sorted(stack.values(),key=lambda h: -h.logprob)[:beam_size]: # prune
        print("\nnow", ii)
        for h in sorted(stack,key=lambda h: -h.logprob)[:beam_size]: # prune
            for j in range(ii+1,len(sent_in)+1):
                print(h.phrase, ii, j, end='\t')
    #             print(sent_in[ii:j])
                if sent_in[ii:j] in tm.phrase_set:
    #                 for phrase_new, trans_prob in tm[sent_in[i:j]].items():
                    for phrase_new, trans_prob in sorted(tm[sent_in[ii:j]].items(), key=lambda x:-x[1])[:2*beam_size]:
                        # print(phrase_new)
                        logprob = h.logprob + log10(trans_prob)
                        lm_state = h.lm_state
                        for word in phrase_new:
                            lm_state_new = kenlm.State()
                            word_logprob = lm.BaseScore(lm_state, word, lm_state_new)
                            lm_state = lm_state_new
                            logprob += word_logprob
                        logprob += lm.BaseScore(lm_state, "</s>", kenlm.State()) if j == len(sent_in) else 0.0
                        new_hypothesis = hypothesis(logprob, lm_state, h, phrase_new)
    #                     if lm_state not in stacks[j] or stacks[j][lm_state].logprob < logprob: # second case is recombination
    #                         stacks[j][lm_state] = new_hypothesis
                        stacks[j].append(new_hypothesis)
    # winner = max(stacks[-1].values(), key=lambda h: h.logprob)
    print("\n\nRESULT:")
    result = []
    for winner in sorted(stacks[-1],key=lambda h: -h.logprob)[:beam_size]:
        def extract_english(h): 
            return "" if h.predecessor is None else "%s%s " % (extract_english(h.predecessor), " ".join(h.phrase))
        sent_out = extract_english(winner)
        print(sent_out)
        result.append(sent_out)

        if verbose:
            
            def extract_tm_logprob(h):
                 return 0.0 if h.predecessor is None else h.phrase.logprob + extract_tm_logprob(h.predecessor)
            tm_logprob = extract_tm_logprob(winner)
            lm_score = print(lm.score(sent_out, bos = True, eos = True))
            sys.stderr.write("LM = %f, TM = %f, Total = %f\n" % 
              (winner.logprob - tm_logprob, tm_logprob, winner.logprob))
    #           (winner.logprob - tm_logprob, tm_logprob, winner.logprob))
        print()
    return result

""" RESULT:

"""

beam_size = 5
sent_in = tuple(example_en_tokens)
print(" ".join(example_en_tokens))
sent_list = noisy_channel_decode(("i", "suggest", "this", "method"), beam_size, tm, lm, bos = False)
# sent_list = noisy_channel_decode((), beam_size, tm, lm)