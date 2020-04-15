#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 16:20:01 2020

@author: user
"""
from ckiptagger import data_utils, construct_dictionary, WS, POS, NER
import nltk
import re
import numpy as np
ws = WS('data')
pos = POS('data')

def before_edit(text):
    return re.sub('(\[\-|\-\]|\{\+.*?\+\})', '', text)
    
def after_edit(text):
    return re.sub('\[\-.*?\-\]|\{\+|\+\}', '', text)

text = '[-這-]也[-間-][-接-]{+直+}{+接+}{+透露+}{+出+}[-突-][-顯-][-出-]鴻海'


text_before = ' '.join(ws(before_edit(text).splitlines())[0])
print (text_before)

text_after = ' '.join(ws(after_edit(text).splitlines())[0])
print (text_after)


def seg_pos(text):
    inputlist =[]
    inputlist.append(text)
    output=[]
    ws2 = ws(inputlist)
    pos2 = pos(ws2)
    for i in zip(ws2[0], pos2[0]): 
        output.append(i)
    return output
    ##### Your code here #####

sent_orig = seg_pos(before_edit(text))
sent_correct = seg_pos(after_edit(text)) 
sent_orig, sent_correct


def get_sub_cost(o, c, optype):
    if(optype == 'ID'):
        cost =  nltk.edit_distance(o[1] + o[0], '') + nltk.edit_distance(c[1] + c[0], '')
    elif(optype == 'R'):
        cost =  len(set(o) | set(c)) - len(set(o) & set(c))
    return cost

def calculate_edit_cost(orig, cor):
    o_len = len(orig)
    c_len = len(cor)
    # Create the cost_matrix and the op_matrix
    cost_matrix = [[0 for j in range(c_len+1)] for i in range(o_len+1)]
    op_matrix = [["O" for j in range(c_len+1)] for i in range(o_len+1)]
    # Fill in the edges
    for i in range(1, o_len+1):
        cost_matrix[i][0] = nltk.edit_distance(orig[i-1][1] + orig[i-1][0], '')
        op_matrix[i][0] = "D"
    for j in range(1, c_len+1):
        cost_matrix[0][j] = nltk.edit_distance('', cor[j-1][1] + cor[j-1][0])
        op_matrix[0][j] = "I"

    # Loop through the cost_matrix
    for i in range(o_len):
        for j in range(c_len):
            # Matches
            if orig[i] == cor[j]:
                cost_matrix[i+1][j+1] = 0
                op_matrix[i+1][j+1] = "M"
            # Non-matches
            else:
                ed = nltk.edit_distance(orig[i][0],cor[j][0])
                ln = max(len(orig[i][0]),len(cor[j][0]))
                if( (1 - ed/ln) > 0.3 or orig[i][1][0] == cor[j][1][0]):
                # 字詞有一定相似度 或 詞性屬於同一大類(看詞性第一個字)
                    optype = 'R'
                else:
                    optype = 'ID'
                op_matrix[i+1][j+1] = optype   
                cost_matrix[i+1][j+1] = get_sub_cost(orig[i],cor[j],optype)
                
                ##### Your code here #####
            
    # Return the matrices
    return cost_matrix, op_matrix



mycalculate = calculate_edit_cost(sent_orig, sent_correct)

def format_align(cost_matrix, op_matrix, orig, cor):
    set_orig = set(orig)
    set_cor = set(cor)
    output = []
    #check_insert = np.zeros((len(set_orig),len(set_cor))) #檢查insert情況用的
    for wd1 in (set_orig - set_cor):
        count = 0
        use_second = 0
        check = np.zeros(4) #在R的情況時用來比優先順序
        for wd2 in (set_cor - set_orig):
            inx1 = orig.index(wd1) + 1 #在matrix的index
            inx2 = cor.index(wd2) + 1 #在matrix的index
            if(op_matrix[inx1][inx2] != 'ID'): #有R要處理
                count = count + 1
                ed = nltk.edit_distance(wd1,wd2)
                ln = max(len(wd1),len(wd2))
                ed2 = nltk.edit_distance(sent_orig[orig.index(wd1)][1],sent_correct[cor.index(wd2)][1])
                ln2 = max(len(sent_orig[orig.index(wd1)][1]),len(sent_correct[cor.index(wd2)][1]))
                if( (1 - ed/ln) > check[0]):
                    check[0] = 1 - ed/ln
                    check[1] = inx2 - 1
                    use_second = 0 #如果有兩個一樣相似的詞但是他們不是最大相似距離，那也不用方案二
                if( (1 - ed/ln) == check[0]):
                    use_second = 1 #第一種比不出來只好用第二種規則比較
                if( (1 - ed2/ln2) > check[2] ):
                    check[2] = 1 - ed2/ln2
                    check[3] = inx2 - 1
        if(count > 0): #Replace的情況分兩種討論
            if(use_second == 1): #用方案二比較--詞性比較
                ans = '('+str(orig.index(wd1)) + ',\'R\',\'' + wd1 + '\',\'' + cor[int(check[3])+1] +'\')'
            elif(use_second == 0): #用方案一比較--字詞距離比較
                ans = '('+str(orig.index(wd1)) + ',\'R\',\'' + wd1 + '\',\'' + cor[int(check[1])+1] +'\')'
            output.append(ans)
            print(ans)
        else: #Delete的情況 
            if(wd1 not in set_cor):
                ans = '('+str(orig.index(wd1)) + ',\'D\',\'' + wd1 +'\')'
            output.append(ans)
            print(ans)
    """            
    for wd2 in (set_cor - set_orig):
        inx2 = cor.index(wd2) + 1 
        for i in range(1,len(set_orig)+1):
            if(op_matrix[i][inx2] != 'ID' and check_insert[i-1][inx2-1] != 1):
                ans = '('+str(cor.index(wd2)) + ',\'I\',\'' + wd2 +'\')'
                output.append(ans)
                print(ans)
    """

    ##### Your code here #####
    return output

s = ws(before_edit(text).splitlines())[0]
t = ws(after_edit(text).splitlines())[0]
print(s)
print(t)
cost_matrix, op_matrix = calculate_edit_cost(sent_orig, sent_correct)
myans = format_align(cost_matrix, op_matrix, s, t)