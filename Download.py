import json
import urllib.request,urllib.parse
import os
import shutil
import string
import Unzip


# 注意，如果要在命令行里使用，先cd

f = open('test_data.json', encoding='utf-8')
res = f.read()
data = json.loads(res)

if not os.path.exists("data"):
    os.mkdir("data")

for userId in data:
    cases = data[userId]['cases']
    for case in cases:
        caseId = case['case_id']

        # 压缩包损坏
        if caseId == '2528' and userId == '60765':
            continue

        # 方便理解
        file_path = "data/case" + caseId + '/user' + userId + '/'

        # 创建目录
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        print(file_path)

        # 取最后一次提交
        finalUpload = len(case["upload_records"])-1
        if finalUpload < 0:
            continue

        file_url = case["upload_records"][finalUpload]["code_url"]
        filename = urllib.parse.unquote(os.path.basename(file_url))

        # user3544有两个case_id为2908，会有冲突
        # 重新运行时，要跳过成功下载的
        num_of_files = len(os.listdir(file_path))
        if num_of_files != 5:
            if num_of_files > 0:
                shutil.rmtree(file_path)
                os.mkdir(file_path)
            # 中文url不能下载，要quote
            urllib.request.urlretrieve(urllib.parse.quote(file_url, safe=string.printable), file_path + filename)
            Unzip.un_zip(file_path + filename)
            print('成功：'+file_path)
