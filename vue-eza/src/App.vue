<script setup>
import { RouterLink, RouterView, useRoute, useRouter } from 'vue-router'

import { reactive, ref } from 'vue'

const location = useRoute()
const router = useRouter()

// TODO: Get the allowed pages from the API
const pages = ref([
    { label: 'Home', icon: 'pi pi-home', route: '/' },
    { label: 'Charts', icon: 'pi pi-chart-line', route: '/chartsHome' },
    { label: 'Dashboards', icon: 'pi pi-qrcode', route: '/dashboards' },
    { label: 'Connections', icon: 'pi pi-database', route: '/connections' },
    { label: 'User Admin', icon: 'pi pi-users', route: '/users' },
    { label: 'Settings', icon: 'pi pi-cog', route: '/dashboards' },
]);
</script>

<template>
  <header class="p-2">
    <div class="flex flex-row justify-content-between pb-1">
      <div class="flex">
        <h1 id="site-title">EZAnalytics</h1>
      </div>
      <div class="justify-content-end">
        <span>Sign Out</span>
      </div>
    </div>
  </header>
  <div class="flex">
    <div>
      <!-- <Menubar :model="pages"> -->
        <Menu :model="pages">
        <template #item="{ item, props }">
            <router-link v-slot="{ href, navigate }" :to="item.route" custom>
                <a v-ripple :href="href" v-bind="props.action" @click="navigate">
                    <span :class="item.icon" />
                    <span class="ml-2">{{ item.label }}</span>
                </a>
            </router-link>
        </template>
      </Menu>
      <!-- </Menubar> -->
    </div>
    <div>
      <main class="p-2">
        <RouterView />
      </main>
    </div>
  </div>
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