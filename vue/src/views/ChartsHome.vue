<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import axios from '@/axiosConfig'
import EZChart from '@/components/EZChart.vue'

const router = useRouter()
const route = useRoute()
const toast = useToast()

const currentUser = ref(JSON.parse(localStorage.getItem('eza-user')) ?? {})
const deleteChartDialog = ref(false)
const showLogin = ref(false)
const loginTitle = ref('Session Timed Out')

const chartList = ref([])
const selectedChart = ref({title: null, id: null})

const editor = computed(() => {
    if (currentUser.value.admin || currentUser.value['chart_builder']) return true
    return false
})

async function loadPage() {
    if (!currentUser.value.username) {
        currentUser.value = JSON.parse(localStorage.getItem('eza-user')) ?? {}
        if (!currentUser.value?.username) {
            loginTitle.value = null
            showLogin.value = true
            return
        }
    }
    loginTitle.value = 'Session Timed Out'
    await loadCharts()
    if ('chart' in route.query){
        let queryChart = chartList.value.filter(chart => chart.id == route.query.chart)
        selectedChart.value = queryChart[0]
    }
}

async function loadCharts() {
    try {
        let response = await axios.get(`/api/charts`)
        chartList.value = response.data
    } catch (err) {
        if (err.response?.status === 401) {
            showLogin.value = true
        }
    }
}

function newChart() {
    router.push('/chartBuilder')
}

function editChart() {
    if (selectedChart.value) {
        router.push(`/chartBuilder?chart=${selectedChart.value.id}`)
    }
}

async function deleteChart() {
    try {
        let response = await axios.delete(`/api/charts/${selectedChart.value.id}`)
        deleteChartDialog.value = false
        toast.add({severity: 'success', summary: 'Success', detail: `Chart "${selectedChart.value.title}" has been deleted`, life: 3000})
        selectedChart.value = {title: null, id: null}
        loadCharts()
    } catch (err) {
        if (err.response?.status === 401) {
            showLogin.value = true
            return
        }
        toast.add({severity: 'error', summary: 'Error', detail: `Error while deleting "${selectedChart.value.title}"`, life: 3000})
    }
}

onMounted(async () => {
    await loadPage()
})

</script>

<template>
    <div v-if="!(currentUser.admin || currentUser.viewer)" class="flex p-3">
        <Unauthorized />
    </div>
    <div v-else class="grid h-full">
        <div class="col-2 flex flex-column gap-2">
            <div class="h-full">
                <DataTable v-model:selection="selectedChart" :value="chartList" selectionMode="single"
                scrollable class="h-full" dataKey="id">
                    <Column field="title" header="Chart"></Column>
                    <Column field="id" header="ID"></Column>
                </DataTable>
            </div>
            <Button :disabled="!editor" label="New Chart" @click="newChart" />
        </div>
        <div class="col-10 flex flex-column gap-5" id="chart-container">
            <div class="flex justify-content-between">
                <Button :disabled="!editor" severity="danger" label="Delete Chart" @click="deleteChartDialog = true" v-if="selectedChart && selectedChart.id" />
                <Button :disabled="!editor" label="Edit Chart" @click="editChart" v-if="selectedChart && selectedChart.id" />
            </div>
            <EZChart v-if="selectedChart && selectedChart.id" v-model="selectedChart.id" height="100%" @timeout401="showLogin = true"></EZChart>
        </div>
        <ConfirmDelete v-model="deleteChartDialog" :match="selectedChart.title" @delete="deleteChart"></ConfirmDelete>
    </div>
    <Login v-model="showLogin" :title="loginTitle" @login="showLogin = false; loadPage()"></Login>
</template>

<style>
#chart-container {
    height: calc(100vh - 4.5rem)
}
canvas {
    max-height: calc(100vh - 4.5rem - 6rem) !important;
}
</style>