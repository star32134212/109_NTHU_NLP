import sys, fileinput
import re
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import word_tokenize

path = '/Users/user/Desktop/大四下/NLP/HW8/Week8'

lmtzr = WordNetLemmatizer() #回復原型

def tokens(s): return(nltk.word_tokenize(s))

def is_ngram(ngram):
    if ngram.lower() in ngram_set:
        return True
    
def grams(text, n):
    return [text[i:i+n] for i in range(0,len(text)-(n-1))]

def grams_in_nc2(gram):
    for g in gram:
        gram_nc = g[0]+' '+g[1]
        if(gram_nc in ngram_set):
            print(gram_nc+'\t'+line,end='')
            
def grams_in_nc3(gram):
    for g in gram:
        gram_nc = g[0]+' '+g[1]+' '+g[2]
        if(gram_nc in ngram_set):
            print(gram_nc+'\t'+line,end='')        
            
def grams_in_nc4(gram):
    for g in gram:
        gram_nc = g[0]+' '+g[1]+' '+g[2]+' '+g[3]
        if(gram_nc in ngram_set):
            print(gram_nc+'\t'+line,end='')
            
def grams_in_nc5(gram):
    for g in gram:
        gram_nc = g[0]+' '+g[1]+' '+g[2]+' '+g[3]+' '+g[4]
        if(gram_nc in ngram_set):
            print(gram_nc+'\t'+line,end='')
            
ngram_set = set([line.strip() for line in fileinput.input(path+'/nc.txt')])



for line in fileinput.input():
    ##### YOUR CODE HERE #####
    line2 = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）：]+", ' ', line)
    line2 = line2.lower()
    sent = tokens(line2)
    #sent = [lmtzr.lemmatize(word) for word in sent]
    if(len(sent) >= 10 and len(sent) <= 25):
        grams2 = grams(sent, 2)
        grams3 = grams(sent, 3)
        grams4 = grams(sent, 4)
        grams5 = grams(sent, 5)
        grams_in_nc2(grams2)
        grams_in_nc3(grams3)
        grams_in_nc4(grams4)
        grams_in_nc5(grams5)




    
    
    