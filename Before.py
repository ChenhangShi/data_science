import os
from Download import download
from DataCollecting import serialize_all_case_objs
from SaveTrainingResult import serialize_training_result

'''
初始化所需要的文件
'''

if not os.path.exists('data'):
    download()

# 如果在DataCollecting中以main运行，在其他地方调用反序列化时会出现AttributeError，要from DataCollecting import Case才可以
# 为什么不能在DataCollecting.py里序列化：
# 如果在该类定义的模块序列化，其他模块反序列化时会找不到定义，得import这个类。
# 在本模块中序列化，序列化后的开头为"c__main__"，在其他模块中反序列化后也以为在自己的__main__里，就会报找不到属性，得import。
# 在其他模块中序列化，序列化后的开头为"c"+类所在的模块的名称，知道去哪里找。
serialize_all_case_objs()

# PcaModel类不在该函数所在的模块，所以即使在SaveTrainingResult的main中运行，也不用import
serialize_training_result()
