<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

function openChartBuilder() {
    router.push('/chartBuilder')
}

</script>

<template>
    <h1>Charts</h1>
    <h3>Page is currently under construction</h3>
    <p>See <b>User Admin</b> for an up to date example.</p>
    <Button label="Chart Builder" @click="openChartBuilder" />

</template>

<style>
</style>