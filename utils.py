# 把Case对象转为list
def caseToList(case):
    return [case.averageDeduction, case.averageLineNum, case.averageTime, case.averageUploadNum, case.cheatRatio, case.incompleteRatio]


# 把List<Case>转成矩阵
def caseListToMartix(cases):
    mtrx=[]
    for case in cases:
        mtrx.append(caseToList(case))
    return mtrx
