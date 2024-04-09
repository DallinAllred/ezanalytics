<script setup>
import { onMounted, reactive, ref, watch } from 'vue'
import { useToast } from  'primevue/usetoast'
import axios from '@/axiosConfig'
import DataUpload from '@/components/dialogs/DataUpload.vue'


const emit = defineEmits('updateApp')
const toast = useToast()

const DISALLOWED = ['ALTER', 'INSERT', 'DELETE', 'DROP', 'TABLE', 'UPDATE']

const currentUser = ref(JSON.parse(localStorage.getItem('eza-user')))

// Modals
const showLogin = ref(false)
const showUploadModal = ref(false)
const showConnectionModal = ref(false)
const deleteSourceDialog = ref(false)
const submitted = ref(false)

// Source Info
const activeSource = ref({
    name: 'TestConn',
    engine: {name: 'MySQL', value: 'mysql'},
    dbHost: '192.168.100.116',
    dbPort: 3306,
    database: 'external_data',
    dbUser: 'root',
    dbPassword: 'password1',
    query: 'SELECT * FROM sample_data;'
})
const uploadSources = ref([])
const connectionSources = ref()
const noSelect = ref(false)
const unsafeQuery = ref(false)
const confirmUnsafe = ref(false)

const databaseEngines = ref([
    {name: 'MariaDB', value: 'mariadb'},
    {name: 'MySQL', value: 'mysql'},
    {name: 'PostgreSQL', value: 'postgres'}
])

async function loadSources() {
    try{
        let response = await axios.get('/api/sources')
        let sources = response.data
        uploadSources.value = sources.filter(src => src.sourceType === 'upload')
        connectionSources.value = sources.filter(src => src.sourceType === 'external')
    } catch (err) {
        if (err.response?.status === 401) { showLogin.value = true }
        console.log(err)
    }
}

function confirmDeleteSource(source) {
    activeSource.value = source
    deleteSourceDialog.value = true
    activeSource.value = source
}

async function deleteSource() {
    try {
        let response = await axios.delete(`/api/sources/${activeSource.value.sourceId}`)
        let sourceName = response.data.name
        toast.add({severity: 'success', summary: 'Success', detail: `${sourceName} has been deleted`, life: 3000})
        loadSources()
    } catch (err) {
        if (err.response?.status === 401) { showLogin.value = true }
        console.log('Other error', err)
    }
    deleteSourceDialog.value = false
}

async function editConnection(source) {
    if (source == null) {
        activeSource.value = {
            name: '',
            engine: null,
            dbHost: '',
            dbPort: null,
            database: '',
            dbUser: '',
            dbPassword: '',
            query: ''
        }
    } else {
        let response = await axios.get(`/api/sources/conndetails/${source.sourceId}`)
        let connData = response.data
        let engine = connData['db_type']
        engine = databaseEngines.value.filter(eng => eng.value == engine)
        engine = engine.length > 0 ? engine[0] : null
        activeSource.value = {
            id: source.sourceId,
            name: source.sourceLabel,
            engine: engine,
            dbHost: connData['connection_host'] ?? '',
            dbPort: connData['connection_port'] ?? null,
            database: connData['db_name'] ?? '',
            dbUser: connData['connection_user'] ?? '',
            dbPassword: connData['connection_pw'] ?? '',
            query: connData['query'] ?? ''
        }
    }
    showConnectionModal.value = true
}

async function saveConnection() {
    submitted.value = true
    noSelect.value = false
    unsafeQuery.value = false
    if (!(activeSource.value.name
        && activeSource.value.engine
        && activeSource.value.dbHost
        && activeSource.value.dbPort
        && activeSource.value.database
        && activeSource.value.dbUser
        && activeSource.value.dbPassword
        && activeSource.value.query)) { return }
    let query = activeSource.value.query.toUpperCase()
    let temp = query.split(' ')
    if (temp[0] != 'SELECT') {
        noSelect.value = true
        return
    }
    query = query.replace(/(\r\n|\n\r|\n)/gm, ' ')
    for (let word of DISALLOWED) {
        if (confirmUnsafe.value) break
        if (query.includes(word)) {
            unsafeQuery.value = true
            return
        }
    }
    activeSource.value.query = activeSource.value.query.replace(/(\r\n|\n\r|\n)/gm, ' ')

    let data = {
        user: currentUser.value['user_id'],
        ...activeSource.value
    }
    data.engine = activeSource.value.engine.value
    if (activeSource.value.id) {
        try {
            let response = await axios.put(`/api/sources/connection/${activeSource.value.id}`, data)
            toast.add({severity: 'success', summary: 'Success', detail: `Connection saved`, life: 3000})
            loadSources()
            showConnectionModal.value = false
        } catch (err) {
            if (err.response?.status === 401) {
                showLogin.value = true
                return
            }
            toast.add({severity: 'error', summary: 'Error', detail: `Unable to save connection`, life: 3000})
            console.log('Other error', err)
        }
    } else {
        try {
            let response = await axios.post('/api/sources/connection', data)
            toast.add({severity: 'success', summary: 'Success', detail: `Connection saved`, life: 3000})
            loadSources()
            showConnectionModal.value = false
        } catch (err) {
            if (err.response?.status === 401) {
                showLogin.value = true
                return
            }
            toast.add({severity: 'error', summary: 'Error', detail: `Unable to save connection`, life: 3000})
            console.log('Other error', err)
        }
    }

}

function hideConnectionDialog() {
    activeSource.value = {}
    showConnectionModal.value = false
}

onMounted(() => {
    loadSources()
})

watch(showUploadModal, () => {
    if (!showUploadModal.value) loadSources()
})

watch(showConnectionModal, () => {
    if (showConnectionModal) return
    activeSource.value =  {}
    unsafeQuery.value = false
    confirmUnsafe.value = true
    submitted.value = false
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
                    <div><Button label="New DB Connection" icon="pi pi-plus" @click="editConnection(null)" /></div>
                    <div class="px-2"><Button label="Create sample connection" icon="pi pi-plus" @click="saveConnection()" /></div>
                </div>
                <DataTable :value="connectionSources">
                    <Column field="sourceLabel"></Column>
                    <Column style="width: 8rem">
                    <template #body="slotProps">
                        <div class="flex justify-content-center">
                            <Button icon="pi pi-pencil" outlined rounded class="mr-2" @click="editConnection(slotProps.data)" />
                            <Button icon="pi pi-trash" outlined rounded severity="danger" @click="confirmDeleteSource(slotProps.data)" />
                        </div>
                    </template>
                </Column>
                </DataTable>
            </div>
            <ConfirmDelete v-model="deleteSourceDialog" :match="activeSource.sourceLabel" @delete="deleteSource"></ConfirmDelete>
            <DataUpload v-model="showUploadModal" @timeout401="showLogin = true"></DataUpload>

            <Dialog v-model:visible="showConnectionModal" :style="{width: '600px'}" header="Connection Editor" :modal="true" class="p-fluid">
                <div class="field">
                    <label for="name">Connection Name</label>
                    <InputText id="name" v-model.trim="activeSource.name" />
                </div>
                <Divider />
                <div class="flex gap-5">
                    <div class="flex flex-column w-full">
                        <div class="field">
                            <label for="engine">Database Engine</label>
                            <Dropdown v-model="activeSource.engine" :options="databaseEngines" optionLabel="name" placeholder="Select a database engine" />
                            <small class="p-error" v-if="submitted && !activeSource.engine">An engine is required</small>
                        </div>
                        <div class="field">
                            <label for="hostname">Host</label>
                            <InputText id="hostname" v-model.trim="activeSource.dbHost" />
                            <small class="p-error" v-if="submitted && !activeSource.dbHost">Hostname is required</small>
                        </div>
                        <div class="field">
                            <label for="port">Port</label>
                            <InputNumber id="port" v-model.trim="activeSource.dbPort" :useGrouping="false" />
                            <small class="p-error" v-if="submitted && !activeSource.dbPort">Port is required</small>
                        </div>
                    </div>
                    <div class="flex flex-column w-full">
                        <div class="field">
                            <label for="database">Database Name</label>
                            <InputText id="port" v-model.trim="activeSource.database" />
                            <small class="p-error" v-if="submitted && !activeSource.database">Port is required</small>
                        </div>
                        <div class="field">
                            <label for="user">User</label>
                            <InputText id="user" v-model.trim="activeSource.dbUser" />
                            <small class="p-error" v-if="submitted && !activeSource.dbUser">Database user is required</small>
                        </div>
                        <div class="field">
                            <label for="password">Password</label>
                            <InputText id="password" v-model.trim="activeSource.dbPassword" />
                            <small class="p-error" v-if="submitted && !activeSource.dbPassword">Database password is required</small>
                        </div>
                    </div>
                </div>
                <!-- <div>
                    <Button label="Test Connection" />
                </div> -->
                <Divider />
                <div class="field">
                    <label for="query">Query</label>
                    <Textarea v-model="activeSource.query" rows="10" cols="100"/>
                    <small class="p-error" v-if="submitted && (!activeSource.query || noSelect)">A SELECT query is required</small>
                    <div class="flex gap-5" v-if="unsafeQuery">
                        <div class="flex align-items-center w-full">
                            <Message severity="warn">
                                This query appears to contain potentially dangerous keywords.
                                Confirm the query contents before continueing.
                            </Message>
                        </div>
                        <div class="flex align-items-center justify-content-center w-full">
                            <ToggleButton v-model="confirmUnsafe" severity='danger' 
                                offLabel="Yes, the query is okay" onLabel="Potentially unsafe query approved."
                                onIcon="pi pi-check"/>
                        </div>
                    </div>
                </div>
                <template #footer>
                    <Button label="Cancel" icon="pi pi-times" @click="hideConnectionDialog" />
                    <Button label="Save" icon="pi pi-check" @click="saveConnection" :disabled="!confirmUnsafe && unsafeQuery" />
                </template>

            </Dialog>

        </div>
        <Login v-model="showLogin" title="Session Timed Out" @login="showLogin = false; emit('updateApp')"></Login>
    </div>
</template>

<style>
</style>