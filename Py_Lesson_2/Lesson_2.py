# 黑马训练Lesson2   汽车投诉信息采集
# 工号 10083

import requests
from bs4 import BeautifulSoup
import pandas as pd
# import time

def get_page(input_url):
    # 定义函数，得到页面的内容
    # 伪装为浏览器
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    # 获取网页的内容
    html = requests.get(input_url, headers=headers, timeout=20)
    content = html.text
    # 用BS模块html.parse解析网页内容
    soup = BeautifulSoup(content, 'html.parser')  # 默认为utf-8格式 可以不写 from_encoding='utf-8'
    return soup


def analysis(soup):
    # 定义函数，将BeautifulSoup解析后的内容存储到DataFrame中

    # 找到完整的投诉信息框
    base_soup = soup.find('div', class_="tslb_b")

    # 提取表头信息，并将表头存储到列表中
    columns_title = []
    th_list = base_soup.find_all("th")
    for th in th_list:
        columns_title.append(th.text)
    df = pd.DataFrame(columns=columns_title)

    # 将所有非表头行存储到字典中
    tr_list = base_soup.find_all("tr")
    for tr in tr_list:
        # 遍历一行中的所有列
        td_list = tr.find_all('td')
        # 设置空字典temp，用于存储每行的信息。索引index，用于读取表头的值作为字典temp的键。

        temp = {}
        index = 0

        # 判断是否为表头，不是表头则执行以下操作，存储数据
        if len(td_list) > 0:
            for td in td_list:
                # 将每列的变量存储到字典中
                temp[columns_title[index]] = td.text
                index += 1
            # 将字典append到数据表中
            df = df.append(temp, ignore_index=True)
    return df


############  主程序  ############

# 基础URL
url = 'http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-0-0-0-0-0-'
# 翻页数量
num = 20
# 模拟循环翻页
for i in range(num):
    request_url = url + str(i + 1) + ".shtml"
    # time.sleep(2)    # 如果有需要可以控制翻页频率
    soup = get_page(request_url)
    # 显示当前提取进度
    print("当前访问第%d页：%s" % (i + 1, request_url))
    df_temp = analysis(soup)
    if i == 0:
        result = analysis(soup)
    if i != 0:
        result = result.append(df_temp, ignore_index=False)

# 将DataFrame数据打印输出,然后输出到excel
print(result)
result.to_excel("car_complain1.xlsx", index=False)
