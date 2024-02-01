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
  <header class="m-2">
    <div class="flex flex-row justify-content-between pb-1">
      <div class="flex">
        <span id="site-title" class="text-6xl">EZAnalytics</span>
      </div>
      <div>
        <TabMenu :model="pages">
          <template #item="{ item, props }">
              <router-link v-slot="{ href, navigate }" :to="item.route" custom>
                  <a v-ripple :href="href" v-bind="props.action" @click="navigate">
                      <span :class="item.icon" />
                      <span class="ml-2">{{ item.label }}</span>
                  </a>
              </router-link>
          </template>
        </TabMenu>
      </div>

      <div class="justify-content-end">
        <span>Sign Out</span>
      </div>
    </div>
  </header>
  <div class="flex">
    <!-- <div class="w-2"> -->
      <!-- <Menubar :model="pages"> -->
      <!-- <Menu :model="pages">
        <template #item="{ item, props }">
            <router-link v-slot="{ href, navigate }" :to="item.route" custom>
                <a v-ripple :href="href" v-bind="props.action" @click="navigate">
                    <span :class="item.icon" />
                    <span class="ml-2">{{ item.label }}</span>
                </a>
            </router-link>
        </template>
      </Menu> -->
      <!-- </Menubar> -->
    <!-- </div> -->
    <!-- <div class="w-10"> -->
      <main class="m-1 p-2 w-12">
        <RouterView />
      </main>
    <!-- </div> -->
  </div>
</template>

<style>
header {
    background-color: var(--color-accent);
}

#site-title {
  font-family: gruppo;
  /* font-weight: 600 */
}
</style>