import zipfile
import os


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
    zip_path,zip_name=os.path.split(file_name)
    zip_file.extractall(zip_path)

    zip_file.close()
    os.remove(file_name)

    # 列出当前文件夹下所有的文件和子目录，在目前，文件夹下只有一个文件，real_file，所以直接取[0]
    real_file=os.listdir(zip_path)[0] # 不携带父目录信息
    second_un_zip(zip_path+'/'+real_file)


def un_zip(file_name):
    first_un_zip(file_name)