<script setup>
import { computed, onMounted, reactive, ref, watch} from 'vue'
import { useRouter } from 'vue-router'
import axios from '@/axiosConfig'
import { useToast } from  'primevue/usetoast';
import EZDash from '@/components/EZDash.vue'
// import ConfirmDelete from '@/components/dialogs/ConfirmDelete.vue';
// import Login from '@/components/dialogs/Login.vue'
// import Unauthorized from '@/components/Unauthorized.vue';

const router = useRouter()
const toast = useToast()

const currentUser = reactive(JSON.parse(localStorage.getItem('eza-user')))
const editor = computed(() => {
    if (currentUser.admin || currentUser['dash_builder']) return true
    return false
})

const showLogin = ref(false)
const deleteDashDialog = ref(false)
const dashList = ref([])
const selectedDash = ref({title: null, id: null})

async function loadPage() {
    await loadDashboards()
    if (router.query && 'dash' in router.query) {
        let queryDash = dashList.value.filter(dash => dash.id == router.query.dash)
        selectedDash.value = queryDash[0]
    }
}

async function loadDashboards() {
    try {
        let response = await axios.get(`/api/dashboards`)
        dashList.value = response.data
    } catch (err) {
        if (err.response?.status === 401) { showLogin.value = true }
    }
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
        let response = await axios.delete(`/api/dashboards/${selectedDash.value.id}`)
        toast.add({severity: 'success', summary: 'Success', detail: `Dashboard "${selectedDash.value.title}" has been deleted`, life: 3000})
        selectedDash.value = {title: null, id: null}
        deleteDashDialog.value = false
        loadDashboards()
    } catch (err) {
        if (err.response?.status === 401) {
            showLogin.value = true
            return
        }
        toast.add({severity: 'error', summary: 'Error', detail: `Error while deleting "${selectedDash.value.title}"`, life: 3000})
    }
}

onMounted(async () => {
    loadPage()
})

watch(showLogin, () => {
    if (showLogin.value) return
    loadPage()
})

</script>

<template>
    <div v-if="!(currentUser.admin || currentUser.viewer)" class="flex p-3">
        <Unauthorized />
    </div>
    <div v-else class="grid h-full">
        <div class="col-2 flex flex-column gap-2">
            <div class="h-full">
                <DataTable v-model:selection="selectedDash" :value="dashList" selectionMode="single"
                scrollable class="h-full" dataKey="id">
                    <Column field="title" header="Dashboard"></Column>
                    <Column field="id" header="ID"></Column>
                </DataTable>
            </div>
            <Button :disabled="!editor" label="New Dashboard" @click="newDashboard" />
        </div>
        <div class="col-10 flex flex-column gap-2" id="dash-container">
            <div class="flex justify-content-between">
                <Button :disabled="!editor" severity="danger" label="Delete Dashboard" @click="deleteDashDialog = true" v-if="selectedDash && selectedDash.id" />
                <Button :disabled="!editor" label="Edit Dashboard" @click="editDashboard" v-if="selectedDash && selectedDash.id" />
            </div>
            <div class="flex justify-content-center">
                <h2>{{ selectedDash.title }}</h2>
            </div>
            <EZDash v-if="selectedDash && selectedDash.id" v-model="selectedDash.id" @timeout401="showLogin = true"></EZDash>
        </div>
        <ConfirmDelete v-model="deleteDashDialog" :match="selectedDash.title" @delete="deleteDash"></ConfirmDelete>
        <Login v-model="showLogin" title="Session Timed Out" @login="showLogin = false"></Login>
    </div>
</template>

<style>
#dash-container {
    height: calc(100vh - 4.5rem);
    overflow: scroll;
}
</style>