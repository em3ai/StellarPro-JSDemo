# server

## 目录介绍
server目录下是 handTracking 和 slam 的后端服务

- handtracking文件夹: 手势识别SDK, 存放动态库及接口封装文件

- slam文件夹: 空间锚点SDK, 存放动态库及接口封装文件

- demo_hand.py: 调用手势识别接口的demo脚本

- demo_slam.py: 调用空间锚点接口的demo脚本

- server.py: websocket服务器, 负责推送slam或hand数据给前端

## 启动项目

```
// 进入项目目录
cd server

// 下载依赖
python -m pip install websockets

// 启动服务
python3 server.py

```

# client
前端JS项目，包含 handTracking 和 slam 两个 Demo

## 注意：❗️❗️❗️
在启动前端项目之前，先到
client/src/views/Home.vue和
client/src/views/Slam.vue目录下
修改
```
    initSocket () {
      const _that = this
      const socket = new WebSocket('ws:192.168.1.246:56789/handtracking')
      socket.addEventListener('open', function (event) {
        socket.send('Hello')
      })
      socket.addEventListener('message', function (event) {
        _that.handInfo = event.data && JSON.parse(event.data)
      })
    }
```
和
```
initSocket () {
      const _that = this
      _that.socket = new WebSocket('ws:192.168.1.246:56789/slam')
      _that.socket.addEventListener('open', function (event) {
        _that.socket.send('Hello')
      })
      _that.socket.addEventListener('message', function (event) {
        _that.cameraData = event.data && JSON.parse(event.data)
      })
    }
```
这俩方法的 socket服务器的 IP 为 python 服务的IP

## 启动项目： 
```
// 进入项目目录
cd client

// 下载依赖
npm install

// 启动服务
npm run serve
```

## handTracking Demo
client/src/views/Home.vue

## slam Demo
client/src/views/Slam.vue

### Compiles and minifies for production
```
npm run build
```

