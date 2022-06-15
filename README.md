# client
前端JS项目，包含 handTracking 和 slam 两个 Demo

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
pip install websockets

// 启动服务
python3 server.py

```