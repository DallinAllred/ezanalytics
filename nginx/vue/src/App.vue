<script setup>
import { RouterLink, RouterView, useRoute, useRouter } from 'vue-router'
import { computed, onMounted, ref, watch } from 'vue'
import Toast from 'primevue/toast'

const emit = defineEmits('updateApp')
const location = useRoute()
const router = useRouter()

const activePage = ref()
const currentUser = ref({})
const userMenu = ref()
const userMenuItems = ref([{
  items: [
    {
      label: 'Account Settings',
      icon: 'pi pi-cog',
      command: () => router.push('/settings')
    },{
      label: 'Sign Out',
      icon: 'pi pi-sign-out',
      command: () => router.push('/login')
    }
  ]
}])

const pageList = [
  { label: 'Home', icon: 'pi pi-home', route: '/', permissions: 'viewer' },
  { label: 'Charts', icon: 'pi pi-chart-line', route: '/chartsHome', permissions: 'viewer' },
  { label: 'Dashboards', icon: 'pi pi-qrcode', route: '/dashboards', permissions: 'viewer' },
  { label: 'Data Sources', icon: 'pi pi-database', route: '/connections', permissions: 'connections' },
  { label: 'User Admin', icon: 'pi pi-users', route: '/users', permissions: 'admin' }
]

const pages = ref(pageList)

watch(() => location.path, () => {
  let index = pages.value.findIndex(page => page.route === location.path)
  activePage.value = index
})

const loginPage = computed(() => location.path == '/login' )

const toggle = (event) => {
  userMenu.value.toggle(event)
}

function updateNav() {
  currentUser.value = JSON.parse(localStorage.getItem('eza-user')) ?? {}
  pages.value = pageList.filter(page => {
    return (currentUser.value.admin || currentUser.value[page.permissions])
  })
}

onMounted(() => {
  updateNav()
})
</script>

<template>
  <Toast />
  <div class="h-full">
    <header class="p-2">
      <div class="flex flex-row gap-2 justify-content-between">
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
        <div class="justify-content-end">
          <Button v-if="!loginPage" :label="currentUser.username ? currentUser.username : 'Sign In'" icon="pi pi-user" text @click="toggle" />
          <Menu ref="userMenu" id="overlay_menu" :model="userMenuItems" :popup="true" />
        </div>
      </div>
    </header>
    <main class="p-2 w-12">
      <RouterView @updateApp="updateNav" />
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