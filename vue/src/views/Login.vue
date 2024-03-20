<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from '@/axiosConfig'

const router = useRouter()
const showLogin = ref(true)
localStorage.removeItem('eza-user')

onMounted(async () =>{
    let response = await axios.put('/api/auth/logout')
})
</script>

<template>
    <Login v-model="showLogin" @login="router.push('/')"></Login>
</template>

<style>
</style>