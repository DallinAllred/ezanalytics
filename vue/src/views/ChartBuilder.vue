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

const chartData = ref({
        labels: ['Q1', 'Q2', 'Q3', 'Q4'],
        datasets: [
            {
                label: 'Sales',
                data: [540, 325, 702, 620],
                backgroundColor: ['rgba(249, 115, 22, 0.2)', 'rgba(6, 182, 212, 0.2)', 'rgb(107, 114, 128, 0.2)', 'rgba(139, 92, 246 0.2)'],
                borderColor: ['rgb(249, 115, 22)', 'rgb(6, 182, 212)', 'rgb(107, 114, 128)', 'rgb(139, 92, 246)'],
                borderWidth: 1
            }
        ]
    });
const chartOptions = ref({
        plugins: {
            legend: {
                labels: {
                    color: documentStyle.getPropertyValue('--text-color')
                }
            }
        },
        scales: {
            x: {
                ticks: {
                    color: documentStyle.getPropertyValue('--text-color-secondary')
                },
                grid: {
                    color: documentStyle.getPropertyValue('--surface-border')
                }
            },
            y: {
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