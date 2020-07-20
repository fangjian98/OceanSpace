import urllib
import requests
import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver

# 通过webdriver打开浏览器
# browser = webdriver.Chrome()
# url_thir = 'http://192.168.0.166:9200/index.php?v=experience_content&a=edit'
# browser.get(url_thir)
# 输入账号和密码登录thir office
# account = browser.find_element_by_name('name')
# account.send_keys('fangjian')
# pwd = browser.find_element_by_name('pswd')
# pwd.send_keys('123456')
# 查找登录按钮并点击进行登录
# btn_reg = browser.find_element_by_class_name('button')
# btn_reg.click()
# 休息5秒
# time.sleep(5)

# 从page76开始编辑
# page = 76

# 从网页上 检查--network--doc--header 查看cookie
cookie_str = "wikidbUserID=188; wikidbUserName=Fangjian; wikidbToken=4e1e33afd0e6bae8dfdc577624ef0b60; fVEO_2132_saltkey=m7gvz77g; fVEO_2132_lastvisit=1592381455; fVEO_2132_visitedfid=54; wikidb_session=baafpmcltksu3dam5tvn0pii47"

# 把cookie字符串处理成字典，以便接下来使用
cookies = {}
for line in cookie_str.split(';'):
    key, value = line.split('=', 1)
    cookies[key] = value

# 设置请求头，模拟浏览器
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
    'Connection': 'close'}

# 需要的四个网页
circle = [
    "http://192.168.0.138/wiki/index.php?title=%E7%89%B9%E6%AE%8A:%E6%89%80%E6%9C%89%E9%A1%B5%E9%9D%A2&from=1.DDR%E9%99%8D%E9%A2%91%E7%9A%84%E6%96%B9%E6%B3%95&to=MBHC%E5%A4%9A%E6%8C%89%E9%94%AE%E8%80%B3%E6%9C%BA%E6%8E%A7%E5%88%B6_%E4%B8%AD%E6%96%AD",
    "http://192.168.0.138/wiki/index.php?title=%E7%89%B9%E6%AE%8A:%E6%89%80%E6%9C%89%E9%A1%B5%E9%9D%A2&from=MC501&to=Stk3311",
    "http://192.168.0.138/wiki/index.php?title=%E7%89%B9%E6%AE%8A:%E6%89%80%E6%9C%89%E9%A1%B5%E9%9D%A2&from=StressTest_Manual_0517&to=%E9%A6%96%E9%A1%B5",
    "http://192.168.0.138/wiki/index.php?title=%E7%89%B9%E6%AE%8A:%E6%89%80%E6%9C%89%E9%A1%B5%E9%9D%A2&from=%E9%A9%AC%E8%BE%BE%E6%8E%A7%E5%88%B6%E8%8A%AF%E7%89%87DRV8833CRTER&to=%E9%BB%91%E8%89%B2EVB%E7%BB%BF%E8%89%B2EVB%E5%85%BC%E5%AE%B9%E6%96%B9%E6%A1%88",
    ]

for r in circle:
    url = r

    data = requests.get(url, headers=headers, cookies=cookies).text

    pat_url = '<td width="33%"><a href="(.*?)".*?>'
    articles = re.compile(pat_url, re.S).findall(data)
    print(len(articles))

    for j in articles:
        # 构造网址
        thisurl = "http://192.168.0.138" + j
        # 在发送get请求时带上请求头和cookies
        thisdata = requests.get(thisurl, headers=headers, cookies=cookies).text

        # 属于BeautifulSoup解析
        soup = BeautifulSoup(thisdata, 'html.parser')
        # 匹配的标题
        title = soup.h1.text
        # 匹配的内容
        content = ""

        # 将html标签转化为markdown标签
        t_list = soup.find_all(["title", "p", "pre", "img", "span", "li", "dd", "table"])
        for item in t_list:
            if item.name == "title":
                content += ("##" + title + "\n\n")
            elif item.name == "p":
                tag = item.find_all("a")
                if len(tag) == 0:
                    content += (item.get_text() + "\n\n")
                else:
                    for i in tag:
                        if re.compile("http").findall(i.get("href")):
                            content += ("[" + i.get("title") + "](" + i.get("href") + ")" + "\n\n")
                        else:
                            file_target = "http://192.168.0.138" + i.get("href")
                            try:
                                file = requests.get(file_target, headers=headers, cookies=cookies).text
                            except:
                                time.sleep(5)
                                print("Was a nice sleep, now let me continue...")
                                continue
                            pat_file = '<a href="(.*?)" class="internal"'
                            if re.compile(pat_file).findall(file):
                                file_url = re.compile(pat_file).findall(file)[0]
                                file_true = "http://192.168.0.138" + file_url
                                # 下载文件
                                urllib.request.urlretrieve(file_true,
                                                           'D:/wiki/files/%s' % i.get("title").replace(":", "_"))
                                content += ("[" + i.get("title") + "](" + file_true + ")" + "\n\n")
                            else:
                                content += ("[" + str(i.get("title")) + "](" + "http://192.168.0.138" + str(i.get("href")) + ")" + "\n\n")
            elif item.name == "pre":
                content += ("\t" + (item.get_text().replace('\n', '\n\t')) + "\n\n")
            elif item.name == "img":
                if item.get("alt") != "Powered by MediaWiki":
                    img_url = "http://192.168.0.138" + item.get("src")
                    alt = item.get("alt").replace(":", "_")
                    if alt == "":
                        alt = str(time.time()) + ".png"
                    # 下载图片
                    urllib.request.urlretrieve(img_url, 'D:/wiki/images/%s' % alt)
                    content += ("![" + item.get("alt") + "](" + "http://192.168.0.138" + item.get("src") + ")" + "\n\n")
            elif item.name == "span":
                if item.get("class") == ['mw-headline']:
                    content += ("####" + str(item.get_text()) + "\n\n")
            elif item.name == "li":
                if not item.has_attr('class'):
                    if not item.has_attr('id'):
                        content += ("\n" + "- " + item.get_text() + "\n\n")
            elif item.name == "dd":
                if not item.has_attr('class'):
                    if not item.has_attr('id'):
                        content += ("\n" + " " + item.get_text() + "\n\n")
            elif item.name == "table":
                if item.get("id") != "toc":
                    th = item.find_all("th")
                    td = item.find_all("td")
                    count = len(th)
                    for h in th:
                        content += ("|" + h.get_text())
                    for c in range(1, count):
                        content += "| :----:"
                    content += "\n"
                    for d in td:
                        content += ("|" + d.get_text())
                else:
                    pass

        # 将内容保存为*.md文件
        fh = open("D:/wiki/" + title.replace("/", "_").replace("*", "_") + "_" + str(time.time()) + ".md", "w",
                  encoding="utf-8")
        fh.write(content)
        fh.close()

        # 通过selenium自动填写title、keyword和content并点击save提交保存
        # browser.get(url_thir + "&eid=" + str(page))
        # page += 1

        # 查找到textarea 多行的文本输入 (document.getElementById('').innerHTML)
        # js = 'var ucode = document.getElementById("mdedit_text"); ucode.value=arguments[0];'
        # browser.execute_script(js, content)

        # 查到到input的文本框 title keyword
        # title1 = browser.find_element_by_name('title')
        # title1.send_keys(title)
        # keyword = browser.find_element_by_name('keyword')
        # keyword.send_keys(title)

        # 点击保存按钮
        # time.sleep(3)
        # submit = browser.find_element_by_xpath('//input[@value = "Save"]')
        # submit.click()
        # time.sleep(1)

        print(title)

print("完成")
