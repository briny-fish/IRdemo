# -*- coding:utf-8 -*-
'''
@author: Yongchang Cao
@contact: cyc990520@gmail.com
@file: baidu_api.py
@time: 2020/10/22 7:34
@desc: 调用百度翻译API， 每月前200w字免费
'''

# 导入相关模块
import hashlib
import random
import requests
import json

# 你的APP ID
appID = 'kmug50KlrS5GGkFcdE1cgTTE'

apiKey = 'kmug50KlrS5GGkFcdE1cgTTE'
# 你的密钥
secretKey = 'a28P8WQoz2MC7gHKAVA64g1N5xQZiB0Q'
# 百度翻译 API 的 HTTP 接口
apiURL = 'https://aip.baidubce.com/rpc/2.0/mt/texttrans/v1'

def get_accessToken(apiKey, secretKey):
    url = "https://aip.baidubce.com/oauth/2.0/token?client_id=%s&client_secret=%s&grant_type=client_credentials" % (apiKey, secretKey)
    print(url)
    payload = ""
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    ans = json.loads(response.text)
    print(ans['access_token'])
    return ans['access_token']

accessToken = get_accessToken(apiKey,secretKey)

def baiduAPI_translate(query_str, to_lang):
    '''
    传入待翻译的字符串和目标语言类型，请求 apiURL，自动检测传入的语言类型获得翻译结果
    :param query_str: 待翻译的字符串
    :param to_lang: 目标语言类型
    :return: 翻译结果字典
    '''
    params = {
        'q': query_str,
        'from': 'auto',
        'to': to_lang,
        'access_token': accessToken,
    }
    try:
        # 直接将 params 和 apiURL 一起传入 requests.get() 函数
        response = requests.get(apiURL, params=params)
        # 获取返回的 json 数据
        result_dict = response.json()
        # 得到的结果正常则 return
        if 'result' in result_dict and 'trans_result' in result_dict['result']:
            return result_dict
        else:
            print('Some errors occured:\n', result_dict)
    except Exception as e:
        print('Some errors occured: ', e)


def baiduAPI_translate_main(query_str, dst_lang=''):
    '''
    解析翻译结果后输出，默认实现英汉互译
    
    :param query_str: 待翻译的字符串，必填
    :param dst_lang: 目标语言类型，可缺省
    :return: 翻译后的字符串
    '''
    result_dict = baiduAPI_translate(query_str, dst_lang)
    dst = result_dict['result']['trans_result'][0]['dst']
    print('{}: {} -> {}: {}'.format(result_dict['result']['from'], query_str, result_dict['result']['to'], dst))
    return dst


if __name__ == '__main__':
    print(baiduAPI_translate_main('peach   apple','zh'))
    baiduAPI_translate_main('这是中文','en')
    baiduAPI_translate_main('翻译成法语', 'fra')
    # get_accessToken(apiKey,secretKey)