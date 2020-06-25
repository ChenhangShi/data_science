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
    myPCA(X)


# 传入一个矩阵 一行为一条记录 一列为一个特征
def myPCA(X):
    # 第一步 原始数据的标准化
    # 样本数量
    n = len(X)
    # 标准化去量纲
    # 每一列求平均值
    avg = np.mean(X, axis=0)  # TODO return
    # 每一列求标准差
    sd = np.std(X, axis=0)  # TODO return
    # 标准化得到Z sklearn的pca只减去平均值，中心化
    Z = (X - avg) / sd
    # 第二步 求(Z)T的协方差矩阵R 因为Z的一个特征为一列 而不是一行
    R = np.dot(Z.T, Z) / (n - 1)
    # R = np.cov(Z.T)

    # 第三步 求协方差矩阵R的特征值特征向量 eigenVec是一个矩阵，一列为一个特征向量
    # 和pca库里生成的特征矩阵符号相反
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
    total_contribution = 0  # TODO return
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
    print(W.T)
    # Z * W 生成主成分结果U Z有样本容量个行，特征数个列 W有特征数个行，m个列
    # 由于特征向量的符号和调pca库的特征向量符号相反 结果也符号相反
    U = np.dot(Z, W)  # TODO return
    print(U)
    print('\n\n\n\n\n')

    # 加权 综合
    res = []  # TODO return
    each_contributions = []  # TODO return
    for i in range(m):
        each_contributions.append(eigenMaps[i].eigenValue / eigenValue_sum)
    print(each_contributions)
    print('\n\n\n')
    for i in range(n):
        s = 0
        for j in range(m):
            s += U[i, j] * each_contributions[j]
        res.append(s / total_contribution)  # 除以累计贡献
    res.sort()  # TODO return 要不要记录caseId
    print(res)
    print('\n\n\n')
    # 要返回的：综合结果res
    # 对样本pca得到的结果
    # 平均值和标准差 用于将新数据标准化
    # 投影矩阵 也就是训练好的模型 用于将标准化的新数据降维
    # 主成分的总贡献率和分别贡献率 用于将降维的新数据综合


# 调用库
def doPCA(X):
    # Z = StandardScaler().fit_transform(X)

    # 做中心化 而不是标准化
    # 总方差贡献率达85%以上
    pca = PCA(0.85)
    pca.fit(X)
    U2 = pca.transform(X)
    print(pca.components_)
    print()
    print(U2)
    print()
    print(pca.explained_variance_ratio_)
    print('\n\n\n\n\n')


do_pca()
