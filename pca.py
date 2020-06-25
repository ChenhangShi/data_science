from SampleData import getSampleData
import utils
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


# 记录特征值和它对应的是哪个属性
class EigenMap(object):
    def __init__(self, columnIndex, eigenValue):
        self.columnIndex = columnIndex
        self.eigenValue = eigenValue


def do_pca():
    # data是List<Case>
    data = getSampleData()
    # 原始矩阵X
    X = np.mat(utils.caseListToMartix(data))
    doPCA(X)


# 传入一个矩阵 一行为一条记录 一列为一个特征
def doPCA(X):
    # 第一步 原始数据的标准化
    # 样本数量
    n = len(X)
    # 标准化去量纲
    # 每一列求平均值
    avg = np.mean(X, axis=0)  # TODO return
    # 每一列求标准差
    sd = np.std(X, axis=0)  # TODO return
    # 标准化得到Z
    # 还可以只减去平均值 中心化 sklearn的pca就是这样
    # 如果不做处理 后面求的是相关系数矩阵而不是协方差矩阵
    # Z = (X - avg) / sd
    # 改为中心化
    Z = X - avg
    '''
    Z = StandardScaler().fit_transform(X)
    print(Z)
    print('\n\n\n\n\n\n\n')
    '''

    # 第二步 求(Z)T的协方差矩阵R 因为Z的一个特征为一列 而不是一行
    R = np.dot(Z.T, Z) / (n - 1)
    # R = np.cov(Z.T)

    # 第三步 求协方差矩阵R的特征值特征向量 eigenVec是一个矩阵，一列为一个特征向量
    eigenValue, eigenVec = np.linalg.eig(R)
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
    selectedCols=[]
    # 利用率
    total_contribution = 0
    # 第0到第m个特征值之和
    eigenValue_cur = 0
    while total_contribution < 0.85:
        m += 1
        selectedCols.append(eigenMaps[m].columnIndex)
        eigenValue_cur += eigenMaps[m].eigenValue
        total_contribution = eigenValue_cur / eigenValue_sum
    print(selectedCols)
    print('\n\n\n\n\n')
    # m置为选了几个
    m += 1

    # 第四步 转化为主成分
    # 特征向量的矩阵为eigenVec
    # 取前m个特征向量对应的特征矩阵 注意 一列为一个特征矩阵
    select_matrix = []
    for i in range(m):
        select_matrix.append(eigenVec[:, eigenMaps[i].columnIndex])
    # 投影矩阵W 与pca.components_相差一个负号 因为特征向量取反仍然是特征向量
    W = np.concatenate(select_matrix, axis=1)  # TODO return
    # Z * W 生成主成分结果U Z有样本容量个行，特征数个列 W有特征数个行，m个列
    # 由于特征向量的符号和调pca库的特征向量符号相反 结果也符号相反
    U = np.dot(Z, W)  # TODO return
    print(U)
    print('\n\n\n\n\n')

    '''
    # 总方差贡献率达85%以上
    pca = PCA(0.85)
    pca.fit(X)
    U = pca.transform(X)
    print(U)
    print('\n\n\n\n\n')
    '''

    # 加权 综合
    res = []  # TODO return
    each_contributions = []  # TODO return
    for i in range(m):
        each_contributions.append(eigenMaps[i].eigenValue / eigenValue_sum)
    for i in range(n):
        s = 0
        for j in range(m):
            s += U[i, j] * each_contributions[j]
        res.append(s)
    res.sort()
    print(res)


do_pca()
