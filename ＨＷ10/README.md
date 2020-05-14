## 5/12 EM演算法 機器翻譯
統計機器翻譯（英語：Statistical Machine Translation，簡寫為SMT）是機器翻譯的一種。  
也是目前非限定領域機器翻譯中效能較佳的一種方法。  
統計機器翻譯的基本思想是通過對大量的平行語料進行統計分析，構建統計翻譯模型，進而使用此模型進行翻譯。  
從早期基於單字的機器翻譯，後來演化出片語翻譯系統，以進一步提高翻譯的精確性。  
2016年前Google翻譯的大部分語言對採用的都是統計機器翻譯的方法。  
而Google亦在此本領域保持領先地位，在美國國家標準局組織的機器翻譯評測中遙遙領先。  
但Google翻譯在2016年11月開始使用神經機器翻譯作為主要翻譯系統，並開發了Google神經機器翻譯系統。  
統計機器翻譯基於雜訊通道模型，說明語言產生（語言模型），以及轉換語言（通道模型）。在此統計模型基礎上，定義要估計的模型參數（詞彙接續機率，詞彙翻譯機率）。  
早期的基於詞的統計機器翻譯採用的是 EM 演算法，採用最大似然準則進行無監督訓練。  
[作業要求](https://hackmd.io/0E6yI_7lSZeM3hYlSv1zuw#Example)  
#### IBM Model 1
input:  
`check_top_k_prob('學校', 5, t_ef)`
output:  
```
p(school | 學校) = 0.7543461511392134
p(schools | 學校) = 0.14944245769188017
p(at | 學校) = 0.08704250211023348
p(the | 學校) = 0.003338099172844306
p(has | 學校) = 0.0023705730539251087
```

#### IBM Model 2
input:  
`translate(['我', '會', '騎', '腳踏車'], 5, t_ef_2, q_alg)`
output:  
```
possible candidates for the 1-th English word:
i               probability:0.31278907260462047
a               probability:0.07578017037116473
my              probability:0.07443197844766612

possible candidates for the 2-th English word:
i               probability:0.22366274850534001
bike            probability:0.17055958090381093
bicycle         probability:0.07670599220180264

possible candidates for the 3-th English word:
riding          probability:0.08944179294600361
bike            probability:0.08797482551405288
will            probability:0.07686275875064899

possible candidates for the 4-th English word:
i               probability:0.15569392796224918
riding          probability:0.08984803037656636
ride            probability:0.07676970665583595

possible candidates for the 5-th English word:
bike            probability:0.34370933145383814
bicycle         probability:0.15457686492002765
i               probability:0.08895165883739573
```  
### EM Algorithm
[EM演算法](https://zh.wikipedia.org/wiki/%E6%9C%80%E5%A4%A7%E6%9C%9F%E6%9C%9B%E7%AE%97%E6%B3%95)  
### tips
```
test_dic=defaultdict(lambda: defaultdict(lambda: 0.1))
```
這代表默認值為0.1，如果沒有定義某字典值直接呼叫就會是0.1。  
因為是二維，所以`test_doc['test1']['test2']`會回傳0.1。  

`q_alg[i][j][l_e][l_f]`是指第j個英文單字在英文句子長度為l_e、中文句子長度為l_f的情況下，對應到第i個中文詞的機率    