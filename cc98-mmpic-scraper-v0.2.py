# coding=utf-8
import requests
import bs4
import os
import re

class MmPicScraper:
    headers = {
        'Host': 'www.cc98.org',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Cookie': '********',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    }
    post_url = 'http://www.cc98.org/list.asp?'
    root_url = 'http://www.cc98.org/'
    file_url = 'http://file.cc98.org/uploadfile/'
    boardid = '146'
    img_link_compiler = re.compile(r'http://file.cc98.org/uploadfile(.+?)\[/upload\]')

    def __init__(self, cookie, total_page):
        MmPicScraper.headers['Cookie'] = cookie
        self.total_page = total_page
        self.post_link_list = []
        self.img_link_list = []

    def get_post_link(self):
        for i in range(self.total_page):
            data = {'boardid': MmPicScraper.boardid, 'page': str(i + 1), 'action': ''}
            result = requests.get(MmPicScraper.post_url, 'html.parser', headers=MmPicScraper.headers, data=data)
            result.raise_for_status()
            result_soup = bs4.BeautifulSoup(result.text)
            post_link_list = result_soup.select('a[id^="topic_"]')
            self.post_link_list.extend(post_link_list)
        print('前%d页的帖子链接抓取完毕' % self.total_page)

    def get_img_link(self):
        for post_link in self.post_link_list:
            post = requests.get(MmPicScraper.root_url + post_link.attrs['href'], 'html.parser', headers=MmPicScraper.headers)
            post.raise_for_status()
            post_soup = bs4.BeautifulSoup(post.text)
            ubbcode1_text = post_soup.select('#ubbcode1')[0].get_text()
            img_link_list = MmPicScraper.img_link_compiler.findall(ubbcode1_text)
            self.img_link_list.extend(img_link_list)
        print('前%d页的帖子中的图片链接抓取完毕' % self.total_page)

    def download_img(self):
        for img_link in self.img_link_list:
            img_url = MmPicScraper.file_url + img_link
            img_src = requests.get(img_url)
            try:
                img_src.raise_for_status()
            except Exception as exc:
                print('There was a problem: %s' % (exc))
                continue
            img_file = open(os.path.join('mmPic1', os.path.basename(img_url)), 'wb')
            for chunk in img_src.iter_content(100000):
                img_file.write(chunk)
            img_file.close()
        print('前%d页的帖子中的图片下载完毕' % self.total_page)

os.chdir('/Users/yunanlong/Desktop')
os.makedirs('mmPic1', exist_ok=True)
print('输入cookie')
cookie = input()
print('输入爬取页数')
total_page = input()
scraper = MmPicScraper(cookie, int(total_page))
scraper.get_post_link()
scraper.get_img_link()
scraper.download_img()
