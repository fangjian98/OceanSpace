# wiki-to-thir

<p align="left">
  <a>
    <img src="https://img.shields.io/github/issues/fangjian98/wiki-to-thir">
  </a>
  <a>
    <img src="https://img.shields.io/github/forks/fangjian98/wiki-to-thir">
  </a>
  <a>
    <img src="https://img.shields.io/github/stars/fangjian98/wiki-to-thir">
  </a>  
</p>

[![GitHub forks](https://img.shields.io/github/stars/fangjian98/wiki-to-thir/)](https://img.shields.io/github/stars/fangjian98/wiki-to-thir/)

[![Build Status](https://travis-ci.org/alibaba/fastjson.svg?branch=master)](https://travis-ci.org/alibaba/fastjson)
[![Codecov](https://codecov.io/gh/alibaba/fastjson/branch/master/graph/badge.svg)](https://codecov.io/gh/alibaba/fastjson/branch/master)
[![Maven Central](https://maven-badges.herokuapp.com/maven-central/com.alibaba/fastjson/badge.svg)](https://maven-badges.herokuapp.com/maven-central/com.alibaba/fastjson/)
[![GitHub release](https://img.shields.io/github/release/alibaba/fastjson.svg)](https://github.com/alibaba/fastjson/releases)
[![License](https://img.shields.io/badge/license-Apache%202-4EB1BA.svg)](https://www.apache.org/licenses/LICENSE-2.0.html)
[![Gitpod Ready-to-Code](https://img.shields.io/badge/Gitpod-Ready--to--Code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/alibaba/fastjson) 

## 使用PyCharm
- 下载地址：[PyCharm Community](https://www.jetbrains.com/pycharm/download/download-thanks.html?platform=windows&code=PCC)
- Create New Project
- New --> Python File


## 使用的库

```python
import urllib
import requests
import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
```

## 完成的任务

- 模拟浏览器请求网页，并获取网页内容
- 将html标签替换为markdown标签
- 保存html to markdown后的文件*.md
- 下载链接中的文件和图片
- 自动化打开浏览器并完成内容的填充及提交

## Chromedriver

使用selenium调用chrome浏览器需要使用chromedriver

- 首先需要下载Chromedriver载后得到的是一个chromedriver.exe文件，chromedriver下载地址:
http://npm.taobao.org/mirrors/chromedriver/

- 将chromedriver.exe拷贝到chrome浏览器（C:\Program Files (x86)\Google\Chrome\Application）、python（C:\Program Files (x86)\Python36-32）安装根目录的路径下即可，这样就可以使用selenium启动谷歌Chrome浏览器

Tip：使用的chromedriver要和chrome浏览器的版本需要匹配，否则会出现错误。
