import os
import shutil

def organize_sqlite_files(upload_dir, databases_dir):
    # 创建databases目录
    if not os.path.exists(databases_dir):
        os.makedirs(databases_dir)
    
    # 遍历upload目录中的所有文件
    for file_name in os.listdir(upload_dir):
        if file_name.endswith('.sqlite'):
            # 构建目标文件夹路径
            target_dir = os.path.join(databases_dir, os.path.splitext(file_name)[0])
            
            # 如果目标文件夹已存在，则删除文件夹及其内容
            if os.path.exists(target_dir):
                shutil.rmtree(target_dir)
            
            # 创建目标文件夹
            os.makedirs(target_dir)
            
            # 移动文件到目标文件夹
            shutil.move(os.path.join(upload_dir, file_name), os.path.join(target_dir, file_name))

    # 删除upload目录中的所有sqlite文件
    for file_name in os.listdir(upload_dir):
        if file_name.endswith('.sqlite'):
            os.remove(os.path.join(upload_dir, file_name))

# 示例用法
upload_dir = 'uploads'
databases_dir = 'databases'
organize_sqlite_files(upload_dir, databases_dir)
