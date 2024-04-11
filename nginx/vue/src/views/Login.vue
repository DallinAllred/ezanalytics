<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from '@/axiosConfig'

const emit = defineEmits('updateApp')
const router = useRouter()
const showLogin = ref(true)
localStorage.removeItem('eza-user')

onMounted(async () =>{
    let response = await axios.put('/api/auth/logout')
})
</script>

<template>
    <div>
        <Login v-model="showLogin" @login="router.push('/'); emit('updateApp')"></Login>
    </div>
</template>

<style>
</style>