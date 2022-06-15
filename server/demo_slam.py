import sys, os
import time
from slam import slam
from loguru import logger


is_run = False  # 是否在运行中
is_stop = False  # 是否停止业务线程
slam_data = [0.0 for _ in range(7)]  # slam数据


def get_slam_data():
    global is_run, is_stop, slam_data
    is_run, is_stop = True, False
    
    slam.start()
    while True:
        if is_stop:
            break
        slam_data = slam.get_data()
        print(slam_data)
        time.sleep(0.01)
    slam.stop()

    is_run = False
    # print("关闭slam程序")
    logger.info("关闭slam程序")


if __name__ == '__main__':
    get_slam_data()
    