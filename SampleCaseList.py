import json


def getSampleCaseList(from_which):
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

    sampleCaseList = []
    # TODO 步长 或者分析全部的数据
    for i in range(from_which, len(caseList),5):
        sampleCaseList.append(caseList[i])
    f.close()
    return sampleCaseList
