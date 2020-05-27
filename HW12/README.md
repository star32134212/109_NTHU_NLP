## 5/26 利用Rank Ratio 找出英文片語和bigram專有名詞
作業：week13.py  

若兩個單詞湊在一起是個專有名詞或片語的話，那相對其他便湊的兩個字，他出現的頻率應該較高。這次作業實作兩個演算法，可以從文本中挑出這些字。  

### mutal information
`MI = P(hot dog) / (P(hot) * P(dog))`  
`hot dog`出現的次數除以`hot`單獨出現以及`dog`單獨出現的次數乘積  

### Rank Ratio
`RR = sqrt(mean_Rank(hot _) * mean_Rank(_ dog)) / Rank(hot dog)`  
`mean_Rank(hot _)` 所有以hot為開頭的bigram的出現次數排名平均  
`mean_Rank(_ dog)` 所有以dog為結尾的bigram的出現次數排名平均  
`Rank(hot dog)`  hot dog出現次數的排名  
