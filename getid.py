import json

import requests
import xlrd
import csv

if __name__ == '__main__':
    url = "https://hfs-be.yunxiao.com/v2/users/matched-students"
    studentName = ''
    identityCode = ''
    payload = {}
    num = xlrd.open_workbook('test.xls')
    table = num.sheets()[0]
    name = []
    No = []
    list2 = []
    f = open(f"file/test.csv", mode="a", encoding="utf-8", newline='')
    csvWriter1 = csv.writer(f)
    for i in range(table.nrows):
        list1 = []
        if i == 0:
            continue
        identityCode = str(table.row_values(i)[1])
        studentName = str(table.row_values(i)[2])
        params = {
            "roleType": "2",
            "studentName": f"{studentName}",
            "identityCode": f"{identityCode}"
        }
        response = requests.request("GET", url, params=params, data=payload)
        returntext = json.loads(response.text)
        studentId = returntext["data"]["students"][0]["studentId"]
        list1.append(identityCode)
        list1.append(studentId)
        csvWriter1.writerow(list1)
        print(studentId)
        response.close()
