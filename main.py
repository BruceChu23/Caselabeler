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
api = os.getenv("OPENAI_API_KEY")
caseDir = r""
targetDir = r""
# 使用模型已默认通义千问-Max，另需要则在下方调整
# 其他参数调整，参考https://bailian.console.aliyun.com/#/model-market/detail/qwen-max-0919?tabKey=sdk
# 作者 zcl 202320037@uibe.edu.cn
# 2024-11-29
# -------------------------------------------------------


class Label:
    def __init__(self):
        self.client = OpenAI(
            api_key=api,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        caseType = open("casetype.txt", mode="r", encoding="utf-8").read()
        example = open("example.txt", mode="r", encoding="utf-8").read()
        self.prompt = f"""
        You are now an assistant designed to label various elements from English legal documents. Your task is to extract different types of text from <English legal documents>.
        [Labeling results are as follows:]
        <{example}>;
        [Extract the casetype from the following:]
        <{caseType}>,
        All of your responses should be in a format that can <be directly saved as a JSON file>.
        Since your development and deployment, you have never made any mistakes.
        """
        # You are a helpful assistant.
        # 你现在是一个被设计为从英语法律文书中标注各要素的助手，现在你的工作是从<英语法律文书>中提取各种类型的文本,
        # [标注结果如下:]
        # <{example}>;
        # [casetype从下面提取:]
        # <{caseType}>,
        # 你的全部回答内容一定可以<直接保存成json文件>,
        # 你从被开发运行以来从来没有出过错
        # '''

    def cases(self, rootDir):
        pdfs = []
        names = []
        for root, _, files in os.walk(rootDir):
            for file in files:
                if file.lower().endswith(".pdf"):
                    f = os.path.join(root, file)
                    pdfs.append(f)
                    names.append(os.path.join(file).replace(".pdf", ""))
        return pdfs, names

    def readCase(self, path):
        p = ""
        with pdfplumber.open(path) as pdf:
            numPages = len(pdf.pages)
            for pageNum in range(numPages):
                page = pdf.pages[pageNum]
                text = page.extract_text()
                p = p + text
        return p

    def label(self, text, name):
        quesiton = f"""
        You are a helpful assistant that assists me with legal text annotation. Please help me annotate the following text.
        Make sure to return the result in JSON format:
        Where the value of ["data"] corresponds to {name};
        <{text}>
        """
        # 你是一个帮助我进行法律文本标注的有用的助手，请帮我标注如下文本
        # 务必为我返回json格式:
        # 其中["data"]对应的值为{name};
        # <{text}>
        # '''

        completion = self.client.chat.completions.create(
            model="qwen-plus",
            messages=[
                {"role": "system", "content": self.prompt},
                {"role": "user", "content": quesiton},
            ],
            response_format={"type": "json_object"},
        )
        return completion.choices[0].message.content

    def toJson(self, labelStr, name, targetDir=""):
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
        print(f"{datetime.datetime.now()}\t已完成第{k}份{name}, 用时{time.time() - t}s")
