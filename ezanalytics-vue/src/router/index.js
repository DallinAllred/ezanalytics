import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },{
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    },{
      path: '/chartsHome',
      name: 'charts',
      component: () => import('../views/ChartsHome.vue')
    },{
      path: '/chartBuilder',
      name: 'chartBuilder',
      component: () => import('../views/ChartBuilder.vue')
    },{
      path: '/dashboards',
      name: 'dashBoards',
      component: () => import('../views/Dashboards.vue')
    },{
      path: '/dbBuilder',
      name: 'dbBuilder',
      component: () => import('../views/DBBuilder.vue')
    },{
      path: '/users',
      name: 'users',
      component: () => import('../views/Users.vue')
    }
  ]
})

export default router
