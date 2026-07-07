import { createApp } from 'vue'
import { createPinia } from 'pinia'

import PrimeVue from 'primevue/config'
import Aura from '@primevue/themes/aura'
import Lara from '@primevue/themes/lara'
import Nora from '@primevue/themes/nora'
import Material from '@primevue/themes/material'

import 'primeicons/primeicons.css'
import 'leaflet/dist/leaflet.css'

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

// Theme preset map
const presetMap = {
  aura: Aura,
  lara: Lara,
  nora: Nora,
  material: Material,
}

// Load theme store after pinia is installed
import { useThemeStore } from './stores/themeStore'
const themeStore = useThemeStore()

app.use(PrimeVue, {
  theme: {
    preset: presetMap[themeStore.currentPreset] || Material,
    options: {
      prefix: 'p',
      darkModeSelector: false,
      cssLayer: false,
    },
  },
})

app.use(i18n)
app.use(ToastService)
app.mount('#app')