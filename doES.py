from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import sqlite3
conn = sqlite3.connect('sys.db')
cursor = conn.cursor()
es = Elasticsearch([{'host':'localhost','port':9200}])

print(es)
lawname = ['SGB','SGC','HKB','HKC','UKB','UKC']
def readdata():

    rtans=[]
    for name in lawname:
        cursor.execute('select * from %s'%(name))
        bodylist = cursor.fetchall()
        cursor.execute('select * from %s'%(name+'ans'))
        anslist = cursor.fetchall()
        rtans0=[]
        for i in range(len(bodylist)):
            tmplist = []
            tmplist.append(bodylist[i][0])
            tmplist.append(name)
            tmplist.append(bodylist[i][1])
            tmplist.append(bodylist[i][2])
            tmplist.append(anslist[i][1])
            tmplist.append(anslist[i][2])
            tmplist.append(anslist[i][3])
            tmplist.append(anslist[i][4])
            tmplist.append(anslist[i][5])
            tmplist.append(anslist[i][6])
            tmplist.append(anslist[i][7])
            tmplist.append(anslist[i][8])
            tmplist.append(anslist[i][9])
            tmplist.append(anslist[i][10])
            tmplist.append(anslist[i][11])
            tmplist.append(anslist[i][12])
            rtans0.append(tmplist)
        rtans.append(rtans0)
    return rtans

def save2Dict( data ):
    datalist = []
    for d in data:
        try:
            info = {}
            info["nid"] = d[0]
            info["lawname"]=d[1]
            info["title"] = d[2]
            info["body"] = d[3]
            info["SGB"] = d[4]
            info["SGBv"] = d[5]
            info["SGC"] = d[6]
            info["SGCv"] = d[7]
            info["HKB"] = d[8]
            info["HKBv"] = d[9]
            info["HKC"] = d[10]
            info["HKCv"] = d[11]
            info["UKB"] = d[12]
            info["UKBv"] = d[13]
            info["UKC"] = d[14]
            info["UKCv"] = d[15]

            datalist.append( info )
        except:
            print( d ,"is error ")
            continue
    return  datalist

tmpkeys = ['id','SGB','SGBans','SGC','SGCans','HKB','HKBans','HKC','HKCans','UKB','UKBans','UKC','UKCans']
def save2ES( index,type, data ):
    actions = []
    for d in data:
        action = {
            "_index": type,
            "_type": type,
            "_source": d
        }
        actions.append(action)
        # 批量处理
    result = bulk(es, actions, index=index, raise_on_error=True,request_timeout=100)
    print( result )
data = readdata()
for i in range(len(data)):
    data[i]=save2Dict(data[i])
    save2ES('laws',str.lower(lawname[i]),data[i])
