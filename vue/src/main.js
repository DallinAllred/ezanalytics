import './assets/main.css'

import PrimeVue from 'primevue/config';
import 'primevue/resources/themes/aura-dark-lime/theme.css'
import 'primeicons/primeicons.css'
import '/node_modules/primeflex/primeflex.css'
import ToastService from 'primevue/toastservice'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import ConfirmDelete from '@/components/dialogs/ConfirmDelete.vue'
import Login from '@/components/dialogs/Login.vue'

const app = createApp(App)
app.use(PrimeVue)
app.use(ToastService)

app.component('ConfirmDelete', ConfirmDelete)
    .component('Login', Login)

app.use(router)

app.mount('#app')
