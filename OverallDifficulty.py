from DataCollecting import getTraingSet
from DataCollecting import getTestSet
from DataCollecting import Case
from trainingDataVisualization import do_visualization
from SaveTrainingResult import deserialize_training_result

'''
划分总体难度
两个函数
对于总体的训练集的res可视化，根据聚集情况划分难度
用总体的训练集pca返回的PcaModel转换测试集，查看难度划分是否正确
'''


# 对总体的训练集可视化
def show_overall_training_set_res():
    # 对总体训练集pca返回的结果已序列化保存在TrainingResult中
    origin_res = deserialize_training_result()[0]
    # 把数据分为80个区间 （训练数据） （每个区间的平均题目数量是pca的可视化的一半）
    do_visualization(origin_res, 80)


'''
以下记录针对训练数据
生成的x轴：
['-1.38--1.21', '-1.21--1.04', '-1.04--0.87', '-0.87--0.7', '-0.7--0.53', '-0.53--0.36', '-0.36--0.19', '-0.19--0.02', '-0.02-0.15', '0.15-0.32', '0.32-0.49', '0.49-0.66', '0.66-0.83', '0.83-1.0', '1.0-1.17', '1.17-1.34', '1.34-1.51', '1.51-1.68', '1.68-1.85', '1.85-2.02', '2.02-2.19', '2.19-2.36', '2.36-2.53', '2.53-2.7', '2.7-2.87', '2.87-3.04', '3.04-3.21', '3.21-3.38', '3.38-3.55', '3.55-3.72', '3.72-3.89', '3.89-4.06', '4.06-4.23', '4.23-4.4', '4.4-4.57', '4.57-4.74', '4.74-4.91', '4.91-5.08', '5.08-5.25', '5.25-5.42']
各区间个数
[6, 42, 82, 75, 56, 63, 53, 55, 47, 34, 27, 25, 23, 13, 13, 16, 10, 9, 9, 7, 6, 5, 6, 6, 2, 2, 3, 2, 0, 3, 2, 0, 1, 0, 2, 0, 0, 0, 1, 0]

'''


# 对总体的测试集用训练好的模型降维
def cal_overall_test_set_res():
    testSet = getTestSet()
    res, U, pcaModal = deserialize_training_result()
    res_test = pcaModal.transform_case_obj(testSet)[0]
    print(res_test)
    return res_test


if __name__ == '__main__':
    cal_overall_test_set_res()