/*
 * @Date: 2022-05-19 10:35:55
 * @LastEditTime: 2022-07-01 14:08:14
 * @Description: Modify here please
 * @FilePath: /StellarPro-JSDemo/client/src/router/index.js
 */
import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Slam from '../views/Slam.vue'
Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  // {
  //   path: '/',
  //   name: 'Slam',
  //   component: Slam
  // },
  { path: '*', redirect: '/', hidden: true }
]

const router = new VueRouter({
  routes
})

export default router
