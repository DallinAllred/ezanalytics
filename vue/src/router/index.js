import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: HomeView,
      nav: true,
      permissions: 'viewer'
    },{
      path: '/chartsHome',
      name: 'Charts',
      component: () => import('../views/ChartsHome.vue'),
      nav: true,
      permissions: 'viewer'
    },{
      path: '/chartBuilder',
      name: 'Chart Builder',
      component: () => import('../views/ChartBuilder.vue'),
      permissions: 'chart_builder'
    },{
      path: '/dashboards',
      name: 'Dashboards',
      component: () => import('../views/Dashboards.vue'),
      nav: true,
      permssions: 'viewer'
    },{
      path: '/dbBuilder',
      name: 'DB Builder',
      component: () => import('../views/DBBuilder.vue'),
      permissions: 'dash_builder'
    },{
      path: '/connections',
      name: 'Connections',
      component: () => import('../views/Connections.vue'),
      nav: true,
      permissions: 'connections'
    },{
      path: '/users',
      name: 'User Admin',
      component: () => import('../views/Users.vue'),
      nav: true,
      permissions: 'admin'
    },{
      path: '/settings',
      name: 'Settings',
      component: () => import('../views/Settings.vue'),
      permissions: 'viewer'
    },{
      path: '/login',
      name: 'Login',
      component: () => import('../views/Login.vue')
    }
  ]
})

router.beforeEach((to, from) => {
  const permissions = {
    Home: 'viewer',
    Charts: 'viewer',
    Dashboards: 'viewer',
    'Chart Builder': 'chart_builder',
    'DB Builder': 'dash_builder',
    Connections: 'connections',
    Users: 'admin',
    Settings: 'viewer'
  }
  let currentUser = JSON.parse(localStorage.getItem('eza-user'))
  // console.log(currentUser)
  // console.log(currentUser.admin)
  // console.log(to.name, permissions[to.name])
  if (!(currentUser.admin ||
    to.name === 'Login' ||
    currentUser[permissions[to.name]])) return false
})

export default router
