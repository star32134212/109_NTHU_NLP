## 5/6 搭配詞改錯
統計式文法改錯並找出同意思的寫法。
[作業要求](https://hackmd.io/tZ34-bq-SMeZ_Un64cCzDQ?view)  

input:  
`LM([[('reach', 1), ('dream', 3)]], "He reach his dream".split())`  

output:  
```
========Candidate collocations========
[('attain', 'perfection', 6.188068326013832, 1.0), ('confide', 'dream', 4.911246573570186, 0.5), ('reach', 'perfection', 4.266382377932291, 1.0), ('achieve', 'perfection', 4.059131736022359, 1.0), ('communicate', 'dream', 3.8565233872293465, 0.5), ('relinquish', 'dream', 3.516805978898456, 0.5), ('succeed', 'dream', 3.184729928635011, 0.5), ('gain', 'perfection', 3.080774312841924, 1.0)]

[('He reach his perfection', -16.524425506591797, 10265), 
('He achieve his perfection', -16.949195861816406, 12478)]
```  
