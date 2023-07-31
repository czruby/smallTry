import re
from docx import Document
import os


if __name__ == '__main__':
    path = 'file/生物寒假作业答案/'
    docxList = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if os.path.splitext(file)[1] == '.docx':  # 此处指定文件类型
                docxList.append(os.path.join(root, file))  # 此处接收文件
    for li in docxList:
        document = Document(li)
        text = ''
        result = ''
        for paragraph in document.paragraphs:
            text += paragraph.text
        obj1 = re.compile(r"\d+[.][A-D]")
        res1 = obj1.finditer(text)
        for res in res1:
            result += res.group() + '\n'
        obj2 = re.compile(r'\d+[.]答案:.*?解析')
        res2 = obj2.finditer(text)
        for res in res2:
            result += res.group().strip('解析') + '\n'
        print(result)
        name = li.split('/')[2].split('.')[0]
        with open(rf'file\res\{name}.txt', mode='w', encoding='utf-8') as f:
            f.write(result)
