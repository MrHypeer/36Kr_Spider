
def getPage(url):
    try:
        html = urlopen(url)
        html.close()
    except HTTPError as e:
        print('Error：网页在服务器上不存在')
        return None
    except URLError as e:
        print('Error：服务器不存在')
        return None
    try:
        bs = BeautifulSoup(html.read(), 'html.parser')
    except AttributeError as e:
        return None
    return bs #其实可以返回数组的吧？
