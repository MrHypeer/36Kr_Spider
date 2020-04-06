from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

def getPage(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    try:
        bs = BeautifulSoup(html.read(), 'html.parser')
    except AttributeError as e:
        return None
    return bs #其实可以返回数组的吧？

pageInf = getPage('https://36kr.com/')
if pageInf == None:
    print('Title could not be found')
else:
    EssayTag = pageInf.find_all('a',{'class':'article-item-channel'})
    EssayTitle = pageInf.find_all('a',{'class':'article-item-title weight-bold'})
    for i in range(len(EssayTag)):
        print(EssayTag[i].get_text()+'|'+EssayTitle[i].get_text())
