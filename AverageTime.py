import SampleCaseList
import json
from collections import defaultdict


def getAverageTime():

    # 原始值，一个case对应的所有user的提交次数,存放在一个list里
    # defaultdict和dict的区别在于当key不存在时，会返回一个默认值
    # list对应[]，str对应的是空字符串，set对应set()，int对应0
    d = defaultdict(list)
    # 平均提交次数
    averageTime = defaultdict(float)
    # 用来获取排序后的caseId的提交时间
    averageUploadSeqRatio = defaultdict(float)
    # 获得要取的系统抽样后的cases
    sampleCaseList = SampleCaseList.getSampleCaseList()

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
                if len(case['upload_records'])==0 or len(case['upload_records'])==1:
                    continue
                else:
                    beginTime=case['upload_records'][0]['upload_time']
                    endTime=case['upload_records'][len(case['upload_records'])-1]['upload_time']
                    # 毫秒转成分钟，完成代码所需分钟数
                    costTime=(endTime-beginTime)/60000
                    d[caseId].append(costTime)
    # 找到某个caseId在整体caseId中的sequence
    sequence = []
    for caseId in d:
        averageTimeTemp = sum(d[caseId]) / len(d[caseId])
        averageTime[caseId] = averageTimeTemp
        sequence.append(averageTimeTemp)

    sequence.sort()
    for caseId in averageTime:
        temp = averageTime[caseId]
        seq = 0
        for i in range(len(sequence)):
            if temp == sequence[i]:
                seq = i
                break
        averageUploadSeqRatio[caseId]=seq/len(sequence)
    f.close()
    return averageTime,averageUploadSeqRatio

# if __name__ == '__main__':
#     d = getAverageTime()
#     for key, value in d.items():
#        print(key)
#        print(value)
#
# 贴一部分结果，感觉时间偏大得厉害，后期可能需要改一下，不能直接拿最后一次减去第一次再直接平均，这里的value是分钟，不是时间
# 2908
# 3528.6590836601304
# 2456
# 775.8750800000001
# 2892
# 1976.2880686274511
# 2894
# 1831.9257802083337
# 2171
# 118.93713000000002