# Caselabeler法律文书标注模型
基于通义千问大模型的法律文书标注方法

作者 zcl对外经济贸易大学

## 调用实例方法main.py中


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
