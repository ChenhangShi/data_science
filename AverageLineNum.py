import SampleCaseList
import json
import os
from collections import defaultdict


def getAverageLineNum(from_which):  # 返回一个字典case_id : averageLineNum
    sampleCaseList = SampleCaseList.getSampleCaseList(from_which)
    average_line_values = defaultdict(float)

    '''
    average_line_ranks = defaultdict(float)
    # 排序用
    values = []
    '''

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
        # values.append(average_line_values[case_id])
        # print("case_id:", case_id + " average line num:", "%.2f" % average_line_values[case_id])
    '''
    values.sort()
    for case_id in average_line_values:
        value = average_line_values[case_id]
        rank = values.index(value)
        average_line_ranks[case_id] = rank / len(values)
    # print(average_line_values)
    # print(average_line_ranks)
    '''
    return average_line_values  # , average_line_ranks


'''结果先贴在这里
case_id: 2908 average line num: 16.91
case_id: 2456 average line num: 12.73
case_id: 2892 average line num: 20.17
case_id: 2894 average line num: 19.90
case_id: 2171 average line num: 24.76
case_id: 2145 average line num: 22.51
case_id: 2185 average line num: 23.91
case_id: 2182 average line num: 27.07
case_id: 2618 average line num: 14.32
case_id: 2395 average line num: 27.11
case_id: 2425 average line num: 20.73
case_id: 2466 average line num: 22.13
case_id: 2209 average line num: 30.99
case_id: 2283 average line num: 16.64
case_id: 2359 average line num: 22.51
case_id: 2278 average line num: 17.68
case_id: 2461 average line num: 10.76
case_id: 2542 average line num: 17.57
case_id: 2505 average line num: 11.89
case_id: 2441 average line num: 8.81
case_id: 2111 average line num: 21.50
case_id: 2096 average line num: 6.26
case_id: 2127 average line num: 10.19
case_id: 2584 average line num: 5.71
case_id: 2064 average line num: 25.38
case_id: 2134 average line num: 12.51
case_id: 2084 average line num: 42.84
case_id: 2174 average line num: 77.21
case_id: 2296 average line num: 53.09
case_id: 2149 average line num: 158.18
case_id: 2288 average line num: 27.33
case_id: 2415 average line num: 33.17
case_id: 2311 average line num: 45.12
case_id: 2139 average line num: 29.16
case_id: 2790 average line num: 17.38
case_id: 2809 average line num: 13.73
case_id: 2827 average line num: 9.39
case_id: 2846 average line num: 10.16
case_id: 2810 average line num: 23.04
case_id: 2817 average line num: 13.41
case_id: 2801 average line num: 18.18
case_id: 2796 average line num: 17.59
case_id: 2867 average line num: 13.57
case_id: 2843 average line num: 12.26
case_id: 2849 average line num: 15.21
case_id: 2855 average line num: 42.55
case_id: 2830 average line num: 17.39
case_id: 2838 average line num: 12.50
case_id: 2857 average line num: 34.25
case_id: 2921 average line num: 29.21
case_id: 2884 average line num: 17.02
case_id: 2928 average line num: 28.10
case_id: 2923 average line num: 22.19
case_id: 2910 average line num: 25.33
case_id: 2917 average line num: 22.02
case_id: 2909 average line num: 25.79
case_id: 2896 average line num: 20.33
case_id: 2934 average line num: 34.14
case_id: 2192 average line num: 22.83
case_id: 2667 average line num: 9.10
case_id: 2662 average line num: 15.80
case_id: 2656 average line num: 23.43
case_id: 2430 average line num: 23.21
case_id: 2468 average line num: 18.30
case_id: 2729 average line num: 13.69
case_id: 2282 average line num: 27.02
case_id: 2737 average line num: 18.38
case_id: 2220 average line num: 27.26
case_id: 2230 average line num: 17.69
case_id: 2227 average line num: 23.50
case_id: 2123 average line num: 10.57
case_id: 2215 average line num: 13.79
case_id: 2157 average line num: 33.21
case_id: 2375 average line num: 40.06
case_id: 2405 average line num: 73.70
case_id: 2458 average line num: 29.49
case_id: 2432 average line num: 53.08
case_id: 2538 average line num: 15.11
case_id: 2513 average line num: 14.58
case_id: 2516 average line num: 22.68
case_id: 2210 average line num: 33.32
case_id: 2688 average line num: 21.27
case_id: 2287 average line num: 19.55
case_id: 2480 average line num: 15.60
case_id: 2676 average line num: 14.17
case_id: 2951 average line num: 39.29
case_id: 2938 average line num: 8.02
case_id: 2251 average line num: 17.26
case_id: 2325 average line num: 19.48
case_id: 2246 average line num: 17.63
case_id: 2242 average line num: 10.39
case_id: 2216 average line num: 32.35
case_id: 2376 average line num: 6.07
case_id: 2232 average line num: 48.21
case_id: 2213 average line num: 25.29
case_id: 2644 average line num: 18.93
case_id: 2641 average line num: 16.74
case_id: 2639 average line num: 21.84
case_id: 2399 average line num: 42.93
case_id: 2351 average line num: 28.19
case_id: 2369 average line num: 23.21
case_id: 2556 average line num: 25.39
case_id: 2553 average line num: 32.14
case_id: 2663 average line num: 10.13
case_id: 2590 average line num: 19.39
case_id: 2487 average line num: 20.20
case_id: 2725 average line num: 12.63
case_id: 2559 average line num: 15.59
case_id: 2730 average line num: 18.15
case_id: 2974 average line num: 35.06
case_id: 2969 average line num: 19.41
case_id: 2945 average line num: 29.29
case_id: 2235 average line num: 30.12
case_id: 2374 average line num: 23.77
case_id: 2532 average line num: 15.41
case_id: 2524 average line num: 26.03
case_id: 2648 average line num: 18.64
case_id: 2657 average line num: 41.32
case_id: 2598 average line num: 25.89
case_id: 2398 average line num: 24.71
case_id: 2250 average line num: 27.57
case_id: 2324 average line num: 16.62
case_id: 2409 average line num: 12.95
case_id: 2362 average line num: 25.61
case_id: 2377 average line num: 18.49
case_id: 2745 average line num: 31.48
case_id: 2717 average line num: 28.00
case_id: 2573 average line num: 13.96
case_id: 2768 average line num: 14.39
case_id: 2764 average line num: 16.02
case_id: 2779 average line num: 18.00
case_id: 2476 average line num: 20.17
case_id: 2980 average line num: 35.75
case_id: 2976 average line num: 18.76
case_id: 2948 average line num: 24.18
case_id: 2742 average line num: 67.21
case_id: 2713 average line num: 37.51
case_id: 2776 average line num: 27.21
case_id: 2714 average line num: 51.09
case_id: 2623 average line num: 8.20
case_id: 2585 average line num: 22.24
case_id: 2583 average line num: 23.60
case_id: 2613 average line num: 21.15
case_id: 2619 average line num: 24.22
case_id: 2750 average line num: 32.00
case_id: 2752 average line num: 44.17
case_id: 2422 average line num: 16.66
'''
