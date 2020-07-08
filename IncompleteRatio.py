import SampleCaseList
import json
from collections import defaultdict


def getIncompleteRatio(sampleCaseList):

    # 原始值
    d=defaultdict(int)
    # 做的人的数量
    userNum=defaultdict(int)
    # 平均值
    incompleteRatioValues = defaultdict(float)

    # 如果一道题所有人都完成了 结果中会缺失 所以先初始化
    for caseId in sampleCaseList:
        d[caseId]=0
        incompleteRatioValues[caseId]=0.0
        # incompleteRatioRatios[caseId]=0.0

    f=open('test_data.json',encoding='utf-8')
    res=f.read()
    data=json.loads(res)
    # 遍历
    for userId in data:
        cases=data[userId]['cases']
        for case in cases:
            caseId=case['case_id']
            # 是否是要取的
            if caseId in sampleCaseList:
                # 做的人的数量加1
                userNum[caseId]+=1
                # 如果没完成 加一
                if case['final_score']!=100:
                    d[caseId]+=1

    # 排序用
    # values=[]
    for caseId in d:
        incompleteRatio=d[caseId]/userNum[caseId]
        # 既加入字典 又加入list
        incompleteRatioValues[caseId]=incompleteRatio
        # values.append(incompleteRatio)

    '''    
    values.sort()

    # 获得位置
    for caseId in incompleteRatioValues:
        # 该值
        value=incompleteRatioValues[caseId]
        rank=0
        # 遍历查找排第几
        for i in range(len(values)):
            if value==values[i]:
                rank=i
                break
        # 转换成小数
        incompleteRatioRatios[caseId]=rank/len(values)
    '''
    f.close()
    return incompleteRatioValues  # ,incompleteRatioRatios
