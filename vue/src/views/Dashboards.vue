<script setup>
import { onMounted, ref} from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

import { useToast } from  'primevue/usetoast';

import ConfirmDelete from '@/components/dialogs/ConfirmDelete.vue';
import EZDash from '@/components/EZDash.vue'

const router = useRouter()
const toast = useToast()

const deleteDashDialog = ref(false)
const dashList = ref([])
const selectedDash = ref({title: null, id: null})

async function loadDashboards() {
    let response = await axios.get(`http://localhost:5050/api/dashboards`)
    dashList.value = response.data
}

function newDashboard() {
    router.push('/dbBuilder')
}

function editDashboard() {
    if (selectedDash.value) {
        router.push(`/dbBuilder?dash=${selectedDash.value.id}`)
    }
}

async function deleteDash() {
    try {
        let response = await axios.delete(`http://localhost:5050/api/dashboards/${selectedDash.value.id}`)
        toast.add({severity: 'success', summary: 'Success', detail: `Dashboard "${selectedDash.value.title}" has been deleted`, life: 3000})
        selectedDash.value = {title: null, id: null}
        deleteDashDialog.value = false
        loadDashboards()
    } catch {
        toast.add({severity: 'error', summary: 'Error', detail: `Error while deleting "${selectedDash.value.title}"`, life: 3000})
    }
}

onMounted(async () => {
    await loadDashboards()
    console.log(dashList.value)
    console.log(router)
    if (router.query && 'dash' in router.query) {
        let queryDash = dashList.value.filter(dash => dash.id == router.query.dash)
        selectedDash.value = queryDash[0]
    }
})

</script>

<template>
    <div class="grid h-full">
        <div class="col-2 flex flex-column gap-2">
            <div class="h-full">
                <DataTable v-model:selection="selectedDash" :value="dashList" selectionMode="single"
                scrollable class="h-full" dataKey="id">
                    <Column field="title" header="Dashboard"></Column>
                    <Column field="id" header="ID"></Column>
                </DataTable>
            </div>
            <Button label="New Dashboard" @click="newDashboard" />
        </div>
        <div class="col-10 flex flex-column gap-2" id="dash-container">
            <div class="flex justify-content-between">
                <Button severity="danger" label="Delete Dashboard" @click="deleteDashDialog = true" v-if="selectedDash && selectedDash.id" />
                <Button label="Edit Dashboard" @click="editDashboard" v-if="selectedDash && selectedDash.id" />
            </div>
            <div class="flex justify-content-center">
                <h2>{{ selectedDash.title }}</h2>
            </div>
            <EZDash v-if="selectedDash && selectedDash.id" v-model="selectedDash.id"></EZDash>
        </div>
    </div>
    <ConfirmDelete v-model="deleteDashDialog" :match="selectedDash.title" @delete="deleteDash"></ConfirmDelete>

</template>

<style>
#dash-container {
    height: calc(100vh - 4.5rem);
    overflow: scroll;
}
</style>