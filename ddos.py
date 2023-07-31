import time

import requests
from openpyxl import load_workbook
import re
import csv


def get_info(data):
    requests.post(headers=header1, data=data, url=url1)
    response = requests.get(url=url2, headers=header2)
    text = response.text
    response.close()
    obj1 = re.compile(r'<td nowrap="nowrap">(?P<value>.*?)</td>')
    res1 = obj1.finditer(text)
    list1 = []
    for r in res1:
        list1.append(r.group('value'))
    list2.append(list1)


if __name__ == '__main__':
    workbook = load_workbook(filename='file/工作簿1.xlsx')
    sheet = workbook['Sheet1']
    cells1 = sheet['B2:B1569']
    cells2 = sheet['C2:C1569']
    f1 = open(f"file/res.csv", mode="a", encoding="utf-8", newline='')
    csvWriter1 = csv.writer(f1)
    mylist = []
    for i in range(1568):
        a = {
            "kh": cells1[i][0].value,
            "name": cells2[i][0].value
        }
        mylist.append(a)
    url1 = 'https://504729.yichafen.com/public/checkcondition/sqcode/Msjckn1mMDEwM3w0OTIzMmM5YjQxNWQwNDg4NjgwN2JlOTkzZDU3ZjBjY3w1MDQ3MjkO0O0O/htmlType/default.html'
    url2 = 'https://504729.yichafen.com/public/queryresult.html'
    header1 = {
        "Cookie": "acw_tc=2f6a1fde16582883011594990e1af2e9e1a89ae2fdaab38051311d9dc76288; PHPSESSID=882vk59mqvfe3ho2jt1h5hj3b0; scoremgr_teacher_code=504729; acw_tc=2f6a1fcd16582891299532560eb3a9351917620f115eefa248bd047764edc0; PHPSESSID=al5ude6rm4078ivsqti181aef0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.62"
    }
    header2 = {
        "Cookie": "acw_tc=2f6a1fde16582883011594990e1af2e9e1a89ae2fdaab38051311d9dc76288; PHPSESSID=882vk59mqvfe3ho2jt1h5hj3b0; scoremgr_teacher_code=504729; acw_tc=2f6a1fcd16582891299532560eb3a9351917620f115eefa248bd047764edc0; PHPSESSID=al5ude6rm4078ivsqti181aef0",
        "Referer": "https://504729.yichafen.com/public/queryscore/sqcode/Msjckn1mMDEwM3w0OTIzMmM5YjQxNWQwNDg4NjgwN2JlOTkzZDU3ZjBjY3w1MDQ3MjkO0O0O.html",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.62"
    }
    list2 = []
    for l in mylist:
        data = {
            "s_kaohao": f"{l['kh']}",
            "s_xingming": f"{l['name']}"
        }
        try:
            get_info(data)
        except requests.exceptions.RequestException as e:
            print(e)
            print('失败')
            csvWriter1.writerows(list2)
            time.sleep(5)
            list2 = []
            get_info(data)
            continue
        print(1)
    csvWriter1.writerows(list2)
