<script setup>
import axios from '@/axiosConfig'
import { reactive, ref, onMounted, watch } from "vue"

import { useToast } from 'primevue/usetoast'

const model = defineModel()
const props = defineProps(['height', 'width'])

const toast = useToast()

const documentStyle = getComputedStyle(document.documentElement)

const validChart = ref(true)

const rawData = ref()
const dataSource = ref()
const chartType = ref({name: 'Bar', tag: 'bar'})

const xAxis = ref()
const yAxisL = ref([])
const yAxisR = ref([])
const groupBy = ref()

const backgroundColors = ['rgba(249, 115, 22, 0.5)', 'rgba(6, 182, 212, 0.5)', 'rgb(107, 114, 128, 0.5)', 'rgba(139, 92, 246, 0.5)']
const borderColors = ['rgb(249, 115, 22)', 'rgb(6, 182, 212)', 'rgb(107, 114, 128)', 'rgb(139, 92, 246)']

const chartData = reactive({labels: [], datasets: []})
const chartOptions = reactive({
    maintainAspectRation: false,
    responsive: true,
    plugins: {
        legend: {
            labels: { color: documentStyle.getPropertyValue('--text-color') }
        }
    },
    scales: {
        x: {
            stacked: false,
            ticks: { color: documentStyle.getPropertyValue('--text-color-secondary') },
            grid: { color: documentStyle.getPropertyValue('--surface-border') },
        },
        y: {
            beginAtZero: true,
            stacked: false,
            ticks: { color: documentStyle.getPropertyValue('--text-color-secondary') },
            grid: { color: documentStyle.getPropertyValue('--surface-border') },
        }
    }
})

async function getData() {
    let response = await axios.get(`/api/sources/${dataSource.value.sourceId}`)
    let data = response.data
    rawData.value = data
}

async function loadChart(chartId) {
    let chart = {}
    try {
        let response = await axios.get(`/api/charts/${chartId}`)
        chart = response.data
    } catch {
        toast.add({severity: 'error', summary: 'Chart Not Found', detail: `Unable to find chart ${chartId}`, life: 3000})
        return
    }

    dataSource.value = chart.sourceId
    await getData()
    chartType.value = chart.type
    xAxis.value = chart.data.xAxis
    yAxisL.value = chart.data.yAxisL
    yAxisR.value = chart.data.yAxisR ?? null
    groupBy.value = chart.groupBy ?? null
    chartOptions.plugins.title = {
        display: true,
        text: chart.title
    }
    chartOptions.scales.x.stacked = chart.options.stacked
    chartOptions.scales.y.stacked = chart.options.stacked
    chartOptions.scales.x.title = {
        display: true,
        text: chart.data.xAxis
    }
    chartOptions.scales.y.title = {
        display: true,
        text: chart.data.yAxisL
    }
    if (yAxisR.value) {
        chartOptions.scales.y1 = {
            beginAtZero: true,
            position: 'right',
            ticks: { color: documentStyle.getPropertyValue('--text-color-secondary') },
            grid: { color: documentStyle.getPropertyValue('--surface-border') },
        }
        chartOptions.scales.y1.stacked = chart.options.stacked
        chartOptions.scales.y1.title = {
        display: true,
        text: chart.data.yAxisR
    }
    }
    updateLabels(xAxis.value)
    updateChart()
}

function updateLabels(axis) {
    let labels = rawData.value.map(el => el[axis])
    labels = [...new Set(labels)]
    chartData.labels = labels
}

function updateChart() {
    let datasets = []
    if (yAxisL.value && yAxisL.value.length > 0) {
        for (let col of yAxisL.value) {
            datasets = [...datasets, ...buildChart(col, 'y')]
        }
    }
    if (yAxisR.value && yAxisR.value.length > 0) {
        for (let col of yAxisR.value) {
            datasets = [...datasets, ...buildChart(col, 'y1')]
        }
    }
    chartData.datasets = datasets
}

function buildChart(colName, axis) {
    let datasets = []
    if (groupBy.value) {
        let groups = rawData.value.map(el => el[groupBy.value])
        groups = [...new Set(groups)]
        for (const [index, group] of groups.entries()) {
            let data = rawData.value
                .filter(el => el[groupBy.value] == group)

            datasets.push({
                type: chartType.value.tag,
                label: group,
                data,
                backgroundColor: backgroundColors[index % backgroundColors.length],
                borderColor: borderColors[index % borderColors.length],
                borderWidth: 1,
                yAxisID: axis
            })
        }
    } else {
        let bgColors = []
        if (['doughnut', 'pie', 'polarArea', 'radar'].includes(chartType.value.tag)) {
            for (let i = 0; i < xAxis.value.length; i++){
                bgColors.push(backgroundColors[i % backgroundColors.length])
            }
        } else { bgColors = backgroundColors[0] }
        datasets.push({
            type: chartType.value.tag,
            label: colName,
            data: rawData.value,
            backgroundColor: bgColors,
            borderColor: borderColors[0],
            borderWidth: 1,
            yAxisID: axis
        })
    }
    for (let set of datasets) {
        if (xAxis.value) {
            let temp = []
            for (let xLabel of chartData.labels) {
                temp.push(set.data
                    .filter(el => el[xAxis.value] == xLabel)
                    .reduce((acc, el) => acc + el[colName], 0))
            }
            set.data = temp
        } else {
            set.data = set.data.reduce((acc, el) => acc + el[colName], 0)
        }
    }
    return datasets
}

onMounted(() => {
    try {
        loadChart(model.value)
    } catch {
        validChart.value = false
    }
})

watch(model, () => {
    loadChart(model.value)
})

</script>

<template>
    <div :style="`width:${props.width}; height:${props.height}`">
        <Chart :type="chartType.tag" :data="chartData" :options="chartOptions" class="align-self-center"/>
    </div>
</template>

<style>
</style>