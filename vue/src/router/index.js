import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: HomeView,
    },{
      path: '/chartsHome',
      name: 'Charts',
      component: () => import('../views/ChartsHome.vue'),
    },{
      path: '/chartBuilder',
      name: 'Chart Builder',
      component: () => import('../views/ChartBuilder.vue'),
    },{
      path: '/dashboards',
      name: 'Dashboards',
      component: () => import('../views/Dashboards.vue'),
    },{
      path: '/dbBuilder',
      name: 'DB Builder',
      component: () => import('../views/DBBuilder.vue'),
    },{
      path: '/connections',
      name: 'Connections',
      component: () => import('../views/Connections.vue'),
    },{
      path: '/users',
      name: 'User Admin',
      component: () => import('../views/Users.vue'),
    },{
      path: '/settings',
      name: 'Settings',
      component: () => import('../views/Settings.vue'),
    },{
      path: '/login',
      name: 'Login',
      component: () => import('../views/Login.vue'),
    }
  ]
})

export default router
