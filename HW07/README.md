## 4/14 繁體中文 文法改錯
這次作業主要是介紹CKIP，並且使用CKIP完成一個簡易文法改錯標示工具。  
input:  
```
orig = ['這', '也', '間接', '突顯出', '鴻海']
cor = ['也', '直接', '透露出', '鴻海']
```

output:  
```
(2,'R','間接','直接')
(3,'R','突顯出','透露出')
(0,'D','這')
```
[作業說明](https://hackmd.io/1MLfFAuDRB6orc4h8QZXrg?view)  
### 虛擬環境
要安裝這套工具，Python至少要3.6以上，且tensorflow的版本要小於2，因此我決定另外建一個虛擬環境來完成這次作業。  
`conda create --name myenv python=3.6` 雖然用conda介面也可以建，但不知為何我的按下去沒有反應，所以只好用command建一個名為`myenv`的虛擬環境，版本直接指定3.6。  
`source activate myenv` 如果是Linux或macOS可以這樣開啟虛擬環境，開啟後shell前面應該會出現`(虛擬環境名稱)`。  
`activate myenv` Window的開啟方式略有不同。  
接著就是`pip install` 裝這次作業會用到的套件了。  
`conda install spyder` 順便裝個spyder。  
`conda env remove --name myenv` 以後如果要把這個虛擬環境丟掉可以用conda直接刪。  
`pip list` 可以看環境中所有載過的套件及其版本，不合的就uninstall掉重裝適合的版本。  
### 安裝 ckiptagger
這次的作業需要用到CKIP，CKIP是NLP在繁體中文斷詞中的霸主，是由台灣中研院資訊所、語言所於民國 75 年成立的中文語言言小組所開發，也在多個中文斷詞的比賽當中得過獎。在2019年9月終於[開源](https://github.com/ckiplab/ckiptagger/wiki/Chinese-README)了。  
```
pip install ckiptagger
pip install tensorflow==1.9
pip install gdown
```
要裝之前至少先裝好以上三個，ckiptagger就是開源的那包的最簡易版，載下來後有api.py可以再去載其他model。由於model有用到tensorflow，所以也要先載好，而且要 < 2.0。gdown這個套件則是用來從google drive載東西下來的。有了這些以後直接在終端機跑下面的py code。  
```
# -*- coding: utf-8 -*-
from ckiptagger import data_utils
data_utils.download_data_gdown("./")
```
這樣會把雲端的model載到目前的資料夾中，在這裡我遇到一個問題，系統報錯：  
```
AttributeError: module 'tensorflow.compat' has no attribute 'v1'
```
餵狗後的解法是直接去改api，從錯誤訊息中可以看到該api所在位置，直接vim他，找到tf.compat.v1.XXX的部分(XXX是他報錯的function)改成tf.XXX，vim可以直接用`/`去搜尋，很快就可以找到，改完有報錯就再去改api.py，改到沒報錯就可以了。  
接著就可以開啟作業匯入要用到的工具了:  
`from ckiptagger import WS, POS, NER`  
不過還是要去[github](https://github.com/ckiplab/ckiptagger)上的**Download model files**那邊把model下載下來。  

### 其他用到的網站
[中文單字詞性列表](https://github.com/ckiplab/ckiptagger/wiki/POS-Tags)  
[CKIP介紹](https://clay-atlas.com/blog/2019/09/24/python-chinese-tutorial-ckiptagger/)  