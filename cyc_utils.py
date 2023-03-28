# -*- coding:utf-8 -*-
'''
@author: Yongchang Cao
@contact: cyc990520@gmail.com
@file: cyc_utils.py
@time: 2020/10/22 8:53
@desc: 自定义功能库
'''

import os
import pickle
from tqdm import tqdm
# import synonyms


syno_f = open('./dict_synonym.txt', 'r', encoding='utf-8')
syno_dict = [a[9:].strip().split(' ') for a in syno_f.readlines()]
# synonyms.nearby('init')

def get_syno_list(word):            #获取输入单词的近义词list
    # ans = synonyms.nearby(word)[0]
    # if word in ans : ans.remove(word)
    # return ans
    if word == '计算机': return ['电脑']
    for item in syno_dict:
        if word in item:
            item.remove(word)
            return item
    return []

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
    print('\nloading vectors......')
    for line in tqdm(f):
        vec = [float(a) for a in line.strip().split(',')]
        vectors.append(vec)
    titles = []
    f = open(os.path.join(folder, 'titles.txt'), 'r', encoding='utf-8')
    print('\nloading titles......')
    for line in tqdm(f):
        titles.append(line.strip())
    assert len(ids) == len(vectors) == len(titles)
    return ids, vectors, titles

if __name__ == '__main__':

    ans = get_syno_list('计算机')         #获取同义词的case
    print(ans)
    ans = get_syno_list('电脑')  # 获取同义词的case
    print(ans)
    # ans = get_syno_list('刮胡刀')  # 获取同义词的case
    # print(ans)


    ids, vectors, titles = read_from_sim('./sim_folder')
    print(len(ids), len(vectors), len(titles))
