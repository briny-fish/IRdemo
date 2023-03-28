import pandas as pd
import os
base_url='拆分数据集'

#df = pd.read_excel(base_url+'/100000.xlsx')
#df.to_csv('file0.txt', header=None, sep=',', index=False)
for root, dirs, files in os.walk(base_url):
    for file in files:
        print(file) #当前路径下所有非目录子文件
        df = pd.read_excel(base_url+'/'+file)
        df.to_csv(file+'txt', header=None, sep=',', index=False)