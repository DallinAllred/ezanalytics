<script setup>
import { RouterLink, RouterView, useRoute, useRouter } from 'vue-router'
import { computed, onMounted, ref, watch } from 'vue'
import Toast from 'primevue/toast'

const location = useRoute()
const router = useRouter()

const activePage = ref()

const pageList = [
  { label: 'Home', icon: 'pi pi-home', route: '/', permissions: 'viewer' },
  { label: 'Charts', icon: 'pi pi-chart-line', route: '/chartsHome', permissions: 'viewer' },
  { label: 'Dashboards', icon: 'pi pi-qrcode', route: '/dashboards', permissions: 'viewer' },
  { label: 'Connections', icon: 'pi pi-database', route: '/connections', permissions: 'connections' },
  { label: 'User Admin', icon: 'pi pi-users', route: '/users', permissions: 'admin' },
  { label: 'Settings', icon: 'pi pi-cog', route: '/settings', permissions: 'viewer' }
]

const pages = ref(pageList)
// const pages = ref([
//   { label: 'Home', icon: 'pi pi-home', route: '/', permissions: 'viewer' },
//   { label: 'Charts', icon: 'pi pi-chart-line', route: '/chartsHome', permissions: 'viewer' },
//   { label: 'Dashboards', icon: 'pi pi-qrcode', route: '/dashboards', permissions: 'viewer' },
//   { label: 'Connections', icon: 'pi pi-database', route: '/connections', permissions: 'connections' },
//   { label: 'User Admin', icon: 'pi pi-users', route: '/users', permissions: 'admin' },
//   { label: 'Settings', icon: 'pi pi-cog', route: '/settings', permissions: 'viewer' }
// ]);

const pageWatcher = computed(() => {
  return pages.value.findIndex(page => page.route === location.path)
})
watch(pageWatcher, () => {
  let index = pages.value.findIndex(page => page.route === location.path)
  activePage.value = index
  let currentUser = JSON.parse(localStorage.getItem('eza-user')) ?? {}
  pages.value = pageList.filter(page => {
    return (currentUser.admin || currentUser[page.permissions])
  })
})

const loginPage = computed(() => location.path == '/login' )

function signout() { router.push('/login') }

onMounted(() => {
  let currentUser = JSON.parse(localStorage.getItem('eza-user')) ?? {}
  pages.value = pageList.filter(page => {
    return (currentUser.admin || currentUser[page.permissions])
  })
})
</script>

<template>
  <Toast />
  <div class="h-full">
    <header class="p-2">
      <div class="flex flex-row justify-content-between pb-1">
        <div class="flex flex-row gap-2">
          <div class="flex">
            <span id="site-title" class="text-6xl">EZAnalytics</span>
          </div>
          <div v-if="!loginPage">
            <TabMenu :model="pages" v-model:activeIndex="activePage">
              <template #item="{ item, props }">
                <router-link v-slot="{ href, navigate }" :to="item.route" custom>
                  <a :href="href" v-bind="props.action" @click="navigate">
                    <span :class="item.icon" />
                    <span class="ml-2">{{ item.label }}</span>
                  </a>
                </router-link>
              </template>
            </TabMenu>
          </div>
        </div>
        <div class="justify-content-end">
        <Button v-if="!loginPage" label="Sign Out" text @click="signout()" />
        </div>
      </div>
    </header>
    <main class="p-2 w-12">
      <RouterView />
    </main>
  </div>
</template>

<style>
header {
  height: 4.5rem;
}
main {
  height: calc(100vh - 4.5rem);
}
#site-title {
  font-family: gruppo;
}
</style>