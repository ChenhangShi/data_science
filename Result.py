from collections import defaultdict

from DataCollecting import get_case_objs_by_case_id_list
from pca import deserialize_training_result


# 输入caseId的list，输出各道题的难度值、绝对难度、类型、相对难度
def show_result(case_id_list):
    # 难度划分
    d = defaultdict(list)
    d['排序算法'].append(-0.63)
    d['排序算法'].append(0.09)
    d['数字操作'].append(-0.29)
    d['数字操作'].append(1.36)
    d['查找算法'].append(-0.57)
    d['查找算法'].append(0.21)
    d['线性表'].append(-0.76)
    d['线性表'].append(0.14)
    d['字符串'].append(0.12)
    d['字符串'].append(1.37)
    d['数组'].append(-0.64)
    d['数组'].append(0.23)
    d['树结构'].append(0.18)
    d['树结构'].append(1.35)
    d['图结构'].append(0.56)
    d['图结构'].append(2.26)
    d['all'].append(0.15)
    d['all'].append(1.95)

    pcaModel = deserialize_training_result()[2]
    case_list = get_case_objs_by_case_id_list(case_id_list)
    res_test = pcaModel.transform_case_obj(case_list)[0]
    for case in case_list:
        case_id=case.caseId
        print("caseId: "+case_id)
        print("caseType: ", case.caseType[0])
        print("res: ", res_test)
        if res_test[case_id] < d['all'][0]:
            print('绝对难度: 简单')
        elif res_test[case_id] >= d['all'][1]:
            print('绝对难度: 困难')
        else:
            print('绝对难度: 中等')
        if res_test[case_id] < d[case_list[0].caseType[0]][0]:
            print('相对难度: 简单')
        elif res_test[case_id] >= d[case_list[0].caseType[0]][1]:
            print('相对难度: 困难')
        else:
            print('相对难度: 中等')
        print()


if __name__ == '__main__':
    show_result(["2149",])
