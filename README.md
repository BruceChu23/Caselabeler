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

## 从裁判文书中提取关键要素信息，如

    {
      "data": "c7a0d4d9",
      "case name": "PEOPLE OF THE PHILIPPINES, plaintiff-appellee, vs. NANCY LEOÑO y SEBANES, accused-appellant. [G.R. No. 244379. December 5, 2019.]",
      "nature": "Criminal",
      "court": "Supreme Court",
      "date": "December 5, 2019",
      "case type": "Illegal Recruitment in Large Scale and Estafa",
      "focus of dispute": "Whether the accused-appellant is guilty beyond reasonable doubt of the crime of illegal recruitment in large scale and estafa.",
      "legal facts": "Accused-appellant Nancy Leoño y Sebanes and Concepcion Loyola were charged with Illegal Recruitment in Large Scale and Estafa under five separate Information. The private complainants (Dante Pimentel, Resie Fabian Araza, Ramon Cruz, Ernaldo Aloria, Raymond Cruz) paid accused-appellant processing and placement fees for promised employment abroad. Accused-appellant failed to deploy them and did not return the money despite demands. La Corte Travel and General Agency, owned by accused-appellant, was not licensed to recruit workers for overseas employment.",
      "judgement and reason": {
        "RTC": "The RTC found accused-appellant guilty of illegal recruitment in large scale and three counts of estafa. It sentenced her to life imprisonment for illegal recruitment and various prison terms and fines for estafa.",
        "CA": "The CA affirmed the RTC's decision but modified the penalties for estafa. It upheld the conviction for illegal recruitment and estafa, finding that accused-appellant misrepresented her ability to recruit workers for overseas employment and defrauded the private complainants.",
        "SC": "The SC denied the appeal, affirming the CA's decision. It found that the elements of illegal recruitment in large scale and estafa were present, and the positive testimonies of the prosecution witnesses outweighed the accused-appellant's denial."
      },
      "citations": [
        "People v. Temporada, 594 Phil. 680, 710 (2008)",
        "People v. Rivera, 613 Phil. 660, 667 (2009)",
        "People v. Gharbia, 369 Phil. 942, 953 (1999), citing People v. Alvarado, 341 Phil. 725, 726 (1997)",
        "People v. Valenciano, 594 Phil. 235, 244 (2008)",
        "People v. Jamilosa, 541 Phil. 326, 337 (2007), citing People v. Dela Piedra, 403 Phil. 31, 57 (2001)",
        "Romero v. People, 677 Phil. 151, 164 (2011)"
      ],
      "evidence": "Testimonies of private complainants, affidavits, Certification from POEA, receipts, and other documentary evidence."
    }
