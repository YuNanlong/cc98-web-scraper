# !/usr/bin/python
# -*- coding: UTF-8 -*-
import bs4
from selenium import webdriver
import os
import time
import requests
import re

os.chdir('/Users/yunanlong/Desktop')
os.makedirs('mmPic', exist_ok=True)
browser = webdriver.PhantomJS()
browser.get('http://www.cc98.org/login.asp')
username = browser.find_element_by_id('userName')
username.send_keys('***') # 填入自己的用户名
pwd = browser.find_element_by_id('password')
pwd.send_keys('********') # 填入自己的密码
pwd.submit()
browser.implicitly_wait(10) # 爬取过程中可能存在页面没有全部加载完的问题，所以需要调用此函数
linkElem = browser.find_element_by_link_text('休闲娱乐')
linkElem.click()
browser.implicitly_wait(10)
linkElem = browser.find_element_by_link_text('mm图片')
linkElem.click()
resList = []
for i in range(2): # 爬取前十页，可以更改
    browser.implicitly_wait(10)
    print('正在爬取第 %d 页' % (i + 1))
    soup = bs4.BeautifulSoup(browser.page_source, 'html.parser')
    linkTextList = soup.select('a[id^="topic_"] span')
    j = 0
    for linkText in linkTextList:
        browser.implicitly_wait(10)
        j = j + 1
        print('正在爬取本页第 %d 个帖子' % (j))
        try:
            title = linkText.get_text()
            if re.search('【', title) != None: # 以【开头的一般都是公告等等可以跳过
                continue
            linkElem = browser.find_element_by_link_text(title)
            linkElem.click()
            browser.implicitly_wait(10)
            subSoup = bs4.BeautifulSoup(browser.page_source, 'html.parser')
            imgList = subSoup.select('#ubbcode1 .clickloadImage')
            resList.extend(imgList)    
            browser.back()
        except Exception as exc:
            print('There was a problem: %s' % (exc))
    browser.implicitly_wait(10)
    nextPage = browser.find_element_by_link_text('[下一页]')
    nextPage.click()
print('Done')
browser.close() # 必须关闭页面，否则会因为之后程序一直在下载图片而对浏览器没有操作导致浏览器与服务器连接中断，抛出异常

compiler = re.compile('http://file.cc98.org/uploadfile/')
for item in resList:
    imageUrl = item.get('href')
    if compiler.match(imageUrl) == None: # 图片的外链可能不是cc98上的，可能是新浪等等，
                                                                    # 有可能需要登录等等导致无法下载
        continue
    imageSrc = requests.get(imageUrl)
    try:
        imageSrc.raise_for_status()
    except Exception as exc:
        print('There was a problem: %s' % (exc))
        continue
    imageFile = open(os.path.join('mmPic', os.path.basename(imageUrl)), 'wb')
    for chunk in imageSrc.iter_content(100000):
        imageFile.write(chunk)
    imageFile.close()
print('Done')
