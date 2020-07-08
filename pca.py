from SampleData import getSampleData
import utils
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from collections import defaultdict, OrderedDict
import json


class EigenMap(object):
    # 记录特征值和它对应的是哪个属性
    def __init__(self, columnIndex, eigenValue):
        self.columnIndex = columnIndex
        self.eigenValue = eigenValue


class PcaModal(object):
    # 训练好的模型 avg是样本每一列的平均值，sd是样本每一列的标准差，W是投影矩阵，each_contributions是每个主成分的方差贡献率
    # 平均值avg和标准差sd 用于将新数据标准化
    # 投影矩阵W 用于将标准化的新数据降维
    # 主成分的分别贡献率 用于将降维的新数据综合
    def __init__(self, avg, sd, W, each_contributions):
        self.avg = avg
        self.sd = sd
        self.W = W
        self.each_contributions = each_contributions

    # 对于新的数据，直接转换
    # data是List<Case>
    def transform_case_obj(self, data):
        case_id_list = [x.caseId for x in data]
        X = np.mat(utils.caseListToMartix(data))
        return self.transform_matrix(X, case_id_list)

    # X是新数据的6列的矩阵
    # case_id_list是对应的caseId
    def transform_matrix(self, X, case_id_list=None):
        n = len(X)
        m = len(self.each_contributions)
        Z = (X - self.avg) / self.sd
        U = np.dot(Z, self.W)
        res = []
        for i in range(n):
            s = 0
            for j in range(m):
                s += U[i, j] * self.each_contributions[j]
            res.append(s)
        if case_id_list:
            res = dict(zip(case_id_list, res))
        return U, res


def do_pca(from_which):
    # data是List<Case>
    data = getSampleData(from_which)
    # getSampleData运行时间很长，故在此处取出caseId的list，并且与降维之后的res组合成字典
    case_id_list = [x.caseId for x in data]

    # 原始矩阵X
    X = np.mat(utils.caseListToMartix(data))
    return myPCA(X, case_id_list)


# 传入一个矩阵 一行为一条记录 一列为一个特征
def myPCA(X, case_id_list):
    # 第一步 原始数据的标准化
    # 样本数量
    n = len(X)
    # 标准化去量纲
    # 每一列求平均值
    avg = np.mean(X, axis=0)
    # 每一列求标准差
    sd = np.std(X, axis=0)
    # 标准化得到Z sklearn的pca只减去平均值，中心化
    Z = (X - avg) / sd

    # 第二步 求(Z)T的协方差矩阵R 因为Z的一个特征为一列 而不是一行
    R = np.dot(Z.T, Z) / (n - 1)
    # R = np.cov(Z.T)

    # 第三步 求协方差矩阵R的特征值特征向量 eigenVec是一个矩阵，一列为一个特征向量
    eigenValue, eigenVec = np.linalg.eig(R)
    # 对特征向量做正向化处理 因为选取的指标按常识是正相关
    for i in range(len(eigenValue)):
        col = eigenVec[:, i]
        if sum(col) < 0:
            eigenVec[:, i] = -col
    eigenMaps = []
    for i in range(len(eigenValue)):
        eigenMaps.append(EigenMap(i, eigenValue[i]))
    # 确定m值 总方差贡献率达85%以上
    # 特征值的总和
    eigenValue_sum = sum(eigenValue)
    # 按特征值从高到低排序
    eigenMaps.sort(key=lambda eigen: eigen.eigenValue, reverse=True)
    # 选第0到第m个
    m = -1
    # 是哪几列
    selectedCols = []
    # 利用率
    total_contribution = 0
    # 第0到第m个特征值之和
    eigenValue_cur = 0
    while total_contribution < 0.85:
        m += 1
        selectedCols.append(eigenMaps[m].columnIndex)
        eigenValue_cur += eigenMaps[m].eigenValue
        total_contribution = eigenValue_cur / eigenValue_sum
    # m置为选了几个
    m += 1

    # 第四步 转化为主成分
    # 特征向量的矩阵为eigenVec
    # 取前m个特征向量对应的特征矩阵 注意 一列为一个特征矩阵
    select_matrix = []
    for i in range(m):
        select_matrix.append(eigenVec[:, eigenMaps[i].columnIndex])
    # 投影矩阵W
    W = np.concatenate(select_matrix, axis=1)
    # Z * W 生成主成分结果U Z有样本容量个行，特征数个列 W有特征数个行，m个列
    # 由于特征向量的符号和调pca库的特征向量符号相反 结果也符号相反
    U = np.dot(Z, W)

    # 第五步 加权 综合
    res = []
    each_contributions = []
    for i in range(m):
        each_contributions.append(eigenMaps[i].eigenValue / eigenValue_sum)
    for i in range(n):
        s = 0
        for j in range(m):
            s += U[i, j] * each_contributions[j]
        res.append(s)
    # 将caseId和res组合
    res = dict(zip(case_id_list, res))
    print('res:')
    print(res)
    easyDic=defaultdict(list)
    hardDic=defaultdict(list)
    easyDic['2425']=res['2425']
    easyDic['2388']=res['2388']
    easyDic['2386'] = res['2386']
    easyDic['2280'] = res['2280']
    easyDic['2358'] = res['2358']
    easyDic['2278'] = res['2278']
    easyDic['2453'] = res['2453']
    easyDic['2122'] = res['2122']
    easyDic['2063'] = res['2063']
    easyDic['2847'] = res['2847']
    easyDic['2816'] = res['2816']
    easyDic['2801'] = res['2801']
    hardDic['2301']=res['2301']
    hardDic['2310'] = res['2310']
    hardDic['2954'] = res['2954']
    hardDic['2969'] = res['2969']
    hardDic['2348'] = res['2348']
    hardDic['2588'] = res['2588']
    hardDic['2947'] = res['2947']
    hardDic['2887'] = res['2887']
    hardDic['2091'] = res['2091']
    hardDic['2383'] = res['2383']
    hardDic['2273'] = res['2273']
    hardDic['2085'] = res['2085']
    test_dict={
        'easyDic':easyDic,
        'hardDic':hardDic
    }
    json_str = json.dumps(test_dict, indent=4)
    with open('easyData.json', 'w') as json_file:
        json_file.write(json_str)
    print('\n\n\n')
    # 要返回的：
    # 综合结果res
    # 对样本pca得到的结果U
    # 训练好的模型PcaModal
    return res, U, PcaModal(avg, sd, W, each_contributions)


# 调用库
def libPCA(X):
    Z = StandardScaler().fit_transform(X)

    # 总方差贡献率达85%以上
    pca = PCA(0.85)  # 自动做中心化 而不是标准化 如果在之前做了标准化，再做中心化减去0，无影响
    pca.fit(Z)
    U2 = pca.transform(Z)
    print(pca.components_)
    print()
    print(U2)
    print()
    print(pca.explained_variance_ratio_)
    print('\n\n\n\n\n')


if __name__ == '__main__':
    r,u,pcaModal = do_pca(0)
