<script setup>
import { computed, onMounted, ref, watch} from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useToast } from  'primevue/usetoast';
import axios from '@/axiosConfig'
import EZDash from '@/components/EZDash.vue'

const emit = defineEmits('updateApp')
const route = useRoute()
const router = useRouter()
const toast = useToast()

const currentUser = ref(JSON.parse(localStorage.getItem('eza-user')) ?? {})
const showLogin = ref(false)
const loginTitle = ref('Session Timed Out')
const editor = computed(() => {
    if (currentUser.value.admin || currentUser.value['dash_builder']) return true
    return false
})

const deleteDashDialog = ref(false)
const dashList = ref([])
const selectedDash = ref({title: null, id: null})

async function loadPage() {
    if (!currentUser.value.username) {
        currentUser.value = JSON.parse(localStorage.getItem('eza-user')) ?? {}
        if (!currentUser.value?.username) {
            loginTitle.value = null
            showLogin.value = true
            return
        }
    }
    loginTitle.value = 'Session Timed Out'
    await loadDashboards()
    if ('dash' in route.query) {
        let queryDash = dashList.value.filter(dash => dash.id == route.query.dash)
        selectedDash.value = queryDash[0]
    }
}

async function loadDashboards() {
    try {
        let response = await axios.get(`/api/dashboards/`)
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

watch(selectedDash, () => {
    if (selectedDash.value.id) {
        let query = {'dash': selectedDash.value.id}
        router.replace({ path: route.path, query: query})
    }
})

onMounted(async () => {
    loadPage()
})
</script>

<template>
    <div>
        <div v-if="!(currentUser.admin || currentUser.viewer)" class="flex p-3">
            <Unauthorized />
        </div>
        <div v-else>
            <Toolbar class="mb-2">
                <template #start>
                    <Button :disabled="!editor" icon="pi pi-plus" label="New Dashboard" @click="newDashboard" />
                </template>
                <template #center>
                    <Dropdown v-model="selectedDash" :options="dashList" filter optionLabel="title" placeholder="Select a Dashboard">
                        <template #value="slotProps">
                            <div v-if="slotProps.value.title" class="flex">
                                <div>{{ slotProps.value.title }} ({{ slotProps.value.id }})</div>
                            </div>
                            <div v-else>
                                {{ slotProps.placeholder }}
                            </div>
                        </template>
                        <template #option="slotProps">
                            <div class="flex flex-column">
                                <div>{{ slotProps.option.title }}</div>
                                <small>{{ slotProps.option.id }}</small>
                            </div>
                        </template>
                    </Dropdown>
                </template>
                <template #end>
                    <div class="flex gap-2">
                        <Button :disabled="!editor || !(selectedDash && selectedDash.id)" icon="pi pi-pencil" label="Edit Dashboard" @click="editDashboard" />
                        <Button :disabled="!editor || !(selectedDash && selectedDash.id)" severity="danger" icon="pi pi-times" label="Delete Dashboard" @click="deleteDashDialog = true" />
                    </div>
                </template>
            </Toolbar>
            <div class="flex flex-column gap-2" id="dash-container">
                <div class="flex justify-content-center">
                    <h2>{{ selectedDash.title }}</h2>
                </div>
                <EZDash v-if="selectedDash && selectedDash.id" v-model="selectedDash.id" @timeout401="showLogin = true"></EZDash>
            </div>
            <ConfirmDelete v-model="deleteDashDialog" :match="selectedDash.title" @delete="deleteDash"></ConfirmDelete>
        </div>
        <Login v-model="showLogin" :title="loginTitle" @login="showLogin = false; loadPage(); emit('updateApp')"></Login>
    </div>
</template>

<style>
#dash-container {
    height: calc(100vh - 10rem);
}
</style>