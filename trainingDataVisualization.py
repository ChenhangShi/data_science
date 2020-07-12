import matplotlib.pyplot as plt


def do_visualization(raw_data, section_num):
    # 比较尴尬的是在pca数据可视化文件中，这个名字的变量代表各区间的题目数量
    # 在本文件中，各区间的题目数量用section_data表示
    temp = determine_section_len(raw_data, section_num)
    x_axis = temp[0]
    section_data = temp[1]
    # 绘图

    # 设置图片大小，以及横轴字体大小，如果用这个文件跑测试数据的话记得改一下
    plt.figure(figsize=(19.2, 10.8))
    plt.tick_params(labelsize=5)
    # 中文乱码的处理
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
    plt.rcParams['axes.unicode_minus'] = False

    plt.bar(range(len(section_data)), section_data, align='center', color='steelblue', alpha=0.8)
    plt.ylabel('数量')
    plt.title('各难度区间题目个数  总数{}'.format(sum(section_data)))
    plt.xticks(range(len(x_axis)), x_axis, rotation=-30)  # 横坐标字倾斜 这样小屏幕时字不会叠在一起
    # 为每个条形图添加数值标签
    for x, y in enumerate(section_data):
        plt.text(x, y, '%s' % y, ha='center')
    plt.show()


# 根据pca返回的res，确定区间的长度，由此生成横坐标样式，同时计算每个区间内的题目个数（说白了就是x,y轴对数据源）
def determine_section_len(raw_data, section_num):
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

    section_data = [0 for i in range(0, section_num)]  # x 轴数据源，表示每个区间有多少题目
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
