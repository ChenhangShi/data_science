from pca import do_pca_for_training_data  # 这里别删，main中会用到
from DataCollecting import getTraingSetAndTestSet  # 这里别删，main中会用到
import matplotlib.pyplot as plt

section_num = 40  # 这里暂定把数据分为40个区间 （训练数据） （每个区间的平均题目数量和pca的可视化保持一致）


# 如果用这个文件跑测试数据到话记得改一下 （建议改为10）


def do_visualization(raw_data):
    temp = determine_section_len(raw_data)
    x_axis = temp[0]
    section_data = temp[1]
    # 绘图

    # 设置图片大小，以及横轴字体大小，如果用这个文件跑测试数据的话记得改一下
    plt.figure(figsize=(19.2, 10.8))
    plt.tick_params(labelsize=6)
    # 中文乱码的处理
    # plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
    plt.rcParams['axes.unicode_minus'] = False

    plt.bar(range(len(section_data)), section_data, align='center', color='steelblue', alpha=0.8)
    plt.ylabel('数量')
    plt.title('各难度区间题目个数  总数{}'.format(sum(section_data)))
    plt.xticks(range(len(x_axis)), x_axis)
    # 为每个条形图添加数值标签
    for x, y in enumerate(section_data):
        plt.text(x, y, '%s' % y, ha='center')
    plt.show()


# 根据pca返回的res，确定区间的长度，由此生成横坐标样式，同时计算每个区间内的题目个数（说白了就是x,y轴对数据源）
def determine_section_len(raw_data):
    data = sorted(raw_data.items(), key=lambda item: item[1])  # 字典不能排序，排序之后，每个键值对转化为元组
    data = [list(x) for x in data]
    print(data)
    min_num = data[0][1]  # 最小难度值
    max_num = data[-1][1]  # 最大难度值
    section_len = (max_num - min_num) / section_num  # 区间长度原始值
    section_len = int(section_len * 100 + 1) / 100  # 保留两位小数并向上取
    left_border = [min_num + x * section_len for x in range(0, section_num)]  # 左边界数组原始值
    for i in range(0, len(left_border)):  # 左边界数组保留两位小数并向下取
        if left_border[i] < 0:
            left_border[i] = int(left_border[i] * 100 - 1) / 100
        else:
            left_border[i] = int(left_border[i] * 100) / 100
    # 生成x轴
    x_axis = []
    for i in range(0, section_num - 1):
        x_axis.append("{}-{}".format(left_border[i], left_border[i + 1]))
    x_axis.append("{}-{}".format(left_border[-1], left_border[-1] + section_len))
    # 计算x轴数据源
    section_data = [0 for i in range(0, section_num)]  # x 轴数据源
    border = left_border[:]  # 边界数组，其实就是左边界数组多加一项，便于统计x轴数据源
    border.append(border[-1] + section_len)
    border_ptr = 0  # 左边界数组指针
    data_ptr = 0  # data元素指针，这里不能用for in，因为涉及到data元素下标不变的问题
    while data_ptr < len(data):
        cur_data = data[data_ptr][1]
        if border[border_ptr] < cur_data < border[border_ptr + 1]:
            section_data[border_ptr] += 1
            data_ptr += 1
        else:
            border_ptr += 1
    # 由于舍入，可能导致x轴最后一项的左区间超出最大难度数值，这里判断是否要去掉
    # 具体到训练数据，是39个区间
    while section_data[-1] == 0:
        section_data = section_data[:-1]
        x_axis = x_axis[:-1]
    # 这里作为最终结果，所以最终的x轴区间个数可能小于section_num
    # print(x_axis)
    # print(section_data)
    return x_axis, section_data


'''
if __name__ == '__main__':
    origin_res = do_pca_for_training_data(getTraingSetAndTestSet()[1])[0]
    do_visualization(origin_res)
'''

'''
以下记录针对训练数据
生成的x轴：
['-1.38--1.21', '-1.21--1.04', '-1.04--0.87', '-0.87--0.7', '-0.7--0.53', '-0.53--0.36', '-0.36--0.19', '-0.19--0.02', '-0.02-0.15', '0.15-0.32', '0.32-0.49', '0.49-0.66', '0.66-0.83', '0.83-1.0', '1.0-1.17', '1.17-1.34', '1.34-1.51', '1.51-1.68', '1.68-1.85', '1.85-2.02', '2.02-2.19', '2.19-2.36', '2.36-2.53', '2.53-2.7', '2.7-2.87', '2.87-3.04', '3.04-3.21', '3.21-3.38', '3.38-3.55', '3.55-3.72', '3.72-3.89', '3.89-4.06', '4.06-4.23', '4.23-4.4', '4.4-4.57', '4.57-4.74', '4.74-4.91', '4.91-5.08', '5.08-5.25', '5.25-5.42']
各区间个数
[6, 42, 82, 75, 56, 63, 53, 55, 47, 34, 27, 25, 23, 13, 13, 16, 10, 9, 9, 7, 6, 5, 6, 6, 2, 2, 3, 2, 0, 3, 2, 0, 1, 0, 2, 0, 0, 0, 1, 0]

'''
