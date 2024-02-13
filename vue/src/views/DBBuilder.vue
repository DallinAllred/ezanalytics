<script setup>
import { ref } from 'vue'
import { useToast } from  'primevue/usetoast'
const toast = useToast()

function saveDashboard() {
    toast.add({severity: 'info', summary: 'Successful', detail: 'Save Dashboard clicked', life: 3000})
}
function addRow() {
    toast.add({severity: 'info', summary: 'Warning', detail: 'Add Row clicked', life: 3000})
}
function addChart(row) {
    toast.add({severity: 'info', summary: 'Successful', detail: 'Add Chart clicked', life: 3000})
}

const layout = ref([['Table 1_1', 'Table 1_2'], ['Table 2_1', 'Table 2_2']])
</script>

<template>

    <div class="grid">
        <div class="col-12 flex flex-row justify-content-end">
            <div><Button label="Save Dashboard" @click="saveDashboard" /></div>
        </div>
            <div v-for="row of layout" class="col-12 grid h-full align-items-stretch">
                <div v-for="chart of row" :class="`col-${12 / row.length - 1}`">
                    <h4>{{ chart }}</h4>
                    <Skeleton height="10rem"></Skeleton>
                </div>
                <div>
                    <Button icon="pi pi-plus" outlined rounded class="mr-2" @click="addChart(row)" />
                </div>

            </div>
            <div>
                <Button icon="pi pi-plus" outlined rounded class="mr-2" @click="addRow()" />
            </div>
    </div>
</template>

<style>
</style>