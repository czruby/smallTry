import csv
import datetime
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import wuyue_fen
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtCore import QThread, pyqtSignal
import requests
import json
import xlrd


class MainDialog(QDialog):

    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)
        self.ui = wuyue_fen.Ui_Dialog()
        self.ui.setupUi(self)
        self.searchKaoshi()

    def searchKaoshi(self):
        url = "https://m.wylkyj.com/ExamAPI/Common/School/ProjectSchList"
        data = {
            "schoolname": "南阳市一中"
        }
        response = requests.request(url=url, data=data, method="post")
        response.close()
        text = json.loads(response.text)
        list = []
        for l in text["datas"]:
            if l["grd_name"] == "高三":
                list.append(l["exam_name"])
                kaoshiDict[l["exam_no"]] = l["exam_name"]
        self.ui.comboBox.addItems(list)

    def startSpawn(self):
        msg = datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S') + ": 开始生成\n"
        self.ui.textEdit.setText(msg)
        kaoshiName = self.ui.comboBox.currentText()
        msg += datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S') + ": 考试名：" + kaoshiName + "\n"
        self.ui.textEdit.setText(msg)
        kaoshiCode = self.getCode(kaoshiName)
        msg += datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S') + ": 考试号：" + kaoshiCode + "\n"
        self.ui.textEdit.setText(msg)
        self.getId()
        msg += datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S') + ": 考生号读取中" + "\n"
        msg += datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S') + ": 共读取到考生" + str(len(NoData)) + "人\n"
        msg += datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S') + ": 开始查询数据" + "\n"
        self.ui.textEdit.setText(msg)
        self.th = SearchThread(kaoshiCode)
        self.th.signal1.connect(self.progressBar)
        self.th.signal2.connect(self.textEdit)
        self.th.start()

    def getCode(self, kaoshiName):
        for key, value in kaoshiDict.items():
            if kaoshiName == value:
                return key

    def getId(self):
        NoData.clear()
        book = xlrd.open_workbook("test2.xls")
        table = book.sheets()[0]
        for i in range(table.nrows):
            if i == 0:
                continue
            NoData.append(str(table.cell_value(rowx=i, colx=0)).split('.')[0])

    def progressBar(self, n):
        self.ui.progressBar.setValue(n)

    def textEdit(self, msg):
        self.ui.textEdit.setText(self.ui.textEdit.toPlainText() + msg)


class SearchThread(QThread):
    # 使用信号和UI主线程通讯，参数是发送信号时附带参数的数据类型，可以是str、int、list等
    signal1 = pyqtSignal(int)
    signal2 = pyqtSignal(str)
    cishu = 0

    # 带参数示例
    def __init__(self, kaoshiCode, parent=None):
        super(SearchThread, self).__init__(parent)

        self.kaoshiCode = kaoshiCode

    def getFen(self, n, code):
        url = "https://m.wylkyj.com/ExamApiV2/api/v1/scorequery/GetSubCompAnalEnt"
        payload = json.dumps({"stuNo": f"{n}"})
        headers = {
            'exam_no': f'{code}',
            'User-Agent': 'apifox/1.0.0 (https://www.apifox.cn)',
            'Content-Type': 'application/json'
        }
        response = requests.request(url=url, data=payload, headers=headers, method="post")
        text = json.loads(response.text)
        list2 = []
        if text["code"] == 200:
            list2.append(n)
            list1 = text["datas"]["subCompAnalArr"]
            for l in list1:
                list2.append(l["score"])
                list2.append(l["rank"])
        else:
            print(text["code"])
        list3.append(list2)
        self.cishu += 1
        self.signal1.emit(int(self.cishu / len(NoData) * 90))

    def run(self):
        with ThreadPoolExecutor(50) as t:
            for i in range(len(NoData)):
                try:
                    t.submit(self.getFen, NoData[i], self.kaoshiCode)
                except Exception as e:
                    print(e)
                    time.sleep(3)
                    t.submit(self.getFen, NoData[i], self.kaoshiCode)
        self.signal2.emit(datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S') + ": 开始写入文件\n")
        f = open(f"file/{self.kaoshiCode}.csv", mode="a", encoding="utf-8", newline='')
        csvWriter = csv.writer(f)
        csvWriter.writerows(list3)
        self.signal2.emit(datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S') + ": 完成写入文件\n")
        self.signal2.emit(datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S') + ": 生成完成\n")
        self.signal1.emit(100)
        f.close()
        return


if __name__ == '__main__':
    kaoshiDict = {}
    NoData = []
    list3 = []
    myapp = QApplication(sys.argv)
    myDlg = MainDialog()
    myDlg.show()
    sys.exit(myapp.exec_())
