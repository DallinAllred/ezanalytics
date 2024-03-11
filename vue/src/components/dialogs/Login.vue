<script setup>
import { computed, ref, watch } from 'vue'
import axios from '@/axiosConfig'

const emit = defineEmits(['login'])
const model = defineModel()
const props = defineProps(['title'])

const username = ref()
const password = ref()
const submitted = ref(false)
const invalidCredentials = ref(false)

const modalHeader = computed(() => {
    if (props.title) {
        return props.title
    }
    else {
        return 'Login'
    }
})

async function login() {
    submitted.value = true
    invalidCredentials.value = false
    if (!(username.value && password.value)) { return }
    let data = {
        username: username.value,
        password: password.value
    }
    try {
        let response = await axios.put(`/api/auth/login`, data)
        console.log(response)
        emit('login')
    } catch (error) {
        invalidCredentials.value = true
    }
}

</script>

<template>
    <Dialog v-model:visible="model" :style="{width: '450px'}" header="User Login" :modal="true" :closable="false">
        <div class="field flex flex-column gap-1">
            <label for="username">Username</label>
            <InputText id="username" v-model.trim="username" required="true" autofocus :class="{'p-invalid': submitted && !username}" />
            <small class="p-error" v-if="submitted && !username">Username is required</small>
        </div>
        <div class="field flex flex-column gap-1">
            <label for="password">Password</label>
            <InputText id="password" type="password" v-model.trim="password" required="true" :class="{'p-invalid': submitted && !password}" />
            <small class="p-error" v-if="submitted && !password">Password is required</small>
        </div>
        <div>
            <Message v-if="invalidCredentials" severity="error" :closable="false">Invalid credentials</Message>
        </div>

        <template #footer>
            <Button label="Login" @click="login" />
        </template>
    </Dialog>
</template>

<style>
</style>