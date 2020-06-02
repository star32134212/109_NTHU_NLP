#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 16:32:01 2020

@author: user
"""

import re, math
from collections import defaultdict
import nltk, pickle
import pprint
from linggle import Linggle
#from IPython.display import Markdown, display

sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

def words(text): return re.findall("([a-zA-Z'-]+|[0-9]+)", text)
def ngrams(tokens, n=2): return [' '.join(tokens[i:i+n]) for i in range(len(tokens)-n) ]  

count_web1t = [ line.strip().split('\t') for line in open('count_1w.txt').readlines() ]
count_web1t = dict([ (word, int(count)) for word, count in count_web1t ])

count_web2t = [ line.strip().split('\t') for line in open('count_2w.txt').readlines() ]
count_web2t = dict([ (word, int(count)) for word, count in count_web2t ])

count_how_to = defaultdict(lambda: 0)
count_chapter = defaultdict(lambda: defaultdict(lambda: 0))
count_chapter_bigram = defaultdict(lambda: defaultdict(lambda: 0))
chapters = '''01. Accept; 02. Confirm; 03. Adjust; 04. Advice; 05. Birthday; 06. Announce; 07. Apologize; 08. Apply; 09. Appointment; 10. Appreciate; 11. Late; 12. Collect; 13. Complaint; 14. Congrat; 15. Contract; 16. CoverLetters; 17. Credit; 18. Disagree; 19. ToEditor; 20. E-mail; 21. Employ; 22. Family; 23. Fax; 24. Follow-up; 25. RaiseFund; 26. Get-well; 27. Goodwill; 28. Holiday; 29. Instruct; 30. Introduce; 31. Invite; 32. Love; 33. Memos; 34. ToNeighbor; 35. Order; 36. Club; 37. Query; 38. Refer; 39. Refuse; 40. Report; 41. Request; 42. Respond; 43. Resume; 44. Sales; 45. Sensitive; 46. Sympathy; 47. Thank-you; 48. Travel; 49. Wedding; 50. Welcome'''
chapters = [ x.split() for x in chapters.split('; ')]
chaptername = dict([ (int(x[:-1]), x+y) for x, y in chapters ])

chapterno = 1
for chapter in open('how.to.say.it.(raw).txt').read().split('<chapter>')[1:-1]:
    sentences = sent_detector.tokenize(chapter[chapter.index('\nPHRASES\n')+len('\nPHRASES\n'):])
    for sentence in sentences:
        for word in words(sentence):
            count_how_to[word] += 1
            count_chapter[chaptername[chapterno]][word] += 1
        for bigram in ngrams(words(sentence)):
            count_chapter_bigram[chaptername[chapterno]][bigram] += 1
    chapterno += 1
    
#segmenter_file = open('english.pickle', 'r')
#sentence_segmenter = pickle.Unpickler(sent_detector).load()
    
def is_key(word, count, total): #判斷某單字是否為整本書的keyword
    if word not in count_web1t: return False
    rate = math.log10(count)-math.log10(total)-(math.log10(count_web1t[word])-12)
    return rate >= 1

def is_exist(word): #計算某單字存在於幾個章節
    c = 0
    for ch in range(50):
        if word in count_chapter[chaptername[ch+1]]:
            c = c + 1
    return c

def total_bigram_count(bigram): #計算各章節某bigram的出現次數及出現的章節
    total = 0
    c = 0
    for ch in range(50):
        if bigram in count_chapter_bigram[chaptername[ch+1]]:
            c = c + 1
            total = total + count_chapter_bigram[chaptername[ch+1]][bigram]
    return c,total
                

def is_key_in_chapter(word, chapter,keyword_list): #計算某單字是否為某章節的keyword
    if word not in count_web1t: return False
    ch = is_exist(word)    
    chapter_name = chaptername[chapter]
    total_count = count_how_to[word]
    count = count_chapter[chapter_name][word]
    if(count > (total_count / ch)):
        keyword_list.append((word,count))

def is_key_in_chapter_phrase(phrase, chapter,keyword_list): #計算某bigram是否為某章節的keyword
    if phrase not in count_web2t: return False
    chapter_name = chaptername[chapter]
    ch,total_count = total_bigram_count(phrase)
    count = count_chapter_bigram[chapter_name][phrase]
    if(count > (total_count / ch)):
        keyword_list.append((phrase,count))

def chapter_keyword(chapter): #製作單個章節的keyword list
    if(chapter<1 or chapter>50): return False
    kw = []
    keylist = list(count_chapter[chaptername[chapter]].keys())
    for k in keylist:
        is_key_in_chapter(k,chapter,kw)
    return kw
    
def chapter_keyphrase(chapter): #製作單個章節的keyword list
    if(chapter<1 or chapter>50): return False
    kw = []
    keylist = list(count_chapter_bigram[chaptername[chapter]].keys())
    for k in keylist:
        is_key_in_chapter_phrase(k,chapter,kw)
    return kw
    
def check(word): #檢查各章節某單字出現次數
    for i in range(50):
        print(count_chapter[chaptername[i+1]][word])

def check_bigram(phrase,chapter): #檢查某章節特定bigram
    chapter_name = chaptername[chapter]
    ch,total_count = total_bigram_count(phrase)
    count = count_chapter_bigram[chapter_name][phrase]
    print('phrase:',phrase)
    print('ch:',ch)
    print('total_count:',total_count)
    print('count:',count)
    
total = sum(count_how_to.values())
keywords = [ (word, count) for word, count in count_how_to.items() if is_key(word, count, total) and count>3]
#print ('There are', len(keywords), 'keywords in %s.'%('how.to.say.it.bundles.%s.%s+.txt'%(NGRAM_DEGREE,MIN_COUNT)))
#with open('how.to.say.it.bundles.%s.%s+.txt'%(NGRAM_DEGREE,MIN_COUNT), 'w') as outfile:
for word, count in sorted(keywords, key=lambda x: -x[1]):
    print ('\t'.join([word, str(count)]))

"""
Level A
"""  
#klist = chapter_keyword(2)    
#bigram_list = chapter_keyphrase(2)

"""
Level B
"""
linggle = Linggle()

def ngramcount(query):
    return linggle[query]

accept_words = '''accept invite approve certainly delighted
gratifying pleased pleasure
satisfying thoughtful thrilled
touched welcome willing'''.split()
print (accept_words)
print ()

def cluster_analysis(chapter):
    if(chapter<1 or chapter>50): return False
    accept_words = []
    keyword_list = chapter_keyword(chapter)    
    for word,count in keyword_list:
        accept_words.append(word)
    and_grams = ngramcount('%s and %s'%('/'.join(accept_words), '/'.join(accept_words)))
    pprint.pprint (and_grams)

#cluster_analysis(1)

"""
Level C
"""
sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
for chapter in open('how.to.say.it.(raw).txt').read().split('<chapter>')[1:-1]:
    sentences = sent_detector.tokenize(chapter)
    sentences = [ sentence for sentence in sentences 
                     if sentence[0].isupper() and sentence[-1] in '?!.' ]
"""    
def printmd(string):
    return display(Markdown(string))
printmd("I am **delighted to accept** this position with such a distinguished company.")
"""