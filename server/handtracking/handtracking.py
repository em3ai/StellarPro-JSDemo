from ctypes import *
import os


class Vector3(Structure):
    _fields_ = [("x", c_float), ("y", c_float), ("z", c_float)]

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def dot(self, rv):
        return x * rv.x + y * rv.y + z * rv.z


keypoint = Vector3(1., 2., 3.)


class Quaternion(Structure):
    _fields_ = [("x", c_float), ("y", c_float), ("z", c_float), ("w", c_float)]

    def __init__(self):
        self.x = 0.
        self.y = 0.
        self.z = 0.
        self.w = 1.


qua = Quaternion()


class Transform(Structure):
    _fields_ = [("position", Vector3), ("rotation", Quaternion)]


trans = Transform()


class Hand(Structure):
    """参数顺序须与c++一一对应"""
    _fields_ = [("id", c_int), ("confidence", c_float), ("handness", c_int), ("gesture", c_int),
                ("pinchDistance", c_float), ("hasPoint", c_bool), ("isLateral", c_bool), ("keypoints", Vector3 * 21),
                ("wrist", Transform), ("angles", c_float * 20)]


left_pre = Hand()
right_pre = Hand()

is_run = False  # 是否在运行中
is_stop = False  # 是否停止业务线程

def marshal_hand(hand_obj):
    keypoints = hand_obj.keypoints
    info = {
        "confidence": hand_obj.confidence,
        "keypoints": [
            {"x": keypoint.x, "y": keypoint.y, "z": keypoint.z}
            for keypoint in keypoints
        ],
    }
    return info


pDLL = None

def start():
    """开启手势识别程序"""
    global pDLL

    # 记住原来的工作目录
    ori_cwd = os.getcwd()
    print('改变前的工作路径:', ori_cwd)
    # 更改工作目录
    file_path = os.path.abspath(__file__)
    dir_path = os.path.dirname(file_path)
    os.chdir(dir_path)
    print('改变后的工作路径:', os.getcwd())

    pDLL = CDLL('./libmanager_h.so')

    # 恢复回原工作目录
    os.chdir(ori_cwd)
    print('恢复回原工作目录:', os.getcwd())

    pDLL.Start(c_char_p(b'/usr/local/em3/dlmodels/yolov5n.engine'), c_char_p(b'/usr/local/em3/dlmodels/KNet.engine'), c_char_p(b'/usr/local/em3/calibration/stereo_calibration.json'))


def get_data():
    """获取数据"""
    global pDLL, left_pre, right_pre
    if pDLL is None:
        raise 'please call start() first'
    pDLL.GetData(byref(left_pre), byref(right_pre))
    left_info = marshal_hand(left_pre)
    right_info = marshal_hand(right_pre)
    info = {
        "left_info": left_info,
        "right_info": right_info,
    }
    return info


def stop():
    """停止手势识别程序"""
    global pDLL
    if pDLL is None:
        raise 'please call start() first'
    pDLL.Stop()
