import pickle
from DataCollecting import Case
from DataCollecting import getTraingSet
from pca import do_pca_for_training_data

'''
保存对总体训练集pca的结果，包括综合评分res、降维后的矩阵U、返回的PcaModel
'''


def serialize_training_result():
    res, U, pcaModel = do_pca_for_training_data(getTraingSet())
    file_name = 'TrainingResult'
    with open(file_name, 'wb') as f:
        pickle.dump(res, f)
        pickle.dump(U, f)
        pickle.dump(pcaModel, f)


# 返回res, U, pcaModel
def deserialize_training_result():
    file_name = 'TrainingResult'
    with open(file_name, 'rb') as f:
        res = pickle.load(f)
        U = pickle.load(f)
        pcaModel = pickle.load(f)
    return res,U,pcaModel


if __name__ == '__main__':
    serialize_training_result()
