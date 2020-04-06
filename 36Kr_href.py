from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
import re
from random import choice
#处理远程主机强迫关闭了一个现有的连接
import time
import socket

socket.setdefaulttimeout(10)
linkset = set()
linkNum = 0


def getLinks(Url):
    global linkset
    global linkNum
    prefix = 'https://36kr.com'#相对路径补全操作
    try:
        html = urlopen(Url)
        bs = BeautifulSoup(html.read(), 'html.parser')
        html.close()
        for link in bs.find_all('a',href=re.compile('^(/p/)')):
            if 'href' in link.attrs:
                if link.attrs['href'] not in linkset:
                    linkNum = linkNum+1
                    newLink = link.attrs['href']
                    print("%d,%s"%(linkNum,prefix+newLink))
                    linkset.add(newLink)
                    time.sleep(0.3)
                    getLinks(prefix+newLink)
        return linkset
    except HTTPError as e:
        print('Error：网页在服务器上不存在')
        return linkset
    except URLError as e:
        print('Error：服务器不存在')
        return linkset
    except AttributeError as e:
        return linkset

target = 'https://36kr.com/information/web_news'
try:
    collection = getLinks(target)
    if collection == None:
        print('链接异常')
    else:
        print("%s,%d"%('共采集连接 ',len(collection)))
except socket.timeout:
        print('获取连接超时！')
        print("%s,%d"%('共采集连接 ',len(collection)))
