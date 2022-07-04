<!--
 * @Date: 2022-07-01 14:13:08
 * @LastEditTime: 2022-07-04 11:49:37
 * @Description: Modify here please
 * @FilePath: /StellarPro-JSDemo/electron/readme.md
-->
# 注意
以下 electron-app 的打包过程 要在linux环境下执行
# 打包注意事项

### 1.打包需要包含的功能代码在 https://github.com/em3ai/StellarPro-JSDemo 的dev分支
### 2.要分别打两次包，一个是handTracking, 一个是slam


### 3.打包handTracking时 先改 client/package.json 中的name 为 hand-tracking ==> electron 应用的名字

3.1 修改 client/src/router/index.js 中路由默认配置要是 Home

### 4.打包slam时 先改 client/package.json 中的name 为 slam ==> electron 应用的名字

4.1 修改 client/src/router/index.js 中路由默认配置要是 Slam

4.2 修改 client/src/views/Slam.vue 中的  	`const url = '/scene.gltf'` 为 `const url = './scene.gltf'`

4.3 修改 client/src/views/Slam.vue 中的  	`const src = 'environments/skybox.env'` 为 `const src = './environments/skybox.env'`

### 5. 分两次把 handTracking 和 slam 打包出的dist目录下的文件拷贝到 electron-app 项目下的根目录下

### 6. 执行 electron-app 的打包程序，分别得到 handTracking 和 slam 的linux版 app