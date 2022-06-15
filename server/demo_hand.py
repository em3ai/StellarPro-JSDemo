import sys, os
import time
from handtracking import handtracking
from loguru import logger


is_run = False  # 是否在运行中
is_stop = False  # 是否停止业务线程
hand_data = {}  # 手势数据


def get_hand_data():
    global is_run, is_stop, hand_data
    is_run, is_stop = True, False

    handtracking.start()
    while True:
        if is_stop:
            break
        hand_data = handtracking.get_data()
        print(hand_data)
        time.sleep(0.01)
    handtracking.stop()

    is_run = False
    logger.info('关闭handtracking程序')
    # print("关闭handtracking程序")


if __name__ == '__main__':
    get_hand_data()