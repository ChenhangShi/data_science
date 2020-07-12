from DataCollecting import getTraingSetAndTestSetByType
from pca import do_pca_for_training_data
from trainingDataVisualization import do_visualization

'''
划分同类型相对难度
对于某一类型的训练集的res可视化，根据聚集情况划分难度
用某一类型的训练集pca返回的PcaModel转换测试集，查看难度划分是否正确
'''


# 对某类型的训练集可视化
# TODO 传入参数 什么类型的题目
def see_type_training_set():
    origin_res = do_pca_for_training_data(getTraingSetAndTestSetByType('数组')[0])[0]
    # 把数据分为10个区间 （训练数据）
    do_visualization(origin_res, 10)

# TODO 对某类型的测试集用训练好的模型降维

if __name__ == '__main__':
    see_type_training_set()
