import json
from collections import defaultdict


def getAverageUploadNum(sampleCaseList):

    # 原始值，一个case对应的所有user的提交次数,存放在一个list里
    # defaultdict和dict的区别在于当key不存在时，会返回一个默认值
    # list对应[]，str对应的是空字符串，set对应set()，int对应0
    d = defaultdict(list)
    # 平均提交次数
    averageUploadNum = defaultdict(float)

    f = open('test_data.json',encoding='utf-8')
    res = f.read()
    data = json.loads(res)
    # 遍历
    for userId in data:
        # 这里的useId是指最外面的"3544"之类的
        # 涉及到loads后json数据结构转换为python相应数据结构
        cases=data[userId]['cases']
        for case in cases:
            caseId=case['case_id']
            # 只处理在sampleCaseList里的数据
            if caseId in sampleCaseList:
                uploadNum=len(case['upload_records'])
                d[caseId].append(uploadNum)

    # 找到某个caseId在整体caseId中的sequence
    # sequence=[]
    for caseId in d:
        averageUpload = sum(d[caseId]) / len(d[caseId])
        averageUploadNum[caseId] = averageUpload
        # sequence.append(averageUpload)

    '''    
    sequence.sort()

    for caseId in averageUploadNum:
        temp = averageUploadNum[caseId]
        seq = 0
        for i in range(len(sequence)):
            if temp == sequence[i]:
                seq = i
                break
        averageUploadSeqRanks[caseId]=seq/len(sequence)
    '''

    f.close()
    return averageUploadNum  # ,averageUploadSeqRanks
