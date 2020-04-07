#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 13:19:45 2020

@author: user
"""
import re
f = open(r'./ocw.1m')
data = f.readlines()
f.close()
def find_lb(st,l):
    st = st.lower()
    st = re.sub("[\s+\.\!\/\;_,$%^*(+\"\']+|[+——！，。?、~@#￥%……&*()：]+", ' ', st)
    st = st[1:-1] 
    sbst = st.split(" ")
    for i in range(l-4):
        index = ' '.join(sbst[i:i+4])
        #print(index)
        if(index in lb_dic):
            lb_dic[index] = lb_dic[index] + 1
            print(index)
        else:
            lb_dic[index] = 1

lb_dic = {}
for st in data:
    l = len(st.split(" "))
    if(l>=4):
        find_lb(st,l)

common = {k: v for k, v in lb_dic.items() if v > 40}
rank = sorted(common.items(),key=lambda item:item[1],reverse=True)
  