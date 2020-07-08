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
    def __init__(self,caseId,
                 averageDeduction,
                 averageLineNum,
                 averageTime,
                 averageUploadNum,
                 cheatRatio,
                 incompleteRatio,
                 ):
        self.caseId=caseId
        self.averageDeduction=averageDeduction
        self.incompleteRatio=incompleteRatio
        self.averageTime=averageTime
        self.averageUploadNum=averageUploadNum
        self.averageLineNum = averageLineNum
        self.cheatRatio = cheatRatio


def getSampleData():

    caseList = SampleCaseList.getSampleCaseList()
    averageDeductionValues = AverageDeduction.getAverageDeduction()
    averageLineNumValues = AverageLineNum.getAverageLineNum()
    averageTimeValues = AverageTime.getAverageTime()
    averageUploadNumValues = AverageUploadNum.getAverageUploadNum()
    cheatRatioValues = cheatRatio.cheatRatio()
    incompleteRatioValues = IncompleteRatio.getIncompleteRatio()

    sampleData=[]
    for caseId in caseList:
        sampleData.append(Case(caseId,
                               averageDeductionValues[caseId],
                               averageLineNumValues[caseId],
                               averageTimeValues[caseId],
                               averageUploadNumValues[caseId],
                               cheatRatioValues[caseId],
                               incompleteRatioValues[caseId]))
    for i in range(0, len(sampleData)):
        print(sampleData[i].caseId,sampleData[i].averageTime,sampleData[i].averageUploadNum,sampleData[i].cheatRatio
              ,sampleData[i].averageDeduction,sampleData[i].averageLineNum,sampleData[i].incompleteRatio)
    return sampleData

if __name__ == '__main__':
    d = getSampleData()
    for con in d:
        print(con)
