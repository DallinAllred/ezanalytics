<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { FilterMatchMode } from 'primevue/api' 
import axios from '@/axiosConfig'

const emit = defineEmits('updateApp')
const router = useRouter()

const currentUser = ref(JSON.parse(localStorage.getItem('eza-user')) ?? {})
const showLogin = ref(false)
const loginTitle = ref('Session Timed Out')

const chartFilters = ref({
    global: { value: null, matchMode: FilterMatchMode.CONTAINS }
})
const dashFilters = ref({
    global: { value: null, matchMode: FilterMatchMode.CONTAINS }
})

const ownedCharts = ref([])
const ownedDashboards = ref([])
const selectedChart = ref({title: null, id: null})
const selectedDash = ref({title: null, id: null})

async function loadItems() {
    if (!currentUser.value.username) {
        currentUser.value = JSON.parse(localStorage.getItem('eza-user')) ?? {}
        if (!currentUser.value?.username) {
            loginTitle.value = null
            showLogin.value = true
            return
        }
    }
    loginTitle.value = 'Session Timed Out'
    try {
        let response = await axios.get(`/api/charts?user=${currentUser.value['user_id']}`)
        ownedCharts.value = response.data
        response = await axios.get(`/api/dashboards?user=${currentUser.value['user_id']}`)
        ownedDashboards.value = response.data
    } catch (err) {
        if (err.response?.status === 401) { showLogin.value = true}
        console.log(err)
    }
}

function viewCharts() {
    router.push('/chartsHome')
}
function buildChart() {
    router.push('/chartBuilder')
}
function viewDashboards() {
    router.push('/dashboards')
}
function buildDash() {
    router.push('/dbBuilder')
}

watch(selectedChart, () => {
    router.push(`/chartsHome?chart=${selectedChart.value.id}`)
})

watch(selectedDash, () => {
    router.push(`/dashboards?dash=${selectedDash.value.id}`)
})

onMounted(async () => {
    loadItems()
})
</script>

<template>
    <div class="h-full">
        <div v-if="!(currentUser.admin || currentUser.viewer)" class="flex p-3">
            <Unauthorized />
        </div>
        <div v-else class="grid flex h-full p-2 justify-content-around">
            <Splitter class="h-full" style="width: 45vw">
                <SplitterPanel class="flex pl-2" :size="65" :minSize="65">
                    <DataTable class="h-full w-full" v-model:selection="selectedChart" v-model:filters="chartFilters" stripedRows
                    :value="ownedCharts" selectionMode="single" scrollable scrollHeight="100%" dataKey="id">
                    <!-- <template #header>
                        <div class="flex justify-content-start">
                            <span class="p-input-icon-left">
                                <i class="pi pi-search" />
                                <InputText v-model="chartFilters['global'].value" placeholder="Search Charts" />
                            </span>
                        </div>
                    </template> -->
                    <Column field="title" header="My Charts">
                        <template #body="slotProps">
                            <div>{{ slotProps.data.title }}</div>
                            <small>{{ slotProps.data.id }}</small>
                        </template>
                    </Column>
                    </DataTable>
                </SplitterPanel>
                <SplitterPanel class="flex align-items-center justify-content-center px-2" :size="35" :minSize="35">
                    <div class="flex flex-column gap-5">
                        <Button class="home-nav-btn" label="View All Charts" @click="viewCharts" />
                        <Button class="home-nav-btn" icon="pi pi-plus" label="Build a Chart" @click="buildChart" :disabled="!(currentUser.admin || currentUser['chart_builder'])" />
                    </div>
                </SplitterPanel>
            </Splitter>

            <Splitter class="h-full" style="width: 45vw">
                <SplitterPanel class="flex pl-2" :size="65" :minSize="65">
                    <DataTable class="h-full w-full" v-model:selection="selectedDash" v-model:filters="dashFilters" stripedRows
                    :value="ownedDashboards" selectionMode="single" scrollable scrollheight="100%" dataKey="id">
                        <!-- <template #header>
                            <div class="flex justify-content-start">
                                <span class="p-input-icon-left">
                                    <i class="pi pi-search" />
                                    <InputText v-model="dashFilters['global'].value" placeholder="Search Dashboards" />
                                </span>
                            </div>
                        </template> -->
                        <Column header="My Dashboards">
                            <template #body="slotProps">
                                <div>{{ slotProps.data.title }}</div>
                                <small>{{ slotProps.data.id }}</small>
                            </template>
                        </Column>
                    </DataTable>
                </SplitterPanel>
                <SplitterPanel class="flex align-items-center justify-content-center px-2" :size="35" :minSize="35">
                    <div class="flex flex-column gap-5">
                        <Button class="home-nav-btn" label="View All Dashboards" @click="viewDashboards" />
                        <Button class="home-nav-btn" icon="pi pi-plus" label="Build a Dashboard" @click="buildDash" :disabled="!(currentUser.admin || currentUser['dash_builder'])" />
                    </div>
                </SplitterPanel>
            </Splitter>
        </div>
        <Login v-model="showLogin" :title="loginTitle" @login="showLogin = false; loadItems(); emit('updateApp')"></Login>
    </div>
</template>

<style>
</style>
