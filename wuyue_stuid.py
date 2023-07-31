import time

import requests
import json
import csv


def getId(n):
    payload = {
        "e_dbname": "exam_63676",
        "exam_no": "63676",
        "stu_no": f"101420{n}"
    }
    headers = {
        'User-Agent': 'apifox/1.0.0 (https://www.apifox.cn)',
        'Content-Length': ''
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    text = json.loads(response.text)

    response.close()

    code = text["code"]
    if code == 204:
        return
    list1 = [text["datas"]["StuInfo"]["stu_no"], text["datas"]["StuInfo"]["stu_name"]]
    list2.append(list1)


if __name__ == '__main__':

    f1 = open(f"file/stuId.csv", mode="a", encoding="utf-8", newline='')
    csvWriter1 = csv.writer(f1)
    url = "https://m.wylkyj.com/ExamAPI/Exam/ScoreQuery/GetStuInfo"
    list2 = []
    for i in range(2800):
        try:
            getId(str(i).zfill(4))
            print(str(i).zfill(4))
        except requests.exceptions.RequestException as e:
            csvWriter1.writerows(list2)
            print(e)
            print('失败')
            time.sleep(5)
            list2 = []
            getId(str(i).zfill(4))
            continue

    csvWriter1.writerows(list2)
