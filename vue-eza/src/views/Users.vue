<script setup>
import { reactive, ref, onMounted } from 'vue'

const users = ref()
const activeUser = ref({})
const status = ref('')

onMounted(async () => {
    let userData = await fetch('http://localhost:5050/users/')
    userData = await userData.json()
    users.value = userData
})

async function addUser() {
    console.log('Adding user')
}

async function loadUser(user_id) {
    let userData = await fetch(`http://localhost:5050/users/${user_id}`)
    userData = await userData.json()
    activeUser.value = userData[0]
}
</script>

<template>
    <h1>Users</h1>
    <div class="container m-0">
        <div class="row">
            <div class="col-2 d-flex flex-column justify-content-left border border-2 border-dark p-2">
                <div class="mb-2">
                    <button class="btn btn-success">New User</button>
                </div>
                <div>
                    <!-- <h3>Username</h3> -->
                    <table class="table table-striped table-hover">
                        <thead class="table-dark">
                            <tr>
                                <th scope="col">Username</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="user of users">
                                <td @click="loadUser(user.user_id)">{{ user.username }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            <div class="col-3 d-flex flex-column justify-content-left border border-2 border-dark p-2">
                <div>
                    <div>
                        <label for="first_name">First Name*</label>
                        <input name="first_name" type="text" class="form-control" placeholder="First Name" v-model="activeUser.first_name">
                    </div>
                    <div>
                        <label for="middle_name">Middle Name</label>
                        <input name="middle_name" type="text" class="form-control" placeholder="Middle Name" v-model="activeUser.middle_name">
                    </div>
                    <div>
                        <label for="last_name">Last Name*</label>
                        <input name="last_name" type="text" class="form-control" placeholder="Last Name" v-model="activeUser.last_name">
                    </div>
                    <div>
                        <label for="email">Email*</label>
                        <input name="email" type="email" class="form-control" placeholder="Email" v-model="activeUser.user_email">
                    </div>
                </div>
                <div>
                    <div class="btn btn-success" @click="saveUser()">Save</div>
                </div>
            </div>
            <div class="col-7 d-flex flex-column justify-content-left border border-2 border-dark">
                Permissions
            </div>
        </div>
    </div>

</template>

<style>
</style>