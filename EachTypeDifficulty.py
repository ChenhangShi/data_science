from DataCollecting import getTraingSetAndTestSetByType
from pca import do_pca_for_training_data
from trainingDataVisualization import do_visualization

'''
划分同类型相对难度
对于某一类型的训练集的res可视化，根据聚集情况划分难度
用某一类型的训练集pca返回的PcaModel转换测试集，查看难度划分是否正确
'''


# 对某类型的训练集可视化
def show_type_training_set(case_type):
    origin_res = do_pca_for_training_data(getTraingSetAndTestSetByType(case_type)[0])[0]
    # 把数据分为10个区间 （训练数据）
    do_visualization(origin_res, 10)


# 对某类型的测试集用训练好的模型降维
def cal_overall_test_set_res(case_type):
    trainingSet, testSet = getTraingSetAndTestSetByType(case_type)
    res, U, pcaModal = do_pca_for_training_data(trainingSet)
    utest, restest = pcaModal.transform_case_obj(testSet)
    print(restest)


if __name__ == '__main__':
    cal_overall_test_set_res('数组')
