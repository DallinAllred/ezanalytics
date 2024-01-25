<script setup>
import { RouterLink, RouterView, useRoute, useRouter } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'

import { reactive, ref } from 'vue'

const location = useRoute()
const router = useRouter()

// TODO: Get the allowed pages from the API
const pages = ref(['/', '/chartsHome', '/dashboards', '/connections', '/users'])
</script>

<template>
  <header class="row p-2 ">
    <div class="col-4">
      <div class="dropdown align-middle">
        <a class="nav-link dropdown-toggle" role="button" data-bs-toggle="dropdown" aria-expanded="false">
            {{ location.name }}
          </a>
        <ul class="dropdown-menu">
          <li v-for="(route, index) in router.options.routes" :key="index">
            <RouterLink v-if="pages.includes(route.path) && route.nav === true" :to="route.path" class="dropdown-item">{{ route.name }}</RouterLink>
          </li>
        </ul>
      </div>
    </div>
    <div class="col-4 text-center">
      <h1 id="site-title">EZAnalytics</h1>
    </div>
    <div class="col-4 text-end">User Settings</div>
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
