<script setup>
import { reactive, ref, onMounted } from 'vue'
import { FilterMatchMode } from 'primevue/api'
import { useToast } from 'primevue/usetoast'
import axios from '@/axiosConfig'

const emit = defineEmits('updateApp')
const toast = useToast()

const currentUser = reactive(JSON.parse(localStorage.getItem('eza-user')))
const showLogin = ref(false)
const users = ref()
const activeUser = ref({})
const newUser = ref(false)
const userDialog = ref(false)
const deleteUserDialog = ref(false)
const submitted = ref(false)

const filters = ref({
    'global': {value: null, matchMode: FilterMatchMode.CONTAINS}
})

onMounted(async () => {
    loadUsers()
})

function openNew() {
    activeUser.value = { viewer: true }
    submitted.value = false
    userDialog.value = true
    newUser.value = true
}

function hideDialog() {
    userDialog.value = false
    submitted.value = false
}

function confirmDeleteUser(user) {
    deleteUserDialog.value = true
    activeUser.value = user
}

function editUser(user) {
    userDialog.value = true
    activeUser.value = {...user}
}

async function saveUser() {
    submitted.value = true
    if (!(activeUser.value.firstName?.trim()
        && activeUser.value.lastName?.trim()
        && activeUser.value.username?.trim()
        && activeUser.value.userEmail?.trim())) { return }
    if (newUser.value === true) {
        try {
            let response = await axios.post('/api/users', activeUser.value)
            toast.add({severity: 'success', summary: 'Successful', detail: 'User created', life: 3000})
        } catch (err) {
            if (err.response?.status === 401) {
                showLogin.value = true
            } else {
                toast.add({severity: 'error', summary: 'Error', detail: 'Unable to create user', life: 3000})
            }
            return
        }
    } else {
        try {
            await axios.put(`/api/users/${activeUser.value.userId}`, activeUser.value)
            toast.add({severity: 'success', summary: 'Successful', detail: 'User updated', life: 3000})
        } catch (err) {
            if (err.response?.status === 401) {
                showLogin.value = true
            } else {
                toast.add({severity: 'error', summary: 'Error', detail: 'Unable to update user', life: 3000})
            }
            return
        }
    }
    userDialog.value = false
    activeUser.value = {}
    loadUsers()
    newUser.value = false
}

async function loadUsers() {
    if (!currentUser.admin) return
    try {
        let response = await axios.get('/api/users')
        users.value = response.data
    } catch (err) {
        if (err.response?.status === 401) { showLogin.value = true }
        else {
            toast.add({severity: 'error', summary: 'Error', detail: 'Unable to load users', life: 3000})
        }
    }
}

async function deleteUser() {
    try {
        let response = await axios.delete(`/api/users/${activeUser.value.userId}`)
        deleteUserDialog.value = false
        toast.add({severity: 'success', summary: 'Successful', detail: 'User deleted', life: 3000})
        loadUsers()
    } catch (err) {
        if (err.response?.status === 401) { showLogin.value = true }
    }
}
</script>

<template>
    <div>
        <div v-if="!currentUser.admin" class="flex p-3">
            <Unauthorized />
        </div>
        <div v-else>
            <Toolbar class="mb-4">
                <template #start>
                    <Button label="New User" icon="pi pi-plus" class="mr-2" @click="openNew" />
                </template>
            </Toolbar>
    
            <DataTable :value="users" dataKey="id" scrollable scrollHeight="flex"
                :paginator="true" :rows="10" :filters="filters"
                paginatorTemplate="FirstPageLink PrevPageLink PageLinnks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown" :rowsPerPageOptions="[10,25,50]"
                currentPageReportsTemplate="Showing {first} to {last} of {totalRecords} users">
                <template #header>
                    <div class="flex flex-wrap gap-2 align-items-center justify-content-between">
                        <h2 class="m-0">User Administration</h2>
                        <span class="p-input-icon-left">
                            <i class="pi pi-search" />
                            <InputText v-model="filters['global'].value" placeholder="Search..." />
                        </span>
                    </div>
                </template>
                <Column field="username" header="Username" sortable></Column>
                <Column field="lastName" header="Last Name" sortable></Column>
                <Column field="firstName" header="First Name" sortable></Column>
                <Column field="middleName" header="Middle Name" sortable></Column>
                <Column field="userEmail" header="Email" sortable></Column>
                <Column field="admin" header="Administrator" style="width: 8rem">
                    <template #body="slotProps">
                        <Checkbox :modelValue="slotProps.data.admin" :binary="true" :readonly="true" />
                    </template>
                </Column>
                <Column field="viewer" header="Viewer" style="width: 8rem">
                    <template #body="slotProps">
                        <Checkbox :modelValue="slotProps.data.viewer" :binary="true" :readonly="true" />
                    </template>
                </Column>
                <Column field="chart_builder" header="Chart Builder" style="width: 8rem">
                    <template #body="slotProps">
                        <Checkbox :modelValue="slotProps.data.chartBuilder" :binary="true" :readonly="true" />
                    </template>
                </Column>
                <Column field="dash_builder" header="Dashboard Builder" style="width: 8rem">
                    <template #body="slotProps">
                        <Checkbox :modelValue="slotProps.data.dashBuilder" :binary="true" :readonly="true" />
                    </template>
                </Column>
                <Column field="connections" header="Data Connections" style="width: 8rem">
                    <template #body="slotProps">
                        <Checkbox :modelValue="slotProps.data.connections" :binary="true" :readonly="true" />
                    </template>
                </Column>
                <Column style="min-width: 8rem">
                    <template #body="slotProps">
                        <Button icon="pi pi-pencil" outlined rounded class="mr-2" @click="editUser(slotProps.data)" />
                        <Button icon="pi pi-trash" outlined rounded severity="danger" @click="confirmDeleteUser(slotProps.data)" />
                    </template>
                </Column>
            </DataTable>
    
            <Dialog v-model:visible="userDialog" :style="{width: '450px'}" header="User Details" :modal="true" class="p-fluid">
                <div class="field">
                    <label for="firstName">First Name*</label>
                    <InputText id="firstName" v-model.trim="activeUser.firstName" required="true" autofocus :class="{'p-invalid': submitted && !activeUser.firstName}" />
                    <small class="p-error" v-if="submitted && !activeUser.firstName">First name is required</small>
                </div>
                <div class="field">
                    <label for="middleName">Middle Name</label>
                    <InputText id="middleName" v-model.trim="activeUser.middleName" />
                </div>
                <div class="field">
                    <label for="lastName">Last Name*</label>
                    <InputText id="lastName" v-model.trim="activeUser.lastName" required="true" :class="{'p-invalid': submitted && !activeUser.lastName}" />
                    <small class="p-error" v-if="submitted && !activeUser.lastName">Last name is required</small>
                </div>
                <div class="field">
                    <label for="username">Username*</label>
                    <InputText id="username" v-model.trim="activeUser.username" required="true" :class="{'p-invalid': submitted && !activeUser.username}" />
                    <small class="p-error" v-if="submitted && !activeUser.username">Username is required</small>
                </div>
                <div class="field">
                    <label for="userEmail">Email*</label>
                    <InputText id="userEmail" v-model.trim="activeUser.userEmail" required="true" :class="{'p-invalid': submitted && !activeUser.userEmail}" />
                    <small class="p-error" v-if="submitted && !activeUser.userEmail">Email is required</small>
                </div>
                <div class="field">
                    <label for="password">Password</label>
                    <Password id="password" v-model.trim="activeUser.password" toggleMask />
                </div>
                <div class="field">
                    <label class="mb-3">Permissions</label>
                    <div class="formgrid grid">
                        <div class="field-checkbox col-6">
                            <Checkbox v-model="activeUser.admin" :binary="true"></Checkbox>
                            <label for="">Administrator</label>
                        </div>
                        <div class="field-checkbox col-6">
                            <Checkbox v-model="activeUser.viewer" :binary="true"></Checkbox>
                            <label for="">Viewer</label>
                        </div>
                        <div class="field-checkbox col-6">
                            <Checkbox v-model="activeUser.chartBuilder" :binary="true"></Checkbox>
                            <label for="">Chart Builder</label>
                        </div>
                        <div class="field-checkbox col-6">
                            <Checkbox v-model="activeUser.dashBuilder" :binary="true"></Checkbox>
                            <label for="">Dashboard Builder</label>
                        </div>
                        <div class="field-checkbox col-6">
                            <Checkbox v-model="activeUser.connections" :binary="true"></Checkbox>
                            <label for="">Data Connections</label>
                        </div>
                    </div>
                </div>
                <template #footer>
                    <Button label="Cancel" icon="pi pi-times" @click="hideDialog" />
                    <Button label="Save" icon="pi pi-check" @click="saveUser" />
                </template>
            </Dialog>
    
            <ConfirmDelete v-model="deleteUserDialog" :match="activeUser.username" @delete="deleteUser"></ConfirmDelete>
        </div>
        <Login v-model="showLogin" title="Session Timed Out" @login="showLogin = false; loadUsers(); emit('updateApp')"></Login>
    </div>
</template>

<style>
tr[data-p-highlight="true"] {
    background-color: var(--highlight-bg);
}
</style>