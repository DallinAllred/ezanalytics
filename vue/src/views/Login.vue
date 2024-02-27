<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import Login from '@/components/dialogs/Login.vue'

const router = useRouter()

const showLogin = ref(true)
</script>

<template>
    <Login v-model="showLogin" @login="router.push('/')"></Login>
</template>

<style>

</style>