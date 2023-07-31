import requests
from concurrent.futures import ThreadPoolExecutor

uuid = ''
flag = 0


def creat_like(a):
    response = requests.get(url)
    global flag
    if a == 1:
        response.close()
        return
    if a == 0 and response.text == 'success':
        flag = 1
    else:
        flag = -1


if __name__ == '__main__':
    uuid = input('输入uuid')
    url = f"https://lv.dingtalk.com/interaction/createLike?uuid={uuid}&count=100"
    with ThreadPoolExecutor(200) as t:
        while True:
            t.submit(creat_like, flag)
            if flag == -1:
                print("请检查你的uuid")
                break
