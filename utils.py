import AverageDeduction
import AverageLineNum
import AverageTime
import AverageUploadNum
import cheatRatio
import IncompleteRatio
import json


# 获取所有的caseId
def getAllCaseIds():
    f = open('test_data.json', encoding='utf-8')
    res = f.read()
    data = json.loads(res)

    caseList = []
    for userId in data:
        cases = data[userId]['cases']
        for case in cases:
            caseId = case['case_id']
            if caseId not in caseList:
                caseList.append(caseId)
    f.close()
    return caseList


# 获取样本的caseId的list 可指定从哪里开始取 步长为5
def getSampleCaseList(from_which):
    caseList = getAllCaseIds()

    sampleCaseList = []
    for i in range(from_which, len(caseList), 5):
        sampleCaseList.append(caseList[i])
    return sampleCaseList


class Case(object):
    """
    整合数据到对象

    对象属性:
    id
    平均扣分
    未完成比例
    平均时间
    平均提交次数
    平均行数
    面向用例比例
    """

    def __init__(self, caseId,
                 averageDeduction,
                 averageLineNum,
                 averageTime,
                 averageUploadNum,
                 cheatRatio,
                 incompleteRatio,
                 ):
        self.caseId = caseId
        self.averageDeduction = averageDeduction
        self.incompleteRatio = incompleteRatio
        self.averageTime = averageTime
        self.averageUploadNum = averageUploadNum
        self.averageLineNum = averageLineNum
        self.cheatRatio = cheatRatio


# 根据caseId的list收集数据生成List<Case>
def getCaseObjsByCaseIdList(caseList):
    averageDeductionValues = AverageDeduction.getAverageDeduction(caseList)
    averageLineNumValues = AverageLineNum.getAverageLineNum(caseList)
    averageTimeValues = AverageTime.getAverageTime(caseList)
    averageUploadNumValues = AverageUploadNum.getAverageUploadNum(caseList)
    cheatRatioValues = cheatRatio.cheatRatio(caseList)
    incompleteRatioValues = IncompleteRatio.getIncompleteRatio(caseList)

    caseObjs = []
    for caseId in caseList:
        caseObjs.append(Case(caseId,
                             averageDeductionValues[caseId],
                             averageLineNumValues[caseId],
                             averageTimeValues[caseId],
                             averageUploadNumValues[caseId],
                             cheatRatioValues[caseId],
                             incompleteRatioValues[caseId]))
    return caseObjs


# 获取样本的List<Case>
def getSampleData(from_which):
    caseList = getSampleCaseList(from_which)
    return getCaseObjsByCaseIdList(caseList)


# 把Case对象转为list
def caseToList(case):
    return [case.averageDeduction, case.averageLineNum, case.averageTime, case.averageUploadNum, case.cheatRatio,
            case.incompleteRatio]


# 把List<Case>转成矩阵
def caseListToMartix(cases):
    mtrx = []
    for case in cases:
        mtrx.append(caseToList(case))
    return mtrx


# 获取训练集和测试集的caseId，训练集占80%，测试集占20%
def getCaseIdOfTrainingAndTestSet():
    caseList = getAllCaseIds()

    testSet = []
    for i in range(4, len(caseList), 5):
        testSet.append(caseList[i])
    trainingSet = list(set(caseList) - set(testSet))
    return trainingSet, testSet


# 获取训练集和测试集的List<Case>
def getTraingSetAndTestSet():
    case_id_training, case_id_test = getCaseIdOfTrainingAndTestSet()
    trainingSet = getCaseObjsByCaseIdList(case_id_training)
    testSet = getCaseObjsByCaseIdList(case_id_test)
    return trainingSet, testSet
