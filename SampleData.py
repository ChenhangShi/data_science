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
平均扣分rank
未完成比例
未完成比例rank
平均时间
平均时间rank
平均提交次数
平均提交次数rank
平均行数
平均行数rank
面向用例比例
面向用例比例rank
'''


class Case(object):
    def __init__(self,caseId,
                 averageDeductionValue,averageDeductionRank,
                 averageLineNumValue,averageLineNumRank,
                 averageTimeValue,averageTimeRank,
                 averageUploadNumValue,averageUploadNumRank,
                 cheatRatioValue, cheatRatioRank,
                 incompleteRatioValue,incompleteRatioRank):
        self.caseId=caseId
        self.averageDeductionValue=averageDeductionValue
        self.averageDeductionRank=averageDeductionRank
        self.incompleteRatioValue=incompleteRatioValue
        self.incompleteRatioRank=incompleteRatioRank
        self.averageTimeValue=averageTimeValue
        self.averageTimeRank=averageTimeRank
        self.averageUploadNumValue=averageUploadNumValue
        self.averageUploadNumRank=averageUploadNumRank
        self.averageLineNumValue = averageLineNumValue
        self.averageLineNumRank = averageLineNumRank
        self.cheatRatioValue=cheatRatioValue
        self.cheatRatioRank=cheatRatioRank


def getSampleData():

    caseList = SampleCaseList.getSampleCaseList()
    averageDeductionValues, averageDeductionRanks = AverageDeduction.getAverageDeduction()
    averageLineNumValues, averageLineNumRanks = AverageLineNum.getAverageLineNum()
    averageTimeValues, averageTimeRanks = AverageTime.getAverageTime()
    averageUploadNumValues, averageUploadNumRanks = AverageUploadNum.getAverageUploadNum()
    cheatRatioValues, cheatRatioRanks = cheatRatio.cheatRatio()
    incompleteRatioValues, incompleteRatioRanks = IncompleteRatio.getIncompleteRatio()

    sampleData=[]
    for caseId in caseList:
        sampleData.append(Case(caseId,
                               averageDeductionValues[caseId],averageDeductionRanks[caseId],
                               averageLineNumValues[caseId],averageLineNumRanks[caseId],
                               averageTimeValues[caseId],averageTimeRanks[caseId],
                               averageUploadNumValues[caseId],averageUploadNumRanks[caseId],
                               cheatRatioValues[caseId],cheatRatioRanks[caseId],
                               incompleteRatioValues[caseId],incompleteRatioRanks[caseId]))
    return sampleData
