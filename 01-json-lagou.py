import urllib.request
import jsonpath
import json

'''
    拉勾网获取国家区号
    
    通过爬取json文件来获取

'''

url = "https://passport.lagou.com/register/getPhoneCountryCode.json"
request = urllib.request.Request(url)
response = urllib.request.urlopen(request)

html = response.read()
print(html)  # 读取到的是一串json数据
jsonobj = json.loads(html)  # 转换为python对象
city_list = jsonpath.jsonpath(jsonobj, "$..name")
print(city_list)  # 这个变量储存的就是城市


# 储存到文件
file = open("city.txt", "w")
content = json.dumps(city_list, ensure_ascii=False)
print(content)
file.write(content)
file.close()
