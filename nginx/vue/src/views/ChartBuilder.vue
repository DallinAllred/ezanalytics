<script setup>
import { reactive, ref, onMounted, watch } from "vue"
import { useRoute } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import FloatLabel from 'primevue/floatlabel'
import axios from '@/axiosConfig'
import DataUpload from '@/components/dialogs/DataUpload.vue'

const emit = defineEmits('updateApp')
const route = useRoute()
const toast = useToast()

const currentUser = ref(JSON.parse(localStorage.getItem('eza-user')) ?? {})
const documentStyle = getComputedStyle(document.documentElement)
const showLogin = ref(false)
const loginTitle = ref('Session Timed Out')
const showUploadModal = ref(false)

const chartId = ref(null)
const chartOwner = ref(currentUser.value['user_id'])
const chartTitle = ref()
const columns = ref([])
const columnList = ref()
const dataSources = ref([])
const rawData = ref()
const selectedDataSource = ref()
const chartType = ref({name: 'Bar', tag: 'bar'})
const stackedBox = ref(false)

const xAxis = ref()
const yAxisL = ref([])
const yAxisR = ref([])
const groupBy = ref()

const backgroundColors = ['rgba(249, 115, 22, 0.5)', 'rgba(6, 182, 212, 0.5)', 'rgb(107, 114, 128, 0.5)', 'rgba(139, 92, 246, 0.5)']
const borderColors = ['rgb(249, 115, 22)', 'rgb(6, 182, 212)', 'rgb(107, 114, 128)', 'rgb(139, 92, 246)']

const chartTypes = ref([
    {name: 'Bar', tag: 'bar'},
    {name: 'Doughnut', tag: 'doughnut'},
    {name: 'Line', tag: 'line'},
    {name: 'Pie', tag: 'pie'},
    {name: 'Polar Area', tag: 'polarArea'},
    {name: 'Radar', tag: 'radar'},
    {name: 'Scatter', tag: 'scatter'},
])

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

let saving = false

async function loadPage() {
    if (!currentUser.value.username) {
        currentUser.value = JSON.parse(localStorage.getItem('eza-user')) ?? {}
        if (!currentUser.value?.username) {
            loginTitle.value = null
            showLogin.value = true
            return
        }
        chartOwner.value = currentUser.value['user_id']
    }
    loginTitle.value = 'Session Timed Out'
    await getSources()
    if ('chart' in route.query) {
        await loadChart(route.query.chart)
        chartId.value = route.query.chart
    }
}

async function getSources() {
    try {
        let response = await axios.get('/api/sources/')
        dataSources.value = response.data
    } catch (err) {
        if (err.response?.status === 401) {
            showLogin.value = true
            saving = false
            return
        }
    }
}

async function getData() {
    try {
        let response = await axios.get(`/api/sources/${selectedDataSource.value.sourceId}`)
        let data = response.data
        columns.value = []
        columnList.value = []
        for (let col of Object.keys(data[0])) {
            columns.value.push({colName: col, type: 'Cont.'})
            columnList.value.push(col)
        }
        rawData.value = data
    } catch (err) {
        if (err.response?.status === 401) {
            showLogin.value = true
            saving = false
        }
    }
}

async function saveChart() {
    let chart = {
        owner: chartOwner.value,
        sourceId: selectedDataSource.value,
        title: chartTitle.value,
        type: chartType.value,
        groupBy: groupBy.value,
        data: {
            xAxis: xAxis.value,
            yAxisL: yAxisL.value,
        },
        options: {
            stacked: stackedBox.value
        }
    }
    if (yAxisR.value && yAxisR.value.length > 0) {
        chart.data.yAxisR = yAxisR.value
    }
    if (chartId.value) {
        try {
            let response = await axios.put(`/api/charts/${chartId.value}`, chart)
            toast.add({severity: 'success', summary: 'Successful', detail: 'Chart saved', life: 3000})
        } catch (err) {
            if (err.response?.status === 401) {
                showLogin.value = true
                saving = true
                return
            }
            toast.add({severity: 'error', summary: 'Error', detail: 'Chart failed to save', life: 3000})
        }
    } else {
        try {
            let response = await axios.post(`/api/charts`, chart)
            toast.add({severity: 'success', summary: 'Successful', detail: 'Chart saved', life: 3000})
        } catch (err) {
            if (err.response?.status === 401) {
                showLogin.value = true
                saving = true
                return
            }
            toast.add({severity: 'error', summary: 'Error', detail: 'Chart failed to save', life: 3000})
        }
    }
}

async function loadChart(chartId) {
    let chart = {}
    try {
        let response = await axios.get(`/api/charts/${chartId}`)
        chart = response.data
    } catch (err) {
        if (err.response?.status === 401) {
            showLogin.value = true
            saving = false
            return
        }
        toast.add({severity: 'error', summary: 'Chart Not Found', detail: `Unable to find chart ${chartId}`, life: 3000})
        return
    }

    selectedDataSource.value = chart.sourceId
    await getData()
    chartOwner.value = chart.owner ?? currentUser.value['user_id']
    chartTitle.value = chart.title
    chartType.value = chart.type
    xAxis.value = chart.data.xAxis
    yAxisL.value = chart.data.yAxisL
    yAxisR.value = chart.data.yAxisR ?? null
    groupBy.value = chart.groupBy ?? null
    stackedBox.value = chart.options.stacked
    chartOptions.scales.x.stacked = chart.options.stacked
    chartOptions.scales.y.stacked = chart.options.stacked
    if (yAxisR.value) {
        chartOptions.scales.y1 = {
            beginAtZero: true,
            position: 'right',
            ticks: { color: documentStyle.getPropertyValue('--text-color-secondary') },
            grid: { color: documentStyle.getPropertyValue('--surface-border') },
        }
        chartOptions.scales.y1.stacked = chart.options.stacked
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
        for (let col of yAxisL.value) { datasets = [...datasets, ...buildChart(col, 'y')] }
    }
    if (yAxisR.value && yAxisR.value.length > 0) {
        for (let col of yAxisR.value) { datasets = [...datasets, ...buildChart(col, 'y1')] }
    }
    chartData.datasets = datasets
}

function toggleStack() {
    chartOptions.scales.x['stacked'] = stackedBox.value
    chartOptions.scales.y['stacked'] = stackedBox.value
    if (Object.keys(chartOptions.scales).includes('y1')) {
        chartOptions.scales.y1['stacked'] = stackedBox.value
    }
    updateChart()
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

onMounted(async () => {
    await loadPage()
})

watch(showLogin, async () => {
    if (showLogin.value || saving) return
    await loadPage()
})

watch(showUploadModal, () => {
    if (!showUploadModal.value) getSources()
})

watch(chartType, () => {
    if (xAxis.value && (yAxisL.value.length > 0 || yAxisR.value.length > 0)) updateChart()
})
watch(groupBy, () => {
    if (xAxis.value && (yAxisL.value.length > 0 || yAxisR.value.length > 0)) updateChart()
})
watch(xAxis, () => {
    updateLabels(xAxis.value)
    if (yAxisL.value.length > 0 || yAxisR.value.length > 0) updateChart()
})
watch(yAxisL, () => {
    if (xAxis.value) updateChart()
})
watch(yAxisR, () => {
    if (yAxisR.value && yAxisR.value != []) {
        chartOptions.y1 = {
            stacked: stackedBox.value,
            beginAtZero: true,
            position: 'right',
            ticks: { color: documentStyle.getPropertyValue('--text-color-secondary') },
            grid: { color: documentStyle.getPropertyValue('--surface-border') }
        }
    } else { chartOptions.y1 = {} }
    if (xAxis.value) updateChart()
})
</script>

<template>
    <div>
        <div v-if="!(currentUser.admin || currentUser['chart_builder'])" class="flex p-3">
            <Unauthorized />
        </div>
        <div v-else>
            <Toolbar class="mb-2">
                <template #start>
                    <div class="flex gap-2 justify-content-between">
                        <Dropdown v-model="selectedDataSource" :options="dataSources" optionLabel="sourceLabel" placeholder="Select a Table" class="w-14rem" @change="getData()" />
                        <Button label="Upload CSV" icon="pi pi-upload" @click="showUploadModal = true" />
                    </div>
                </template>
                <template #end>
                    <Button label="Save" icon="pi pi-save" @click="saveChart" />
                </template>
            </Toolbar>

            <div class="flex flex-column align-content-center align-items-center gap-3">
                <div class="flex flex-column justify-content-center border-round border-solid border-200 border-1 w-11 py-2">
                    <div class="flex justify-content-between py-4">
                        <div class="flex justify-content-start gap-2">
                            <div class="ml-2">
                                <FloatLabel class="w-full">
                                    <Dropdown v-model="chartType" inputId="chart" :options="chartTypes" optionLabel="name" placeholder="Select a Chart Type" class="w-full md:w-14rem" />
                                    <label for="chart">Chart Type</label>
                                </FloatLabel>
                            </div>
                            <div class="flex align-items-center gap-1" v-if="chartType.tag == 'bar' ? true : false">
                                <Checkbox v-model="stackedBox" inputId="stackCheck" :binary="true" @change="toggleStack"/>
                                <label for="stackCheck">Stacked</label>
                            </div>
                        </div>
                        <div class="flex justify-content-center">
                            <InputText type="text" v-model="chartTitle" placeholder="Title" class="justify-self-center"/>
                        </div>
                        <div class="mr-2">
                            <FloatLabel class="w-full">
                                <Dropdown v-model="groupBy" inputId="group" showClear :options="columnList" placeholder="Group By..." :disabled="columnList && chartType ? false : true"/>
                                <label for="group">Group By</label>
                            </FloatLabel>
                        </div>
                    </div>
                    <div class="flex justify-content-center gap-2">
                        <div class="flex align-items-center gap-1">
                            <div class="rot-90">
                                <MultiSelect v-model="yAxisL" :options="columnList" placeholder="Y-Axis" :maxSelectedLabels="3" :disabled="columnList && chartType ? false : true">
                                    <template #dropdownicon>{{  }}</template>
                                </MultiSelect>
                                <label v-if="yAxisL">{{ yAxisL.col }}</label>
                            </div>
                        </div>
                        <div class="flex flex-column align-content-center chart-container">
                            <Chart :type="chartType.tag" :data="chartData" :options="chartOptions" class="align-self-center" />
                            <Dropdown v-model="xAxis" :options="columnList" placeholder="X-Axis" :disabled="columnList && chartType ? false : true"/>
                        </div>
                        <div class="flex flex-row align-items-center gap-1">
                            <div class="rot-p90">
                                <MultiSelect v-model="yAxisR" :options="columnList" placeholder="Y-Axis" :maxSelectedLabels="3" :disabled="columnList && chartType ? false : true">
                                    <template #dropdownicon>{{  }}</template>
                                </MultiSelect>
                            </div>
                        </div>
                    </div>

                </div>
                <div class="border-round border-solid border-200 border-1 w-11">
                    <DataTable :value="rawData" scrollable scrollHeight="15rem">
                        <Column v-for="col in columnList" :field="col" :header="col"></Column>
                    </DataTable>
                </div>
            </div>
            <DataUpload v-model="showUploadModal" @timeout401="showLogin = true"></DataUpload>
        </div>
        <Login v-model="showLogin" :title="loginTitle" @login="showLogin = false; emit('updateApp')"></Login>
    </div>
</template>

<style>
.rot-90 {
    writing-mode: vertical-lr;
    rotate: 180deg;
}
.rot-p90 {
    writing-mode: vertical-lr;
}
/*
.chart-builder{
    height: calc(100vh - 4.5rem);
}

.chart-builder-header {
    height: 4rem;
}*/

.chart-builder-main {
    height: calc(100vh - 4.5rem - 4rem - 15rem - 2rem);
}

/* .chart-container {
    height: 450px;
} */
canvas {
    height: calc(100vh - 4.5rem - 4rem - 15rem - 2rem - 145px) !important;
}

.chart-builder-table {
    height: 10rem;
}
</style>

<script>
// const chartOptions = reactive({
//     maintainAspectRation: false,
//     responsive: true,
//     plugins: {
//         legend: {
//             labels: { color: documentStyle.getPropertyValue('--text-color') }
//         },
//         title: {
//             display: true,
//             text: 'Custom Chart Title'
//         }
//     },
//     scales: {
//         x: {
//             stacked: false,
//             ticks: { color: documentStyle.getPropertyValue('--text-color-secondary') },
//             grid: { color: documentStyle.getPropertyValue('--surface-border') },
//             title: {
//                 display: true,
//                 text: 'My X-Axis'
//             }
//         },
//         y: {
//             beginAtZero: true,
//             stacked: false,
//             ticks: { color: documentStyle.getPropertyValue('--text-color-secondary') },
//             grid: { color: documentStyle.getPropertyValue('--surface-border') },
//             title: {
//                 display: true,
//                 text: 'Left Y-Axis'
//             }
//         }
//         // ,y1: {}
//         //     beginAtZero: true,
//         //     stacked: true,
//         //     position: 'right',
//         //     ticks: { color: documentStyle.getPropertyValue('--text-color-secondary') },
//         //     grid: { color: documentStyle.getPropertyValue('--surface-border') },
//         //     title: {
//         //         display: true,
//         //         text: 'Right Y-Axis'
//         //     }
//         // }
//     }
// })


// const chartData = reactive({
//     labels: ['Data'],
//     datasets: [
//         {
//             type: 'bar',
//             label: 'Sales',
//             data: [540, 325, 702, 620],
//             backgroundColor: ['rgba(249, 115, 22, 0.5)', 'rgba(6, 182, 212, 0.5)', 'rgb(107, 114, 128, 0.5)', 'rgba(139, 92, 246, 0.5)'],
//             borderColor: ['rgb(249, 115, 22)', 'rgb(6, 182, 212)', 'rgb(107, 114, 128)', 'rgb(139, 92, 246)'],
//             borderWidth: 1
//         }
//     ]
// })

// const chartData = ref({
//         labels: ['Q1', 'Q2', 'Q3', 'Q4'],
//         datasets: [
//             {
//                 type: 'scatter',
//                 label: 'Sales',
//                 // data: [540, 325, 702, 620],
//                 data:[
//                     {x: 'Q1', y: 100},
//                     {x: 'Q2', y: 500},
//                     {x: 'Q3', y: 750},
//                     {x: 'Q4', y: 1000},
//                     {x: 'Q1', y: 200},
//                     {x: 'Q2', y: 600},
//                     {x: 'Q3', y: 150},
//                     {x: 'Q4', y: 100},
//                     {x: 'Q3', y: 850},
//                     {x: 'Q4', y: 350}
//                 ],
//                 backgroundColor: ['rgba(249, 115, 22, 0.5)'],//, 'rgba(6, 182, 212, 0.5)', 'rgb(107, 114, 128, 0.5)', 'rgba(139, 92, 246, 0.5)'],
//                 borderColor: ['rgb(249, 115, 22)'],//, 'rgb(6, 182, 212)', 'rgb(107, 114, 128)', 'rgb(139, 92, 246)'],
//                 borderWidth: 1
//             },{
//                 type: 'scatter',
//                 label: 'Global',
//                 // data: [540, 325, 702, 620],
//                 data:[
//                     {x: 'Q1', y: 1000},
//                     {x: 'Q2', y: 5000},
//                     {x: 'Q3', y: 7500},
//                     {x: 'Q4', y: 10000},
//                     {x: 'Q1', y: 2000},
//                     {x: 'Q2', y: 6000},
//                     {x: 'Q3', y: 1500},
//                     {x: 'Q4', y: 1500},
//                     {x: 'Q3', y: 8500},
//                     {x: 'Q4', y: 3500}
//                 ],
//                 backgroundColor: ['rgba(6, 182, 212, 0.5)'],//, 'rgb(107, 114, 128, 0.5)', 'rgba(139, 92, 246, 0.5)'],
//                 borderColor: ['rgb(6, 182, 212)'],//, 'rgb(107, 114, 128)', 'rgb(139, 92, 246)'],
//                 borderWidth: 1
//             },
//             // {
//             //     type: 'bar',
//             //     label: 'Bids',
//             //     data: [700, 650, 1400, 1200],
//             //     backgroundColor: ['rgba(50, 135, 52, 0.2)', 'rgba(255, 50, 40, 0.2)', 'rgb(50, 114, 50, 0.2)', 'rgba(139, 0, 100, 0.2)'],
//             //     // borderColor: ['rgb(249, 115, 22)', 'rgb(6, 182, 212)', 'rgb(107, 114, 128)', 'rgb(139, 92, 246)'],
//             //     borderWidth: 1
//             // },
//             // {
//             //     type: 'line',
//             //     label: 'LineChart',
//             //     borderColor: documentStyle.getPropertyValue('--orange-500'),
//             //     borderWidth: 2,
//             //     fill: false,
//             //     tension: 0.5,
//             //     data: [500, 250, 120, 480, 560, 760, 420]
//             // }
//         ]
//     })

// watch(selectedDataSource, async () => {
//     getData()
// })
</script>