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
          <!-- Help Button -->
          <Button
            ref="helpBtn"
            icon="pi pi-question-circle"
            :label="$t('app.help')"
            severity="help"
            size="small"
            @click="toggleHelpPanel"
          />

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

    <!-- Help Overlay Panel -->
    <OverlayPanel
      ref="helpPanel"
      :showCloseIcon="true"
      :dismissable="true"
      :style="{ width: '360px' }"
      :breakpoints="{ '960px': '75vw', '640px': '90vw' }"
    >
      <div style="display: flex; flex-direction: column; gap: 1rem;">
        <div style="display: flex; align-items: center; gap: 0.75rem;">
          <div style="width: 40px; height: 40px; border-radius: 0.5rem; background: var(--p-primary-100); display: flex; align-items: center; justify-content: center;">
            <i class="pi pi-book" style="font-size: 1.25rem; color: var(--p-primary-color);"></i>
          </div>
          <div>
            <h3 style="margin: 0; font-size: 1rem; font-weight: 600;">{{ $t('app.help_title') }}</h3>
            <p style="margin: 0.15rem 0 0 0; font-size: 0.8rem; color: var(--p-text-muted-color);">{{ $t('app.help_subtitle') }}</p>
          </div>
        </div>

        <Divider />

        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
          <p style="margin: 0; font-size: 0.875rem; color: var(--p-text-muted-color);">{{ $t('app.help_description') }}</p>

          <div style="display: flex; flex-direction: column; gap: 0.25rem; margin-top: 0.5rem;">
            <div style="display: flex; align-items: center; gap: 0.5rem; font-size: 0.85rem;">
              <i class="pi pi-bolt" style="color: var(--p-primary-color); font-size: 0.8rem;"></i>
              <span>{{ $t('nav.predict') }}</span>
            </div>
            <div style="display: flex; align-items: center; gap: 0.5rem; font-size: 0.85rem;">
              <i class="pi pi-cog" style="color: var(--p-orange-500); font-size: 0.8rem;"></i>
              <span>{{ $t('nav.simulate') }}</span>
            </div>
            <div style="display: flex; align-items: center; gap: 0.5rem; font-size: 0.85rem;">
              <i class="pi pi-map" style="color: var(--p-green-500); font-size: 0.8rem;"></i>
              <span>{{ $t('nav.regional') }}</span>
            </div>
          </div>
        </div>

        <Button
          :label="$t('app.open_manual')"
          icon="pi pi-external-link"
          severity="primary"
          size="small"
          @click="openManual"
        />
      </div>
    </OverlayPanel>

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
import OverlayPanel from 'primevue/overlaypanel'
import Divider from 'primevue/divider'
import { useThemeStore } from '@/stores/themeStore'

const { locale, t } = useI18n()
const route = useRoute()
const router = useRouter()
const themeStore = useThemeStore()

const helpPanel = ref<InstanceType<typeof OverlayPanel> | null>(null)
const helpBtn = ref<InstanceType<typeof Button> | null>(null)

const languages = [
  { code: 'en', label: 'EN' },
  { code: 'pt', label: 'PT' },
]

const setLocale = (lang: string) => {
  locale.value = lang
  localStorage.setItem('app-locale', lang)
}

const isActive = (path: string) => route.path === path

const toggleHelpPanel = (event: Event) => {
  helpPanel.value?.toggle(event)
}

const openManual = () => {
  helpPanel.value?.hide()
  window.open('/UserManual.pdf', '_blank')
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