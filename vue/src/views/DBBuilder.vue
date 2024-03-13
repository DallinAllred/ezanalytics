<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useToast } from  'primevue/usetoast'
import axios from '@/axiosConfig'
import Login from '@/components/dialogs/Login.vue'

import EZChart from '@/components/EZChart.vue'

const toast = useToast()

const showLogin = ref(false)

const chartList = ref([])
const dashTitle = ref('')

const layout = ref([])
const enableAddRow = computed(() => {
    let numRows = layout.value.length
    if (layout.value[0]) {
        return (layout.value.length > 0 && layout.value[numRows - 1].length > 0)
    }
    return false
})

const currentUser = ref('admin')

const submitted = ref(false)

let saving = false

async function loadCharts() {
    try {
        let response = await axios.get(`/api/charts`)
        chartList.value = response.data
    } catch (err) {
        if (err.response?.status === 401) {
            showLogin.value = true
            saving = false
        }
    }
}

function saveDashboard() {
    submitted.value = true
    if (!(dashTitle.value.trim()
    && layout.value.length > 0)) { return }
    let dashboard = {
        title: dashTitle.value,
        owner: currentUser.value,
        layout: layout.value
    }
    try {
        let response = axios.post(`/api/dashboards`, dashboard)
        toast.add({severity: 'success', summary: 'Success', detail: 'Dashboard saved', life: 3000})
    } catch (err) {
        if (err.response?.status === 401) {
            showLogin.value = true
            saving = true
        }
        toast.add({severity: 'error', summary: 'Error', detail: 'An error occurred while saving the dashboard', life: 3000})
    }
    submitted.value = false
}
function addRow() {
    if (enableAddRow.value) layout.value.push([])
}
function addChart(row) {
    if (!layout.value[0]) {
        layout.value.push([])
        layout.value[row].push({title: null, id: null})
    }
    else if (layout.value[row].length < 3) {
        layout.value[row].push({title: null, id: null})
    }
}
function removeChart(row, col) {
    layout.value[row].splice(col, 1)
    if (layout.value.length > 1 && layout.value[row].length == 0) {
        layout.value.splice(row, 1)
    }
}

onMounted(() => {
    loadCharts()
})

watch(showLogin, () => {
    if (showLogin.value || saving) return
    loadCharts()
})

</script>

<template>
    <div class="grid">
        <div class="col-12 flex">
            <div class="col-4 col-offset-4 flex flex-column justify-content-center align-items-center gap-2">
                <InputText v-model.trim="dashTitle" type="text" placeholder="Dashboard Title" required="true" :class="{'p-invalid': submitted && !dashTitle}"/>
                <small class="p-error" v-if="submitted && !dashTitle">Title is required.</small>
            </div>
            <div class="col-2 col-offset-2 flex justify-content-end">
                <Button label="Save Dashboard" @click="saveDashboard" />
            </div>
        </div>
        <div v-for="(row, index) of layout" key class="col-12 grid h-full align-items-stretch">
            <div class="col-11 grid justify-content-around">
                <div v-for="(chart, col) of row" :class="`col-${12 / row.length}`" class="dash-row">
                    <div v-if="chart.id">
                        <div class="flex justify-content-between">
                            <Dropdown v-model="layout[index][col]" :options="chartList" optionLabel="title" placeholder="Select a Chart"></Dropdown>
                            <Button icon="pi pi-times" outlined rounded severity="danger" class="mr-2" @click="removeChart(index, col)" />
                        </div>
                        <EZChart v-model="chart.id" height="100%"></EZChart>
                    </div>
                    <div v-else>
                        <div class="flex justify-content-between">
                            <Dropdown v-model="layout[index][col]" :options="chartList" filter optionLabel="title" placeholder="Select a Chart"></Dropdown>
                            <Button icon="pi pi-times" outlined rounded severity="danger" class="mr-2" @click="removeChart(index, col)" />
                        </div>
                        <Skeleton height="100%" width="100%"></Skeleton>
                    </div>
                </div>
            </div>
            <div class="col-1 flex align-items-center justify-content-center">
                <Button icon="pi pi-plus" outlined rounded label="Add Chart" class="mr-2" @click="addChart(index)" :disabled="row.length > 2" />
            </div>
        </div>
        <div v-if="layout.length == 0" class="col-12 grid">
            <div class="col-11 grid gap-2">
                <Skeleton v-if="layout.length == 0" height="100px" width="100%"></Skeleton>
            </div>
            <div class="col-1 flex align-items-center justify-content-center">
                <Button icon="pi pi-plus" outlined rounded label="Add Chart" class="mr-2" @click="addChart(0)" />
                <!-- <Button icon="pi pi-plus" outlined rounded class="mr-2" @click="addChart(row)" /> -->
            </div>
        </div>
        <div class="flex justify-content-center w-full">
            <Button v-if="enableAddRow" icon="pi pi-plus" outlined rounded label="Add Row" class="mr-2" @click="addRow()" />
        </div>
    </div>
    <Login v-model="showLogin" title="Session Timed Out" @login="showLogin = false"></Login>
</template>

<style>
.dash-row {
    min-height: 40vh;
}
</style>