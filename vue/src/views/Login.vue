<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import Login from '@/components/dialogs/Login.vue'
import axios from '@/axiosConfig'

const router = useRouter()

const showLogin = ref(true)

onMounted(async () =>{
    let response = axios.put('/api/auth/logout')
})

</script>

<template>
    <Login v-model="showLogin" @login="router.push('/')"></Login>
</template>

<style>

</style>