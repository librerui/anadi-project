<template>
  <div style="min-height: 100vh; background: var(--p-surface-50);">
    <Menubar :model="items" style="margin-bottom: 1rem; position: sticky; top: 0; z-index: 1000;">
      <template #start>
        <div style="display: flex; align-items: center; gap: 0.5rem;">
          <Avatar icon="pi pi-bolt" shape="circle" />
          <span style="font-weight: bold; font-size: 1.25rem;">{{ $t('app.title') }}</span>
        </div>
      </template>
      
      <template #item="{ item, props, hasSubmenu }">
        <router-link v-if="item.to" v-slot="{ href, navigate }" :to="item.to" custom>
          <a 
            :href="href" 
            v-bind="props.action" 
            @click="navigate"
            :style="{ fontWeight: isActive(item.to) ? 'bold' : 'normal' }"
          >
            <span :class="item.icon" />
            <span style="margin-left: 0.5rem;">{{ item.label }}</span>
          </a>
        </router-link>
        <a v-else :href="item.url" :target="item.target" v-bind="props.action">
          <span :class="item.icon" />
          <span style="margin-left: 0.5rem;">{{ item.label }}</span>
          <i v-if="hasSubmenu" class="pi pi-angle-down" style="margin-left: 0.5rem;"></i>
        </a>
      </template>

      <template #end>
        <div style="display: flex; align-items: center; gap: 0.5rem;">
          <!-- Preset Selector -->
          <!-- <Dropdown
            v-model="themeStore.preset"
            :options="presetOptions"
            optionLabel="label"
            optionValue="value"
            size="small"
            style="min-width: 120px;"
            @change="onPresetChange"
          /> -->

          <!-- Language Buttons -->
          <Button 
            v-for="lang in languages" 
            :key="lang.code"
            :label="lang.label"
            :severity="locale === lang.code ? 'primary' : 'secondary'"
            size="small"
            @click="setLocale(lang.code)"
          />
        </div>
      </template>
      
    </Menubar>

    <div style="padding: 1rem; max-width: 1400px; margin: 0 auto;">
      <router-view />
    </div>

    <Toast position="top-right" />
  </div>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute, useRouter } from 'vue-router'
import Menubar from 'primevue/menubar'
import Button from 'primevue/button'
import Avatar from 'primevue/avatar'
import Toast from 'primevue/toast'
import Dropdown from 'primevue/dropdown'
import { useThemeStore } from '@/stores/themeStore'

const { locale, t } = useI18n()
const route = useRoute()
const router = useRouter()
const themeStore = useThemeStore()

const languages = [
  { code: 'en', label: 'EN' },
  { code: 'pt', label: 'PT' },
]

const setLocale = (lang: string) => {
  locale.value = lang
  localStorage.setItem('app-locale', lang)
}

const isActive = (path: string) => route.path === path

const presetOptions = computed(() => [
  { value: 'aura', label: t('theme.aura') },
  { value: 'lara', label: t('theme.lara') },
  { value: 'nora', label: t('theme.nora') },
  { value: 'material', label: t('theme.material') },
])

const onPresetChange = () => {
  window.location.reload()
}

const items = ref([
  { 
    label: t('nav.dashboard'), 
    icon: 'pi pi-home', 
    to: '/',
    command: () => router.push('/')
  },
  { 
    label: t('nav.predict'), 
    icon: 'pi pi-chart-line', 
    to: '/predict',
    command: () => router.push('/predict')
  },
  { 
    label: t('nav.simulate'), 
    icon: 'pi pi-cog', 
    to: '/simulate',
    command: () => router.push('/simulate')
  },
  { 
    label: t('nav.regional'), 
    icon: 'pi pi-map', 
    to: '/regional',
    command: () => router.push('/regional')
  },
  { 
    label: t('nav.health'), 
    icon: 'pi pi-heart', 
    to: '/health',
    command: () => router.push('/health')
  },
])

watch(locale, () => {
  items.value = [
    { label: t('nav.dashboard'), icon: 'pi pi-home', to: '/', command: () => router.push('/') },
    { label: t('nav.predict'), icon: 'pi pi-chart-line', to: '/predict', command: () => router.push('/predict') },
    { label: t('nav.simulate'), icon: 'pi pi-cog', to: '/simulate', command: () => router.push('/simulate') },
    { label: t('nav.regional'), icon: 'pi pi-map', to: '/regional', command: () => router.push('/regional') },
    { label: t('nav.health'), icon: 'pi pi-heart', to: '/health', command: () => router.push('/health') },
  ]
})
</script>