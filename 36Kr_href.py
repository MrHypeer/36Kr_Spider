from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
import re
from random import choice
#处理远程主机强迫关闭了一个现有的连接
import time
import socket
import csv
import sys

class Website:
    """describing the webpage"""

    def __init__(self, name, url, targetPattern, absoluteUrl, titleTag, bodyTag):
        self.name = name
        self.url = url
        self.targetPattern = targetPattern
        self.absoluteUrl = absoluteUrl
        self.titleTag = titleTag
        self.bodyTag = bodyTag

class Content:
    """describing content in a page"""

    def __init__(self, url, title):
        self.url = url
        self.title = title

    def print(self):
        print("URL: {}".format(self.url))
        print("TITLE: {}".format(self.title))

class Crawler:
    """docstring for Crawler"""
    def __init__(self, site):
        self.site = site

    def getPage(self,url): # NOTE: 返回BeautifulSoup对象
        try:
            html = urlopen(url)
            html.encoding = 'UTF-8'
        except HTTPError as e:
            print('Error：网页在服务器上不存在')
            return None
        except URLError as e:
            print('Error：服务器不存在')
            return None
        except AttributeError as e:
            print('AttributeErrorError')
            return None
        return BeautifulSoup(html.read(), 'html.parser')

    def write_csv(self,data):
        path = '36Kr_news.csv'
        # with open(path,'a+') as f:
        with open(path,'a+',encoding='utf-8') as f:
        # NOTE: 由于atom和excel采用编码形式不同，在aton中乱码，在excel中是完整的encoding='utf-8'
            p = csv.writer(f)
            p.writerow(data)

    def clean_text(self,text):
        # NOTE: 完全清除所有的符号，只保留中文
        # comp = re.compile('[^A-Z^a-z^0-9^\u4e00-\u9fa5]')
        # return comp.sub('', text)
        # NOTE: 将中文特殊符号使用‘，’进行替换
        return re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])",",",text)

    def write_txt(self,data):

        fw = open('d:\\Data\Webspider\\news\\' + self.clean_text(data[0]) + '.txt','a+',encoding='utf-8')
        # NOTE:上述代码需要在制定位置建立相应的文件夹
        # filename = str(data[0])+ '.txt' # NOTE: r'D:\Data\Webspider\news'+'\\' +
        # fw = open(filename,'a+',encoding='utf-8')
        for element in data:
            fw.write(str(element))
            fw.write('\r\n')

    def getessay(self,url):
        contentlist = list()
        paragraph = list()
        absurl = 'https://36kr.com'+url
        bs = self.getPage(absurl)
        title = bs.find('h1').get_text()
        summary = bs.find('div',{'class':'summary'}).get_text()
        content = bs.find('div',{'class':'common-width content articleDetailContent kr-rich-text-wrapper'}).find_all('p')
        print('Title:',title)
        print('Summary:',summary)
        print('-'*20)
        contentlist.append(title)
        contentlist.append(absurl)
        contentlist.append(summary)
        for each in content:
            contentlist.append(each.get_text())
        # self.write_csv(contentlist)
        self.write_txt(contentlist)


    def parse(self,url):
        linkset = set()
        bs = self.getPage(url)
        if bs is not None:
            for link in bs.find_all('a',href=re.compile('^(/p/)')):
                if 'href' in link.attrs:
                    url = link.attrs['href']
                    title = link.get_text()
                    if url != '' and title != '' and url not in linkset:
                        linkset.add(url)
                        content = Content(url,title)
                        # content.print()
                        self.getessay(url)
                        print('-'*30)
                time.sleep(0.3)


socket.setdefaulttimeout(10)
target = 'https://36kr.com/information/web_news'
try:
    crawler = Crawler(target)
    crawler.parse(target)
except socket.timeout:
        print('获取连接超时！')
