from pca import do_pca
from scipy import stats as ss
from pcaDataVisualization import do_visualization


def check_score(res):
    # 测试的比较简单的题目，发现都是小于0的，符合预期
    print(2425, res['2425'])
    print(2388, res['2388'])
    print(2386, res['2386'])
    print(2280, res['2280'])
    print(2358, res['2358'])
    print(2278, res['2278'])
    print(2453, res['2453'])
    print(2122, res['2122'])
    print(2063, res['2063'])
    print(2847, res['2847'])
    print(2816, res['2816'])
    print(2801, res['2801'])
    print('\n')

    # 测试的比较难的题目,发现都是大于0.6的，符合预期
    # 2301的作弊率非常高，因而算出来的结果也很大，虽然代码行数、花费时间都很小，但综合算出来的结果仍然很大，符合预期
    print(2301, res['2301'])
    print(2310, res['2310'])
    print(2954, res['2954'])
    print(2969, res['2969'])
    print(2348, res['2348'])
    print(2588, res['2588'])
    print(2947, res['2947'])
    print(2887, res['2887'])
    print(2091, res['2091'])
    print(2383, res['2383'])
    print(2273, res['2273'])
    print(2085, res['2085'])
    print('\n\n\n')


def check_distribution(res, another_res):
    l1 = []
    l2 = []
    for key in res:
        l1.append(res[key])
    for key in another_res:
        l2.append(another_res[key])
    print('判断是否同分布')
    print(ss.kstest(l1, l2))
    print('\n\n\n')


def check_pca_res(from_which):
    res = do_pca(0)[0]
    check_score(res)
    another_res = do_pca(from_which)[0]
    check_distribution(res, another_res)
    do_visualization(res)
    do_visualization(another_res)


check_pca_res(1)
