# 列出所需文件的全部路径
# 查看服务器备份文件路径
# 删除没有在所需文件路径里面的文件

import os
import shutil
import logging
logging.basicConfig(level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s- %(message)s')

log = logging.debug

log("Start of program")


def list_file(path):
    for root, sec, files in os.walk(path):
        for file in files:
            yield os.path.join(root, file)


def suffix(path):
    if r'server_update' in path:
        return path.split("server_update")[-1]
    else:
        return path.split("new")[-1]


def remove(remove_path, target_path):
    for path in list_file(remove_path):
        if suffix(path) not in list(map(suffix, list_file(target_path))):
            os.remove(path)
            log(f'{path} is deleted')


target_path = r"C:\Users\steven\Desktop\new"
remove_path = r"C:\Users\steven\Desktop\server_update"

needs = list(list_file(target_path))
wait_remove = list(list_file(remove_path))
log(f"Before remove, target file num: {len(needs)}")
log(f"Before remove, remove file num: {len(wait_remove)}")

remove(remove_path, target_path)
needs = list(list_file(target_path))
wait_remove = list(list_file(remove_path))
log(f"after remove, target file num: {len(needs)}")
log(f"after remove, remove file num: {len(wait_remove)}")
log("End of program")
