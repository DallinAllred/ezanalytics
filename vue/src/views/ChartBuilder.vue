<script setup>
import { ref, onMounted } from "vue";


/*
Graph needs
    type: graphTypes
    data: 
    options
*/

const documentStyle = getComputedStyle(document.documentElement);

const selectedDataSource = ref();
const selectedGraphType = ref();
const dataSources = ref([
    { name: 'New York', code: 'NY' },
    { name: 'Rome', code: 'RM' },
    { name: 'London', code: 'LDN' },
    { name: 'Istanbul', code: 'IST' },
    { name: 'Paris', code: 'PRS' }
]);
const graphTypes = ref([
    {name: 'Pie', value: 'pie'},
    {name: 'Doughtnut', value: 'doughtnut'},
    {name: 'Line', value: 'line'},
    {name: 'Bar', value: 'bar'},
    {name: 'Radar', value: 'radar'},
    {name: 'Polar Area', value: 'polarArea'}
])

const columns = ref([
    {colName: 'id', type: 'Cont.'},
    {colName: 'bit', type: 'Cat.'},
    {colName: 'defects', type: 'Cont.'},
    {colName: 'vendor', type: 'Cat.'},
    {colName: 'jobs', type: 'Cont.'},
])

function saveChart() {
    console.log('Saving chart')
    toast.add({severity: 'info', summary: 'Successful', detail: 'Chart save requested', life: 3000})
}

function uploadData() {
    console.log('Uploading data')
    toast.add({severity: 'info', summary: 'Successful', detail: 'Data upload triggered', life: 3000})
}

// Chart Setup for Demo Chart
// onMounted(() => {
//     chartData.value = setChartData();
//     chartOptions.value = setChartOptions();
// });

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



const chartData = ref({
        labels: ['Q1', 'Q2', 'Q3', 'Q4', '5', '6', '7'],
        datasets: [
            {
                type: 'scatter',
                label: 'Sales',
                // data: [540, 325, 702, 620],
                data:[{
                    x: 1, y: 100
                }, {
                    x: 2, y: 500
                }, {
                    x: 3, y: 750
                }, {
                    x: 5, y: 1000
                }],
                backgroundColor: ['rgba(249, 115, 22, 0.5)', 'rgba(6, 182, 212, 0.5)', 'rgb(107, 114, 128, 0.5)', 'rgba(139, 92, 246, 0.5)'],
                borderColor: ['rgb(249, 115, 22)', 'rgb(6, 182, 212)', 'rgb(107, 114, 128)', 'rgb(139, 92, 246)'],
                borderWidth: 1
            },{
                type: 'bar',
                label: 'Bids',
                data: [700, 650, 1400, 1200],
                backgroundColor: ['rgba(50, 135, 52, 0.2)', 'rgba(255, 50, 40, 0.2)', 'rgb(50, 114, 50, 0.2)', 'rgba(139, 0, 100, 0.2)'],
                // borderColor: ['rgb(249, 115, 22)', 'rgb(6, 182, 212)', 'rgb(107, 114, 128)', 'rgb(139, 92, 246)'],
                borderWidth: 1
            },{
                type: 'line',
                label: 'LineChart',
                borderColor: documentStyle.getPropertyValue('--orange-500'),
                borderWidth: 2,
                fill: false,
                tension: 0.5,
                data: [500, 250, 120, 480, 560, 760, 420]
            }
        ]
    });

// CHART OPTIONS
// Plugins:
//      title: Input field
const chartOptions = ref({
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
                }
            },
            y: {
                // stacked: true,
                beginAtZero: true,
                ticks: {
                    color: documentStyle.getPropertyValue('--text-color-secondary')
                },
                grid: {
                    color: documentStyle.getPropertyValue('--surface-border')
                }
            }
        }
    });

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
//     };
// };
// const setChartOptions = () => {
//     const documentStyle = getComputedStyle(document.documentElement);
//     const textColor = documentStyle.getPropertyValue('--text-color');
//     const textColorSecondary = documentStyle.getPropertyValue('--text-color-secondary');
//     const surfaceBorder = documentStyle.getPropertyValue('--surface-border');

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
//     };
// }

</script>

<template>
    <div class="grid h-full">
        <div class="col-12 flex flex-row gap-2">
            <div><Dropdown v-model="selectedDataSource" :options="dataSources" optionLabel="name" placeholder="Select a Table" class="w-full md:w-14rem" /></div>
            <div><Button label="Upload CSV" icon="pi pi-upload" severity="success" class="mr-2" @click="uploadData" /></div>
            <div><Dropdown v-model="selectedGraphType" :options="graphTypes" optionLabel="name" placeholder="Select a Table" class="w-full md:w-14rem" /></div>
            <div><Button label="Save" icon="pi pi-save" severity="success" class="mr-2" @click="saveChart" /></div>
        </div>
        <div class="col-12 grid h-full">
            <div class="col-2 h-full">
                <DataTable :value="columns">
                    <Column field="colName" header="Column" sortable></Column>
                    <Column field="type" header="Type"></Column>
                </DataTable>
            </div>
            <div class="col-10">
                <div class="grid">
                    <div class="col-10">
                        Chart Builder
                        <Chart type="bar" :data="chartData" :options="chartOptions" />
                    </div>
                    <div class="col-2">
                        Stats display
                    </div>
                </div>
                <div>
                    Data table
                    <DataTable>

                    </DataTable>
                </div>
            </div>
        </div>
    </div>

</template>

<style>
</style>