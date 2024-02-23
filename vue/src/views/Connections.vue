<script setup>
import { useToast } from  'primevue/usetoast';

const toast = useToast()

function deleteDataSource() {
    toast.add({severity: 'warn', summary: 'Warning', detail: 'Delete Data Source clicked', life: 3000})
}

function uploadData() {
    toast.add({severity: 'info', summary: 'Successful', detail: 'Upload Data clicked', life: 3000})
}

function deleteConnection() {
    toast.add({severity: 'warn', summary: 'Warning', detail: 'Delete Connection clicked', life: 3000})
}

function newConnection() {
    toast.add({severity: 'info', summary: 'Successful', detail: 'New Connection clicked', life: 3000})
}


</script>

<template>
    <div class="grid h-full justify-content-between px-2">
        <div class="col-6 flex flex-column gap-2">
            <h2>Uploaded Data</h2>
            <Skeleton height="100%"></Skeleton>
            <div class="flex flex-row justify-content-between">
                <div><Button label="Delete Data Source" @click="deleteDataSource" /></div>
                <div><Button label="Upload Data" @click="uploadData" /></div>
            </div>
        </div>
        <div class="col-6 flex flex-column gap-2">
            <h2>Database Connections</h2>
            <Skeleton height="100%"></Skeleton>
            <div class="flex flex-row justify-content-between">
                <div><Button label="Delete Connection" @click="deleteConnection" /></div>
                <div><Button label="New Connection" @click="newConnection" /></div>
            </div>
        </div>
    </div>
</template>

<style>
</style>