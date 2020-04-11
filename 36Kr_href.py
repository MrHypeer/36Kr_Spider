from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
import re
import time
import socket
import sys
from selenium import webdriver

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

    def parse(self,url):
        html = urlopen(url)
        bs = BeautifulSoup(html,'html.parser')
        if bs is not None:
            return bs
        else:
            print("bs = None!")
            return None

    def getPage(self,url): # NOTE: 返回BeautifulSoup对象 link:"https://36kr.com/information/technology"
        linkset = set()
        try:
            option = webdriver.ChromeOptions()
            option.add_argument('headless')
            drivepath = r'D:\Software\Python 3.6.8\Lib\site-packages\selenium\chromedriver.exe'
            browser = webdriver.Chrome(executable_path=drivepath,chrome_options = option)
            browser.get(url)
            for i in range(3):
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);") # execute_script是插入js代码的
                time.sleep(2) #加载需要时间，2秒比较合理
            for j in range(10):
                try:
                    button = browser.execute_script("var div = document.getElementsByClassName('kr-loading-more-button show'); div[0].click();")
                    time.sleep(2)
                except:
                    print('could not click more!')
                    sys.exit()
            bs = BeautifulSoup(browser.page_source,'html.parser')
            if bs is not None:
                for link in bs.find_all('a',href=re.compile('^(/p/)')):
                    if 'href' in link.attrs:
                        url = link.attrs['href']
                        if url != '' and url not in linkset:
                            linkset.add(url)
                    time.sleep(0.3)
        except HTTPError as e:
            print('Error：网页在服务器上不存在')
            return None
        except URLError as e:
            print('Error：服务器不存在')
            return None
        except AttributeError as e:
            print('AttributeErrorError')
            return None
        return linkset

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
        absurl = 'https://36kr.com'+url
        bs = self.parse(absurl)
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


socket.setdefaulttimeout(25)
target = 'https://36kr.com/information/technology'
num = 0
try:
    crawler = Crawler(target)
    linkset = crawler.getPage(target)
    for relalink in linkset:
        num = num + 1
        print(num)
        crawler.getessay(relalink)
    print('Job finished, total '+str(num)+' essays obtained!')
except socket.timeout:
        print('获取连接超时！')
