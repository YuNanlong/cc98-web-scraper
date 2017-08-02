# README

用于爬取浙江大学校内论坛CC98->休闲娱乐->mm图片板块的帖子中的妹子图片。

需要selenium、requests和beautifulsoup4这三个第三方库和PhantomJS这个第三方工具。本爬虫脚本编写时使用的是python3.5.1，selenium3.4.3，requests2.18.2，beautifulsoup4 4.6.0，PhantomJS2.1.1。运行环境是MacBook Pro (Retina, 13-inch, Early 2015)， macOS Sierra10.12.6 (16G29)。如果在其他环境中运行可能需要更改源代码第10行的路径。运行前需要连接ZJUWLAN并在源代码中填写自己的账号名和密码。

selenium下载

```
pip3 install selenium
```

requests下载

```
pip3 install requests
```

beautifulsoup下载

```
pip3 install beautifulsoup4
```

PhantomJS下载（Mac）

```
brew install phantomjs
```

命令行执行

```
python3 cc98.py
```
由于本人技术水平有限，尝试使用requests的post方法发送HTTP header和form data来绕过CC98论坛的登录，但是依然无法获取登录后的界面，所以使用selenium结合PhantomJS来模拟浏览器进行爬取，同时为了避免爬取过程中某些页面请求时间过长导致PhantomJS与CC98服务器的连接中断，在爬取过程中仅保存图片的URL，在爬取结束后再调用requests库的get方法下载URL。

如果有绕过登录的其他方法，欢迎提issue。