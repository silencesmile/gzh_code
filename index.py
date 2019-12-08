# -*- coding: utf-8 -*-
# @Time    : 2019/12/6 2:27 PM
# @Author  : 公众号：Python数据分析实战
# @File    : index.py
# @Software: PyCharm
# -*- coding: utf-8 -*-
import re

import requests
import jsonpath
import json

headers = {
"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
"Host": "mp.weixin.qq.com",
"Referer": "https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit&action=edit&type=10&isMul=1&isNew=1&lang=zh_CN&token=1862390040",
"Cookie": "自己的Cookie"
       }

def getInfo():
    for i in range(1):
        # token  random 需要要自己的   begin：参数传入
        url = "https://mp.weixin.qq.com/cgi-bin/appmsg?token=改为自己的&lang=zh_CN&f=json&ajax=1&random=改为自己的&action=list_ex&begin={}&count=5&query=&fakeid=MzI4MzkzMTc3OA%3D%3D&type=9".format(str(i * 5))

        response = requests.get(url, headers = headers)

        jsonRes = response.json()


        titleList = jsonpath.jsonpath(jsonRes, "$..title")
        coverList = jsonpath.jsonpath(jsonRes, "$..cover")
        urlList = jsonpath.jsonpath(jsonRes, "$..link")

        # 遍历 构造可存储字符串
        for index in range(len(titleList)):
            title = titleList[index]
            cover = coverList[index]
            url = urlList[index]

            scvStr = "%s,%s, %s,\n" % (title, cover, url)
            with open("info.csv", "a+", encoding="gbk", newline='') as f:
                f.write(scvStr)


        # 下载视频
        for index in range(len(urlList)):
            # 获取 wxv
            url_wxv = urlList[index]
            video_title = titleList[index]

            print(video_title, url_wxv)
            try:
                getVideo(video_title, url_wxv)
            except Exception as e:
                print("内容可能不是视频:", url_wxv)

def getVideo(video_title, url_wxv):
    video_path = './videoFiles/' + video_title + ".mp4"

    response = requests.get(url_wxv, headers=headers)

    # 我用的是正则，也可以使用xpath
    jsonRes = response.text  #  匹配:wxv_1105179750743556096
    dirRe = r"wxv_.{19}"
    result = re.search(dirRe, jsonRes)

    wxv = result.group(0)
    print(wxv)

    # 拼接视频url
    # 页面播放形式
    video_url = "https://mp.weixin.qq.com/mp/readtemplate?t=pages/video_player_tmpl&auto=0&vid=" + wxv
    print("video_url", video_url)


    # 页面可下载形式
    video_url_temp = "https://mp.weixin.qq.com/mp/videoplayer?action=get_mp_video_play_url&preview=0&__biz=MzI4MzkzMTc3OA==&mid=2247488495&idx=4&vid=" + wxv
    response = requests.get(video_url_temp, headers=headers)
    content = response.content.decode()
    content = json.loads(content)
    url_info = content.get("url_info")
    video_url2 = url_info[0].get("url")
    print(video_url2)

    # 请求要下载的url地址
    html = requests.get(video_url2)
    # content返回的是bytes型也就是二进制的数据。
    html = html.content
    with open(video_path, 'wb') as f:
        f.write(html)

if __name__ == '__main__':
    getInfo()
