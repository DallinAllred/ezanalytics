<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useToast } from  'primevue/usetoast'
import axios from '@/axiosConfig'

import EZChart from '@/components/EZChart.vue'

const emit = defineEmits(['timeout401'])
const model = defineModel()

const toast = useToast()

const dashTitle = ref('')
const layout = ref([])

const currentUser = ref('admin')

async function loadDash(dashId) {
    try {
        let response = await axios.get(`/api/dashboards/${dashId}`)
        let data = response.data
        dashTitle.value = data.title
        layout.value = data.layout
    } catch (err) {
        if (err.response?.status === 401) {
            emit('timeout401')
            return
        }
        toast.add({severity: 'error', summary: 'Dashboard Not Found', detail: `Unable to find dashboard ${dashId}`, life: 3000})
        return
    }
}

onMounted(() => {
    loadDash(model.value)
})

watch(model, () => {
    loadDash(model.value)
})

</script>

<template>
    <div class="grid ezdash">
        <div v-for="(row, index) of layout" key class="col-12 grid">
            <div class="col-12 grid flex justify-content-between">
                <div v-for="(chart, col) of row" :class="`col-${12 / row.length}`" class="dash-row flex justify-content-center">
                    <div v-if="chart.id">
                        <EZChart v-model="chart.id" height="100%"></EZChart>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style>
.dash-row {
    min-height: 30vh;
}
.ezdash {
    height: 100%;
    overflow-x: hidden;
    /* overflow-y: scroll; */
}
</style>