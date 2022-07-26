<template>
  <div class="about">
    <canvas id="renderCanvas" touch-action="none"></canvas>
    <!-- <div :class="{'explosion-btn': true, 'EM3':true, 'EM3-explosion': true, 'explosion-active': explosionStatus} " @click="enterExplosionMode">
      <div class="tips">爆炸</div>
    </div>
    <div :class="{'reset-btn': true, 'EM3':true, 'EM3-reset': true} " @click="handleReset">
      <div class="tips">重置</div>
    </div> -->
  </div>
</template>
<script>
import * as BABYLON from 'babylonjs'
import { SceneLoader } from '@babylonjs/core/Loading/sceneLoader'
import '@babylonjs/loaders'
import '@babylonjs/core/Loading/Plugins'
import { MeshExploder } from '@babylonjs/core/Misc/meshExploder'
import Loading from '@/utils/loading/loading'
import '@/utils/loading/loading.css'
import { Toast } from '@/utils/toast/index'
export default {
  name: 'Slam',
  components: {
  },

  data () {
    return {
      canvas: null,
      meshes: [],
      scene: null,
      explosionStatus: false,
      camera: null,
      cameraData: null,
      socket: null,
      freeCamera: null,
      VRCamera: null,
      // cameraData: { position: [-0.0, 0.0, -0.0], rotation: [-0.0, 0.0, -0.0, 0.0] }
      // {"position": [-0.0, 0.0, -0.0], "rotation": [-0.0, 0.0, -0.0, 0.0]}
      load: null,
      loadFlag: true,
      deviceDisconnect: null,
      deviceDidconnectFlag: false,
      noService: null,
      noServiceFlag: false
    }
  },
  mounted () {
    this.load = new Loading(
      {
        type: 3,
        tipLabel: '双目匹配中，请稍后...'
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
    this.initBabylon()
    this.initSocket()
  },
  beforeDestroy () {
  },
  methods: {
    // 同步眼镜数据到camera
    updateCamera6DOF () {
      const _that = this, camera = this.camera
      _that.scene.registerBeforeRender(() => {
        // console.log(_that.cameraData)
        if (_that.cameraData) {
          // 相机空间坐标
          camera.position.x = _that.cameraData[0] * 1
          camera.position.y = _that.cameraData[1] * 1
          camera.position.z = _that.cameraData[2] * 1
          // 相机角度
          const Q = new BABYLON.Quaternion(-_that.cameraData[4], _that.cameraData[5], -_that.cameraData[6], _that.cameraData[3])
          camera.rotationQuaternion = Q
          // this.camera.rotation = Q.toEulerAngles()
        }
      })
    },
    enterFullScreen: function () {
      const docEle = document.documentElement
      
      if (docEle.requestFullscreen) {  
        docEle.requestFullscreen();  
      } else if (docEle.mozRequestFullScreen) {  
        docEle.mozRequestFullScreen();  
      } else if (docEle.webkitRequestFullScreen) {  
        docEle.webkitRequestFullScreen();  
      } else if (docEle.msRequestFullscreen) {  
        docEle.msRequestFullscreen();  
      }
    },

    initBabylon () {
      if (!BABYLON.Engine.isSupported()) {
        return
      }
    
      BABYLON.Engine.ShadersRepository = "/src/Shaders/";
      BABYLON.Animation.AllowMatricesInterpolation = !0;
    
      // engine
      var canvas = document.getElementById("renderCanvas");
      if (!canvas) return;

      this.canvas = canvas;

      var engine = new BABYLON.Engine(
        canvas, 
        true, 
        { 
          preserveDrawingBuffer: true, 
          stencil: true, // highlightLayer的前提需要设置该项
          premultipliedAlpha: false
        }, 
        true // AdaptToDeviceRatio on
      );
      if (!engine) {
          this.showError('Fail to create Babylon engine.')
          return;
      }
      engine.enableOfflineSupport = false; // 减少内存消耗
      engine.doNotHandleContextLost = true;

      this.scene = new BABYLON.Scene(engine)
      
      // the canvas/window resize event handler
      window.addEventListener('resize', function () {
        engine.resize()
      })

      this.loadAssets();
    },

    loadAssets () {
      // load mesh
      // const url = 'http://192.168.1.62:8080/scene.gltf'
      const url = `./scene.gltf`
      const that = this
      SceneLoader.ImportMeshAsync(null, url, null, this.scene).then(result => {
        console.log(result, 'd')
        that.meshes = result.meshes;

        that.prepareCamera()
        // that.prepareBgSkybox()
        that.prepareBackgroundColor()
        that.prepareLighting()

        // Wait for textures and shaders to be ready
        that.scene.executeWhenReady(function () {
          // engine.hideLoadingUI();
          const engine = that.scene.getEngine()
          engine.runRenderLoop(function () {
              that.scene.render();
          });

          that.updateCamera6DOF()
        })
      })
    },

    prepareCamera () {
      const scene = this.scene
      var worldExtends = scene.getWorldExtends(function (mesh) { return mesh.isVisible && mesh.isEnabled(); });
      var worldSize = worldExtends.max.subtract(worldExtends.min);
      var worldCenter = worldExtends.min.add(worldSize.scale(0.5));
      // var camera = null;
      var radius = worldSize.length() * 1.5;
      // empty scene scenario!
      if (!isFinite(radius)) {
          radius = 1;
          worldCenter.copyFromFloats(0, 0, 0);
      }
    
      this.freeCamera = new BABYLON.FreeCamera("default camera", new BABYLON.Vector3(worldCenter.x, worldCenter.y, -radius), scene);
      // VRCamera
      this.VRCamera = new BABYLON.VRDeviceOrientationFreeCamera("camera2", new BABYLON.Vector3(worldCenter.x, worldCenter.y, -radius), scene, undefined);
      // freeCamera.setTarget(worldCenter);
      // 判断2D / 3D
      if (window.screen.width === 1920) {
        this.camera = this.freeCamera;
        scene.activeCamera = this.camera;
      } else if (window.screen.width === 3840) {
        this.camera = this.VRCamera;
        scene.activeCamera = this.camera;
      }
      console.log(`worldC: ${worldCenter.x}, ${worldCenter.y}, ${worldCenter.z}`)
  
      this.camera.minZ = radius * 0.01;
      this.camera.maxZ = radius * 1000;
      this.camera.speed = radius * 0.2;
        
      this.camera.attachControl();

      // 调整相机位姿：使得相机位于原点，并且模型和相机相对空间坐标合适
      const CoT = new BABYLON.TransformNode('CoT')
      CoT.position = worldCenter.clone();

      console.log(`camera pos0: ${this.camera.position.x}, ${this.camera.position.y}, ${this.camera.position.z}`)
      console.log(`mesh pos0: ${CoT.position.x}, ${CoT.position.y}, ${CoT.position.z}`)
         
      this.meshes.forEach(mesh => {
        /* 注意设置parent的方式有几种，效果不一样
          * setParent(CoT): child的世界坐标系空间坐标不会变化，实际上是以parent为参照系，来修改child内部的position、rotationQuaternion(或者rotation)、scaling等状态值
          * parent = CoT: child的世界坐标系空间坐标发生变化，实际上是保持child内部的状态参数不变，以parent为参照系重新计算世界坐标空间坐标
          * 详见：https://doc.babylonjs.com/divingDeeper/mesh/transforms/parent_pivot/parent
          */
        mesh.setParent(CoT);
      })
      const realtiveVec = CoT.position.subtract(this.camera.position);
      this.camera.position = BABYLON.Vector3.Zero()
      CoT.position = realtiveVec
      CoT.rotation.y = 1 // 调整模型角度
      this.meshes.forEach(mesh => {
        mesh.setParent(null)
      })
      console.log(`camera pos: ${this.camera.position.x}, ${this.camera.position.y}, ${this.camera.position.z}`)
      console.log(`mesh pos: ${CoT.position.x}, ${CoT.position.y}, ${CoT.position.z}`)
    },

    prepareBackgroundColor () {
      const scene = this.scene
      scene.autoClear = true;
      scene.clearColor = new BABYLON.Color4(0, 0, 0, 1);
    },

    // 背景天空盒
    prepareBgSkybox: function () {
      const name = 'skyBox'
      const src = './environments/skybox.env'
      const scene = this.scene
      const camera = scene.activeCamera
    
      let texture = null
      if (src.indexOf(".hdr") === src.length - 4) {
        // 512->256, 可以减少2秒时长，效果肉眼无差异
        texture = new BABYLON.HDRCubeTexture(src, scene, 256, false, true, false, true)
      } else {
        texture = new BABYLON.CubeTexture.CreateFromPrefilteredData(src, scene)
      }

      // var hdrTexture = new HDRCubeTexture(src, scene, 256, false, true, false, true);
      var skyboxMaterial = new BABYLON.StandardMaterial("skyBox", scene);
      skyboxMaterial.backFaceCulling = false;
      skyboxMaterial.reflectionTexture = texture;
      skyboxMaterial.reflectionTexture.coordinatesMode = BABYLON.Texture.SKYBOX_MODE;
      skyboxMaterial.diffuseColor = new BABYLON.Color3(1, 0, 0);
      skyboxMaterial.specularColor = new BABYLON.Color3(0, 1, 0);
      skyboxMaterial.disableLighting = true;
      var skybox = BABYLON.MeshBuilder.CreateBox(name, { size: camera.maxZ * 0.0125 }, scene);
      skybox.material = skyboxMaterial;
      skybox.visibility = 1;
      skybox.isPickable = false
      skyboxMaterial.freeze()
      skybox.doNotSyncBoundingInfo = true;
      skybox.convertToUnIndexedMesh();
    },

    prepareLighting: function () {
      const scene = this.scene
      // const camera = scene.activeCamera

      // gltf使用环境纹理，基于图像的光照 image-based-lighting（IBL）
      if (!scene.environmentTexture) {
        scene.environmentTexture = this.loadSkyboxPathTexture(scene)
      }
      if (scene.environmentTexture) {
        // scene.createDefaultSkybox(scene.environmentTexture, true, (camera.maxZ -camera.minZ) / 2, .3, false);
        this._lightBox = scene.createDefaultSkybox(scene.environmentTexture, true, Infinity, 0.3, false);
        this._lightBox.doNotSyncBoundingInfo = true;
        this._lightBox.convertToUnIndexedMesh()
      }
    },

    loadSkyboxPathTexture: function () {
      // let skyboxes = ["https://em3dviewer-beijing1.oss-cn-beijing.aliyuncs.com/3dTeam/2/1341614909305266176/test7_512.hdr"]
      // let skyboxes = ['environments/hy.hdr']
      const skyboxes = ['environments/environment.env']
      const file = skyboxes[0]
      if (file.indexOf(".hdr") === file.length - 4) {
          // 512->256, 可以减少2秒时长，效果肉眼无差异
          return new BABYLON.HDRCubeTexture(file, this.scene, 256, false, true, false, true)
      } else {
          return new BABYLON.CubeTexture.CreateFromPrefilteredData(file, this.scene)
      }
    },

    // 进入爆炸模式
    enterExplosionMode: function () {
      if (this.explosionStatus) return
      this.explosionStatus = true
      const min = 0, max = 3
      const step = (max - min) * 0.01
      const value = (max - min) / 2

      const that = this;
      this.execExplode(value, {
        type: 'easeIn',
        duration: 200
      })
    },

    // 执行爆炸：multiple为爆炸半径， animationConfig为动画配置，或者boolean值可选，
    // 可包含：type(类型，支持easeIn、easeOut、linear三种)、begin(开始半径, 如没有则从当前值开始)、duration(动画时长)
    // endCallback 完成后的回调
    execExplode: function (multiple, animationConfig, endCallback) {
      if (!this._explosion) {
        this._explosion = new MeshExploder(this.meshes);
      }

      // 停止以前的未完成的爆炸动画
      if (this._explosionTimer) {
        clearInterval(this._explosionTimer)
        this._explosionTimer = null
      }

      // 开始本次爆炸
      if (!animationConfig) { // 非动画，直接执行
        // console.warn(multiple)
        this._explosion.explode(multiple);
        this.explosionSliderValue = multiple

        endCallback && endCallback();
        // this._explosion.getMeshes()[0].unfreezeWorldMatrix() // 爆炸完成后释放？
        return;
      }

      // 动画时间函数、默认线性
      const timingFunction = this.timingFunction(animationConfig.type || 'linear')

      const that = this
      const stepInterval = 30 // 动画每次刷新步骤间的时间间隔，暂定30毫秒
      const begin = animationConfig.begin || this.explosionSliderValue || 0, end = multiple
      var duration = Math.ceil((animationConfig.duration || 200) / stepInterval) || 1, curtime = 1
      this._explosionTimer = setInterval(() => {
        const tempMultiple = timingFunction(curtime, begin, end, duration)
        // console.warn(tempMultiple)
        that._explosion.explode(tempMultiple)
        that.explosionSliderValue = tempMultiple
        curtime++
        // 动画结束
        if (Math.floor(curtime) > duration) {
          clearInterval(that._explosionTimer)
          that._explosionTimer = null
          
          that.explosionSliderValue = end

          that.meshes.forEach(mesh => {
            if (mesh._submeshesOctree) {
              mesh.createOrUpdateSubmeshesOctree(512, 2)
            }
          }) 

          endCallback && endCallback();
        }
      }, 30);

      that.explosionSliderValue = end // 先设置值（因为一些判断需要用到，如果等动画结束后在设定，可能会有影响，只能这样了（比如爆炸和剖切间的切换涉及到freeWorldMatrix）） 
    },

    // 动画时间函数：quad
    timingFunction: function (type) {
      if (type === 'easeIn') {
        return (curtime, begin, end, duration) => {
          const x = curtime / duration; // x值
          const y = x * x; // y值
          return begin + (end - begin) * y; // 套入最初的公式
        }
      }
      if (type === 'easeOut') {
        return (curtime, begin, end, duration) => {
          const x = curtime / duration; // x值
          const y = -x * x + 2 * x; // y值
          return begin + (end - begin) * y; // 套入最初的公式
        }
      }
      if (type === 'linear') {
        return (curtime, begin, end, duration) => {
          const x = curtime / duration; // x值
          return begin + (end - begin) * x; // 套入最初的公式
        }
      }
    },

    // 连接后端服务，获取眼镜 空间坐标和四元数信息
    initSocket () {
      const _that = this
      // 注意：下面 socket 连接的 IP 应为 python 起服务的 IP
      // _that.socket = new WebSocket(`ws:${window.location.hostname}:56789/slam`)
      _that.socket = new WebSocket(`ws:localhost:56789/slam`)
      _that.socket.addEventListener('open', function (event) {
        // _that.socket.send('Hello')
        Toast('socket 已连接！', 2000)
        if (_that.deviceDidconnectFlag) {
          _that.deviceDisconnect.hide()
          _that.deviceDidconnectFlag = false
        }
        if (_that.noServiceFlag) {
          _that.noService.hide()
          _that.noServiceFlag = false
        }
      })
      _that.socket.addEventListener('close', function (event) {
        // 连接出错/断开
        // _that.deviceDisconnect.init()
        if (!_that.noServiceFlag) {
          _that.noService.init()
          _that.noServiceFlag = true
        }
      })
      _that.socket.addEventListener('message', function (event) {
        _that.cameraData = event.data && JSON.parse(event.data)
        // 双目匹配中
        if (_that.loadFlag && _that.cameraData && _that.cameraData.length > 0) {
          _that.loadFlag = false
          _that.load.hide()
        } else if (!_that.loadFlag && ((_that.cameraData && _that.cameraData.length <= 0) || !_that.cameraData)) {
          _that.loadFlag = true
          _that.load.init()
        }

        // TODO 设备断开连接
      })
    },

    handleReset () {
        this.socket.send('reset')
        // 重新连接 socket
        setTimeout(() => {
          this.initSocket()
        }, 1000)
    },
    beforeDestroy () {
      this.socket = null
    }
  }
}
</script>

<style lang="scss">
.about {
  width: 100%;
  height: 100%;
  position: relative;
  background: #000;
  .explosion-btn {
    position: absolute;
    z-index: 999;
    top: 4vh;
    right: 4vw;
    width: 60px;
    height: 60px;
    font-size: 60px;
    line-height: 60px;
    color: chocolate;
    text-align: center;
  }
  .reset-btn {
    position: absolute;
    z-index: 999;
    top: 14vh;
    right: 4vw;
    width: 60px;
    height: 60px;
    font-size: 60px;
    line-height: 60px;
    color: red;
    text-align: center;
  }
  .explosion-btn, .reset-btn {
    .tips {
      position: absolute;
      font-size: 20px;
      width: 0;
      height: 0;
      opacity: 0;
    }
  } 
  .explosion-btn:hover, .reset-btn:hover {
    cursor: pointer;
    .tips {
      position: absolute;
      opacity: 1;
      width: 40px;
      height: 20px;
      line-height: 20px;
      font-size: 20px;
      color: #fff;
      left: -60px;
      top: 50%;
      transform: translateY(-50%);
    }
  }
  .explosion-active {
    color: #2560f3;
  }
}
canvas {
  width: 100%;
  height: 100%;
}
</style>
