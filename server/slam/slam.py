from ctypes import *
import os



pDLL = None

def start():
    """开启slam程序"""
    global pDLL

    # 记住原来的工作目录
    ori_cwd = os.getcwd()
    print('改变前的工作路径:', ori_cwd)
    # 更改工作目录
    file_path = os.path.abspath(__file__)
    dir_path = os.path.dirname(file_path)
    os.chdir(dir_path)
    print('改变后的工作路径:', os.getcwd())

    pDLL = CDLL('./libmanager_s.so')

    # 恢复回原工作目录
    os.chdir(ori_cwd)
    print('恢复回原工作目录:', os.getcwd())

    pDLL.Start(c_char_p(b'/usr/local/em3/calibration/stereo_calibration.json'), c_char_p(b''))


def get_data():
    """获取空间锚点信息"""
    global pDLL
    if pDLL is None:
        raise 'please call start() first'
    x, y, z, w, a, b, c = [c_float() for _ in range(7)]
    pDLL.GetData_(byref(x), byref(y), byref(z), byref(w), byref(a), byref(b), byref(c))
    return [x.value, y.value, z.value, w.value, a.value, b.value, c.value]


def stop():
    """停止slam程序"""
    if pDLL is None:
        raise 'please call start() first'
    pDLL.Stop()



