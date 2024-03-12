<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from '@/axiosConfig'
import Login from '@/components/dialogs/Login.vue'

const router = useRouter()

const showLogin = ref(false)

const userId = 1
const ownedCharts = ref([])
const ownedDashboards = ref([])

async function loadItems() {
    try {
        let response = await axios.get(`/api/charts`)//?user=${userId}`)
            .then((response) => {
                console.log('Then block')
                return response
            })
            .catch((err) => {
                console.log('Catch block')
                console.log(err)
                console.log(err.status)
                if (err.response?.status === 401) showLogin.value = true
            })
        console.log('Response: ', response.status)
        ownedCharts.value = response.data
        return
        response = await axios.get(`/api/dashboards?user=${userId}`)
            // .then((response) => response)
            // .catch((err) => {
            //     if (err.response?.status === 401) showLogin.value = true
            // })
        ownedDashboards.value = response.data
    } catch (err) {
        console.log('Error: ', err)
        console.log('Status: ', err)
    }

}

function viewCharts() {
    console.log('View Charts')
}
function buildChart() {
    console.log('Build Chart')
}
function viewDashboards() {
    console.log('View Dashboards')
}
function buildDash() {
    console.log('Build Dashboard')
}

onMounted(async () => {
    loadItems()
})

</script>

<template>
      <div class="grid h-full flex flex-column">
        <div class="col-6 col-offset-3 flex gap-8 justify-contents-center">
            <Button class="home-nav" label="View Charts" @click="viewCharts" />
            <Button class="home-nav" label="Build a Chart" @click="buildChart" />
        </div>
        <div class="col-6 col-offset-3 flex gap-8">
            <Button class="home-nav" label="View Dashboards" @click="viewDashboards" />
            <Button class="home-nav" label="Build a Dashboard" @click="buildDash" />
        </div>

        <!-- <div class="col-12 flex flex-column gap-2">
            <h2>Saved</h2>
            <Skeleton height="100%"></Skeleton>
        </div>
        <div class="col-12 flex flex-column gap-2">
            <h2>Recently Accessed</h2>
            <Skeleton height="100%"></Skeleton>
        </div> -->
    </div>
    <Login v-model="showLogin" title="Session Timed Out" @login="router.push('/')"></Login>
</template>

<style>
.home-nav {
    width: 150px;
    height: 150px;
}
</style>