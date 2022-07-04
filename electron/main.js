const { app, BrowserWindow, globalShortcut } = require('electron')
// app.disableHardwareAcceleration() // 关闭硬件加速 https://segmentfault.com/a/1190000041824934
const createWindow = () => {
  // We cannot require the screen module until the app is ready.
  const { screen } = require('electron')

  // Create a window that fills the screen's available work area.
  // const primaryDisplay = screen.getPrimaryDisplay()
  // const { width, height } = primaryDisplay.size
  const win = new BrowserWindow({
    // width,
    // height,
    frame: false, // 创建一个无边框窗口
    backgroundColor: '#000',
    fullscreen: true, // 是否全屏
    // alwaysOnTop: true,
  })
  screen.on('display-metrics-changed', () => {
    // 重启应用 ==>> 解决 2D / 3D 切换 时不全屏的问题（不太好的方法）
    app.relaunch()
    app.exit(0)
  })
  // win.loadURL('http://192.168.1.246:8000/jsDemo')
  // win.loadURL('http://192.168.1.82:10000/')
  win.loadFile('web/index.html')
  // win.webContents.openDevTools () // 打开控制台
}
app.whenReady().then(() => {
  // 注册一个'CommandOrControl+Esc' 快捷键监听器
  const ret = globalShortcut.register('CommandOrControl+Esc', () => {
    console.log('CommandOrControl+Esc is pressed')
    // 触发后 退出应用
    app.quit()
  })

  if (!ret) {
    console.log('registration failed')
  }
  
  createWindow()
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})
app.on('will-quit', () => {
  // 注销快捷键
  globalShortcut.unregister('CommandOrControl+Esc')
})
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit()
})
