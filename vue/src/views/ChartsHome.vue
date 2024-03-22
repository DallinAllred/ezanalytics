<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import axios from '@/axiosConfig'
import EZChart from '@/components/EZChart.vue'

const emit = defineEmits('updateApp')
const route = useRoute()
const router = useRouter()
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

watch(selectedChart, () => {
    if (selectedChart.value.id) {
        let query = {'chart': selectedChart.value.id}
        router.replace({ path: route.path, query: query})
    }
})

onMounted(async () => {
    await loadPage()
})
</script>

<template>
    <div>
        <div v-if="!(currentUser.admin || currentUser.viewer)" class="flex p-3">
            <Unauthorized />
        </div>
        <div v-else>
            <Toolbar class="mb-2">
                <template #start>
                    <Button :disabled="!editor" icon="pi pi-plus" label="New Chart" @click="newChart" />
                </template>
                <template #center>
                    <Dropdown v-model="selectedChart" :options="chartList" filter optionLabel="title" placeholder="Select a Chart">
                        <template #value="slotProps">
                            <div v-if="slotProps.value.title" class="flex">
                                <div>{{ slotProps.value.title }} ({{ slotProps.value.id }})</div>
                            </div>
                            <div v-else>
                                {{ slotProps.placeholder }}
                            </div>
                        </template>
                        <template #option="slotProps">
                            <div class="flex flex-column">
                                <div>{{ slotProps.option.title }}</div>
                                <small>{{ slotProps.option.id }}</small>
                            </div>
                        </template>
                    </Dropdown>
                </template>
                <template #end>
                    <div class="flex gap-2">
                        <Button :disabled="!editor || !(selectedChart && selectedChart.id)" icon="pi pi-pencil" label="Edit Chart" @click="editChart" />
                        <Button :disabled="!editor || !(selectedChart && selectedChart.id)" severity="danger" icon="pi pi-times" label="Delete Chart" @click="deleteChartDialog = true" />
                    </div>
                </template>
            </Toolbar>
            <div id="chart-container">
                <EZChart v-if="selectedChart && selectedChart.id" v-model="selectedChart.id" height="100%" @timeout401="showLogin = true"></EZChart>
            </div>
            <ConfirmDelete v-model="deleteChartDialog" :match="selectedChart.title" @delete="deleteChart"></ConfirmDelete>
        </div>
        <Login v-model="showLogin" :title="loginTitle" @login="showLogin = false; loadPage(); emit('updateApp')"></Login>
    </div>
</template>

<style>
#chart-container {
    /* height: calc(100vh - 4.5rem); */
    height: calc(100vh - 10rem);
}
canvas {
    /* max-height: calc(100vh - 4.5rem - 6rem) !important; */
    max-height: calc(100vh - 10rem) !important;
}
</style>