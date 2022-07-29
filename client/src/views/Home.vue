<!--
 * @Date: 2022-05-19 10:35:55
 * @LastEditTime: 2022-07-29 16:49:36
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
import { Toast } from '@/utils/toast/index'
import Loading from '@/utils/loading/loading'
import '@/utils/loading/loading.css'
import { SceneLoader } from '@babylonjs/core/Loading/sceneLoader'
import '@babylonjs/loaders'
import '@babylonjs/core/Loading/Plugins'
export default {
  name: 'Home',
  data () {
    return {
      handInfo: '',
      scene: null,
      model: '',
      sphere2: null,
      freeCamera: null,
      VRCamera: null,
      camera: null,
      sphere: null,
      load: null,
      loadFlag: false,
      deviceDisconnect: null,
      deviceDisconnectFlag: false,
      noService: null,
      noServiceFlag: false
    }
  },
   watch: {
    // 2D / 3D模式切换
    model: function (newVal, oldVal) {
      if (newVal && newVal === '3d') {
        this.scene.activeCamera = this.VRCamera
        this.sphere.position.y = 10
        this.sphere.position.z = 4
        this.disc.position.x = -3
        this.disc.position.z = 4
        this.disc1.position.x = 3
        this.disc1.position.z = 4
      } else if (newVal && newVal === '2d') {
        this.scene.activeCamera = this.freeCamera
        this.camera.lockedTarget = this.sphere2
        this.sphere.position.y = 4
        this.sphere.position.z = 10
        this.disc.position.x = -2
        this.disc.position.z = 10
        this.disc1.position.x = 2
        this.disc1.position.z = 10
      }
    }
  },
  components: {
  },
  mounted () {
    this.load = new Loading(
      {
        type: 3,
        tipLabel: '正在初始化，请稍后...'
      }
    )
    this.deviceDisconnect = new Loading(
      {
        type: 3,
        tipLabel: '设备已断开连接...'
      }
    )
    this.noService = new Loading(
      {
        type: 3,
        tipLabel: 'socket 未连接！'
      }
    )
    this.initSocket()
    this.initBabylon()
    // 判断2D / 3D
    if (window.screen.width <= 1920) {
      this.model = '2d'
    } else if (window.screen.width === 3840 || window.screen.width > 1920) {
      this.model = '3d'
    }
  },
  beforeDestroy () {
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
        _that.VRCamera = new BABYLON.VRDeviceOrientationFreeCamera("camera2", new BABYLON.Vector3(0, 5, -10), scene, undefined)
        _that.camera = _that.freeCamera
        // Attach the _that.camera to the canvas
        _that.camera.attachControl(canvas, false)
        // 球体
         _that.sphere = BABYLON.MeshBuilder.CreateSphere('sphere1', { segments: 16, diameter: 4, sideOrientation: BABYLON.Mesh.FRONTSIDE }, scene)
        // 设置颜色
        _that.sphere.renderOverlay = true
        _that.sphere.overlayColor = new BABYLON.Color3.Blue()
        _that.sphere.overlayAlpha = 0.2
        // 通过 创建个隐形球，相机朝向这个球
        _that.sphere2 = BABYLON.MeshBuilder.CreateSphere('sphere2', { segments: 6, diameter: 0.0000001, sideOrientation: BABYLON.Mesh.FRONTSIDE }, scene)

        // 创建 锥体
        _that.disc = BABYLON.MeshBuilder.CreateCylinder('cylinder', { height: 2, diameter: 2, diameterTop: 0, tessellation: 16 })
        // 设置颜色
        _that.disc.renderOverlay = true
        _that.disc.overlayColor = new BABYLON.Color3.Red()
        _that.disc.overlayAlpha = 0.4

        _that.disc1 = BABYLON.MeshBuilder.CreateCylinder('cylinder', { height: 2, diameter: 2, diameterTop: 0, tessellation: 16 })

        _that.disc1.renderOverlay = true
        _that.disc1.overlayAlpha = 0.4
        // 自传
        // var cylinderRotation = 0
        // scene.registerBeforeRender(() => {
        //   cylinderRotation += 0.01
        //   _that.disc.rotation.y = cylinderRotation
        //   _that.disc1.rotation.y = cylinderRotation
        //   if (cylinderRotation > 2 * Math.PI) {
        //     cylinderRotation = 0
        //   }
        // })

        const light = new BABYLON.HemisphericLight('light', new BABYLON.Vector3(50, 1000, -5), scene)
        console.log(light)
        // 改变背景颜色
        scene.autoClear = true
        scene.clearColor = new BABYLON.Color4(0, 0, 0, 1)
        const leftUrl = `./hand.glb`
        SceneLoader.ImportMeshAsync(null, leftUrl, null, scene).then(result => {
          console.log(result, 'd')
          _that.meshes = result.meshes
          _that.skeletons = result.skeletons
          _that.transformNodes = result.transformNodes
          console.log(_that.transformNodes, 'transformNodes')

          // 左右手 默认不在视野内
          var leftRoot = _that.scene.getNodeByName('Armature.001')
          console.log(leftRoot)
          // leftRoot.position.x = -2

          // leftRoot.position.x = 10000
          // leftRoot.rotationQuaternion = new BABYLON.Vector3(0, 0, -Math.PI).toQuaternion()
          // rightRoot.position.x = 10000
        })
        // const rightUrl = `./right-hand.glb`
        // SceneLoader.ImportMeshAsync(null, rightUrl, null, scene).then(result => {
        //   console.log(result, 'd')
        //   _that.meshes = result.meshes
        //   _that.skeletons = result.skeletons
        //   _that.transformNodes = result.transformNodes
        //   console.log(_that.transformNodes, 'transformNodes')
        //   var rightRoot = _that.scene.getNodeByName('Armature')
        //   console.log(rightRoot)
        //   // rightRoot.rotationQuaternion = new BABYLON.Vector3(0, Math.PI, 0).toQuaternion()

        //   // rightRoot.position.x = 10000
        //   rightRoot.position.x = 2
        // })

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
            var points = _that.handInfo.left_info.keypoints
            // 最新代码
            var angles = _that.handInfo.left_info.angles
            var leftRoot = _that.scene.getNodeByName('Armature.001')
            console.log(leftRoot, 'leftRoot-------========')
            var leftBone = leftRoot && leftRoot.getChildTransformNodes(false)
            let Q = null
            leftBone && leftBone.map(item => {
              leftRoot.scaling = new BABYLON.Vector3(0.8, -0.8, 0.8)
              leftRoot.position = new BABYLON.Vector3(-points[9].x * 10, points[9].y * 10, points[9].z * 10)
              _that.matchLeftHand(item, angles, Q)
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
              _that.sphere.overlayColor = new BABYLON.Color3.Yellow()
              if (leftDistance < 0.4 && leftTouch) {
                console.log('创建呀------')
                leftTouch = false
                var newCylinder = ''
                if (_that.model === '3d') {
                  newCylinder = BABYLON.MeshBuilder.CreateCylinder('cylinder', { height: 3, diameter: 3, diameterTop: 0, tessellation: 16 })
                  newCylinder.position.x = Math.random() * 8 * (Math.random() > 0.5 ? 1 : -1)
                  newCylinder.position.y = Math.random() * 4 * (Math.random() > 0.5 ? 1 : -1) - 2
                  newCylinder.position.z = Math.random() * 5 + 5
                } else {
                  newCylinder = BABYLON.MeshBuilder.CreateCylinder('cylinder', { height: 2, diameter: 2, diameterTop: 0, tessellation: 16 })
                  newCylinder.position.x = Math.random() * 14 * (Math.random() > 0.5 ? 1 : -1)
                  newCylinder.position.y = Math.random() * 6 * (Math.random() > 0.5 ? 1 : -1) - 4
                  newCylinder.position.z = Math.random() * 10 + 5
                }
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
                _that.sphere.overlayColor = new BABYLON.Color3.Blue()
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
            var points = _that.handInfo.right_info.keypoints
            // 最新代码
            var angles = _that.handInfo.right_info.angles
            var rightRoot = _that.scene.getNodeByName('Armature')
            console.log(rightRoot, 'rightRoot-------========')
            var rightBone = rightRoot && rightRoot.getChildTransformNodes(false)
            let Q = null
            rightBone && rightBone.map(item => {
              rightRoot.scaling = new BABYLON.Vector3(0.8, -0.8, 0.8)
              // rightRoot.position = new BABYLON.Vector3(-points[9].x * 10, points[9].y * 10, points[9].z * 10)
              _that.matchRightHand(item, angles, Q)
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
              _that.sphere.overlayColor = new BABYLON.Color3.Yellow()
              // 在碰到球体 的前提下 判断捏合 ==> 生成球体
              if (rightDistance < 0.4 && rightTouch) {
                console.log('创建呀------')
                rightTouch = false
                if (_that.model === '3d') {
                  newCylinder = BABYLON.MeshBuilder.CreateCylinder('cylinder', { height: 3, diameter: 3, diameterTop: 0, tessellation: 16 })
                  newCylinder.position.x = Math.random() * 8 * (Math.random() > 0.5 ? 1 : -1)
                  newCylinder.position.y = Math.random() * 4 * (Math.random() > 0.5 ? 1 : -1) - 2
                  newCylinder.position.z = Math.random() * 5 + 5
                } else {
                  newCylinder = BABYLON.MeshBuilder.CreateCylinder('cylinder', { height: 2, diameter: 2, diameterTop: 0, tessellation: 16 })
                  newCylinder.position.x = Math.random() * 14 * (Math.random() > 0.5 ? 1 : -1)
                  newCylinder.position.y = Math.random() * 6 * (Math.random() > 0.5 ? 1 : -1) - 4
                  newCylinder.position.z = Math.random() * 10 + 5
                }
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
                _that.sphere.overlayColor = new BABYLON.Color3.Blue()
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
      // const socket = new WebSocket(`ws:${window.location.hostname}:56789/handtracking`)
      // const socket = new WebSocket(`ws:localhost:56789/handtracking`)
      const socket = new WebSocket(`ws:192.168.1.246:56789/handtracking`)
      socket.addEventListener('open', function (event) {
        Toast('socket 已连接！', 2000)
        if (_that.noServiceFlag) {
          _that.noService.hide()
          _that.noServiceFlag = false
        }
      })
      socket.addEventListener('close', function (event) {
        // socket 连接出错/断开
        if (!_that.noServiceFlag) {
          _that.noService.init()
          _that.noServiceFlag = true
        }
      })
      socket.addEventListener('message', function (event) {
        if (event.data &&
          JSON.parse(event.data) &&
          JSON.parse(event.data).status &&
          Number(JSON.parse(event.data).status) === -1 &&
          !_that.deviceDisconnectFlag) {
          // 眼镜断开连接
          _that.deviceDisconnect.init()
          _that.deviceDisconnectFlag = true
          if (_that.loadFlag) {
            // 双目匹配成功
            _that.loadFlag = false
            _that.load.hide()
          }
        } else if (event.data &&
          (JSON.parse(event.data) &&
          JSON.parse(event.data).status &&
          Number(JSON.parse(event.data).status) !== -1 ||
          (JSON.parse(event.data) && !JSON.parse(event.data).status))) {
            // 眼镜已连接
            if (_that.deviceDisconnectFlag) {
              _that.deviceDisconnect.hide()
              _that.deviceDisconnectFlag = false
            }
            _that.handInfo = event.data && JSON.parse(event.data)
            if (_that.loadFlag &&
              _that.handInfo &&
              JSON.stringify(_that.handInfo) !== '{}') {
                // 双目匹配成功
                _that.loadFlag = false
                _that.load.hide()
            } else if (!_that.loadFlag &&
              ((_that.handInfo &&
              JSON.stringify(_that.handInfo) === '{}') ||
              !_that.handInfo)) {
              // 双目匹配中
              _that.loadFlag = true
              _that.load.init()
            }
        }
      })
    },
    // 左手模型 角度
    matchLeftHand(item, angles, Q) {
      switch (item.id) { 
          // case 'Bone.019': // 拇指
          //   // item.rotation.z = angles[0] // * 180 / Math.PI
          //   // item.rotation.x = angles[2] // * 180 / Math.PI
          //   Q = new BABYLON.Vector3(angles[2], 0, angles[0]).toQuaternion()
          //   item.rotationQuaternion = Q
          //   console.log(Q, 'item.rotation.x---')
          //   // item.position = new BABYLON.Vector3(-points[2].x * scale, points[2].y * scale, -points[2].z * scaleZ)
          //   break;
          // case 'Bone.018':
          //   item.rotation.x = angles[3] // * 180 / Math.PI
          //   Q = new BABYLON.Vector3(angles[3], 0, 0).toQuaternion()
          //   item.rotationQuaternion = Q
          //   // item.position = new BABYLON.Vector3(-points[3].x * scale, points[3].y * scale, -points[3].z * scaleZ)
          //   break;
          case 'Bone.015': // 食指
            var x = -angles[5]
            var z = (Math.PI/2) - angles[4] - (Math.PI/7)
            Q = new BABYLON.Vector3(x, 0, z).toQuaternion()
            item.rotationQuaternion = Q
            break;
          case 'Bone.014':
            var x = -angles[6]
            Q = new BABYLON.Vector3(x, 0, 0).toQuaternion()
            item.rotationQuaternion = Q
            break; 
          case 'Bone.013':
            var x = -angles[7]
            Q = new BABYLON.Vector3(x, 0, 0).toQuaternion()
            item.rotationQuaternion = Q
            break;
          case 'Bone.011': // 中指
            var x = -angles[9]
            var z = (Math.PI/2) - angles[8]
            Q = new BABYLON.Vector3(x, 0, z).toQuaternion()
            item.rotationQuaternion = Q
            break;
          case 'Bone.010':
            var x = - angles[10]
            Q = new BABYLON.Vector3(x, 0, 0).toQuaternion()
            item.rotationQuaternion = Q
            break;
          case 'Bone.009':
            var x = -angles[11]
            Q = new BABYLON.Vector3(x, 0, 0).toQuaternion()
            item.rotationQuaternion = Q
            break;
          case 'Bone.007': // 无名指
            var x = -angles[13]
            var z = (Math.PI/2) - angles[12] + (Math.PI/7)
            Q = new BABYLON.Vector3(x, 0, z).toQuaternion()
            item.rotationQuaternion = Q
            break;
          case 'Bone.006':
            var x = -angles[14]
            Q = new BABYLON.Vector3(x, 0, 0).toQuaternion()
            item.rotationQuaternion = Q
            break;
          case 'Bone.005':
            var x = -angles[15]
            Q = new BABYLON.Vector3(x, 0, 0).toQuaternion()
            item.rotationQuaternion = Q
            break;
          case 'Bone.003': // 小拇指
            var x = -angles[17]
            var z = (Math.PI/2) - angles[16] + (Math.PI/4)
            Q = new BABYLON.Vector3(x, 0, z).toQuaternion()
            item.rotationQuaternion = Q
            break;
          case 'Bone.002':
            var x = -angles[18]
            Q = new BABYLON.Vector3(x, 0, 0).toQuaternion()
            item.rotationQuaternion = Q
            break;
          case 'Bone.001':
            var x = -angles[19]
            Q = new BABYLON.Vector3(x, 0, 0).toQuaternion()
            item.rotationQuaternion = Q
            break;
      }
    },
    // 右手模型角度
    matchRightHand(item, angles, Q) {
      switch (item.id) { 
          // case 'Bone.025': // 拇指
          //   item.position = new BABYLON.Vector3(-points[4].x * scale, points[4].y * scale, -points[4].z * scaleZ)
          //   break;
          // case 'Bone.004':
          //   item.position = new BABYLON.Vector3(-points[3].x * scale, points[3].y * scale, -points[3].z * scaleZ)
          //   break;
          // case 'Bone.003':
          //   item.position = new BABYLON.Vector3(-points[2].x * scale, points[2].y * scale, -points[2].z * scaleZ)
          //   break;
          // case 'Bone.002':
          //   item.position = new BABYLON.Vector3(-points[1].x * scale, points[1].y * scale, -points[1].z * scaleZ)
          //   break; 
          // // case 'Bone.001':
          // //   item.position = new BABYLON.Vector3(-points[0].x * scale, points[0].y * scale, -points[0].z * scaleZ)
          // //   break;
          //   case 'Bone':
          //   item.position = new BABYLON.Vector3(-points[0].x * scale, points[0].y * scale, -points[0].z * scaleZ)
          //   break;
        case 'Bone.015': // 食指
            var x = -angles[5]
            var z = (Math.PI/2) - angles[4] - (Math.PI/7)
            Q = new BABYLON.Vector3(x, 0, z).toQuaternion()
            item.rotationQuaternion = Q
            break;
          case 'Bone.014':
            var x = -angles[6]
            Q = new BABYLON.Vector3(x, 0, 0).toQuaternion()
            item.rotationQuaternion = Q
            break; 
          case 'Bone.013':
            var x = -angles[7]
            Q = new BABYLON.Vector3(x, 0, 0).toQuaternion()
            item.rotationQuaternion = Q
            break;
          case 'Bone.011': // 中指
            var x = -angles[9]
            var z = (Math.PI/2) - angles[8]
            Q = new BABYLON.Vector3(x, 0, z).toQuaternion()
            item.rotationQuaternion = Q
            break;
          case 'Bone.010':
            var x = - angles[10]
            Q = new BABYLON.Vector3(x, 0, 0).toQuaternion()
            item.rotationQuaternion = Q
            break;
          case 'Bone.009':
            var x = -angles[11]
            Q = new BABYLON.Vector3(x, 0, 0).toQuaternion()
            item.rotationQuaternion = Q
            break;
          case 'Bone.007': // 无名指
            var x = -angles[13]
            var z = (Math.PI/2) - angles[12] + (Math.PI/7)
            Q = new BABYLON.Vector3(x, 0, z).toQuaternion()
            item.rotationQuaternion = Q
            break;
          case 'Bone.006':
            var x = -angles[14]
            Q = new BABYLON.Vector3(x, 0, 0).toQuaternion()
            item.rotationQuaternion = Q
            break;
          case 'Bone.005':
            var x = -angles[15]
            Q = new BABYLON.Vector3(x, 0, 0).toQuaternion()
            item.rotationQuaternion = Q
            break;
          case 'Bone.003': // 小拇指
            var x = -angles[17]
            var z = (Math.PI/2) - angles[16] + (Math.PI/4)
            Q = new BABYLON.Vector3(x, 0, z).toQuaternion()
            item.rotationQuaternion = Q
            break;
          case 'Bone.002':
            var x = -angles[18]
            Q = new BABYLON.Vector3(x, 0, 0).toQuaternion()
            item.rotationQuaternion = Q
            break;
          case 'Bone.001':
            var x = -angles[19]
            Q = new BABYLON.Vector3(x, 0, 0).toQuaternion()
            item.rotationQuaternion = Q
            break;
      }
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
