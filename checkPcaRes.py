from pca import do_pca
from scipy import stats as ss
from pcaDataVisualization import do_visualization


def check_score(res):
    easyDic = defaultdict(list)
    hardDic = defaultdict(list)
    easyDic['2425'] = res['2425']
    easyDic['2388'] = res['2388']
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
    hardDic['2301'] = res['2301']
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
    test_dict = {
        'easyDic': easyDic,
        'hardDic': hardDic
    }
    json_str = json.dumps(test_dict, indent=4)
    with open('easyData.json', 'w') as json_file:
        json_file.write(json_str)


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
    print('visual-----------------------------------------------------')
    do_visualization(res)
    do_visualization(another_res)


check_pca_res(1)
