<script setup>
import { reactive, ref, onMounted } from 'vue'

const users = ref()
const activeUser = ref({})
const selectedUser = ref()
const status = ref('')

onMounted(async () => {
    let userData = await fetch('http://localhost:5050/users/')
    userData = await userData.json()
    users.value = userData
})

async function addUser() {
    console.log('Adding user')
    let userInfo = {
        firstName: 'Will',
        middleName: 'T',
        lastName: 'Riker',
        userEmail: 'riker@mail.com',
    }
    console.log(userInfo)
    let response = await fetch(`http://localhost:5050/users/`, {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(userInfo)
    })
}

async function loadUser(event) {
    let userId = event.data.user_id
    let userData = await fetch(`http://localhost:5050/users/${userId}`)
    userData = await userData.json()
    console.log('Single User: ', userData)
    activeUser.value = userData[0]
}
</script>

<template>
    <div class="m-0">
        <div class="grid gap-2">
            <div class="col-2 border-solid border-1 border-primary-200 p-2">
                <div class="mb-2">
                    <button class="btn btn-success">New User</button>
                </div>
                <div class="mb-2">
                    <button class="btn btn-success" @click="addUser()">Add User</button>
                </div>
                <div>
                    <DataTable :value="users" stripedRows v-model:selection="selectedUser" :selection.sync="selectedRow" selectionMode="single" @rowSelect="loadUser" rowHover>
                        <Column selectionMode="single" headerStyle="width: 3rem"></Column>
                        <Column field="username" header="Username"></Column>
                    </DataTable>
                </div>
            </div>
            <div class="col-4 border-solid border-1 border-primary-200 p-2">
                <div>
                    <div class="flex flex-column gap-2">
                        <label for="firstName">First Name*</label>
                        <InputText id="firstName" type="text" v-model="activeUser.firstName"></InputText>
                    </div>
                    <div class="flex flex-column py-3">
                        <label for="middleName">Middle Name</label>
                        <InputText id="middleName" type="text" v-model="activeUser.middleName"></InputText>
                    </div>
                    <div class="flex flex-column py-3">
                        <label for="lastName">Last Name*</label>
                        <InputText id="lastName" type="text" v-model="activeUser.lastName"></InputText>
                    </div>
                    <div class="flex flex-column py-3">
                        <label for="email">Email*</label>
                        <InputText id="email" type="text" v-model="activeUser.userEmail"></InputText>
                    </div>
                    <div class="flex flex-column py-3">
                        <label for="email">Username*</label>
                        <InputText id="email" type="text" v-model="activeUser.username"></InputText>
                    </div>
                </div>
                <div>
                    <Button class="btn btn-success" @click="saveUser()" label="Save" />
                </div>
            </div>
            <div class="col border-solid border-1 border-primary-200 p-2">
                Permissions
            </div>
        </div>
    </div>

</template>

<style>
tr[data-p-highlight="true"] {
    background-color: var(--highlight-bg);
}
</style>