<script setup>
import { ref, onMounted } from 'vue'

const users = ref()

onMounted(async () => {
    let userData = await fetch('http://localhost:5050/users/')
    userData = await userData.json()
    console.log(userData)
    users.value = userData
})
</script>

<template>
    <h1>Users</h1>
    <div class="container m-0">
        <div class="row">
            <div class="col-2 d-flex flex-column justify-content-left border border-2 border-dark p-2">
                <div>
                    <button>New User</button>
                </div>
                <div>
                    <h3>Username</h3>
                    <ul>
                        <li v-for="user of users">{{ user.first_name }}</li>
                    </ul>
                </div>
            </div>
            <div class="col-3 d-flex flex-column justify-content-left border border-2 border-dark">
                Details for selected user
            </div>
            <div class="col-7 d-flex flex-column justify-content-left border border-2 border-dark">
                Permissions
            </div>
        </div>
    </div>

</template>

<style>
</style>