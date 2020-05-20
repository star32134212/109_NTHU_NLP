## 5/19 以英翻中再翻英處理同義字代換
作業：week12.py  
[作業要求](https://hackmd.io/fF1PP3sXShGNy50-_FwNXw?view)    

有一種同義詞找法是先把同義詞翻成另一種語言的單詞，再對該語言單詞從新翻譯回來，此次作業就是要實作這種方法。  
e1 -> c1 -> e2 : 表示從英文單字e1翻譯成中文單字c1，再從c1翻譯成英文單詞e2，c1不只一個，先對所有路徑算出paraphrase probability = P(c1|e1) * P(e2|c1)，也就是e1翻譯成c1的機率乘上c1翻譯成e2的機率，然後將原本的句子透過kenlm model得到一個 sentence probability ，再求paraphrase probability 與 sentence probability 的乘積，求乘積最高的值即為該句最恰當的同義詞。  