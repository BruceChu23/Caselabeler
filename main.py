from openai import OpenAI
import pdfplumber
import json
import datetime
import time
import os

# -------------------------------------------------------
# 使用说明
# 需要在阿里云百炼注册api
# 需要提交法律文书pdf所在目录地址
# 需要提交json保存的位置(默认为同一文件夹)
api = ''
caseDir = r''
targetDir = r''
# 使用模型已默认通义千问-Max-2024-09-19，另需要则在下方调整
# 其他参数调整，参考https://bailian.console.aliyun.com/#/model-market/detail/qwen-max-0919?tabKey=sdk
# 2024-11-29
# -------------------------------------------------------

class Label:
    def __init__(self):
        self.client = OpenAI(
            api_key=api, 
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        caseType = open('casetype.txt', mode='r', encoding='utf-8').read()
        example = open('example.txt', mode='r', encoding='utf-8').read()
        self.prompt = f'''
        You are a helpful assistant.
        你现在是一个文本提取者，现在你的工作是从[英语法律文书]中提取各种类型的文本,
        [标注类型如下:]
        {caseType},
        [标注结果如下:]
        {example}
        你的全部回答内容一定可以[直接保存成json文件]
        '''
    def cases(self, rootDir):
        pdfs = []
        names = []
        for root, _, files in os.walk(rootDir):
            for file in files:
                if file.lower().endswith('.pdf'):
                    f = os.path.join(root, file)
                    pdfs.append(f)
                    names.append(os.path.join(file).replace('.pdf', ''))
        return pdfs, names
    def readCase(self, path):
        p = ''
        with pdfplumber.open(path) as pdf:
            numPages = len(pdf.pages)    
            for pageNum in range(numPages):
                page = pdf.pages[pageNum]
                text = page.extract_text()
                p = p + text
        return p
    def label(self, text, name):
        quesiton = f'''
        你是一个法律文本标注者，请帮我标注如下文本
        务必为我返回json格式:
        其中["data"]对应的值为{name};
        {text}
        '''
        completion = self.client.chat.completions.create(
            model="qwen-plus",
            messages=[
                {'role': 'system', 'content': self.prompt},
                {'role': 'user', 'content': quesiton}],
            response_format={"type": "json_object"}
            )
        return completion.choices[0].message.content
    def toJson(self, labelStr, name, targetDir=''):
        try:
            parsedJson = json.loads(labelStr)
            tn = rf"{targetDir}\{name}.json" if targetDir else rf"{name}.json"
            with open(tn, "w", encoding="utf-8") as json_file:
                json.dump(parsedJson, json_file, indent=2, ensure_ascii=False)
        except json.JSONDecodeError as e:
            print(f"文件{name}-JSON 解析错误: {e}")


if __name__ == "__main__":

    label = Label()
    cases, names = label.cases(caseDir)
    k = 0
    for case, name in zip(cases, names):
        t = time.time()
        text = label.readCase(case)
        anwser = label.label(text, name)
        label.toJson(anwser, name, targetDir)
        k += 1
        print(f'{datetime.datetime.now()}\t已完成第{k}份{name}, 用时{time.time() - t}s')
        
