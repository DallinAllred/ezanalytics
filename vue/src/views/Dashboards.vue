<script setup>
import { useToast } from  'primevue/usetoast';
import { useRouter } from 'vue-router'

const router = useRouter()

const toast = useToast()

function newDashboard() {
    router.push('/dbBuilder')
    toast.add({severity: 'info', summary: 'Successful', detail: 'New Dashboard clicked', life: 3000})
}

</script>

<template>
    <div class="grid h-full">
        <div class="col-2 flex flex-column gap-2">
            <Skeleton height="100%"></Skeleton>
            <Button label="New Dashboard" @click="newDashboard" />
        </div>
        <div class="col-10 flex flex-column gap-2">
            <Skeleton height="100%"></Skeleton>
        </div>
    </div>
</template>

<style>
</style>