<script setup>
import { RouterLink, RouterView, useRoute, useRouter } from 'vue-router'

const router = useRouter()

router.push('/users')
</script>

<template>
  <main>
    <h1>Home Page</h1>
    <h2>Default landing page</h2>
  </main>
</template>
