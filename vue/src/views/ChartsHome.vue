<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

function newChart() {
    router.push('/chartBuilder')
}

// TODO: Update this to use a query string to load the desired chart
function loadChart() {
    router.push('/chartBuilder')
}

</script>

<template>
    <div class="grid h-full">
        <div class="col-2 flex flex-column gap-2">
            <Skeleton height="100%"></Skeleton>
            <Button label="New Chart" @click="newChart" />
        </div>
        <div class="col-10 flex flex-column gap-2">
            <Skeleton height="100%"></Skeleton>
        </div>
    </div>
</template>

<style>
</style>