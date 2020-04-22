## 4/21 SKELL 字典最佳例句
英文字典的例句目的是要讓人容易搞懂這個單字的意思與用法，因此一本好的字典對於例句的選擇也是一個重要課題，這次作業是從Simple Wiki的句子找出常出現的ngram並且針對每個ngram給予最適合的例句。

### data
sentences.txt: Simple Wikipedia中取出的句子，Simple Wiki是使用比較簡單的單字的維基百科  
nc.txt: high-frequency ngrams 多個詞組成  
high_freq_words.txt: 17000 個 high-frequency words 單字  
prons.txt: a list of pronouns 代名詞 he,her,i,it之類的  
collocation.txt: collocations 搭配詞 兩個詞 ('A','B')  
evp.dataset.txt: 常用英文單字  
mp.collocation.sort.txt: 常見搭配詞＋詞性＋關係＋次數＋mutual information  其中 pair-wise mutual information 代表搭配的強度  

### python
共分為兩個py檔，一個是找出Simple Wiki中的所有常用ngram，另一個是針對每個ngram給予最合適的例句，例句來源同樣是Simple Wiki。由於input與output很大，此次作業設計成可以直接用command的pipeline送資料並輸出的方式。  

`GDEX-map.py`：  
找出Simple Wiki中的所有常用ngram，須滿足以下條件，規則可自訂：  
* the length (number of words) of sentence should >=10 and <=25
* ngram is from 2gram to 5gram
* ngram exists in nc.txt

`GDEX-reduce.py`：
針對每個ngram給予最合適的例句，自訂給分規則，選最高分的三個，主要考慮的點有以下四個，比例可以自己定，可以先算每個考慮因素的平均再調整比例，以下是我最終的打分規則：  
```
score = 0.25*location of ngram in the sentence S #ngram在例句中的位置 
    – 0.25*(word ∈ S & word ∉ high_freq_words.txt) #非常用字數量
    – 0.5*(word ∈ S & word ∈ prons.txt) #代名詞數量
    + 0.25*(collocation ∈ S & collocation ∈ collocation.txt) #涵蓋的常用搭配詞組數
```

### command line
`cat sentences.txt | python GDEX-map.py > result_map.txt`  
`cat result_map.txt | python GDEX-reduce.py > result_reduce.txt`  

[作業要求](https://hackmd.io/@BpUgvpG2TZy_PvDRF1bwvw/HyYCs7iPI)  
