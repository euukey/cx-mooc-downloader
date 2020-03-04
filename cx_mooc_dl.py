# 超星慕课视频批量下载 v1.0
# 功能：↑↑
# author: Euukey
# 2020.3.3


from bs4 import BeautifulSoup
import requests
import re
import random
from fake_useragent import UserAgent
import time
import os
import shutil

#链接课程网站
url = input("输入超星视频课程页面链接[如:http://mooc1.chaoxing.com/course/161102.html]：")
# url = "http://mooc1.chaoxing.com/course/161102.html"

#伪装ua
fake_ua = UserAgent()
headers = {'User-Agent':fake_ua.random} # 随机生成ua
r = requests.get(url,headers = headers)
soup = BeautifulSoup(r.text, 'html.parser')


# 创建保存视频的文件夹
save_dir = 'D:/'+soup.title.text #保存路径
if os.path.exists(save_dir):
    shutil.rmtree(save_dir) #清空文件夹
os.mkdir(save_dir)

#  课程链接列表
url_list = []

#搜索所有章节链接，并添加到列表中
for link in soup.find_all(href=re.compile("nodedetailcontroller")):
    course = link.get('href')
    url_list.append('http://mooc1.chaoxing.com'+course)  #补全链接

#文件编号
num = 1

# 遍历所有链接下载
print("开始下载视频！默认下载到D盘。")
for v_url in url_list:
    v_r = requests.get(v_url, headers=headers)
    v_soup = BeautifulSoup(v_r.text, 'html.parser')
    # 搜索视频id
    for dict in v_soup.find_all('iframe'):
        data = eval(dict.get('data'))
    # 下载
    print('downloading……')
    req = requests.get('http://d0.ananas.chaoxing.com/download/' + data['objectid'], headers=headers)
    with open(save_dir+'/'+str(num)+'.'+v_soup.find(id="nodeTitleEle").text + '.mp4', "wb") as f:# 标题:soup.find(id="nodeTitleEle").text
        f.write(req.content)
    print(v_soup.find(id="nodeTitleEle").text+'complete！')
    time.sleep(5+random.randint(1,11)) # 随机添加访问间隔
    num+=1
print("所有视频下载完成！")




