# StellarPro-JSDemo

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


## handTracking Demo
src/views/Home.vue
## slam Demo
src/views/Slam.vue
## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).
