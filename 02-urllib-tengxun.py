import urllib.request
import re

'''
    通过urllib库来进行对腾讯社会招聘网的爬取
    
    爬取职位名称，职位类型，招聘人数，工作地点，发布时间，以及职位详情连接
'''
# url = "https://careers.tencent.com/search.html?query=ot_40001001,ot_40001002,ot_40001003,ot_40001004,ot_40001005,ot_40001006&index=3"


class Spider(object):
    def __init__(self):
        self.begin_page = int(input("请输入起始页："))
        self.end_page = int(input("请输入终止页："))
        self.base_url = "https://careers.tencent.com/"

    def load_page(self):
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
        header = {"User-Agent": user_agent}

        for page in range(self.begin_page, self.end_page + 1):
            url = self.base_url + \
                "search.html?query=ot_40001001,ot_40001002,ot_40001003,ot_40001004,ot_40001005,ot_40001006&index=" + \
                str(page+1)
            request = urllib.request.Request(url, headers=header)
            # 获取每页html源代码的字符串
            response = urllib.request.urlopen(request)
            html = response.read().decode("UTF-8")
            print(html)

    def parse_page(self, html):
        # 查找所有职位的名字
        # name_list = re.findall(r'lid=0" >(.*?)</a>', html)
        names_list = re.findall(r'"work=title">(.*?)</div>', html)

        # 查找所有详情的连接
        # links_list = re.findall(r'<a targer="_blank" href="(.*?)">', html)

        # 查所有工作职责
        duty_list = re.findall(r'"duty work-module">(.*?)</div>', html)

        # 查找所有的工作要求
        requirement_list = re.findall(
            r'"requirement work-module">(.*?)</div>', html)

        # 查找所有的岗位标签
        wrapper_list = re.findall(r'"recruit-tips">(.*?)</div>', html)

        # 查找其他元素
        # temp_list = re.findall(r'<td>(.*?)</td>', html)
        temp_list = re.findall(
            r'<div data-v-58f864bf class="max-center">(.*?)</div>', html)
        others_list = temp_list[4:]  # 去除表格的标题
        category_list = others_list[0::4]  # 从others_List截取所有职位的类别
        counts_list = others_list[1::4]  # 从others_list截取所有招聘人数
        location_list = others_list[2::4]  # 从others_list截取所有的工作地点
        publist_time_list = others_list[3::4]  # 从others_lit截取所有发布时间

        items = []
        for i in range(0, len(names_list)):
            item = {}
            item["职位名称"] = names_list[i]
            item["工作职责"] = duty_list[i]
            item["工作要求"] = requirement_list[i]
            item["岗位标签"] = wrapper_list[i]

            # item["职位链接"] = self.base_url + links_list[i]
            # item["职位类型"] = category_list[i]
            # item["招聘人数"] = counts_list[i]
            # item["工作地点"] = location_list[i]
            # item["发布时间"] = publist_time_list[i]
            items.append(item)
        print(items)


sp = Spider()
sp.load_page()
#  sp.parse_page(sp.load_page())
