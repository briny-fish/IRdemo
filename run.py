from flask import Flask,render_template,request
from flask_bootstrap import Bootstrap
from elasticsearch import Elasticsearch
from flask import Flask, Response, jsonify
from queue import PriorityQueue as PQ
import Levenshtein
import ngtdemo
import numpy as np
import baidu_api
import heapq
import cyc_utils
import  random
from elasticsearch.helpers import bulk
es = Elasticsearch([{'host':'localhost','port':9200}], http_auth=('elastic', '123456123'),)
app = Flask(__name__)
import sqlite3

def getvec():
    return cyc_utils.read_from_sim('./sim_folder')

ids,vec,title = getvec()
Vec={}
Title={}
for i in range(len(ids)):
    Vec[ids[i]]=vec[i]
    Title[ids[i]]=title[i]
index = ngtdemo.getIndex(vec[0:-1])
bootstrap = Bootstrap(app)

def Comp(a,b):
    c = np.multiply(np.array(a),np.array(b))
    mo = np.linalg.norm(np.array(a))*np.linalg.norm(np.array(b))
    c = c.tolist()
    if mo<=0.00001:return 0.0
    return 1-((1-((1.0+sum(c)/mo)/2.0))*3)
def stIpc(data):
    tot = {}
    ans = []
    for i in data:
        tmp = i['ipcmain'][0:4]
        if(tmp not in tot.keys()):
            tot[tmp] = 0
        else:
            tot[tmp]+=1
    for key,value in tot.items():
        if(value>10):
            ans.append((key,value))
    return ans
def stApplicant(data):
    tot = {}
    ans = []
    for i in data:
        tmp = i['applicant']
        if (tmp not in tot.keys()):
            tot[tmp] = 0
        else:
            tot[tmp] += 1
    for key,value in tot.items():
        if(value>10):
            ans.append((key,value))
    return ans
def stAgency(data):
    tot = {}
    maxagency = ''
    maxnum = 0
    ans = []
    for i in data:
        tmp = i['Agency']
        if (tmp not in tot.keys()):
            tot[tmp] = 0
        else:
            tot[tmp] += 1
    for key,value in tot.items():
        if(value>10):
            ans.append((key,value))
    return ans
@app.route('/',methods=['GET','POST'])
def home():
    return render_template('search.html')
@app.route('/list',methods=['GET','POST'])
def lis():
    return render_template('list.html')
@app.route('/searchAll',methods=['GET','POST'])
def searchAll():
    print(request.args)
    data = request.args.get('keyword')
    page = int(request.args.get('page'))
    page_size = int(request.args.get('page_size'))
    #翻译api暂时没更新
    # data = baidu_api.baiduAPI_translate_main(data,'zh')

    if(len(data)<=3):
        tmp = cyc_utils.get_syno_list(data)
        mi = min(len(tmp),4)
        if(mi>0):
            data=data+' '+' '.join(tmp[:mi])
    data1 = es.search(index=str.lower('full_item'), size=500, body={
        "query": {

    "bool": {
      "should": [
        {
          "match": {
            "title": {
              "query": data,
              "boost": 3
            }
          }
        },
        {
          "match": {
            "abstract": data
          }
        },
          {
              "match": {
                  "requirement": data
              }
          }
      ]
    }
  }
})['hits']
    print(data)
    datart = []
    for line in data1['hits']:
            datart.append(line['_source'])
    rst = {}
    rst['statisticsIpc'] = stIpc(datart)
    rst['statisticsApplicant'] = stApplicant(datart)
    rst['statisticsAgency'] = stAgency(datart)

    rst['zh'] = data
    rst['total'] = data1['total']['value']
    rst['total1'] = len(datart)
    rst['textList'] = datart[(page - 1) * page_size:page * page_size]
    rst['code'] = 200

    return jsonify(rst)

@app.route('/searchipc',methods=['GET','POST'])
def searchipc():
    print(request.args)
    data = request.args.get('ipc')
    print(data)
    page = int(request.args.get('page'))
    page_size = int(request.args.get('page_size'))
    data1 = es.search(index=str.lower('full_item'),size=500, body={
    "query": {

        "wildcard": { "ipcmain": data+"*"}
         }
        ,"track_total_hits":True
    })['hits']
    datart = []
    for line in data1['hits']:
        datart.append(line['_source'])
    rst = {}
    rst['total'] = data1['total']['value']
    rst['total1'] = len(datart)
    rst['textList'] = datart[(page - 1) * page_size:page * page_size]
    rst['code'] = 200
    rst['statisticsIpc'] = stIpc(datart)
    rst['statisticsApplicant'] = stApplicant(datart)
    rst['statisticsAgency'] = stAgency(datart)
    print(data1)
    return jsonify(rst)

@app.route('/searchappnum',methods=['GET','POST'])
def searchappnum():
    print(request.args)
    data = request.args.get('appnum')
    print(data)
    data1 = es.search(index=str.lower('full_item'),size=1, body={

    "query": {
        "match": { "appnum": data}
         }
    })['hits']
    datart = []
    for line in data1['hits']:
        datart.append(line['_source'])
    rst = {}
    rst['total'] = data1['total']['value']
    rst['total1'] = len(datart)
    rst['textList'] = datart
    rst['code'] = 200
    rst['statisticsIpc'] = stIpc(datart)
    rst['statisticsApplicant'] = stApplicant(datart)
    rst['statisticsAgency'] = stAgency(datart)
    print(data1)
    return jsonify(rst)

@app.route('/searchenzh',methods=['GET','POST'])
def searchenzh():
    print(request.args)
    data = request.args.get('en')
    page = int(request.args.get('page'))
    page_size = int(request.args.get('page_size'))
    # 翻译api暂时没更新
    data = baidu_api.baiduAPI_translate_main(data,'zh')
    print(data)
    if (len(data) <= 3):
        tmp = cyc_utils.get_syno_list(data)
        mi = min(len(tmp), 4)
        if (mi > 0):
            data = data + ' ' + ' '.join(tmp[:mi])
    data1 = es.search(index=str.lower('full_item'), size=500, body={
        "query": {

            "bool": {
                "should": [
                    {
                        "match": {
                            "title": {
                                "query": data,
                                "boost": 3
                            }
                        }
                    },
                    {
                        "match": {
                            "abstract": data
                        }
                    },
                    {
                        "match": {
                            "requirement": data
                        }
                    }
                ]
            }
        }
    })['hits']
    print(data)
    datart = []
    for line in data1['hits']:
        datart.append(line['_source'])
    rst = {}
    rst['statisticsIpc'] = stIpc(datart)
    rst['statisticsApplicant'] = stApplicant(datart)
    rst['statisticsAgency'] = stAgency(datart)

    rst['zh'] = data
    rst['total'] = data1['total']['value']
    rst['total1'] = len(datart)
    rst['textList'] = datart[(page - 1) * page_size:page * page_size]
    rst['code'] = 200

    return jsonify(rst)


@app.route('/detail',methods=['GET','POST'])
def detail():
    data = request.args.get('id')
    print(data)
    return render_template('detail.html')
@app.route('/text',methods=['GET','POST'])
def gettext():
    print(request.args)
    data = request.args.get('id')

    print(data)
    data1 = es.search(index=str.lower('full_item'), size=1, body={
        "query": {
            "match": {
                "appnum": data
            }
        }
    })['hits']['hits'];
    print(data1)
    datart = []
    for line in data1:
        datart.append(line['_source'])
    rst = {}
    print(datart)
    rst['total'] = len(datart)
    rst['data'] = datart[0]
    rst['code'] = 200

    return jsonify(rst)
def comptitle(a,b):
    return Levenshtein.ratio(a, b)
def getIdList(id):
    q = []
    print(2)
    print(len(Vec[id]))
    idx,dist=ngtdemo.getneighbours(Vec[id],500,index)
    print(3)
    T = Title[id]
    for i in idx:
        simtitle=comptitle(T,Title[ids[i]])
        q.append((simtitle*(Comp(Vec[id],Vec[ids[i]])),ids[i]))
    datas=[]
    scores=[]
    tmp = heapq.nlargest(10,q,key=lambda x:x[0])
    for i in tmp:
        datas.append(i[1])
        scores.append(i[0])
    return datas,scores
@app.route('/recom',methods=['GET','POST'])
def getrecom():
    print(request.args)
    print(1)
    datas,scores = getIdList(request.args.get('id'))
    print(datas)
    datart = []
    cnt=0
    for data in datas:
        data1 = es.search(index=str.lower('full_item'), size=1, body={
            "query": {
                "match": {
                    "appnum": data
                }
            }
        })['hits']['hits'];
        print(data1)

        for line in data1:
            datart.append(line['_source'])
            datart[-1]['score']=scores[cnt]
        cnt+=1
    rst = {}
    print(datart)
    rst['total'] = len(datart)
    rst['textList'] = datart
    rst['code'] = 200

    return jsonify(rst)

if(__name__=='__main__'):
    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', port=5000)
