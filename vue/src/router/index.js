import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
// import Users from '../views/Users.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: HomeView,
      nav: true
    },
    // {
    //   path: '/chartsHome',
    //   name: 'Charts',
    //   component: () => import('../views/ChartsHome.vue'),
    //   nav: true
    // },{
    //   path: '/chartBuilder',
    //   name: 'Chart Builder',
    //   component: () => import('../views/ChartBuilder.vue')
    // },{
    //   path: '/dashboards',
    //   name: 'Dashboards',
    //   component: () => import('../views/Dashboards.vue'),
    //   nav: true
    // },{
    //   path: '/dbBuilder',
    //   name: 'DB Builder',
    //   component: () => import('../views/DBBuilder.vue')
    // },{
    //   path: '/connections',
    //   name: 'Connections',
    //   component: () => import('../views/Connections.vue'),
    //   nav: true
    // },
    {
      path: '/users',
      name: 'User Admin',
      // component: Users,
      component: () => import('../views/Users.vue'),
      nav: true
    },
    // {
    //   path: '/settings',
    //   name: 'Settings',
    //   component: () => import('../views/Settings.vue')
    // }
  ]
})

export default router
