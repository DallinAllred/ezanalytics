<script setup>
import { ref, onMounted } from 'vue'
import { FilterMatchMode } from 'primevue/api'
import { useToast } from 'primevue/usetoast'


const users = ref()
const activeUser = ref({})
const newUser = ref(false)
const userDialog = ref(false)
const deleteUserDialog = ref(false)
const submitted = ref(false)

const toast = useToast()

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
        let response = await fetch(`http://localhost:5050/users/`, {
            method: 'POST',
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(activeUser.value)
        })
        toast.add({severity: 'success', summary: 'Successful', detail: 'User created', life: 3000})
    } else {
        let response = await fetch(`http://localhost:5050/users/${activeUser.value.userId}`, {
            method: 'PUT',
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(activeUser.value)
        })
        toast.add({severity: 'success', summary: 'Successful', detail: 'User updated', life: 3000})
    }
    userDialog.value = false
    activeUser.value = {}
    loadUsers()
    newUser.value = false
}

async function loadUsers() {
    let userData = await fetch('http://localhost:5050/users/')
    userData = await userData.json()
    users.value = userData
}

async function deleteUser() {
    let response = await fetch(`http://localhost:5050/users/${activeUser.value.userId}`, {
        method: 'DELETE'
    })
    deleteUserDialog.value = false
    toast.add({severity: 'success', summary: 'Successful', detail: 'User deleted', life: 3000})
    loadUsers()
}
</script>

<template>
    <div>
        <Toolbar class="mb-4">
            <template #start>
                <Button label="New User" icon="pi pi-plus" severity="success" class="mr-2" @click="openNew" />
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
            <!-- <Column selectionMode="multiple" style="width: 3rem"></Column> -->
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
                <small class="p-error" v-if="submitted && !activeUser.firstName">First name is required.</small>
            </div>
            <div class="field">
                <label for="middleName">Middle Name</label>
                <InputText id="middleName" v-model.trim="activeUser.middleName" autofocus />
            </div>
            <div class="field">
                <label for="lastName">Last Name*</label>
                <InputText id="lastName" v-model.trim="activeUser.lastName" required="true" autofocus :class="{'p-invalid': submitted && !activeUser.lastName}" />
                <small class="p-error" v-if="submitted && !activeUser.lastName">Last name is required.</small>
            </div>
            <div class="field">
                <label for="username">Username*</label>
                <InputText id="username" v-model.trim="activeUser.username" required="true" autofocus :class="{'p-invalid': submitted && !activeUser.username}" />
                <small class="p-error" v-if="submitted && !activeUser.username">Username is required.</small>
            </div>
            <div class="field">
                <label for="userEmail">Email*</label>
                <InputText id="userEmail" v-model.trim="activeUser.userEmail" required="true" autofocus :class="{'p-invalid': submitted && !activeUser.userEmail}" />
                <small class="p-error" v-if="submitted && !activeUser.userEmail">Email is required.</small>
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
                <Button label="Cancel" icon="pi pi-times" text @click="hideDialog" />
                <Button label="Save" icon="pi pi-check" text @click="saveUser" />
            </template>
        </Dialog>

        <Dialog v-model:visible="deleteUserDialog" :style="{width: '450px'}" header="Confirm" :modal="true">
            <div class="confirmation-content">
                <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
                <span v-if="activeUser">Are you sure you want to delete <b>{{ activeUser.username }}</b>?</span>
            </div>
            <template #footer>
                <Button label="No" icon="pi pi-times" text @click="deleteUserDialog = false" />
                <Button label="Yes" icon="pi pi-check" text @click="deleteUser" />
            </template>
        </Dialog>

        <!-- <Dialog v-model:visible="deleteUsersDialog" :style="{width: '450px'}" header="Confirm" :modal="true">
            <div class="confirmation-content">
                <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
                <span v-if="activeUser">Are you sure you want to delete the selected users?</span>
            </div>
            <template #footer>
                <Button label="No" icon="pi pi-times" text @click="deleteUsersDialog = false" />
                <Button label="Yes" icon="pi pi-check" text @click="deleteUsers" />
            </template>
        </Dialog> -->
    </div>
</template>

<!-- <template>
    <div class="grid gap-2 m-0 h-full">
        <div class="flex flex-column col-2 border-solid border-1 border-primary-200 p-2 align-content-center">
            <div class="flex flex-row justify-content-center mb-2">
                <Button icon="pi pi-user-plus" iconPos="right" @click="addUser()" label="New User" />
            </div>
            <div>
                <DataTable :value="users" stripedRows v-model:selection="selectedUser"
                :selection.sync="selectedRow" :selectionMode="newUser ? '' : 'single'"
                @rowSelect="loadUser" rowHover>
                    <Column field="username" header="Username"></Column>
                </DataTable>
            </div>
        </div>
        <div class="flex flex-column justify-content-between col-4 border-solid border-1 border-primary-200 p-3">
            <div class="flex flex-column gap-5">
                <h2>User Information</h2>
                <div class="flex flex-column">
                    <label for="firstName">First Name*</label>
                    <InputText id="firstName" type="text" v-model="activeUser.firstName"></InputText>
                </div>
                <div class="flex flex-column">
                    <label for="middleName">Middle Name</label>
                    <InputText id="middleName" type="text" v-model="activeUser.middleName"></InputText>
                </div>
                <div class="flex flex-column">
                    <label for="lastName">Last Name*</label>
                    <InputText id="lastName" type="text" v-model="activeUser.lastName"></InputText>
                </div>
                <div class="flex flex-column">
                    <label for="email">Email*</label>
                    <InputText id="email" type="text" v-model="activeUser.userEmail"></InputText>
                </div>
                <div class="flex flex-column">
                    <label for="username">Username*</label>
                    <InputText id="username" type="text" v-model="activeUser.username"></InputText>
                </div>
                <div v-if="newUser" class="flex flex-column">
                    <label for="password">Password*</label>
                    <InputText id="password" type="text" v-model="activeUser.password"></InputText>
                    <small id="password-help">Enter a password or leave blank to use default: firstName_lastName</small>
                </div>
            </div>
            <div class="flex flex-row gap-2 justify-content-end">
                <Button v-if="activeUser.userId" @click="deleteUser()" label="Delete User" severity="danger" />
                <Button v-if="newUser" @click="() => {newUser = !newUser; activeUser = {}}" label="Cancel" severity="warning" />
                <Button @click="saveUser()" label="Save" severity="primary" />
            </div>
        </div>
        <div class="flex flex-column gap-5 col border-solid border-1 border-primary-200 p-2">
            <h2>User Permissions</h2>
            <div class="flex flex-column gap-5">
                <div class="flex flex-row gap-3">
                    <Checkbox v-model="activeUser.admin" :binary="true"></Checkbox>
                    <label for="">Administrator</label>
                </div>
                <div class="flex flex-row gap-3">
                    <Checkbox v-model="activeUser.viewer" :binary="true"></Checkbox>
                    <label for="">Viewer</label>
                </div>
                <div class="flex flex-row gap-3">
                    <Checkbox v-model="activeUser.chartBuilder" :binary="true"></Checkbox>
                    <label for="">Chart Builder</label>
                </div>
                <div class="flex flex-row gap-3">
                    <Checkbox v-model="activeUser.dashBuilder" :binary="true"></Checkbox>
                    <label for="">Dashboard Builder</label>
                </div>
                <div class="flex flex-row gap-3">
                    <Checkbox v-model="activeUser.connections" :binary="true"></Checkbox>
                    <label for="">Connections</label>
                </div>
            </div>
        </div>
    </div>
</template> -->

<style>
tr[data-p-highlight="true"] {
    background-color: var(--highlight-bg);
}
</style>