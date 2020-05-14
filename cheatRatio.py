import SampleCaseList
import json
import os
from collections import defaultdict
import re


def cheatRatio():
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
    sampleCaseList = SampleCaseList.getSampleCaseList()

    is_cheat_judge_1 = defaultdict(float)
    is_cheat_judge_2 = defaultdict(float)  # 以后没有更改的话，考虑重命名：cheat_ratio_values
    # 在样本中排行的位置(由于目前只用了judge2，所以这样命名 以后没有更改的话，考虑重命名：cheat_ratio_ratios
    is_cheat_judge_2_ranks = defaultdict(float)
    values = []  # 排序用
    all_scores = defaultdict(list)  # 储存的是case_id : list(list)，是一个case的所有人的各次提交分数
    for case_id in sampleCaseList:
        is_cheat_judge_1[case_id] = 0
        is_cheat_judge_2[case_id] = 0
        all_scores[case_id] = []
        is_cheat_judge_2_ranks[case_id] = 0

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
        values.append(cheat_count_for_one_case / len(user_matches.values()))
        # print("case_id: ", case_id, "cheats: " ,cheat_count_for_one_case, "total users: ", len(user_matches.values()))
    # print(is_cheat_judge_2)
    values.sort()
    for case_id in is_cheat_judge_2:
        # 该值
        value = is_cheat_judge_2[case_id]
        rank = values.index(value)
        is_cheat_judge_2_ranks[case_id] = rank / len(values)
    # print(is_cheat_judge_2_ranks)
    return is_cheat_judge_2, is_cheat_judge_2_ranks

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

# if __name__ == '__main__':
#    cheatRatio()
