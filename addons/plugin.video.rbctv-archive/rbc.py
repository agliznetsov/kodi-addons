import urllib2
import datetime
import re
from bs4 import BeautifulSoup


HOST = 'http://rbctv.rbc.ru'
NEWS_URL = ['/archive/news', '/archive/oboz']

class RbcClient:

    def __init__(self):
        self.today = datetime.date.today().isoformat()

    def fetchFavorites(self, path, res):
        for folder in self.issues(path):
            text = folder['text']
            for file in self.files(folder['path']):
                if file['date'] == self.today:
                    file['text'] = text
                    res.append(file)
                    if len(res) >= 5:
                        return
                else:
                    return

    def favorites(self):
        res = []
        for path in NEWS_URL:
            self.fetchFavorites(path, res)
        return sorted(res, key=lambda it: it['time'])


    def programs(self):
        html = urllib2.urlopen(HOST + '/archive').read()
        doc = BeautifulSoup(html)
        list = doc.select('ul.menu2 li a')
        list = sorted(list, key=lambda s: s.text)
        res = []
        for s in list:
            res.append({'text': s.text, 'path': s.attrs['href']})
        return res

    def issues(self, path):
        html = urllib2.urlopen(HOST + path).read()
        doc = BeautifulSoup(html)
        list = doc.select('div.l-blocks')
        res = []
        for block in list:
            list = block.select('div.block_lastest')
            for item in list:
                href = item.select('div.video_s a')[0].attrs['href']
                text1 = item.select('div.video_s a span noindex')[0].text
                text2 = item.select('p.video_title')[0].text
                res.append({'text': text1 + ' ' + text2, 'path': href})
        return res


    def files(self, path):
        html = urllib2.urlopen(HOST + path).read()
        doc = BeautifulSoup(html)
        list = doc.select('div.info_block p a')
        res = []
        for item in list:
            href = item.attrs['href']
            if href.endswith('.wmv'):
                m = re.search('(\d\d\d\d\/\d\d\/\d\d).*?(\d\d\d\d)', href)
                date = m.group(1).replace('/', '-')
                time = m.group(2)
                res.append({'text': href, 'path': href, 'date': date, 'time': time})
        return res


