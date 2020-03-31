## 3/31 HW5 Disambiguation
背單字常會遇到一個詞有多個意思的情況，這次作業就是要判定某一句話中的特定詞是其多個語意中的哪一個。  
以作業舉例來講，Bass這個詞可以有三個意思：  
* 低音部、男低音
* 樂器
* 鱸魚

透過訓練文本找出bass分別當這三種意思時與句中其他單詞的出現頻率，透過累加找出最有可能代表的意思。  
以bass為例，bass為一個word，他有三個意思表示三個class，一句話中除了要片段的字以外的詞定為Wi。  
每個word都有訓練集，訓練集由以各個class為意思的句子組成。

P1 = Wi在Class1訓練集中的出現次數 / Class1訓練集中的所有字數  
P2 = Wi在word訓練集中的出現次數 / word訓練集中的總和字數   
Weighti = log(P1/P2)  

接著比較整句話中要判斷的word以各個意思來看的Weight加總，最高的就是那個意思。  
範例output:  
```
most_similar('bass', 'Bass, catfish, and bluegill also inhabit the creek.') 
    = ("fish", 14.814981643783032)

most_similar('issue', 'He\'s contributed to several publications, including LA Review of Books, Purple, Issue, and Hesperios Journal.') 
    = ("magazine", 5.123843862532843)

most_similar('sentence', 'If it finds the accused guilty, it passes sentence on the accused according to law.') 
    = ("law", 5.77941354006321)
```
[作業要求](https://hackmd.io/r4m1CJOaSFee09tevLHbTA)  
