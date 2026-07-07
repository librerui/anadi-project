<template>
  <div style="display: flex; align-items: center; gap: 0.5rem;">
    <!-- Light/Dark Toggle -->
    <Button
      :icon="themeStore.isDark ? 'pi pi-moon' : 'pi pi-sun'"
      :label="themeStore.isDark ? $t('theme.dark') : $t('theme.light')"
      text
      size="small"
      @click="themeStore.toggleColorScheme()"
      :title="$t('theme.toggle')"
    />

    <!-- Preset Selector -->
    <Dropdown
      v-model="themeStore.preset"
      :options="presetOptions"
      optionLabel="label"
      optionValue="value"
      size="small"
      style="min-width: 120px;"
      @change="onPresetChange"
    />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import Button from 'primevue/button'
import Dropdown from 'primevue/dropdown'
import { useThemeStore } from '@/stores/themeStore'

const { t } = useI18n()
const themeStore = useThemeStore()

const presetOptions = computed(() => [
  { value: 'aura', label: t('theme.aura') },
  { value: 'lara', label: t('theme.lara') },
  { value: 'nora', label: t('theme.nora') },
  { value: 'material', label: t('theme.material') },
])

const onPresetChange = () => {
  // PrimeVue themes require a reload to switch presets properly
  window.location.reload()
}
</script>