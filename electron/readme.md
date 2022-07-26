# 注意
打包linux应用时，以下 electron-app 的打包过程 要在linux环境下执行（打包相应平台的应用，要在相应平台的环境下进行打包）
# 打包注意事项

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

### 处理成系统应用
#### 1.
准备工作：
mkdir extract
mkdir extract/DEBIAN
mkdir build

解包命令为：
#解压出包中的文件到extract目录下
dpkg -X xxx.deb extract/

#解压出包的控制信息extract/DEBIAN/下：
dpkg -e xxx.deb extract/DEBIAN/

修改文件XXX

对修改后的内容重新进行打包生成deb包
dpkg-deb -b extract/ build/

#### 2.1 解压 handtracking 的 deb 包
增加：electron/out/hand-tracking-deb/extract/usr/lib/systemd/user/handtracking.service
文件内容
```
[Unit]
Description=handtracking

[Service]
WorkingDirectory=/usr/local/em3/handtracking
Type=simple
ExecStart=/usr/local/em3/handtracking/handtracking.sh
ExecReload=/usr/local/em3/handtracking/handtracking.sh
Restart=no

[Install]
WantedBy=default.target
```

#### 2.2 添加SH文件
electron/out/hand-tracking-deb/extract/usr/local/em3/handtracking/handtracking.sh
文件内容
```
#!/bin/bash
hand-tracking
```

#### 2.3 改变 handtracking.sh 权限
```
chmod a+x handtracking.sh
```
#### 2.4 重新通过 dpkg-deb -b extract/ build/ 打包 handtracking


#### 3.1 解压 slam 的 deb 包
增加：electron/out/slam-deb/extract/usr/lib/systemd/user/slam.service
文件内容
```
[Unit]
Description=slam

[Service]
WorkingDirectory=/usr/local/em3/slam
Type=simple
ExecStart=/usr/local/em3/slam/slam.sh
ExecReload=/usr/local/em3/slam/slam.sh
Restart=no

[Install]
WantedBy=default.target
```

#### 2.2 添加SH文件
electron/out/slam-deb/extract/usr/local/em3/slam/slam.sh
文件内容
```
#!/bin/bash
slam
```

#### 2.3 改变 slam.sh 权限
```
chmod a+x slam.sh
```
#### 2.4 重新通过 dpkg-deb -b extract/ build/ 打包 slam
