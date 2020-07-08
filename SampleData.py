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
    averageDeductionValues = AverageDeduction.getAverageDeduction(from_which)
    averageLineNumValues = AverageLineNum.getAverageLineNum(from_which)
    averageTimeValues = AverageTime.getAverageTime(from_which)
    averageUploadNumValues = AverageUploadNum.getAverageUploadNum(from_which)
    cheatRatioValues = cheatRatio.cheatRatio(from_which)
    incompleteRatioValues = IncompleteRatio.getIncompleteRatio(from_which)

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
