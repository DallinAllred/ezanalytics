<script setup>
import { onMounted, ref, reactive, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

import EZChart from '@/components/EZChart.vue'

const router = useRouter()

const route = useRoute()

const chartList = ref([])
const selectedChart = ref(null)

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

function deleteChart() {
    console.log('Deleting chart')
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
                <Button severity="danger" label="Delete Chart" @click="deleteChart" v-if="selectedChart && selectedChart.id" />
                <Button label="Edit Chart" @click="editChart" v-if="selectedChart && selectedChart.id" />
            </div>
            <EZChart v-if="selectedChart && selectedChart.id" v-model="selectedChart.id" height="100%"></EZChart>
        </div>
    </div>
</template>

<style>
#chart-container {
    height: calc(100vh - 4.5rem)
}
canvas {
    max-height: calc(100vh - 4.5rem - 6rem) !important;
}
</style>