#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 15:18:27 2020

@author: user
"""

import json
from collections import defaultdict, Counter
from nltk import word_tokenize
from math import log, sqrt
import numpy as np

with open('/Users/user/Desktop/大四下/NLP/HW5/week5_lab.page-to-cats.json') as f:
    page_category = json.load(f)

print(page_category['Bass (fish)'])

def returnSum(myDict): 
      
    sum = 0
    for i in myDict: 
        sum = sum + myDict[i] 
      
    return sum

# count the appearance of possible classes in the page title
def page_to_class(page):
    class_list = []
    if '(' in page and 'disambiguation' not in page:
        class_list.append(page.split('(')[1][:-1])
    return class_list


print(page_to_class('Bass (fish)'))

category_class_count = defaultdict(lambda: defaultdict(lambda: 0))

for page, category_list in page_category.items():
    for page_class in page_to_class(page):
        for category in category_list:
            category_class_count[category][page_class] = category_class_count[category][page_class] + 1
 
            
            #print('page: '+page+' category_list: '+ str(category_list)+ ' page_class: '+page_class+' category: '+category)
            ##### YOUR CODE HERE #####
        
            
category_class_count['Category:Fish common names']['fish']

with open('/Users/user/Desktop/大四下/NLP/HW5/week5_labsentences.json') as f:
    sentences = json.load(f)
    
    
sentences['bass']['Bass (fish)'][:5]

page_class_count = defaultdict(lambda: defaultdict(lambda: 0))

for page_list in sentences.values():
    for page in page_list:
        #Bass (fish) Bass (sound) Bass (Voice Type)
        for category in page_category[page]:
            #['Category:Bass (sound)', 'Category:Contrabass instruments']
            for c, count in category_class_count[category].items():
                #dict_items([('sound', 1), ('instrument', 1)])
                page_class_count[page][c] = page_class_count[page][c] + count

                
page_class_count['Bass (fish)']['fish']

page_class = defaultdict(dict)

for page, class_counts in page_class_count.items():
    #print("page: "+str(page))
    #print("class_count: "+str(class_counts))
    page_class[page] = max(class_counts,key = class_counts.get)

page_class['Bass (fish)']


class_sents = defaultdict(lambda: defaultdict(list))

for word, v in sentences.items():
    for page, sents in v.items():
        #Bass (fish) , 668
        class_sents[word][page_class[page]] = sents

print(list(class_sents['bass'].keys()))
print(len(class_sents['bass']['fish']))

weight = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))
mydic = {}
for word, v in class_sents.items():
    #word=bass,bow.....etc
    total_words = {}
    for wiki_class, sents in v.items():
        #class: fish 668, music 2141, sound 2533
        total_words[wiki_class] = Counter([word.lower() for sent in sents for word in word_tokenize(sent)])
    total = 0
    for i in total_words:
        tt = sum(total_words[i].values())
        mydic[i] = tt
        total = total + tt
    N = total
    for wiki_class, sents in v.items():
        n = mydic[wiki_class]
        print('n: '+str(n)+' N: '+str(N))
        for tks in total_words[wiki_class]:
            if(n==0): #duty中的criminal law
                continue
            else:
                w1 = total_words[wiki_class][tks]
                total2 = 0
                for allclass in total_words:
                    total2 = total2 + total_words[allclass][tks]
                w2 = total2
                weight[word][wiki_class][tks] = log((w1/n)/(w2/N))

            
print(weight['bass']['fish']['freshwater'])
print(max(weight['bass']['fish'].items(), key = lambda x: x[1]))


"""

"""


weight = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))

for word in class_sents.items():
    #word=bass,bow.....etc
    total_words = {}
    for wiki_class, sents in v.items():
        #class: fish 668, music 2141, sound 2533
        total_words[wiki_class] = Counter([word.lower() for sent in sents for word in word_tokenize(sent)])
    total = 0
    for i in total_words:
        tt = sum(total_words[i].values())
        total = total + tt
    N = total
    for wiki_class, sents in v.items():
        n = sum(total_words[wiki_class].values())
        for tks in total_words[wiki_class]:
            print('n: '+str(n)+' N: '+str(N))
            if(n==0): #duty中的criminal law
                continue
            else:
                w1 = total_words[wiki_class][tks]
                total2 = 0
                for allclass in total_words:
                    total2 = total2 + total_words[allclass][tks]
                w2 = total2
                weight[word][wiki_class][tks] = log(w1/n)/(total_words[wiki_class][tks]/N)
