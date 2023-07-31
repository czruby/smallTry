import sys

from openpyxl import load_workbook
import datetime
import random
import os


def get_current_week():
    monday, sunday = datetime.date.today(), datetime.date.today()
    one_day = datetime.timedelta(days=1)
    while monday.weekday() != 0:
        monday -= one_day
    while sunday.weekday() != 6:
        sunday += one_day
    friday = sunday - one_day * 2
    # 返回当前的星期一和星期五的日期
    return monday, friday


def make_rand(cells):
    for i in range(random.randint(5, 10)):
        row = random.choice(cells)
        cell = random.choice(row)
        n = 0
        while n == 0:
            n = random.randint(-1, 2)
        cell.value = n


if __name__ == '__main__':
    option = int(input("欢迎使用量化表生成脚本。\n"
                       "输入1以随机生成积分表\n"
                       "输入2以自定义量化表\n"))
    monday, friday = get_current_week()
    mondayMonth = monday.month
    mondayDay = monday.day
    fridayMonth = friday.month
    fridayDay = friday.day
    a_date = f'       27 班  A部  {mondayMonth} 月 {mondayDay} 日—  {fridayMonth} 月 {fridayDay}  日量化得分记录表'
    b_date = f'       27 班  B部  {mondayMonth} 月 {mondayDay} 日—  {fridayMonth} 月 {fridayDay}  日量化得分记录表'
    path = os.path.dirname(os.path.realpath(sys.argv[0]))
    filepath = path + '/量化积分表.xlsx'
    print(filepath)
    try:
        workbook = load_workbook(filename=filepath)
    except FileNotFoundError:
        print('找不到模板文件')
        print('请确保在程序同目录下有名为’量化积分表.xlsx‘的模板文件')
        sys.exit()
    sheet = workbook['sheet1']
    cell1 = sheet['A1']
    cell1.value = a_date
    cell2 = sheet['A47']
    cell2.value = b_date
    filename = path + f'/27班每日量化积分表{mondayMonth}.{mondayDay}—{fridayMonth}.{fridayDay}.xlsx'
    if option == 1:
        cells1 = sheet['C5:AF21']
        cells2 = sheet['C51:AF66']
        make_rand(cells1)
        make_rand(cells2)
        workbook.save(filename=filename)
        print("已保存随机分数文件")
        input()
    if option == 2:
        workbook.save(filename=filename)
        print("已保存文件，请自定义分数项")
        input()
