<script setup>
import axios from '@/axiosConfig'
import { onMounted, reactive, ref, watch } from "vue"

import { useToast } from 'primevue/usetoast'

const emit = defineEmits(['timeout401'])
const model = defineModel()
const props = defineProps(['height', 'width', 'dashSize'])

const toast = useToast()

const documentStyle = getComputedStyle(document.documentElement)

const chartComp = ref(null)
const chartContainer = ref(null)

const validChart = ref(true)

const rawData = ref()
const dataSource = ref()
const chartType = ref({name: 'Bar', tag: 'bar'})

const xAxis = ref()
const yAxisL = ref([])
const yAxisR = ref([])
const groupBy = ref()

const backgroundColors1 = ['rgba(249, 115, 22, 0.8)', 'rgba(6, 182, 212, 0.8)', 'rgb(107, 114, 128, 0.8)', 'rgba(139, 92, 246, 0.8)']
const backgroundColors2 = ['rgba(249, 0, 100, 0.4)', 'rgba(100, 249, 0, 0.4)', 'rgb(0, 100, 249, 0.4)', 'rgba(255, 200, 0, 0.4)']
const borderColors1 = ['rgb(249, 115, 22)', 'rgb(6, 182, 212)', 'rgb(107, 114, 128)', 'rgb(139, 92, 246)']
const borderColors2 = ['rgb(249, 0, 100)', 'rgb(100, 249, 0)', 'rgb(0, 100, 249)', 'rgb(255, 200, 0)']

const chartData = reactive({labels: [], datasets: []})
const chartOptions = reactive({
    responsive: true,
    maintainAspectRatio: true,
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
    try {
        let response = await axios.get(`/api/sources/${dataSource.value.sourceId}`)
        let data = response.data
        rawData.value = data
    } catch (err) {
        if (err.response?.status === 401) emit('timeout401')
    }
}

async function loadChart(chartId) {
    let chart = {}
    try {
        let response = await axios.get(`/api/charts/${chartId}`)
        chart = response.data
    } catch (err) {
        if (err.response?.status === 401) {
            emit('timeout401')
            return
        }
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
    chartComp.value.reinit()
}

function updateLabels(axis) {
    let labels = rawData.value.map(el => el[axis])
    labels = [...new Set(labels)]
    chartData.labels = labels
}

function updateChart() {
    let datasets = []
    if (yAxisL.value && yAxisL.value.length > 0) {
        datasets = [...datasets, ...buildChart(yAxisL.value, 'y')]
    }
    if (yAxisR.value && yAxisR.value.length > 0) {
        datasets = [...datasets, ...buildChart(yAxisR.value, 'y1')]
    }
    chartData.datasets = datasets
}

function buildChart(colName, axis) {
    if (chartType.value.name == 'Bar') {
        chartOptions.scales.x.display = true
        chartOptions.scales.y.display = true
        if (yAxisR.value) {
            chartOptions.scales.y1.display = true
        } else if (!yAxisR.value && chartOptions.scales.y1) {
            chartOptions.scales.y1.display = false
        }
    } else {
        chartOptions.scales.x.display = false
        chartOptions.scales.y.display = false
        if (chartOptions.scales.y1) {
            chartOptions.scales.y1.display = false
        }
    }
    if (['doughnut', 'pie', 'polarArea', 'radar'].includes(chartType.value.tag)) {
        chartOptions.aspectRatio = 1
    } else {
        chartOptions.aspectRatio = chartContainer.value.clientWidth  / chartContainer.value.clientHeight
    }
    let datasets = []
    if (groupBy.value) {
        let groups = rawData.value.map(el => el[groupBy.value])
        groups = [...new Set(groups)]
        for (const [index, group] of groups.entries()) {
            let data = rawData.value
                .filter(el => el[groupBy.value] == group)

            datasets.push({
                type: chartType.value.tag,
                label: `${colName}-${group}`,
                data,
                backgroundColor: axis == 'y' ? backgroundColors1[index % backgroundColors1.length] : backgroundColors2[index % backgroundColors2.length],
                borderColor: axis == 'y' ? borderColors1[index % borderColors1.length] : borderColors2[index % borderColors2.length],
                borderWidth: 1,
                yAxisID: axis
            })
        }
    } else {
        let bgColors = []
        if (['doughnut', 'pie', 'polarArea', 'radar'].includes(chartType.value.tag)) {
            bgColors = backgroundColors1
        } else { bgColors = axis == 'y' ? backgroundColors1[0] : backgroundColors2[0] }
        datasets.push({
            type: chartType.value.tag,
            label: colName,
            data: rawData.value,
            backgroundColor: bgColors,
            borderColor: axis == 'y' ? borderColors1[0] : borderColors2[0],
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

watch(() => props.dashSize, () => {
    loadChart(model.value)
    chartComp.value.reinit()
})
</script>

<template>
    <div ref="chartContainer" class="w-full h-full">
        <Chart ref="chartComp" :type="chartType.tag" :data="chartData" :options="chartOptions"
        class="flex justify-content-center align-self-center w-full h-full pb-2"/>
    </div>
</template>

<style>
canvas {
    max-height: 100%;
}
</style>