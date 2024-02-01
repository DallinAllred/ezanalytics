import './assets/main.css'
// import './assets/sass/style.css'

import PrimeVue from 'primevue/config';
import 'primevue/resources/themes/aura-dark-indigo/theme.css'
import 'primeicons/primeicons.css'
import '/node_modules/primeflex/primeflex.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const app = createApp(App)
app.use(PrimeVue)

app.use(router)

app.mount('#app')
