<script setup>
import { RouterLink, RouterView, useRoute, useRouter } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'

import { reactive, ref } from 'vue'

const location = useRoute()
const router = useRouter()

console.log(router.options.routes)


// TODO: Get the allowed pages from the API
const dataPages = ref(['/', '/chartsHome', '/dashboards'])
const adminPages = ref(['/connections', '/users'])
</script>

<template>
  <header class="row p-2 ">
    <div class="col-4 d-flex align-items-end">
      <div v-for="(route, index) in router.options.routes" :key="index" class="m-2">
        <RouterLink v-if="dataPages.includes(route.path) && route.nav === true" :to="route.path" class="nav-link">{{ route.name }}</RouterLink>
      </div>

          <!-- <div class="m-2"><RouterLink to="/" class="nav-link active">Home</RouterLink></div>
          <div class="m-2"><RouterLink to="/chartsHome" class="nav-link">Charts</RouterLink></div>
          <div class="m-2"><RouterLink to="/dashboards" class="nav-link">Dashboards</RouterLink></div> -->
    </div>
    <div class="col-4 text-center">
      <h1 id="site-title">EZAnalytics</h1>
    </div>
    <div class="col-4 d-flex align-items-end justify-content-end">
          <div class="m-2"><RouterLink to="/connections" class="nav-link">Connections</RouterLink></div>
          <div class="m-2"><RouterLink to="/users" class="nav-link">User Manager</RouterLink></div>
          <div class="m-2"><a class="nav-link">Settings</a></div>
    </div>
  </header>
  <main>
      <RouterView />
  </main>
</template>

<style>
header {
    background-color: var(--color-accent);
}

#site-title {
  font-family: gruppo;
  font-weight: 600
}
</style>


      <!-- <div class="dropdown align-middle">
        <a class="nav-link dropdown-toggle" role="button" data-bs-toggle="dropdown" aria-expanded="false">
            {{ location.name }}
          </a>
        <ul class="dropdown-menu">
          <li v-for="(route, index) in router.options.routes" :key="index">
            <RouterLink v-if="pages.includes(route.path) && route.nav === true" :to="route.path" class="dropdown-item">{{ route.name }}</RouterLink>
          </li>
        </ul>
      </div> -->
      <!-- <ul class="nav nav-pills">
        <li class="nav-item">
          <RouterLink to="/" class="nav-link active">Home</RouterLink>
        </li>
        <li class="nav-item">
          <RouterLink to="/chartsHome" class="nav-link">Charts</RouterLink>
        </li>
        <li class="nav-item">
          <RouterLink to="/dashboards" class="nav-link">Dashboards</RouterLink>
        </li>
      </ul>
    </div>
    <div class="col-4 text-center">
      <h1 id="site-title">EZAnalytics</h1>
    </div>
    <div class="col-4 text-end">
      <ul class="nav nav-pills">
        <li class="nav-item">
          <RouterLink to="/connections" class="nav-link">Connections</RouterLink>
        </li>
        <li class="nav-item">
          <RouterLink to="/users" class="nav-link">User Manager</RouterLink>
        </li>
        <li class="nav-item">
          <a class="nav-link">Settings</a>
        </li>
      </ul> -->