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

# electron
把 client 中的代码打包成linux应用服务
## 打包注意事项
打包linux应用时，以下 electron-app 的打包过程 要在linux环境下执行（打包相应平台的应用，要在相应平台的环境下进行打包）


### 1.打包需要包含的功能代码在 https://github.com/em3ai/StellarPro-JSDemo 的for-electron分支

## 2.打包 hand-tracking 应用
### 2.1 下载 client 依赖 和 打包 client 
```
cd client

下载依赖：npm install

打包（打包后的代码在electron/web目录下）： npm run build
```
### 2.2 下载 electron 依赖 和 打包 electron
```
cd electron

下载依赖：npm install

打包：npm run make

```
### 2.3 hand-tracking的deb包在 electron/out/make/deb/arm64 目录下
拷贝文件到新的目录，或者直接安装
```
cd electron/out/make/deb/arm64

安装指令
sudo dpkg -i 'hand-tracking_1.1.2_arm64.deb'
```
## 3.打包 slam 应用
### 3.1 下载 client 依赖
```
cd client

下载依赖：npm install
```
### 3.2 修改 client 下代码
修改client/src/router/index.js内代码

注释掉 Home 路由
放开 Slam 路由

### 3.3 打包client
```
打包（打包后的代码在electron/web目录下）： npm run build
```
### 3.4 下载 electron 依赖
```
cd electron

下载依赖：npm install
```
### 3.5 修改 package.json 配置文件
```
1. "name": "hand-tracking" 修改为 "name": "slam"
2. "description": "hand tracking applications" 修改为 "description": "slam applications"

3. "icon": "./assets/appIcon/handTracking.png" 修改为 "icon": "./assets/appIcon/slam.png"
```
### 3.6 打包 electron 得到 slam 应用
```
打包：npm run make
```
### 3.7 slam的deb包在 electron/out/make/deb/arm64 目录下
拷贝文件到新的目录，或者直接安装
```
cd electron/out/make/deb/arm64

安装指令
sudo dpkg -i 'slam_1.1.2_arm64.deb'
```

