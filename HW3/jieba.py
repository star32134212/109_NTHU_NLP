# %%
import re
import string
import random
import glob
import operator
import heapq
from collections import defaultdict, Counter, defaultdict
from math import log10
from functools import reduce
import csv
from pprint import pprint
from functools import lru_cache
from datetime import datetime


# %%
# read datas from file
# data format:
#   token \t count
def datafile(name, sep="\t"):
    "Read key,value pairs from file."
    with open(name) as f:
        datas = csv.reader(f, delimiter=sep)
        for data in datas:
            yield [data[0], int(data[1])]


# %%
# convert data to dict in the following way
# take '中華民國' for example:
#   tokens['中'] = count
#   tokens['中華'] = count
#   tokens['中華民']  = 0, if '中華民' not in data
#   tokens['中華民國'] = count
tokens = {}
N = 0
for i in datafile("merge.tsv", sep="\t"):
    name, count = i[0], i[1]
    N += count
    tokens[name] = count

    for j in range(len(name)):
        t = name[: j + 1]
        if t not in tokens:
            tokens[t] = 0


# %%
# Convert tokens to DAG(Directed Acyclic Graph)
# take '火鍋是四川的特色' for example:
#      '０１２３４５６７'
# [
#  {0: 1351, 1: 327},     # 火 火鍋
#  {1: 633},             # 鍋
#  {2: 346856},          # 是
#  {3: 3640, 4: 348},    # 四 四川
#  {4: 138},              # 川
#  {5: 1185058},         # 的
#  {6: 1245, 7: 4453},   # 特 特色
#  {7: 835}             # 色
# ]
# example:
#   >>> pprint(build_tree('火鍋是四川的特色'))
# [
#  {0: 1351, 1: 327},
#  {1: 633},
#  {2: 346856},
#  {3: 3640, 4: 348},
#  {4: 138},
#  {5: 1185058},
#  {6: 1245, 7: 4453},
#  {7: 835}
# ]
def build_tree(sentence):
    tree = []
    for idx, word in enumerate(sentence):
        l = len(sentence)
        words = {}
        for i in range(1, l - idx + 1):
            token = sentence[idx : idx + i]
            value = tokens.get(token)
            if value != None:
                if value != 0:
                    words[idx + i - 1] = tokens[token]
                else:
                    continue
            else:
                break
        tree.append(words)
    return tree


# %%
pprint(build_tree("火鍋是四川的特色"))
# %%


# use closure to simulate private variables
# if you don't know what is closure, it's ok, just handle dp function.
# example:
#   >>> print(parse('孫中山先生推翻滿清建立中華民國'))
#   [-26.955841777998064, ['孫中山', '先生', '推翻', '滿清', '建立', '中華民國']]
def parse(sentence):

    sentence = sentence
    tree = build_tree(sentence)
    print("樹")
    print(tree)
    # use dynamic programming to parse sentence to tokens
    # !!!note!!! you must return something like [probability, [tokens]]
    # !!!note!!! you should use cache function to cache function result.
    #
    # !!!hits!!! python build-in lru_cache can help you cache function result.

    @lru_cache(None)
    def dp(index=0):
        possibles = []
        if index >= len(sentence):
            return [log10(1), []]
        for i in tree[index]:
            possibles.append([sentence[index : i + 1], sentence[i + 1 :]])
        # print(possibles)

        prob_possibles = []
        for i in possibles:
            other = dp(index=len(sentence) - len(i[1]))

            
            prob = log10((tokens[i[0]]) / N) + other[0]
            possible = [i[0]] + other[1]
            prob_possibles.append([prob, possible])

        m = max(prob_possibles, key=lambda x: x[0])
        return m

    # !!!note!!! you must return something like [probability, [tokens]]
    return dp(0)


# %%
print(parse("孫中山先生推翻滿清建立中華民國"))

# %%
sentences = [
    "今天可能下雨",
    "中華民國於一九九五年三月一日開始實施全民健保",
    "孫中山先生推翻滿清建立中華民國",
    "教授應該要為辛苦的助教加薪",
    "火鍋是四川的特色",
    "波士頓茶葉事件促使美國革命",
    "羅馬帝國皇帝遭到殺害",
]

# %%
for i in sentences:
    print(parse(i))

# %%
# result(different implementation details may lead to different numbers)
# [-10.970361739190729, ['今天', '可能', '下雨']]
# [-31.937781660374768, ['中華民國', '於', '一九九五年', '三月', '一日', '開始', '實施', '全民健保']]
# [-26.955841777998064, ['孫中山', '先生', '推翻', '滿清', '建立', '中華民國']]
# [-27.05945291889755, ['教授', '應該', '要', '為', '辛苦', '的', '助教', '加薪']]
# [-16.95450965070056, ['火鍋', '是', '四川', '的', '特色']]
# [-25.07845561290892, ['波士頓', '茶葉', '事件', '促使', '美國', '革命']]
# [-23.817296657004494, ['羅馬', '帝國', '皇帝', '遭到', '殺害']]











def datafile(name, sep="\t"):
    "Read key,value pairs from file."
    with open(name) as f:
        datas = csv.reader(f, delimiter=sep)
        for data in datas:
            yield [data[0], int(data[1])]

tokens = {}
N = 0
for i in datafile("COCT.small.txt", sep=" "):
    print(i)
    name, count = i[0], i[1]
    N += count
    tokens[name] = count

    for j in range(len(name)):
        t = name[: j + 1]
        if t not in tokens:
            tokens[t] = 0