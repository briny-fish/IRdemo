# -*- coding:utf-8 -*-
'''
@author: Yongchang Cao
@contact: cyc990520@gmail.com
@file: MydoES.py
@time: 2020/10/20 22:16
@desc:  实现将数据封装到es
'''
import os
import pickle
import math
from tqdm import tqdm
import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
# import sqlite3
# conn = sqlite3.connect('sys.db')
# cursor = conn.cursor()
es = Elasticsearch(hosts=['127.0.0.1:9200'])

print(es)
def read_from_file(folder, begin=100000, end=100000, test=False):
    '''
    从folder中读取文件列表，并从所有文件中选取最多max_item个项目
    '''
    num_item = 0
    retdata = []
    colname = ['title', 'abstract', 'applicant', 'Agency', 'ipc', 'ipcmain', 'appnum', 'appdata', 'requirement']

    filelist = os.listdir(folder)
    for name in filelist:
        if not test and name=='0001.xlsx': continue     #排除测试文件
        filename = os.path.join(folder, name)       #拼接
        data = pd.read_excel(filename, header=None, index_col=None, usecols=[0,1,4,13,22,23,39,55,119], names=colname)
        datalist = [data[col].values.tolist() for col in colname]
        for i in tqdm(range(len(datalist[0]))):
            details = [datalist[j][i] for j in range(len(colname))]
            for k in range(len(details)):
                if k == 7 and type(details[k])==type(0.0) and math.isnan(details[k]): details[k] = 'None'
                elif k!=7 and type(details[k])==type(0.0) and math.isnan(details[k]): details[k] ='None'
                if k==5: details[k] = details[k].replace('/','.')
            if 'None' in details:
                continue
            num_item += 1
            if num_item >= begin:
                retdata.append({a: b for a, b in zip(colname, details)})
                if len(retdata) > 100000:
                    save2ES('ThirdBulk', 'full_item', retdata, epochsize=1000)
                    retdata = []
            if num_item >= end:
                save2ES('ThirdBulk', 'full_item', retdata, epochsize=1000)
                retdata = []
                return
    if retdata != []:save2ES('ThirdBulk', 'full_item', retdata, epochsize=1000)
    return

def read_from_sim(folder, ):
    appid2id_path = os.path.join(folder, 'appid2id.txt')
    f = open(appid2id_path, 'rb')
    appid2id = pickle.load(f)
    id2appid = {b:a for a,b in appid2id.items()}
    f = open(os.path.join(folder, 'id_np.csv'), 'r', encoding='utf-8')
    ids = [int(float(line.strip())) for line in f.readlines()]
    ids = [id2appid[a] for a in ids]
    vectors = []
    f = open(os.path.join(folder, 'embed_np.csv'), 'r', encoding='utf-8')
    print('loading vectors')
    for line in tqdm(f):
        vec = [float(a) for a in line.strip().split(',')]
        vectors.append(vec)
    assert len(ids) == len(vectors)
    return ids, vectors

def save2ES(index, type, data, epochsize=1000):
    '''
    将{index, type, data}格式的数据放入ES，每次放入的大小为epochsize个
    '''
    actions = []
    for i, d in tqdm(enumerate(data)):
        action = {
            "_index": type,
            "_type": type,
            "_source": d
        }
        actions.append(action)
        if i+1 % epochsize == 0:        #按批次处理
            result = bulk(es, actions, index=index, raise_on_error=True, request_timeout=100)
            action = []
            print(result)
    result = bulk(es, actions, index=index, raise_on_error=True, request_timeout=100)
    print(result)

if __name__ =='__main__':
    # res = es.indices.delete('hot_keyword')
    read_from_file(r'C:\Users\cyc\Documents\新建文件夹',test=False, begin=0, end=1000000)
    # read_from_sim('./sim_folder')
    # print('num_item: ', num_item)
    # save2ES('ThirdBulk', 'full_item', data, epochsize=1000)

