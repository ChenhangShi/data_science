import json
import os
import re
from collections import defaultdict
import pickle

'''
收集6个属性
获取所有的caseId
按步长为5获取样本的caseId，可指定起始位置
根据caseId的list获取List<Case>
获取训练集和测试集的List<Case>
'''


# 平均扣分
def getAverageDeduction(sampleCaseList):
    # 原始值
    d = defaultdict(list)
    # 平均值
    averageDeductionValues = defaultdict(float)

    f = open('test_data.json', encoding='utf-8')
    res = f.read()
    data = json.loads(res)
    # 遍历
    for userId in data:
        cases = data[userId]['cases']
        for case in cases:
            caseId = case['case_id']
            # 是否是要取的
            if caseId in sampleCaseList:
                deduction = 100 - case['final_score']
                d[caseId].append(deduction)

    for caseId in d:
        averageDeduction = sum(d[caseId]) / len(d[caseId])
        averageDeductionValues[caseId] = averageDeduction

    f.close()
    return averageDeductionValues


# 平均行数
def getAverageLineNum(sampleCaseList):  # 返回一个字典case_id : averageLineNum
    average_line_values = defaultdict(float)

    # 所有数据的路径
    data_path = os.getcwd() + "/data"
    for case_id in sampleCaseList:
        # caseXXXX的路径
        cur_case_dir = data_path + "/case" + case_id
        if not os.path.isdir(cur_case_dir):
            print(cur_case_dir + "not found\n")

        # 这里对一个case进行统计
        average_line_values[case_id] = 0
        # average_line_ranks[case_id] = 0  # 顺便初始化
        count = 0
        # 遍历该case下面的所有main.py文件
        for user_files in os.listdir(cur_case_dir):
            file_path = cur_case_dir + '/' + user_files + "/main.py"
            if os.path.isfile(file_path):
                with open(file_path, 'r') as f:
                    average_line_values[case_id] += len(f.readlines())
                # count += len(f.readlines())
        average_line_values[case_id] /= len(os.listdir(cur_case_dir))

    return average_line_values


# 平均用时（分钟）
def getAverageTime(sampleCaseList):
    # 原始值，一个case对应的所有user的提交次数,存放在一个list里
    # defaultdict和dict的区别在于当key不存在时，会返回一个默认值
    # list对应[]，str对应的是空字符串，set对应set()，int对应0
    d = defaultdict(list)
    # 平均提交次数
    averageTime = defaultdict(float)

    f = open('test_data.json', encoding='utf-8')
    res = f.read()
    data = json.loads(res)
    # 遍历
    for userId in data:
        # 这里的useId是指最外面的"3544"之类的
        # 涉及到loads后json数据结构转换为python相应数据结构
        cases = data[userId]['cases']
        for case in cases:
            caseId = case['case_id']
            # 只处理在sampleCaseList里的数据
            if caseId in sampleCaseList:
                if len(case['upload_records']) == 0 or len(case['upload_records']) == 1:
                    continue
                else:
                    beginTime = case['upload_records'][0]['upload_time']
                    endTime = case['upload_records'][len(case['upload_records']) - 1]['upload_time']
                    # 毫秒转成分钟，完成代码所需分钟数
                    costTime = (endTime - beginTime) / 60000
                    d[caseId].append(costTime)

    for caseId in d:
        averageTimeTemp = sum(d[caseId]) / len(d[caseId])
        averageTime[caseId] = averageTimeTemp

    f.close()
    return averageTime


# 平均提交次数
def getAverageUploadNum(sampleCaseList):
    # 原始值，一个case对应的所有user的提交次数,存放在一个list里
    # defaultdict和dict的区别在于当key不存在时，会返回一个默认值
    # list对应[]，str对应的是空字符串，set对应set()，int对应0
    d = defaultdict(list)
    # 平均提交次数
    averageUploadNum = defaultdict(float)

    f = open('test_data.json', encoding='utf-8')
    res = f.read()
    data = json.loads(res)
    # 遍历
    for userId in data:
        # 这里的useId是指最外面的"3544"之类的
        # 涉及到loads后json数据结构转换为python相应数据结构
        cases = data[userId]['cases']
        for case in cases:
            caseId = case['case_id']
            # 只处理在sampleCaseList里的数据
            if caseId in sampleCaseList:
                uploadNum = len(case['upload_records'])
                d[caseId].append(uploadNum)

    for caseId in d:
        averageUpload = sum(d[caseId]) / len(d[caseId])
        averageUploadNum[caseId] = averageUpload

    f.close()
    return averageUploadNum  # ,averageUploadSeqRanks


# 面向用例比例
def cheatRatio(sampleCaseList):
    """
    统计每道题目面向用例的比例
    # （暂未生效）假设： 所有面向用例的题目均为满分
    # 思路：两方面的分析，其一是提交的分数占据所有分数的程度，其二是代码中是否出现 if == print结构
    # （暂未生效）假设： 用例个数不超过3个的题目只能用第二种方法判断
    # 更正: 目前只用第二种方法来判断
    # 第二种方法思路：
    # 1、查找 if ｜ elif ｜ else  +  ==  +  print 的结构
    # 2、统计这种结构在单个代码中出现的次数
    # （暂未实施）统计这种结构代码行数在整体中所占比例
    # 3、这种结构的个数大于等于3，判定面向用例
    # 未来可以扩充的部分：1、查找得分情况，根据得分综合判断  2、代码文本匹配，假设先提交者为原创  3、过滤不是python的代码
    :return: 返回字典， case_id : cheat_Ratio 对应面向用例的比例
    """

    is_cheat_judge_1 = defaultdict(float)
    is_cheat_judge_2 = defaultdict(float)  # 以后没有更改的话，考虑重命名：cheat_ratio_values
    all_scores = defaultdict(list)  # 储存的是case_id : list(list)，是一个case的所有人的各次提交分数
    for case_id in sampleCaseList:
        is_cheat_judge_1[case_id] = 0
        is_cheat_judge_2[case_id] = 0
        all_scores[case_id] = []

    # 第一部分
    f = open('test_data.json', encoding='utf-8')
    res = f.read()
    data = json.loads(res)

    # 收集每道题目满分的所有score
    for user_id in data:
        cases = data[user_id]['cases']
        for case in cases:
            cur_case_id = case['case_id']
            if cur_case_id in sampleCaseList:
                if case['final_score'] == 100:
                    scores = []
                    for upload_record in case['upload_records']:
                        scores.append(upload_record['score'])
                    all_scores[cur_case_id].append(scores)

    # 对每道题目所有分数进行分析
    for case in all_scores.keys():
        case_scores = all_scores[case]
        temp = analyse_scores(case_scores)
        # print("case_id: ", case, "ratio: ", temp)

    # 第二部分

    # 所有数据的路径
    data_path = os.getcwd() + "/data"
    for case_id in sampleCaseList:

        user_matches = defaultdict(int)  # user_id : match_num

        # caseXXXX的路径
        cur_case_dir = data_path + "/case" + case_id
        if not os.path.isdir(cur_case_dir):
            print(cur_case_dir + "not found\n")  # 多打一个空行，调试的时候方便发现
        for user_files in os.listdir(cur_case_dir):
            user_matches[user_files] = 0
            file_path = cur_case_dir + '/' + user_files + "/main.py"
            if os.path.isfile(file_path):
                with open(file_path, 'r') as f:
                    total_matches = 0
                    lines = f.readlines()
                    # for line_num in range(0, len(lines)):
                    line_ptr = 0
                    while True:
                        if line_ptr >= len(lines):
                            break
                        cur_line = lines[line_ptr]  # debug用
                        one_try_res = match_pattern(lines, line_ptr)
                        total_matches += one_try_res[0]
                        line_ptr = one_try_res[1]
                    # print(total_matches)
                    user_matches[user_files] = total_matches
        # print(case_id, user_matches)

        cheat_count_for_one_case = 0
        for matched_pattern in user_matches.values():
            if matched_pattern >= 3:
                cheat_count_for_one_case += 1
        is_cheat_judge_2[case_id] = cheat_count_for_one_case / len(user_matches.values())

    return is_cheat_judge_2


def analyse_scores(scores: list) -> float:
    """
    分析scores数组，返回该数组所对应的面向用例的比例
    大致过程：先根据最小分数间距找到这道题目的用例个数，然后判断有没有人从0分逐步递增到100分，有的话判断面向用例
    这个方法暂时不用，因为发现很多实际面向用例，但是直接100分的代码
    :param scores: 某case_id下所有的分数组，其中每个分数组对应一个user的所有次提交的分数
    :return: 该case_id的面向用例的比例
    """
    res = 0.0
    cheat_num = 0
    # 首先根据所有人的结果，找出这道题目的用例个数
    min_gap = 100
    for score in scores:  # 这个时候score仍然是一个数组，表示一个人对所有提交
        for i in range(1, len(score)):
            if min_gap > score[i] - score[i - 1] > 1:  # 大于1是为了防止某些可能的特殊情况
                min_gap = score[i] - score[i - 1]
    test_case_num = round(100 / min_gap)
    if test_case_num <= 3:
        return 0.0

    cheat_count_judge1 = 0
    for score in scores:

        set_score = list(set(score))
        set_score.sort()
        # if set_score[0] != 0: #第一次提交就不是零分，一定不会面向用例
        #  continue
        min_gap_num = 0  # 记录一个人的所有记录得分的间距情况
        for i in range(1, len(set_score)):
            if abs((set_score[i] - set_score[i - 1]) - min_gap) < 1:
                min_gap_num += 1
        if min_gap_num == test_case_num:  # 每个用例都尝试过，判定面向用例
            # print(score)
            cheat_num += 1
    return cheat_num / len(scores)


def match_pattern(lines: list, cur_pos):  # 判断有多少个那种结构
    """
    从cur_pos开始，找到下一个"if  == print"结构，返回该结构的下一行
    :param lines: 某一user的代码
    :param cur_pos: 代码行指针，代码行从0算起
    :return: 数组，第一个元素是"if == print"的结构个数（在第cur_pos行和第line_ptr行之间的个数），第二个元素是当前代码行指针的位置
    """
    res = [0, cur_pos]
    re1 = re.compile('(if|elif)')
    re2 = re.compile('(==|operator.eq)')
    re3 = re.compile('print\(')
    re4 = re.compile('else')
    line_ptr = cur_pos
    max_lines = len(lines)
    cur_line = lines[line_ptr]
    if re4.search(cur_line) or (re1.search(cur_line) and re2.search(cur_line)):
        if re3.search(cur_line):
            line_ptr += 1
            res[0] += 1
            res[1] = line_ptr
            return res
        line_ptr += 1
        while True:
            if line_ptr >= max_lines:
                res[1] = line_ptr
                return res
            cur_line = lines[line_ptr]
            if re4.search(cur_line) or (re1.search(cur_line) and re2.search(cur_line)):
                res[1] = line_ptr
                return res
            if re3.search(cur_line):
                res[0] += 1
                res[1] = line_ptr + 1
                return res
            line_ptr += 1
    res[1] = line_ptr + 1
    return res


# 未完成比例
def getIncompleteRatio(sampleCaseList):
    # 原始值
    d = defaultdict(int)
    # 做的人的数量
    userNum = defaultdict(int)
    # 平均值
    incompleteRatioValues = defaultdict(float)

    # 如果一道题所有人都完成了 结果中会缺失 所以先初始化
    for caseId in sampleCaseList:
        d[caseId] = 0
        incompleteRatioValues[caseId] = 0.0

    f = open('test_data.json', encoding='utf-8')
    res = f.read()
    data = json.loads(res)
    # 遍历
    for userId in data:
        cases = data[userId]['cases']
        for case in cases:
            caseId = case['case_id']
            # 是否是要取的
            if caseId in sampleCaseList:
                # 做的人的数量加1
                userNum[caseId] += 1
                # 如果没完成 加一
                if case['final_score'] != 100:
                    d[caseId] += 1

    # 排序用
    # values=[]
    for caseId in d:
        incompleteRatio = d[caseId] / userNum[caseId]
        incompleteRatioValues[caseId] = incompleteRatio

    f.close()
    return incompleteRatioValues  # ,incompleteRatioRatios


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
def generateCaseObjsByCaseIdList(case_id_list):
    averageDeductionValues = getAverageDeduction(case_id_list)
    averageLineNumValues = getAverageLineNum(case_id_list)
    averageTimeValues = getAverageTime(case_id_list)
    averageUploadNumValues = getAverageUploadNum(case_id_list)
    cheatRatioValues = cheatRatio(case_id_list)
    incompleteRatioValues = getIncompleteRatio(case_id_list)

    caseObjs = []
    for caseId in case_id_list:
        caseObjs.append(Case(caseId,
                             averageDeductionValues[caseId],
                             averageLineNumValues[caseId],
                             averageTimeValues[caseId],
                             averageUploadNumValues[caseId],
                             cheatRatioValues[caseId],
                             incompleteRatioValues[caseId]))
    return caseObjs


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


# 将所有的Case对象序列化，因为自定义对象不能直接转成json
def serialize_all_case_objs():
    file_name = 'AllCaseObjs'
    with open(file_name, 'wb') as f:
        pickle.dump(generateCaseObjsByCaseIdList(getAllCaseIds()), f)


# 反序列化获取所有的对象
def deserialize_all_case_objs():
    file_name = 'AllCaseObjs'
    with open(file_name, 'rb') as f:
        all_case_objs = pickle.load(f)
    return all_case_objs


def get_case_objs_by_case_id_list(case_id_list):
    all_case_objs = deserialize_all_case_objs()
    required_case_objs = []
    for case in all_case_objs:
        if case.caseId in case_id_list:
            required_case_objs.append(case)
    return required_case_objs


# 获取样本的caseId的list 可指定从哪里开始取 步长为5
def getSampleCaseIdList(from_which):
    all_case_id_list = getAllCaseIds()
    sampleCaseList = []
    for i in range(from_which, len(all_case_id_list), 5):
        sampleCaseList.append(all_case_id_list[i])
    return sampleCaseList


# 获取样本的List<Case>
def getSampleData(from_which):
    sample_case_id_list = getSampleCaseIdList(from_which)
    return get_case_objs_by_case_id_list(sample_case_id_list)


# 获取训练集和测试集的caseId，训练集占80%，测试集占20%
def getCaseIdOfTrainingAndTestSet():
    caseList = getAllCaseIds()

    testSet = []
    for i in range(4, len(caseList), 5):
        testSet.append(caseList[i])
    trainingSet = list(set(caseList) - set(testSet))
    return trainingSet, testSet


# 获取训练集的List<Case>
def getTraingSet():
    case_id_training = getCaseIdOfTrainingAndTestSet()[0]
    trainingSet = get_case_objs_by_case_id_list(case_id_training)
    return trainingSet


# 获取测试集的List<Case>
def getTestSet():
    case_id_test = getCaseIdOfTrainingAndTestSet()[1]
    testSet = get_case_objs_by_case_id_list(case_id_test)
    return testSet


# 获取caseType类型的caseId
def getCaseIdsByType(caseType):
    f = open('test_data.json', encoding='utf-8')
    res = f.read()
    data = json.loads(res)

    caseList = []
    for userId in data:
        cases = data[userId]['cases']
        for case in cases:
            caseId = case['case_id']
            tempType = case['case_type']
            if (caseId not in caseList) and (tempType == caseType):
                caseList.append(caseId)
    f.close()
    return caseList


# 根据case type来获取基础集和测试集的caseId，基础集占80%，测试集占20%
# 基础集用来可视化、划分难度区间，类似于训练集，不过训练集是总体的80%，用来生成PcaModel
def getCaseIdOfBaseAndTestSetByType(caseType):
    caseList = getCaseIdsByType(caseType)
    testSet = []
    for i in range(4, len(caseList), 5):
        testSet.append(caseList[i])
    baseSet = list(set(caseList) - set(testSet))
    return baseSet, testSet


# 根据case type来获取基础集和测试集的List<Case>
def getBaseSetByType(caseType):
    case_id_base = getCaseIdOfBaseAndTestSetByType(caseType)[0]
    baseSet = get_case_objs_by_case_id_list(case_id_base)
    return baseSet


# 根据case type来获取测试集的List<Case>
def getTestSetByType(caseType):
    case_id_test = getCaseIdOfBaseAndTestSetByType(caseType)[1]
    testSet = get_case_objs_by_case_id_list(case_id_test)
    return testSet


if __name__ == '__main__':
    serialize_all_case_objs()
