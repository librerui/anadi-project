<template>
  <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 0.75rem;">
    <div
      v-for="charger in chargers"
      :key="charger.id"
      @click="select(charger)"
      :style="{
        border: charger.id === modelValue ? '2px solid var(--p-primary-color)' : '1px solid var(--p-surface-300)',
        background: charger.id === modelValue ? 'var(--p-primary-50, var(--p-surface-100))' : 'var(--p-surface-0)',
        borderRadius: '0.75rem',
        padding: '0.75rem',
        cursor: 'pointer',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: '0.4rem',
        textAlign: 'center',
        transition: 'all 0.15s ease',
      }"
    >
      <ChargerIcon :type="charger.icon" :variant="charger.type" style="width: 56px; height: 56px;" />
      <div>
        <p style="margin: 0; font-weight: 600; font-size: 0.875rem;">{{ charger.brand }}</p>
        <p style="margin: 0; font-size: 0.8rem; color: var(--p-text-muted-color);">{{ charger.model }}</p>
      </div>
      <Tag :severity="charger.type === 'DC' ? 'danger' : 'info'" :value="charger.type" style="font-size: 0.65rem;" />
      <p style="margin: 0; font-weight: 700; font-size: 0.9rem;">{{ charger.power }} kW</p>
      <p style="margin: 0; font-size: 0.7rem; color: var(--p-text-muted-color);">{{ charger.connector }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import Tag from 'primevue/tag'
import ChargerIcon from './ChargerIcon.vue'
import { chargerModels, type ChargerModel } from '@/data/chargerModels'

const props = defineProps<{
  modelValue: string | null
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
  (e: 'select', charger: ChargerModel): void
}>()

const chargers = chargerModels

const select = (charger: ChargerModel) => {
  emit('update:modelValue', charger.id)
  emit('select', charger)
}
</script>
