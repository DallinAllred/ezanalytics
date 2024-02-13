<script setup>
import { useToast } from  'primevue/usetoast';
const toast = useToast()

function saveDashboard() {
    toast.add({severity: 'info', summary: 'Successful', detail: 'Save Dashboard clicked', life: 3000})
}
function deleteConnection() {
    toast.add({severity: 'warn', summary: 'Warning', detail: 'Delete Connection clicked', life: 3000})
}
function newConnection() {
    toast.add({severity: 'info', summary: 'Successful', detail: 'New Connection clicked', life: 3000})
}

</script>

<template>

    <div class="grid h-full align-content-start">
        <div class="col-12 flex-none flex flex-row justify-content-end h-5rem">
            <div><Button label="Save Dashboard" @click="saveDashboard" /></div>
        </div>
        <div class="col-12 grid flex-grow-1 h-full">
            <div class="col-6 flex flex-column gap-2">
                <h2>Charts</h2>
                <Skeleton height="80%"></Skeleton>
                <div class="flex flex-row justify-content-between">
                    <div><Button label="Delete Data Source" @click="deleteConnection" /></div>
                    <div><Button label="Upload Data" @click="newConnection" /></div>
                </div>
            </div>
            <div class="col-6 flex flex-column gap-2">
                <h2>Dashboards</h2>
                <Skeleton height="10rem"></Skeleton>
                <div class="flex flex-row justify-content-between">
                    <div><Button label="Delete Connection" @click="deleteConnection" /></div>
                    <div><Button label="New Connection" @click="newConnection" /></div>
                </div>
            </div>
        </div>

    </div>

</template>

<style>
</style>