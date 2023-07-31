import os
import urllib.request
import datetime
import time
import json
import requests

# 公共目录
directory = "D:\copyFile"


def create_file(url, file_name, filetype):
    """创建文件"""
    try:
        if not os.path.exists(directory):
            os.mkdir(directory)
        # 更新替换文件前需停止待更新程序
        if filetype == "exe":
            os.system('taskkill /f /t /im %s.exe' % file_name)
        if not url:
            return "url is null"
        exe_file_path = "%s/%s.%s" % (directory, file_name, filetype)
        r = requests.get(url)
        with open(exe_file_path, "wb") as code:
            code.write(r.content)
    except IOError:
        return "cannot open url"
    except Exception as e:
        return "fail"
    return "success"


def run_exe(file_name):
    """启动程序"""
    os.system('start "" "%s/%s.exe"' % (directory, file_name))


def get_data_by_url(url):
    """获取远程数据"""
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'
    }  # 头部信息
    request = urllib.request.Request(url=url, headers=header)  # 请求处理
    b64_text = urllib.request.urlopen(request).read()  # 读取结果
    return b64_text


def read_version_json():
    """读取本地版本文件"""
    if not os.path.exists("%s/version.json" % directory):
        return {}

    with open("%s/version.json" % directory, mode='r', encoding='utf-8') as j:
        return json.load(j)


def write_version_json(data):
    """更新写入版本文件"""
    with open('%s/version.json' % directory, 'w') as f:
        json.dump(data, f)


def write_log(text):
    """记录日志"""
    f = open('%s/Update.log' % directory, mode='a', encoding='utf-8')
    f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S' + "\t" + text + "\n"))
    f.close()


def run():
    while True:
        try:
            online_json = json.loads(
                get_data_by_url("http://120.25.170.209/Updater/UpdateVersion.json"))
            local_json = read_version_json()
            if online_json == local_json:
                # sleep 1 hour
                time.sleep(3600)
                continue
            for program_name in online_json:
                if local_json.get(program_name):
                    if online_json.get(program_name).get("version") > local_json.get(program_name).get("version"):
                        write_log("更新：%s 版本：%s->%s" % (
                            program_name, local_json.get(program_name).get("version"),
                            online_json.get(program_name).get("version")))
                        write_log("更新地址：%s" % online_json.get(program_name).get("url"))
                        write_log("更新结果：%s" % create_file(online_json.get(program_name).get("url"), program_name,
                                                          online_json.get(program_name).get("type")))
                        if online_json.get(program_name).get("is_run"):
                            run_exe(program_name)
                else:
                    write_log(
                        "更新：%s 版本: %s" % (program_name, online_json.get(program_name).get("version")))
                    write_log("更新地址：%s" % online_json.get(program_name).get("url"))
                    write_log("更新结果：%s" % create_file(online_json.get(program_name).get("url"), program_name,
                                                      online_json.get(program_name).get("type")))
                    if online_json.get(program_name).get("is_run"):
                        run_exe(program_name)
            # 更新version
            write_version_json(data=online_json)
        except Exception:
            write_log("更新失败")
        # sleep 1 hour
        time.sleep(3600)


if __name__ == '__main__':
    if os.path.exists("%s/%s.exe" % (directory, 'USBcopy')):
        os.system('start "" "%s/%s.exe"' % (directory, 'USBcopy'))
    run()
