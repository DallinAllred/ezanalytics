<script setup>
import { reactive, ref, onMounted } from 'vue'

const users = ref()
const activeUser = ref({})
const selectedUser = ref()
const newUser = ref(false)

onMounted(async () => {
    loadUsers()
})

async function loadUsers() {
    let userData = await fetch('http://localhost:5050/users/')
    userData = await userData.json()
    users.value = userData
}

async function loadUser(event) {
    let userId = event.data.user_id
    let userData = await fetch(`http://localhost:5050/users/${userId}`)
    userData = await userData.json()
    activeUser.value = userData
    console.log(activeUser.value)
}

async function addUser() {
    newUser.value = true
    activeUser.value = {}
    selectedUser.value = null
}

async function saveUser() {
    console.log(activeUser.value)
    if (newUser.value === true) {
        let response = await fetch(`http://localhost:5050/users/`, {
            method: 'POST',
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(activeUser.value)
        })
    } else {
        let response = await fetch(`http://localhost:5050/users/${activeUser.value.userId}`, {
            method: 'PUT',
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(activeUser.value)
        })
    }
    loadUsers()
    newUser.value = false
}

async function deleteUser() {
    console.log('Deleting: ', activeUser.value.userId)
    let response = await fetch(`http://localhost:5050/users/${activeUser.value.userId}`, {
        method: 'DELETE'//,
        // headers: {
        //     "Content-Type": "application/json",
        // },
        // body: JSON.stringify(activeUser.value)
    })
    loadUsers()
}


</script>

<template>
    <div class="grid gap-2 m-0 h-full">
        <div class="flex flex-column col-2 border-solid border-1 border-primary-200 p-2 align-content-center">
            <div class="flex flex-row justify-content-center mb-2">
                <Button icon="pi pi-user-plus" iconPos="right" @click="addUser()" label="New User" />
            </div>
            <div>
                <DataTable :value="users" stripedRows v-model:selection="selectedUser"
                :selection.sync="selectedRow" :selectionMode="newUser ? '' : 'single'"
                @rowSelect="loadUser" rowHover>
                    <!-- <Column selectionMode="single" headerStyle="width: 3rem"></Column> -->
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

</template>

<style>
tr[data-p-highlight="true"] {
    background-color: var(--highlight-bg);
}
</style>