import json
import os
import shutil
import string
import urllib.parse
import urllib.request
import zipfile

'''
注意，如果要在命令行里使用，先cd
不被其他地方调用
形成data-case-user的目录结构
'''


# 下载下来时，实际是套了一层压缩包，要解两次
# 因为一个(case,user)只需要一份代码，最终文件解压到./case****/user****/，不解压到新文件夹

def second_un_zip(file_name):
    if not os.path.exists(file_name):
        pass
    zip_file = zipfile.ZipFile(file_name)

    # 分割目录和文件
    zip_path, zip_name = os.path.split(file_name)

    # 解压到当前目录
    zip_file.extractall(zip_path)
    zip_file.close()
    os.remove(file_name)


def first_un_zip(file_name):
    if not os.path.exists(file_name):
        pass
    zip_file = zipfile.ZipFile(file_name)
    # 解压到当前文件夹
    zip_path, zip_name = os.path.split(file_name)
    zip_file.extractall(zip_path)

    zip_file.close()
    os.remove(file_name)

    # 列出当前文件夹下所有的文件和子目录，在目前，文件夹下只有一个文件，real_file，所以直接取[0]
    real_file = os.listdir(zip_path)[0]  # 不携带父目录信息
    second_un_zip(zip_path + '/' + real_file)


def un_zip(file_name):
    first_un_zip(file_name)


def download():
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
            finalUpload = len(case["upload_records"]) - 1
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
                un_zip(file_path + filename)
                print('成功：' + file_path)
