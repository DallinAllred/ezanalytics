<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import axios from '@/axiosConfig'

const emit = defineEmits('updateApp')
const router = useRouter()

const currentUser = ref(JSON.parse(localStorage.getItem('eza-user')) ?? {})
const showLogin = ref(false)
const loginTitle = ref('Session Timed Out')

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
        console.log(response.data)
        response = await axios.get(`/api/dashboards?user=${currentUser.value['user_id']}`)
        ownedDashboards.value = response.data
    } catch (err) {
        if (err.response?.status === 401) { showLogin.value = true}
        console.log(err)
    }
}

function viewCharts() {
    console.log('View Charts')
    router.push('/chartsHome')
}
function buildChart() {
    console.log('Build Chart')
    router.push('/chartBuilder')
}
function viewDashboards() {
    console.log('View Dashboards')
    router.push('/dashboards')
}
function buildDash() {
    console.log('Build Dashboard')
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
    <div>
        <div v-if="!(currentUser.admin || currentUser.viewer)" class="flex p-3">
            <Unauthorized />
        </div>
        <div v-else class="flex justify-content-around">
            <div class="flex gap-8">
                <DataTable v-model:selection="selectedChart" :value="ownedCharts" selectionMode="single"
                scrollable class="h-full" dataKey="id" tableStyle="min-width: 20rem; max-height: calc(100vh - 6.5rem)">
                <Column header="My Charts">
                    <template #body="slotProps">
                        <div>{{ slotProps.data.title }}</div>
                        <small>{{ slotProps.data.id }}</small>
                    </template>
                </Column>
                </DataTable>
                <div class="flex flex-column gap-5">
                    <Button class="home-nav-btn" label="View All Charts" @click="viewCharts" />
                    <Button class="home-nav-btn" icon="pi pi-plus" label="Build a Chart" @click="buildChart" :disabled="!(currentUser.admin || currentUser['chart_builder'])" />
                </div>
            </div>
            <div class="flex gap-8">
                <DataTable v-model:selection="selectedDash" :value="ownedDashboards" selectionMode="single"
                scrollable class="h-full" dataKey="id">
                    <Column header="My Dashboards">
                        <template #body="slotProps">
                            <div>{{ slotProps.data.title }}</div>
                            <small>{{ slotProps.data.id }}</small>
                        </template>
                    </Column>
                </DataTable>
                <div class="flex flex-column gap-5">
                    <Button class="home-nav-btn" label="View All Dashboards" @click="viewDashboards" />
                    <Button class="home-nav-btn" icon="pi pi-plus" label="Build a Dashboard" @click="buildDash" :disabled="!(currentUser.admin || currentUser['dash_builder'])" />
                </div>
            </div>
        </div>
        <Login v-model="showLogin" :title="loginTitle" @login="showLogin = false; loadItems(); emit('updateApp')"></Login>
    </div>
</template>

<style>
.home-nav-btn {
    /* width: 150px;
    height: 150px; */
}
</style>