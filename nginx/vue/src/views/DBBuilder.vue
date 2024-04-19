<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useToast } from  'primevue/usetoast'
import axios from '@/axiosConfig'
import EZChart from '@/components/EZChart.vue'

const emit = defineEmits('updateApp')
const route = useRoute()
const toast = useToast()

const currentUser = ref(JSON.parse(localStorage.getItem('eza-user')) ?? {})
const showLogin = ref(false)
const loginTitle = ref('Session Timed Out')
const submitted = ref(false)

const chartRows = ref([])
const chartList = ref([])
const dashId = ref(null)
const dashOwner = ref(currentUser.value['user_id'])
const dashTitle = ref('')
const layout = ref([])
const enableAddRow = computed(() => {
    let numRows = layout.value.length
    if (layout.value[0]) {
        return (layout.value.length > 0 && layout.value[numRows - 1].length > 0)
    }
    return false
})

const dashSize = computed(() => {
    let temp = []
    for (let row of layout.value) {
        temp.push(row.length)
    }
    return temp
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
        dashOwner.value = currentUser.value['user_id']
    }
    loginTitle.value = 'Session Timed Out'
    await getCharts()
    if ('dash' in route.query) {
        await loadDashboard(route.query.dash)
        dashId.value = route.query.dash
    }
}

async function getCharts() {
    try {
        let response = await axios.get(`/api/charts/`)
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
            let response = axios.post(`/api/dashboards/`, dashboard)
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
    dashOwner.value = dash.owner ?? currentUser.value['user_id']
    dashTitle.value = dash.title
    layout.value = dash.layout
}

function addRow() {
    if (enableAddRow.value) { layout.value.push([]) }
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
    loadPage()
})
</script>

<template>
    <div>
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
                    <Button icon="pi pi-save" label="Save" @click="saveDashboard" />
                </div>
            </div>
            <div v-for="(row, index) of layout" key class="col-12 grid h-full align-items-stretch" ref="chartRows">
                <div class="col-11 grid justify-content-around">
                    <div v-for="(chart, col) of row" :class="`col-${12 / row.length} ${layout.length > 1 ? 'dash-row-multi' : 'dash-row'}`">
                        <div v-if="chart.id" class="w-full h-full">
                            <div class="flex justify-content-between">
                                <Dropdown v-model="layout[index][col]" :options="chartList" optionLabel="title" placeholder="Select a Chart"></Dropdown>
                                <Button icon="pi pi-times" outlined rounded severity="danger" class="mr-2" @click="removeChart(index, col)" />
                            </div>
                            <div style="height: 90%">
                                <EZChart :dashSize="dashSize" v-model="chart.id"></EZChart>
                            </div>
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
                </div>
            </div>
            <div class="flex justify-content-center w-full">
                <Button v-if="enableAddRow" icon="pi pi-plus" outlined rounded label="Add Row" class="mr-2" @click="addRow()" />
            </div>
        </div>
        <Login v-model="showLogin" :title="loginTitle" @login="showLogin = false; emit('updateApp')"></Login>
    </div>
</template>

<style>
.dash-row {
    /* max-height: calc(100vh - 20rem); */
    height: 80vh;
}

.dash-row-multi {
    height: 60vh;
}
</style>