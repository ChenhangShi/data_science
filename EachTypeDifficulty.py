from DataCollecting import getBaseSetByType
from DataCollecting import getTestSetByType
from trainingDataVisualization import do_visualization
from pca import deserialize_training_result

'''
划分同类型相对难度
对于某一类型的基础集的res可视化，根据聚集情况划分难度
用某一类型的训练集pca返回的PcaModel转换测试集，查看难度划分是否正确
'''


# 对某类型的基础集可视化，pca模型已训练好，保存在文件中
def show_type_base_set_res(case_type):
    pcaModel = deserialize_training_result()[2]
    origin_res = pcaModel.transform_case_obj(getBaseSetByType(case_type))[0]
    # 把数据分为10个区间 （训练数据）
    do_visualization(origin_res, 10)


# 对某类型的测试集用训练集训练好的模型降维
def cal_type_test_set_res(case_type):
    pcaModel = deserialize_training_result()[2]
    res_test = pcaModel.transform_case_obj(getTestSetByType(case_type))[0]
    print(res_test)
    return res_test


if __name__ == '__main__':
    show_type_base_set_res('树结构')
