### pip install textrank4zh --user
import codecs
from textrank4zh import TextRank4Keyword

tr4w = TextRank4Keyword()
def getKeyWord(text, topK=12):
    
    ans = []
    tr4w.analyze(text=text, lower=True, window=2)
    for item in tr4w.get_keywords(topK, word_min_len=1):
        ans.append(item.word)
    return ' '.join(ans[:topK])

if __name__ == '__main__':
    text = '会上,中华社会救助基金会与“第二届中国爱心城市大会”承办方晋江市签约,许嘉璐理事长接受晋江市参与“百万孤老关爱行动”向国家重点扶贫地区捐赠的价值400万元的款物。'
    ans = getKeyWord(text)
    print(ans)
