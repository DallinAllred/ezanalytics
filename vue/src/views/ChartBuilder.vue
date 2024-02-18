<script setup>
import axios from 'axios'
import { computed, reactive, ref, onMounted, watch } from "vue"
import { useToast } from 'primevue/usetoast'
import Settings from './Settings.vue'

const toast = useToast()

/*
Graph needs
    type: chartTypes
    data: 
    options
*/

const documentStyle = getComputedStyle(document.documentElement)

const chartTitle = ref()
const columns = ref([])
const columnList = ref()
const dataSources = ref([])
const rawData = ref()
const selectedDataSource = ref()
const chartType = ref()

const xAxis = ref()
const yAxis1 = ref([])
const yAxis2 = ref([])
const groupBy = ref()
const tempAxis = ref()
const activeAxis = ref()

const yAxisDialog = ref(false)


// let chartLabels = ['Data']
// let datasets = []

const backgroundColors = ['rgba(249, 115, 22, 0.5)', 'rgba(6, 182, 212, 0.5)', 'rgb(107, 114, 128, 0.5)', 'rgba(139, 92, 246, 0.5)']
const borderColors = ['rgb(249, 115, 22)', 'rgb(6, 182, 212)', 'rgb(107, 114, 128)', 'rgb(139, 92, 246)']

const chartTypes = ref([
    {name: 'Scatter', tag: 'scatter'},
    {name: 'Pie', tag: 'pie'},
    {name: 'Doughnut', tag: 'doughnut'},
    {name: 'Line', tag: 'line'},
    {name: 'Bar', tag: 'bar'},
    {name: 'Radar', tag: 'radar'},
    {name: 'Polar Area', tag: 'polarArea'}
])

async function getSources() {
    let response = await axios.get('http://localhost:5050/api/sources/')
    dataSources.value = response.data
}

async function getData() {
    let response = await axios.get(`http://localhost:5050/api/sources/${selectedDataSource.value.sourceId}`)
    let data = response.data
    columns.value = []
    columnList.value = []
    for (let col of Object.keys(data[0])) {
        columns.value.push({colName: col, type: 'Cont.'})
        columnList.value.push(col)
    }
    rawData.value = data
    // console.log(data)
}

function saveChart() {
    console.log('Saving chart')
    toast.add({severity: 'info', summary: 'Successful', detail: 'Chart save requested', life: 3000})
}

function uploadData() {
    console.log('Uploading data')
    toast.add({severity: 'info', summary: 'Successful', detail: 'Data upload triggered', life: 3000})
}

// function editYAxis(side) {
//     activeAxis.value = side
//     tempAxis.value = side == 'left' ? JSON.parse(JSON.stringify(yAxis1.value)) : JSON.parse(JSON.stringify(yAxis2.value))
//     if (tempAxis.value == []) {}
//     tempAxis.value = {type: '', col: '', group: ''}
//     yAxisDialog.value = true
// }

function updateChart() {
    // // if (activeAxis.value == 'left') {
    // //     yAxis1.value = JSON.parse(JSON.stringify(tempAxis.value))
    // // } else {
    // //     yAxis2.value = JSON.parse(JSON.stringify(tempAxis.value))
    // // }
    // // console.log(yAxis1.value)
    // let datasets = []
    // // for (let chart of yAxis1.value) {
    // if (yAxis1.value && yAxis1.value.length > 1) {
    //     // console.log('Updating left Y-axis')
    //     datasets = bar(yAxis1.value)
    // }
    // // }
    // // for (let chart of yAxis2.value) {
    // if (yAxis2.value && yAxis2.value.length > 0) {
    //     // console.log('Updating right Y-axis')
    //     datasets = [...datasets, ...bar(yAxis2.value)]
    // }
    // // }
    // // console.log('Datasets: ', datasets)
    // console.log('Updating charts...')
    let datasets = []
    if (yAxis1.value && yAxis1.value.length > 0) {
        for (let col of yAxis1.value) {
            datasets = [...datasets, ...buildChart(col, 'y')]
        }
    }
    if (yAxis2.value && yAxis2.value.length > 0) {
        for (let col of yAxis2.value) {
            datasets = [...datasets, ...buildChart(col, 'y1')]
        }
    }

    chartData.datasets = datasets
    // console.log(chartData)
    yAxisDialog.value = false
}

function buildChart(colName, axis) {
    let datasets = []
    if (groupBy.value) {
        // console.log('Grouping by: ', groupBy.value)
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
        datasets.push({
            type: chartType.value.tag,
            label: colName,
            data: rawData.value,
            backgroundColor: backgroundColors[0],
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

// function bar(chart, axis='y') {
//     // console.log('Chart: ', chart)
//     let type = chart.type.value
//     let label = chart.col
//     let datasets = []
//     if (chart.group) {
//         let groups = rawData.value.map(el => el[chart.group])
//         groups = [...new Set(groups)]
//         for (const [index, group] of groups.entries()) {
//             let data = rawData.value// .map(el => el[chart.col])
//                 .filter(el => el[chart.group] == group)
//             datasets.push({
//                 // type,
//                 label: group,
//                 data,
//                 backgroundColor: backgroundColors[index % backgroundColors.length],
//                 borderColor: borderColors[index % borderColors.length],
//                 borderWidth: 1,
//                 yAxisID: axis
//             })
//         }
//     } else {
//         datasets.push({
//             // type,
//             label,
//             data: rawData.value, // data: rawData.value.map(el => el[chart.col]),
//             backgroundColor: backgroundColors[0],
//             borderColor: borderColors[0],
//             borderWidth: 1,
//             yAxisID: axis
//         })
//     }
//     for (let set of datasets) {
//         if (xAxis.value) {
//             let temp = []
//             for (let xLabel of chartData.labels) {
//                 temp.push(set.data
//                     .filter(el => el[xAxis.value] == xLabel)
//                     .reduce((acc, el) => acc + el[chart.col], 0))
//             }
//             set.data = temp
//         } else {
//             set.data = set.data.reduce((acc, el) => acc + el[chart.col], 0)
//         }
//     }
//     return datasets
// }

const chartData = reactive({
    labels: ['Data'],
    datasets: [
        {
            type: 'bar',
            label: 'Sales',
            data: [540, 325, 702, 620],
            backgroundColor: ['rgba(249, 115, 22, 0.5)', 'rgba(6, 182, 212, 0.5)', 'rgb(107, 114, 128, 0.5)', 'rgba(139, 92, 246, 0.5)'],
            borderColor: ['rgb(249, 115, 22)', 'rgb(6, 182, 212)', 'rgb(107, 114, 128)', 'rgb(139, 92, 246)'],
            borderWidth: 1
        }
    ]
})

// Chart Setup for Demo Chart
onMounted(() => {
    getSources()
    // chartData.value = setChartData()
    // chartOptions.value = setChartOptions()
})

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

// CHART OPTIONS
// Plugins:
//      title: Input field
//      legend
const chartOptions = ref({
    responsive: true,
    plugins: {
        legend: {
            labels: {
                color: documentStyle.getPropertyValue('--text-color')
            }
        },
        title: {
            display: true,
            text: 'Custom Chart Title'
        }
    },
    scales: {
        x: {
            // stacked: true,
            ticks: {
                color: documentStyle.getPropertyValue('--text-color-secondary')
            },
            grid: {
                color: documentStyle.getPropertyValue('--surface-border')
            },
            title: {
                display: true,
                text: 'My X-Axis'
            }
        },
        y: {
            // stacked: true,
            // beginAtZero: true,
            ticks: {
                color: documentStyle.getPropertyValue('--text-color-secondary')
            },
            grid: {
                color: documentStyle.getPropertyValue('--surface-border')
            },
            title: {
                display: true,
                text: 'My Y-Axis'
            }
        }
    }
})



watch(selectedDataSource, async () => {
    getData()
})
watch(chartType, () => {
    // console.log(chartType.value)
    if (xAxis.value && (yAxis1.value.length > 0 || yAxis2.value.length > 0)) updateChart()
})
watch(groupBy, () => {
    if (xAxis.value && (yAxis1.value.length > 0 || yAxis2.value.length > 0)) updateChart()
})
watch(xAxis, () => {
    let labels = rawData.value.map(el => el[xAxis.value])
    labels = [...new Set(labels)]
    chartData.labels = labels
    if (yAxis1.value.length > 0 || yAxis2.value.length > 0) updateChart()
})
watch(yAxis1, () => {
    // console.log('Y-Axis1: ', yAxis1.value)
    if (xAxis.value) updateChart()
})
watch(yAxis2, () => {
    // console.log('Y-Axis2: ', yAxis2.value)
    if (xAxis.value) updateChart()
})

</script>

<template>
    <div class="grid h-full">
        <div class="col-12 flex flex-row gap-2">
            <div><Dropdown v-model="selectedDataSource" :options="dataSources" optionLabel="sourceLabel" placeholder="Select a Table" class="w-full md:w-14rem" /></div>
            <div><Button label="Upload CSV" icon="pi pi-upload" severity="success" class="mr-2" @click="uploadData" /></div>
            <div><Dropdown v-model="chartType" :options="chartTypes" optionLabel="name" placeholder="Select a Chart Type" class="w-full md:w-14rem" /></div>
            <div><Button label="Save" icon="pi pi-save" severity="success" class="mr-2" @click="saveChart" /></div>
        </div>
        <div class="col-12 grid h-full">
            <div class="col-10 col-offset-1">
                <div class="grid">
                    <div class="col-10 justify-content-center">
                        <div class="grid">
                            <div class="col-6 col-offset-3 flex justify-content-center">
                                <InputText type="text" v-model="chartTitle" placeholder="Title" class="justify-self-center"/>
                            </div>
                            <div class="col-2 col-offset-1">
                                <Dropdown v-model="groupBy" showClear :options="columnList" placeholder="Group By..." :disabled="columnList && chartType ? false : true"/>
                            </div>
                        </div>
                        <div class="flex flex-row gap-2">
                            <div class="flex flex-row align-items-center gap-1">
                                <div class="rot-90">
                                    <MultiSelect v-model="yAxis1" :options="columnList" placeholder="Y-Axis" :maxSelectedLabels="3" :disabled="columnList && chartType ? false : true">
                                        <template #dropdownicon>{{  }}</template>
                                    </MultiSelect>
                                    <label v-if="yAxis1">{{ yAxis1.col }}</label>
                                </div>
                            </div>
                            <div class="flex flex-column align-content-center w-full">
                                <Chart type="bar" :data="chartData" :options="chartOptions" />
                                <Dropdown v-model="xAxis" :options="columnList" placeholder="X-Axis" :disabled="columnList && chartType ? false : true"/>
                            </div>
                            <div class="flex flex-row align-items-center gap-1">
                                <div class="rot-p90">
                                    <MultiSelect v-model="yAxis2" :options="columnList" placeholder="Y-Axis" :maxSelectedLabels="3" :disabled="columnList && chartType ? false : true">
                                        <template #dropdownicon>{{  }}</template>
                                    </MultiSelect>
                                </div>
                            </div>
                        </div>

                    </div>
                    <div class="col-2">
                        Stats display
                    </div>
                </div>
                <div>
                    <DataTable :value="rawData">
                        <Column v-for="col in columnList" :field="col" :header="col"></Column>
                    </DataTable>
                </div>
            </div>
        </div>
    </div>

    <Dialog v-model:visible="yAxisDialog" :style="{width: '450px'}" header="Axis Details" :modal="true" class="p-fluid">
        <Card v-model="tempAxis">
            <template #content>
            <div class="flex gap-3">
                <div :style="{width: '400px'}" class="flex flex-column gap-1">
                    <Dropdown v-model="tempAxis.col" :options="columnList" placeholder="Select a Column" />
                    <Dropdown v-model="tempAxis.type" :options="chartTypes" optionLabel="name" placeholder="Select a Chart Type" />
                </div>
                <div>
                    <Dropdown v-model="tempAxis.group" :options="columnList" placeholder="Group data by..." />
                </div>
            </div>
            </template>
        </Card>
        <Divider />
        <template #footer>
            <Button label="Cancel" icon="pi pi-times" text @click="yAxisDialog = false" />
            <Button label="Save" icon="pi pi-check" text @click="updateChart" />
        </template>
    </Dialog>

    <!-- <Dialog v-model:visible="yAxisDialog" :style="{width: '450px'}" header="Axis Details" :modal="true" class="p-fluid">
        <Card v-for="(chart, index) in tempAxis" :key="index">
            <template #content>
            <div class="flex gap-3">
                <div :style="{width: '400px'}" class="flex flex-column gap-1">
                    <Dropdown v-model="chart.col" :options="columnList" placeholder="Select a Column" />
                    <Dropdown v-model="chart.type" :options="chartTypes" optionLabel="name" placeholder="Select a Chart Type" />
                </div>
                <div class="flex align-items-center">
                    <Button outlined rounded icon="pi pi-times" severity="danger" @click="removeChart(index)" />
                </div>
            </div>
            </template>
        </Card>
        <div v-if="!yAxis1 || yAxis1.length < 4" class="flex justify-content-center">
            <Button outlined rounded icon="pi pi-plus" severity="success" @click="addChart" />
        </div>
        <Divider />
        <template #footer>
            <Button label="Cancel" icon="pi pi-times" text @click="yAxisDialog = false" />
            <Button label="Save" icon="pi pi-check" text @click="updateChart" />
        </template>
    </Dialog> -->
</template>

<style>
.rot-90 {
    writing-mode: vertical-lr;
    rotate: 180deg;
}
.rot-p90 {
    writing-mode: vertical-lr;
}
</style>


<!-- :pt="{
    item: ({ props, state, context }) => {
        console.log(props, state, context)
        context.disabled = true
    }
    }" -->

<script>
// function editYAxis(side) {
//     activeAxis.value = side
//     tempAxis.value = side == 'left' ? JSON.parse(JSON.stringify(yAxis1.value)) : JSON.parse(JSON.stringify(yAxis2.value))
//     if (tempAxis.value && tempAxis.value.length > 1) chartTypes.value[0].optionDisabled = true
//     yAxisDialog.value = true
// }

// function addChart() {
//     if (!tempAxis.value) {
//         tempAxis.value = []
//     }
//     tempAxis.value.push({col: null, type: null})
// }

// function removeChart(index) {
//     tempAxis.value.splice(index, 1)
// }


// CHART MODEL
/*
    {
        _id: MongoID,
        name: Display Name,
        user: User creating chart,
        datasource: Access_id,
        data: {},
        options: {}
    }
*/

// CHART DATA
// Labels
//      Need to look into this. Is it just the x-axis?
// Datasets
//      Label = Column Name - Alias would be nice...
//      Type: Need a good way to add additional types
//      Data: Pulled from table
//          Scatter requires data: [{x: val, y: val}, {x: val, y: val},...]
//      
//      Need to programatically create new chart if splitting by column
//          Label becomes filter key, data becomes filtered array
//          Type matches parent

// const setChartData = () => {
//     return {
//         labels: ['Q1', 'Q2', 'Q3', 'Q4'],
//         datasets: [
//             {
//                 label: 'Sales',
//                 data: [540, 325, 702, 620],
//                 backgroundColor: ['rgba(249, 115, 22, 0.2)', 'rgba(6, 182, 212, 0.2)', 'rgb(107, 114, 128, 0.2)', 'rgba(139, 92, 246 0.2)'],
//                 borderColor: ['rgb(249, 115, 22)', 'rgb(6, 182, 212)', 'rgb(107, 114, 128)', 'rgb(139, 92, 246)'],
//                 borderWidth: 1
//             }
//         ]
//     }
// }
// const setChartOptions = () => {
//     const documentStyle = getComputedStyle(document.documentElement)
//     const textColor = documentStyle.getPropertyValue('--text-color')
//     const textColorSecondary = documentStyle.getPropertyValue('--text-color-secondary')
//     const surfaceBorder = documentStyle.getPropertyValue('--surface-border')

//     return {
//         plugins: {
//             legend: {
//                 labels: {
//                     color: textColor
//                 }
//             }
//         },
//         scales: {
//             x: {
//                 ticks: {
//                     color: textColorSecondary
//                 },
//                 grid: {
//                     color: surfaceBorder
//                 }
//             },
//             y: {
//                 beginAtZero: true,
//                 ticks: {
//                     color: textColorSecondary
//                 },
//                 grid: {
//                     color: surfaceBorder
//                 }
//             }
//         }
//     }
// }
</script>