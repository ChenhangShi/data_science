import SampleCaseList
import AverageDeduction
import AverageLineNum
import AverageTime
import AverageUploadNum
import cheatRatio
import IncompleteRatio

'''
整合数据到对象

对象属性:
id
平均扣分
未完成比例
平均时间
平均提交次数
平均行数
面向用例比例
'''


class Case(object):
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


def getSampleData(from_which):
    caseList = SampleCaseList.getSampleCaseList(from_which)
    averageDeductionValues = AverageDeduction.getAverageDeduction(caseList)
    averageLineNumValues = AverageLineNum.getAverageLineNum(caseList)
    averageTimeValues = AverageTime.getAverageTime(caseList)
    averageUploadNumValues = AverageUploadNum.getAverageUploadNum(caseList)
    cheatRatioValues = cheatRatio.cheatRatio(caseList)
    incompleteRatioValues = IncompleteRatio.getIncompleteRatio(caseList)

    sampleData = []
    for caseId in caseList:
        sampleData.append(Case(caseId,
                               averageDeductionValues[caseId],
                               averageLineNumValues[caseId],
                               averageTimeValues[caseId],
                               averageUploadNumValues[caseId],
                               cheatRatioValues[caseId],
                               incompleteRatioValues[caseId]))
    return sampleData


if __name__ == '__main__':
    d = getSampleData()
    for con in d:
        print(con)
