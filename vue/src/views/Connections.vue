<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useToast } from  'primevue/usetoast'
import axios from '@/axiosConfig'
import DataUpload from '@/components/dialogs/DataUpload.vue'


const emit = defineEmits('updateApp')
const toast = useToast()

const currentUser = reactive(JSON.parse(localStorage.getItem('eza-user')))

const showLogin = ref(false)
const showUploadModal = ref(false)
const connectionDialog = ref(false)
const deleteSourceDialog = ref(false)

const activeSource = ref({})
const uploadSources = ref([])
const connectionSources = ref()

async function loadSources() {
    try{
        let response = await axios.get('/api/sources')
        let sources = response.data
        uploadSources.value = sources.filter(src => src.sourceType === 'upload')
        connectionSources.value = sources.filter(src => src.sourceType === 'connection')
        console.log(response.data)
    } catch (err) {
        console.log(err)
    }
}

function confirmDeleteSource(source) {
    console.log(source)
    deleteSourceDialog.value = true
    activeSource.value = source
}

function deleteSource() {
    toast.add({severity: 'warn', summary: 'Warning', detail: 'Delete Data Source clicked', life: 3000})
    deleteSourceDialog.value = false
}

function deleteConnection() {
    toast.add({severity: 'warn', summary: 'Warning', detail: 'Delete Connection clicked', life: 3000})
}

function newConnection() {
    toast.add({severity: 'info', summary: 'Successful', detail: 'New Connection clicked', life: 3000})
}

onMounted(() => {
    loadSources()
})
</script>

<template>
    <div>
        <div v-if="!(currentUser.admin || currentUser.connections)" class="flex p-3">
            <Unauthorized />
        </div>
        <div v-else class="grid h-full justify-content-between px-2">
            <div class="col-6 flex flex-column gap-2">
                <h2>Uploaded Data</h2>
                <div class="flex flex-row justify-content-start">
                    <!-- <div><Button label="Delete Data Source" @click="deleteSource" /></div> -->
                    <div><Button label="Upload Data" icon="pi pi-plus" @click="showUploadModal = true" /></div>
                </div>
                <DataTable :value="uploadSources">
                    <Column field="sourceLabel"></Column>
                    <Column style="width: 8rem">
                    <template #body="slotProps">
                        <div class="flex justify-content-center">
                            <Button icon="pi pi-trash" outlined rounded severity="danger" @click="confirmDeleteSource(slotProps.data)" />
                        </div>
                    </template>
                </Column>
                </DataTable>
            </div>
            <div class="col-6 flex flex-column gap-2">
                <h2>Database Connections</h2>
                <div class="flex flex-row justify-content-start">
                    <div><Button label="New DB Connection" icon="pi pi-plus" @click="newConnection" /></div>
                </div>
                <Skeleton height="100%"></Skeleton>
                <DataTable :value="connectionSources">
                    <Column field="sourceLabel"></Column>
                    <Column style="width: 8rem">
                    <template #body="slotProps">
                        <div class="flex justify-content-center">
                            <Button icon="pi pi-pencil" outlined rounded class="mr-2" @click="editSource(slotProps.data)" />
                            <Button icon="pi pi-trash" outlined rounded severity="danger" @click="confirmDeleteSource(slotProps.data)" />
                        </div>
                    </template>
                </Column>
                </DataTable>
            </div>
            <ConfirmDelete v-model="deleteSourceDialog" :match="activeSource.sourceLabel" @delete="deleteSource"></ConfirmDelete>
            <DataUpload v-model="showUploadModal" @timeout401="showLogin = true"></DataUpload>
        </div>
        <Login v-model="showLogin" title="Session Timed Out" @login="showLogin = false; emit('updateApp')"></Login>
    </div>
</template>

<style>
</style>