from os import write
import parsel
import requests
import re
import csv
import time


beging_page = int(input("请输入爬取的开始页："))
ending_page = int(input("请输入爬取的终止页："))

hearders = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
}

f = open('招聘数据.csv', mode='a', encoding='utf-8', newline='')
csv_writer = csv.DictWriter(
    f, fieldnames=['职位名称', '公司名', '薪资', '城市', '基本要求', '福利待遇'])
csv_writer.writeheader()

for page in range(beging_page, ending_page + 1):
    print("正在爬取第 {} 页...".format(page))
    url = 'https://www.liepin.com/zhaopin/?compkind=&dqs=&pubTime=&pageSize=40&salary=&compTag=&sortFlag=&degradeFlag=0&compIds=&subIndustry=&jobKind=&industries=&compscale=&key=C%2B%2B&siTag=9vh8n9z4s8Pwf5Px7ocSyQ%7EfA9rXquZc5IkJpXC-Ycixw&d_sfrom=search_fp&d_ckId=2c57cb2805d72ed5b40d0683ea3797c9&d_curPage=0&d_pageSize=40&d_headId=2c57cb2805d72ed5b40d0683ea3797c9&curPage=' + \
        str(page+1)
    params = {
        'pageSize': '40',
        'degradeFlag': '0',
        'key': 'C++',
        'siTag': '9vh8n9z4s8Pwf5Px7ocSyQ~fA9rXquZc5IkJpXC-Ycixw',
        'd_sfrom': 'search_fp',
        'd_ckId': '2c57cb2805d72ed5b40d0683ea3797c9',
        'd_curPage': '0',
        'd_pageSize': '40',
        'd_headId': '2c57cb2805d72ed5b40d0683ea3797c9',
        'curPage': page,
    }

    response = requests.get(url=url, headers=hearders)
    selector = parsel.Selector(response.text)
    href = selector.css(
        '.job-content .sojob-list li .job-info h3 a::attr(href)').getall()

    def change_title(work_title):
        mode = re.compile(r'[\\\/\:\*\?\"\<\>\|]')
        new_work_tile = re.sub(mode, '_', work_title)
        return new_work_tile

    for link in href:
        # 对每个详情页进行发送请求 获取源代码数据
        response_1 = requests.get(url=link, headers=hearders)
        selector_1 = parsel.Selector(response_1.text)

        # 获取职位名称
        work_title = selector_1.css('.title-info h1::text').get()

        # 获取公司名称
        company_name = selector_1.css('.title-info h3 a::text').get()

        # 获取薪资
        money = selector_1.css('.job-item-title::text').get().strip()

        # 获取职位工作地点
        work_location = selector_1.css('.basic-infor a::text').get()

        # 获取职位的要求 获取到的是列表
        duty_list = selector_1.css('.job-qualifications span::text').getall()
        duty_work = ' | '.join(duty_list)

        # 获取职位的福利标签
        wrapper_list = selector_1.css('.comp-tag-list span::text').getall()
        wrapper_name = ' | '.join(wrapper_list)
        dict = {
            '职位名称': work_title,
            '公司名': company_name,
            '薪资': money,
            '城市': work_location,
            '基本要求': duty_work,
            '福利待遇': wrapper_name,
        }

        csv_writer.writerow(dict)

        # 获取任职要求 列表转字符串
        requirement_list = selector_1.css(
            '.job-description .content-word::text').getall()
        work_requirement = '\n'.join(requirement_list)

        # 写入txt文件
        new_title = change_title(work_title)  # 避免非法字符
        with open('职位信息\\' + company_name + '_' + new_title + '.txt', mode='w', encoding='utf-8') as f:
            f.write(work_requirement)

        print(work_title, company_name, money, work_location,
              duty_work, wrapper_name, sep=' | ')
        print(work_requirement)
        time.sleep(7.5)
