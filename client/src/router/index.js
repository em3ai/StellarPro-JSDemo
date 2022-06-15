/*
 * @Date: 2022-05-19 10:35:55
 * @LastEditTime: 2022-06-10 17:05:05
 * @Description: Modify here please
 * @FilePath: /slam-babylonjs/src/router/index.js
 */
import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/slam',
    name: 'Slam',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/Slam.vue')
  },
  { path: '*', redirect: '/', hidden: true }
]

const router = new VueRouter({
  routes
})

export default router
