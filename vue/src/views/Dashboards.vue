<script setup>
import { onMounted, ref, reactive, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

import { useToast } from  'primevue/usetoast';

import EZChart from '@/components/EZChart.vue'

const router = useRouter()

const dashList = ref([])
const selectedDash = ref(null)

async function loadDashboards() {
    let response = await axios.get(`http://localhost:5050/api/dashboards`)
    dashList.value = response
}

function newDashboard() {
    router.push('/dbBuilder')
}

function editDashboard() {
    if (selectedDash.value) {
        router.push(`/dbBuilder?dash=${selectedDash.value.id}`)
    }
}

onMounted(async () => {
    await loadDashboards()
    if ('dash' in router.query) {
        let queryDash = dashList.value.filter(dash => dash.id == router.query.dash)
        selectedDash.value = queryDash[0]
    }
})

</script>

<template>
    <div class="grid h-full">
        <div class="col-2 flex flex-column gap-2">
            <div class="h-full">
                <DataTable v-model:selection="selectedDash" :value="dashList" selectionMode="single"
                scrollable class="h-full" dataKey="id">
                    <Column field="title" header="Dashboard"></Column>
                    <Column field="id" header="ID"></Column>
                </DataTable>
            </div>
            <Button label="New Dashboard" @click="newDashboard" />
        </div>
        <div class="col-10 flex flex-column gap-2">
            <Skeleton height="100%"></Skeleton>
        </div>
    </div>
</template>

<style>
</style>