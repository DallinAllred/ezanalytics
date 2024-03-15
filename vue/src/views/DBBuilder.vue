<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useToast } from  'primevue/usetoast'
import axios from '@/axiosConfig'
import EZChart from '@/components/EZChart.vue'
// import Login from '@/components/dialogs/Login.vue'
// import Unauthorized from '@/components/Unauthorized.vue'

const route = useRoute()
const toast = useToast()

const currentUser = JSON.parse(localStorage.getItem('eza-user'))

const showLogin = ref(false)

const chartList = ref([])
const dashId = ref(null)
const dashOwner = ref(currentUser['user_id'])
const dashTitle = ref('')

const layout = ref([])
const enableAddRow = computed(() => {
    let numRows = layout.value.length
    if (layout.value[0]) {
        return (layout.value.length > 0 && layout.value[numRows - 1].length > 0)
    }
    return false
})


const submitted = ref(false)

let saving = false

async function loadPage() {
    await getCharts()
    if ('dash' in route.query) {
        await loadDashboard(route.query.dash)
        dashId.value = route.query.dash
    }
}

async function getCharts() {
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
        owner: dashOwner.value,
        layout: layout.value
    }
    if (dashId.value) {
        try {
            let response = axios.put(`/api/dashboards/${dashId.value}`, dashboard)
            toast.add({severity: 'success', summary: 'Success', detail: 'Dashboard saved', life: 3000})
        } catch (err) {
            if (err.response?.status === 401) {
                showLogin.value = true
                saving = true
            }
            toast.add({severity: 'error', summary: 'Error', detail: 'An error occurred while saving the dashboard', life: 3000})
        }
    } else {
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
    }
    submitted.value = false
}

async function loadDashboard(dashId) {
    let dash = {}
    try {
        let response = await axios.get(`/api/dashboards/${dashId}`)
        dash = response.data
    } catch (err) {
        if (err.response.status === 401) {
            showLogin.value = true
            saving = false
        }
        toast.add({severity: 'error', summary: 'Dashboard Not Found', detail: `Unable to find dashboard ${dashId}`, life: 3000})
        return
    }
    dashOwner.value = dash.owner ?? currentUser['user_id']
    dashTitle.value = dash.title
    layout.value = dash.layout
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
    loadPage()
})

watch(showLogin, () => {
    if (showLogin.value || saving) return
    getCharts()
})
</script>

<template>
    <div v-if="!(currentUser.admin || currentUser['dash_builder'])" class="flex p-3">
        <Unauthorized />
    </div>
    <div v-else class="grid">
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
        <Login v-model="showLogin" title="Session Timed Out" @login="showLogin = false"></Login>
    </div>
</template>

<style>
.dash-row {
    min-height: 40vh;
}
</style>