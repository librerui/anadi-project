import { createApp } from 'vue'
import { createPinia } from 'pinia'
import PrimeVue from 'primevue/config'
import Aura from '@primevue/themes/aura'
import 'primeicons/primeicons.css'
import { createI18n } from 'vue-i18n'
import en from './locales/en.json'
import pt from './locales/pt.json'

import App from './App.vue'
import router from './router'

import ToastService from 'primevue/toastservice'

const i18n = createI18n({
  locale: 'pt',
  fallbackLocale: 'pt',
  messages: { en, pt },
})

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(PrimeVue, {
  theme: {
    preset: Aura,
  },
})
app.use(i18n)

app.use(ToastService)

app.mount('#app')