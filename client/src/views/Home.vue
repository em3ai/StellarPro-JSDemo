<!--
 * @Date: 2022-05-19 10:35:55
 * @LastEditTime: 2022-06-28 18:22:38
 * @Description: Modify here please
 * @FilePath: /StellarPro-JSDemo/client/src/views/Home.vue
-->
<template>
  <div class="home">
    <canvas id="renderCanvas" touch-action="none"></canvas>
  </div>
</template>

<script>
import * as BABYLON from 'babylonjs'
// import { PointerEventTypes } from '@babylonjs/core/Events/pointerEvents'

export default {
  name: 'Home',
  data () {
    return {
      handInfo: '',
      scene: null,
      model: '2d',
      sphere2: null,
      freeCamera: null,
      VRCamera:null,
      camera: null
    }
  },
   watch: {
    // 2D / 3D模式切换
    'model': function (newVal, oldVal) {
      if (newVal && newVal ==='3d') {
        this.scene.activeCamera = this.VRCamera
      } else if (newVal && newVal ==='2d') {
        this.scene.activeCamera = this.freeCamera
        this.camera.lockedTarget = this.sphere2
      }
    }
  },
  components: {
  },
  mounted () {
    this.initSocket()
    this.initBabylon()
    const _that = this
    // 判断2D / 3D
    setInterval(() => {
      console.log(_that)
      if (window.screen.width === 1920) {
        _that.model = '2d'
      } else if (window.screen.width === 3840) {
        _that.model = '3d'
      }
    }, 3000)
    
  },
  methods: {
    initBabylon () {
      const _that = this
      // Get the canvas DOM element
      const canvas = document.getElementById('renderCanvas')
      // Load the 3D engine
      const engine = new BABYLON.Engine(canvas, true, { preserveDrawingBuffer: true, stencil: true })
      // CreateScene function that creates and return the scene
      const createScene = function () {
        // Create a basic BJS Scene object
        const scene = new BABYLON.Scene(engine)
        // Create a FreeCamera, and set its position to {x: 0, y: 5, z: -10}
        _that.freeCamera = new BABYLON.FreeCamera('camera1', new BABYLON.Vector3(0, 5, -10), scene)
        // VRCamera
        _that.VRCamera = new BABYLON.VRDeviceOrientationFreeCamera("", new BABYLON.Vector3(0, 5, -10), scene, undefined)
        _that.camera = _that.freeCamera
        // Target the _that.camera to scene origin
        _that.camera.setTarget(BABYLON.Vector3.Zero())
        // Attach the _that.camera to the canvas
        _that.camera.attachControl(canvas, false)
        // 球体
        const sphere = BABYLON.MeshBuilder.CreateSphere('sphere1', { segments: 16, diameter: 4, sideOrientation: BABYLON.Mesh.FRONTSIDE }, scene)
        sphere.position.y = 4
        sphere.position.z = 10

        // 设置颜色
        sphere.renderOverlay = true
        sphere.overlayColor = new BABYLON.Color3.Blue()
        sphere.overlayAlpha = 0.2
        console.log(sphere.position, 'sphere.position===---')
        // 通过 创建个隐形球，相机朝向这个球
        _that.sphere2 = BABYLON.MeshBuilder.CreateSphere('sphere2', { segments: 6, diameter: 0.0000001, sideOrientation: BABYLON.Mesh.FRONTSIDE }, scene)
        _that.camera.lockedTarget = _that.sphere2

        // 创建 锥体
        const disc = BABYLON.MeshBuilder.CreateCylinder('cylinder', { height: 2, diameter: 2, diameterTop: 0, tessellation: 16 })
        disc.position.x = -2
        disc.position.z = 10
        // 设置颜色
        disc.renderOverlay = true
        disc.overlayColor = new BABYLON.Color3.Red()
        disc.overlayAlpha = 0.4

        const disc1 = BABYLON.MeshBuilder.CreateCylinder('cylinder', { height: 2, diameter: 2, diameterTop: 0, tessellation: 16 })
        disc1.position.x = 2
        disc1.position.z = 10

        disc1.renderOverlay = true
        disc1.overlayAlpha = 0.4
        // 自传
        // var cylinderRotation = 0
        // scene.registerBeforeRender(() => {
        //   cylinderRotation += 0.01
        //   disc.rotation.y = cylinderRotation
        //   disc1.rotation.y = cylinderRotation
        //   if (cylinderRotation > 2 * Math.PI) {
        //     cylinderRotation = 0
        //   }
        // })

        const light = new BABYLON.HemisphericLight('light', new BABYLON.Vector3(0, 0, -1), scene)
        console.log(light)
        // 改变背景颜色
        scene.autoClear = true
        scene.clearColor = new BABYLON.Color4(0, 0, 0, 1)

        // 点击事件
        // scene.onPointerObservable.add(pointerInfo => {
        //   const { type, event, pickInfo } = pointerInfo
        //   // console.log(PointerEventTypes.POINTERUP, type)
        //   if (type !== PointerEventTypes.POINTERUP) return
        //   console.log('1 --单击', event, pickInfo)
        //   // 1.增加 三角 mesh
        //   // 点击到mesh && 点击的是球体 && 物体增加到一定数量不可增加
        //   if (pickInfo.pickedMesh && pickInfo.pickedMesh.id === 'sphere1' && scene.rootNodes.length < 62) { // 实际生成的三角数量为 20-4 手 21+21 62-21-21-4
        //     const newCylinder = BABYLON.MeshBuilder.CreateCylinder('cylinder', { height: 1, diameter: 0.8, diameterTop: 0, tessellation: 16 })
        //     newCylinder.position.x = Math.random() * 5 * (Math.random() > 0.5 ? 1 : -1)
        //     newCylinder.position.y = Math.random() * 2 * (Math.random() > 0.5 ? 1 : -1) - 2
        //     newCylinder.position.z = Math.random() * 10 + 5

        //     // 设置颜色
        //     newCylinder.renderOverlay = true
        //     newCylinder.overlayAlpha = 0.4
        //     // 自传
        //     cylinderRotation = 0
        //     scene.registerBeforeRender(() => {
        //       cylinderRotation += 0.01
        //       newCylinder.rotation.y = cylinderRotation
        //       if (cylinderRotation > 2 * Math.PI) {
        //         cylinderRotation = 0
        //       }
        //     })

        //     // 2. 删除 三角 mesh
        //   } else if (pickInfo.pickedMesh && pickInfo.pickedMesh.id !== 'sphere1') {
        //     // 点击的是非球体的mesh 删除mesh
        //     console.log(event, pickInfo, '哪里', scene.rootNodes)
        //     console.log(pickInfo.pickedMesh.uniqueId)
        //     pickInfo.pickedMesh.isVisible = false // 点击物体不可见
        //     const delIdx = scene.rootNodes.findIndex((item) => {
        //       return item.uniqueId === pickInfo.pickedMesh.uniqueId
        //     })
        //     if (delIdx !== -1) {
        //       scene.rootNodes.splice(delIdx, 1) // 改变 rootNodes 长度
        //     }
        //   }
        // })
        // 左手 21个 关节
        const handLeft = []
        for (var num = 0; num < 21; num++) {
          handLeft.push(BABYLON.MeshBuilder.CreateSphere('sphere3', { segments: 16, diameter: 0.2, sideOrientation: BABYLON.Mesh.FRONTSIDE }, scene))
        }
        console.log('handLeft:', handLeft)
        // 右手 21个 关节
        const handRight = []
        for (var nums = 0; nums < 21; nums++) {
          handRight.push(BABYLON.MeshBuilder.CreateSphere('sphere3', { segments: 16, diameter: 0.2, sideOrientation: BABYLON.Mesh.FRONTSIDE }, scene))
        }
        console.log('handRight:', handRight)
        var leftRay = '', leftRayHelper = '',
        rightRay = '', rightRayHelper = '',
        leftTouch = true, rightTouch = true,
        leftDistance = '',
        leftOriginOne = '',
        leftOriginTwo = '',
        leftLocalMeshDirection = '',
        leftLocalMeshOrigin = '',
        leftRayInfo = '',
        rightDistance = '',
        rightOriginOne = '',
        rightOriginTwo = '',
        rightLocalMeshDirection = '',
        rightLocalMeshOrigin = '',
        rightRayInfo = '',
        leftHand = false, // 左手射线是否碰到物体
        rightHand = false // 右手射线是否碰到物体
        scene.registerBeforeRender(function () {
          // console.log(_that.handInfo)
          // 一、生成左手
          if (_that.handInfo && _that.handInfo.left_info && Number(_that.handInfo.left_info.confidence) > 0) {
            // 1. 渲染21个指关节
            _that.handInfo && _that.handInfo.left_info && _that.handInfo.left_info.keypoints && _that.handInfo.left_info.keypoints.map((item, index) => {
              handLeft[index].isVisible = true
              handLeft[index].position.x = item.x * 10
              handLeft[index].position.y = item.y * 10
              handLeft[index].position.z = item.z * 10
            })
             // 2. 创建 射线
            leftOriginOne = _that.handInfo.left_info.keypoints[0]
            leftOriginTwo = _that.handInfo.left_info.keypoints[8]
            leftRayHelper && leftRayHelper.dispose()
            leftLocalMeshDirection = new BABYLON.Vector3(leftOriginTwo.x - leftOriginOne.x, leftOriginTwo.y - leftOriginOne.y, leftOriginTwo.z - leftOriginOne.z)
            leftLocalMeshOrigin = new BABYLON.Vector3(leftOriginTwo.x * 10, leftOriginTwo.y * 10, leftOriginTwo.z * 10 + 0.2)
            leftRay = new BABYLON.Ray(leftLocalMeshOrigin, leftLocalMeshDirection, 200)
            leftRayHelper = new BABYLON.RayHelper(leftRay)
            leftRayHelper.show(scene)
            // 3.1 判断射线碰到球体 ==> 改变球体颜色
            leftRayInfo = scene.pickWithRay(leftRay)
            leftDistance = Math.sqrt(Math.abs((handLeft[4].position.x - handLeft[8].position.x) * (handLeft[4].position.x - handLeft[8].position.x) + (handLeft[4].position.y - handLeft[8].position.y) + (handLeft[4].position.z - handLeft[8].position.z)))
            if (leftRayInfo && leftRayInfo.pickedMesh && leftRayInfo.pickedMesh.id === 'sphere1') {
              !leftHand && (leftHand = true)
              sphere.overlayColor = new BABYLON.Color3.Yellow()
              if (leftDistance < 0.4 && leftTouch) {
                console.log('创建呀------')
                leftTouch = false
                const newCylinder = BABYLON.MeshBuilder.CreateCylinder('cylinder', { height: 2, diameter: 2, diameterTop: 0, tessellation: 16 })
                newCylinder.position.x = Math.random() * 5 * (Math.random() > 0.5 ? 1 : -1)
                newCylinder.position.y = Math.random() * 2 * (Math.random() > 0.5 ? 1 : -1) - 2
                newCylinder.position.z = Math.random() * 10 + 5
                // 设置颜色
                newCylinder.renderOverlay = true
                newCylinder.overlayAlpha = 0.4
                // scene.registerBeforeRender(() => {
                //   cylinderRotation += 0.01
                //   newCylinder && newCylinder.rotation && (newCylinder.rotation.y = cylinderRotation)
                //   if (cylinderRotation > 2 * Math.PI) {
                //     cylinderRotation = 0
                //   }
                // })
              } else if (leftDistance >= 0.4) {
                leftTouch = true
              }
            } else if (leftRayInfo && leftRayInfo.pickedMesh && leftRayInfo.pickedMesh.id !== 'sphere1' && leftRayInfo.pickedMesh.id !== 'sphere3') {
              // 3.2 射线碰撞到圆锥体 改变圆锥体颜色
              !leftHand && (leftHand = true)
              leftRayInfo.pickedMesh.overlayColor = new BABYLON.Color3.Yellow()
              // 捏合
              if (leftDistance < 0.4) {
                // 删除圆锥体
                leftRayInfo.pickedMesh.dispose()
                console.log('消失呀---')
              }
            } else {
              // 3.3 射线没有碰到物体时， 物体恢复原色
              leftHand && (leftHand = false)
              if (!rightHand) {
                sphere.overlayColor = new BABYLON.Color3.Blue()
                scene.rootNodes.forEach(item => {
                  if (item.id === 'cylinder') {
                    // 圆锥体恢复颜色
                    item.overlayColor = new BABYLON.Color3.Red()
                  }
                })
              }
            }
          } else {
            leftRayHelper && leftRayHelper.dispose()
            handLeft.map((item) => {
              item.isVisible = false
            })
          }
          // 二、 生成右手
          if (_that.handInfo && _that.handInfo.right_info && Number(_that.handInfo.right_info.confidence) > 0) {
            // 1. 渲染21个指关节
            _that.handInfo && _that.handInfo.right_info && _that.handInfo.right_info.keypoints && _that.handInfo.right_info.keypoints.map((item, index) => {
              handRight[index].isVisible = true
              handRight[index].position.x = item.x * 10
              handRight[index].position.y = item.y * 10
              handRight[index].position.z = item.z * 10
            })

            // 2. 创建 射线
            rightOriginOne = _that.handInfo.right_info.keypoints[0]
            rightOriginTwo = _that.handInfo.right_info.keypoints[8]
            rightRayHelper && rightRayHelper.dispose()
            rightLocalMeshDirection = new BABYLON.Vector3(rightOriginTwo.x - rightOriginOne.x, rightOriginTwo.y - rightOriginOne.y, rightOriginTwo.z - rightOriginOne.z)
            rightLocalMeshOrigin = new BABYLON.Vector3(rightOriginTwo.x * 10, rightOriginTwo.y * 10, rightOriginTwo.z * 10 + 0.2)
            rightRay = new BABYLON.Ray(rightLocalMeshOrigin, rightLocalMeshDirection, 200)
            rightRayHelper = new BABYLON.RayHelper(rightRay)
            rightRayHelper.show(scene)
            // 3.1 判断射线碰到球体 ==> 改变球体颜色
            rightRayInfo = scene.pickWithRay(rightRay)
            rightDistance = Math.sqrt(Math.abs((handRight[4].position.x - handRight[8].position.x) * (handRight[4].position.x - handRight[8].position.x) + (handRight[4].position.y - handRight[8].position.y) + (handRight[4].position.z - handRight[8].position.z)))
            if (rightRayInfo && rightRayInfo.pickedMesh && rightRayInfo.pickedMesh.id === 'sphere1') {
              !rightHand && (rightHand = true)
              sphere.overlayColor = new BABYLON.Color3.Yellow()
              // 在碰到球体 的前提下 判断捏合 ==> 生成球体
              if (rightDistance < 0.4 && rightTouch) {
                console.log('创建呀------')
                rightTouch = false
                const newCylinder = BABYLON.MeshBuilder.CreateCylinder('cylinder', { height: 2, diameter: 2, diameterTop: 0, tessellation: 16 })
                newCylinder.position.x = Math.random() * 5 * (Math.random() > 0.5 ? 1 : -1)
                newCylinder.position.y = Math.random() * 2 * (Math.random() > 0.5 ? 1 : -1) - 2
                newCylinder.position.z = Math.random() * 10 + 5
                // 设置颜色
                newCylinder.renderOverlay = true
                newCylinder.overlayAlpha = 0.4
                // scene.registerBeforeRender(() => {
                //   cylinderRotation += 0.01
                //   newCylinder && newCylinder.rotation && (newCylinder.rotation.y = cylinderRotation)
                //   if (cylinderRotation > 2 * Math.PI) {
                //     cylinderRotation = 0
                //   }
                // })
              } else if (rightDistance >= 0.4) {
                rightTouch = true
              }
            } else if (rightRayInfo && rightRayInfo.pickedMesh && rightRayInfo.pickedMesh.id !== 'sphere1' && rightRayInfo.pickedMesh.id !== 'sphere3') {
              // 3.2 射线碰撞到圆锥体 改变圆锥体颜色
              !rightHand && (rightHand = true)
              rightRayInfo.pickedMesh.overlayColor = new BABYLON.Color3.Yellow()
              // 捏合
              // console.log(rightDistance, 'rightDistance---')
              if (rightDistance < 0.4) {
                // 删除圆锥体
                rightRayInfo.pickedMesh.dispose()
                console.log('消失呀---')
              }
            } else {
              // 3.3 射线没有碰到物体时， 物体恢复原色
              rightHand && (rightHand = false)
              if (!leftHand) {
                sphere.overlayColor = new BABYLON.Color3.Blue()
                scene.rootNodes.forEach(item => {
                  if (item.id === 'cylinder') {
                    // 圆锥体恢复颜色
                    item.overlayColor = new BABYLON.Color3.Red()
                  }
                })
              }
            }
          } else {
            // 释放射线
            rightRayHelper && rightRayHelper.dispose()
            handRight.map((item) => {
              item.isVisible = false
            })
          }
        })
        return scene
      }
      // call the createScene function
      const scene = createScene()
      // run the render loop
      engine.runRenderLoop(function () {
        scene.render()
      })
      // the canvas/window resize event handler
      window.addEventListener('resize', function () {
        engine.resize()
      })
      _that.scene = scene
    },
    // 连接后端服务，获取左右手的空间坐标
    initSocket () {
      const _that = this
      // 注意：下面 socket 连接的 IP 应为 python 起服务的 IP
      const socket = new WebSocket(`ws:${window.location.hostname}:56789/handtracking`)
      socket.addEventListener('open', function (event) {
        // socket.send('Hello')
      })
      socket.addEventListener('message', function (event) {
        _that.handInfo = event.data && JSON.parse(event.data)
      })
    }
  }
}
</script>

<style lang="scss">
.home {
  width: 100vw;
  height: 100vh;
  background: #000;
}
canvas {
  width: 100%;
  height: 100%;
}
</style>
