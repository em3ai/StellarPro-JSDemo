import asyncio
import os
import sys
import subprocess
from threading import Thread
from time import time
import websockets
import json

from loguru import logger

import demo_hand as ht
import demo_slam as sl


def run_cmd(cmd: str) -> str:
    """运行命令行"""
    output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
    output = output.decode()
    return output


def restart_self():
    # 重启本程序
    interpreter = sys.executable
    os.execl(interpreter, interpreter, *sys.argv)


async def send_slam_data(websocket):
    """发送slam数据"""
    while True:
        json_str = json.dumps(sl.slam_data)
        try:
            await websocket.send(json_str)
        except Exception as e:
            print("用户断开连接:{}, type:{}".format(e, type(e)))

            return
        await asyncio.sleep(0.01)


async def send_hand_data(websocket):
    """发送handtracking数据"""
    while True:
        json_str = json.dumps(ht.hand_data)
        try:
            await websocket.send(json_str)
        except Exception as e:
            print("用户断开连接:{}, type:{}".format(e, type(e)))
            return
        await asyncio.sleep(0.01)


async def send(websocket, path):
    # 服务器端主逻辑, websocket和path是该函数被回调时自动传过来的，不需要自己传
    if path == "/slam":  # 开启slam
        print("{} connected".format(path))
        ht.is_stop = True  # 停止handtracking线程
        if not sl.is_run:
            await asyncio.sleep(6)  # 等待相机释放
            logger.info("开启 slam 线程")
            Thread(target=sl.get_slam_data, daemon=True).start()
        await send_slam_data(websocket)

    elif path == '/handtracking':  # 开启handtracking
        print("{} connected".format(path))
        sl.is_stop = True  # 停止slam线程
        
        if not ht.is_run:
            await asyncio.sleep(6)  # 等待相机释放
            logger.info("开启 handtracking 线程")
            Thread(target=ht.get_hand_data, daemon=True).start()
        await send_hand_data(websocket)

    # TODO: 当上面两者都断开连接时, 开启mouseop
    
    print("{} connect, refuse".format(path))


async def recv(websocket, path):
    while True:
        try:
            ret = await websocket.recv()
            print("收到客户端消息:", ret)
            if ret == "reset":
                restart_self()
        except Exception as e:
            print("用户断开连接:{}, type:{}".format(e, type(e)))
            return
        await asyncio.sleep(0.5)



async def handler(websocket, path):
    await asyncio.gather(send(websocket, path), recv(websocket, path))


if __name__ == '__main__':
    main_logic = websockets.serve(handler, '0.0.0.0', 56789)
    print("开启ws server")
    loop = asyncio.get_event_loop()
    # 启动协程
    loop.run_until_complete(main_logic)
    loop.run_forever()