<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

import { useToast } from 'primevue/usetoast'

import ConfirmDelete from '@/components/dialogs/ConfirmDelete.vue'
import EZChart from '@/components/EZChart.vue'

const router = useRouter()
const route = useRoute()
const toast = useToast()

const deleteChartDialog = ref(false)
const chartList = ref([])
const selectedChart = ref({title: null, id: null})

async function loadCharts() {
    let response = await axios.get(`http://localhost:5050/api/charts`)
    chartList.value = response.data
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
        let response = await axios.delete(`http://localhost:5050/api/charts/${selectedChart.value.id}`)
        console.log(response)
        deleteChartDialog.value = false
        toast.add({severity: 'success', summary: 'Success', detail: `Chart "${selectedChart.value.title}" deleted`, life: 3000})
        selectedChart.value = {title: null, id: null}
        loadCharts()
    } catch {
        toast.add({severity: 'error', summary: 'Error', detail: `Error while deleting "${selectedChart.value.title}"`, life: 3000})
    }
}

onMounted(async () => {
    await loadCharts()
    if ('chart' in route.query){
        let queryChart = chartList.value.filter(chart => chart.id == route.query.chart)
        selectedChart.value = queryChart[0]
    }
})

</script>

<template>
    <div class="grid h-full">
        <div class="col-2 flex flex-column gap-2">
            <div class="h-full">
                <DataTable v-model:selection="selectedChart" :value="chartList" selectionMode="single"
                scrollable class="h-full" dataKey="id">
                    <Column field="title" header="Chart"></Column>
                    <Column field="id" header="ID"></Column>
                </DataTable>
            </div>
            <Button label="New Chart" @click="newChart" />
        </div>
        <div class="col-10 flex flex-column gap-5" id="chart-container">
            <div class="flex justify-content-between">
                <Button severity="danger" label="Delete Chart" @click="deleteChartDialog = true" v-if="selectedChart && selectedChart.id" />
                <Button label="Edit Chart" @click="editChart" v-if="selectedChart && selectedChart.id" />
            </div>
            <EZChart v-if="selectedChart && selectedChart.id" v-model="selectedChart.id" height="100%"></EZChart>
        </div>
    </div>
    <ConfirmDelete v-model="deleteChartDialog" :match="selectedChart.title" @delete="deleteChart"></ConfirmDelete>
</template>

<style>
#chart-container {
    height: calc(100vh - 4.5rem)
}
canvas {
    max-height: calc(100vh - 4.5rem - 6rem) !important;
}
</style>