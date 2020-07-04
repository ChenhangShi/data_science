import SampleCaseList
import json
from collections import defaultdict


def getAverageDeduction():

    # 原始值
    d=defaultdict(list)
    # 平均值
    averageDeductionValues = defaultdict(float)
    # 在样本中的排行位置
    # averageDeductionRanks = defaultdict(float)

    # 获得要取的cases
    sampleCaseList=SampleCaseList.getSampleCaseList()

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
                deduction=100-case['final_score']
                d[caseId].append(deduction)

    '''
    # 排序用
    values=[]
    '''

    for caseId in d:
        averageDeduction=sum(d[caseId])/len(d[caseId])
        # 既加入字典 又加入list
        averageDeductionValues[caseId]=averageDeduction
        # values.append(averageDeduction)
    # values.sort()

    '''
    # 获得位置
    for caseId in averageDeductionValues:
        # 该值
        value=averageDeductionValues[caseId]
        rank=0
        # 遍历查找排第几
        for i in range(len(values)):
            if value==values[i]:
                rank=i
                break
        # 转换成小数
        averageDeductionRanks[caseId]=rank/len(values)
    '''

    f.close()
    return averageDeductionValues  # , averageDeductionRanks
