<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from '@/axiosConfig'

const router = useRouter()

const currentUser = ref(JSON.parse(localStorage.getItem('eza-user')) ?? {})
const showLogin = ref(false)
const loginTitle = ref('Session Timed Out')

const ownedCharts = ref([])
const ownedDashboards = ref([])

async function loadItems() {
    if (!currentUser.value.username) {
        currentUser.value = JSON.parse(localStorage.getItem('eza-user')) ?? {}
        if (!currentUser.value?.username) {
            loginTitle.value = null
            showLogin.value = true
            return
        }
    }
    loginTitle.value = 'Session Timed Out'
    console.log('Loading charts and dashboards')
    try {
        let response = await axios.get(`/api/charts?user=${currentUser.value['user_id']}`)
        console.log('Response: ', response.status)
        ownedCharts.value = response.data
        response = await axios.get(`/api/dashboards?user=${currentUser.value['user_id']}`)
        ownedDashboards.value = response.data
        console.log(ownedCharts.value, ownedDashboards.value)
    } catch (err) {
        if (err.response?.status === 401) { showLogin.value = true}
        console.log(err)
    }
}

function viewCharts() {
    console.log('View Charts')
    router.push('/chartsHome')
}
function buildChart() {
    console.log('Build Chart')
    router.push('/chartBuilder')
}
function viewDashboards() {
    console.log('View Dashboards')
    router.push('/dashboards')
}
function buildDash() {
    console.log('Build Dashboard')
    router.push('/dbBuilder')
}

onMounted(async () => {
    loadItems()
})

</script>

<template>
    <div v-if="!(currentUser.admin || currentUser.viewer)" class="flex p-3">
        <Unauthorized />
    </div>
    <div v-else class="grid h-full flex flex-column">
        <div class="col-6 col-offset-3 flex gap-8 justify-contents-center">
            <Button class="home-nav" label="View Charts" @click="viewCharts" />
            <Button class="home-nav" label="Build a Chart" @click="buildChart" />
        </div>
        <div class="col-6 col-offset-3 flex gap-8">
            <Button class="home-nav" label="View Dashboards" @click="viewDashboards" />
            <Button class="home-nav" label="Build a Dashboard" @click="buildDash" />
        </div>
    </div>
    <Login v-model="showLogin" :title="loginTitle" @login="showLogin = false; loadItems()"></Login>
</template>

<style>
.home-nav {
    width: 150px;
    height: 150px;
}
</style>