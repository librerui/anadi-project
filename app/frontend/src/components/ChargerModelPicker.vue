<template>
  <div>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 0.75rem;">
      <div
        v-for="model in chargerModels"
        :key="model.id"
        @click="selectModel(model)"
        style="cursor: pointer; padding: 1rem; border-radius: 0.75rem; border: 2px solid transparent; text-align: center; transition: all 0.2s;"
        :style="{
          background: selectedId === model.id ? 'var(--p-primary-50)' : 'var(--p-surface-100)',
          borderColor: selectedId === model.id ? 'var(--p-primary-color)' : 'transparent',
          boxShadow: selectedId === model.id ? '0 2px 8px var(--p-primary-200)' : 'none',
        }"
      >
        <div style="width: 64px; height: 64px; margin: 0 auto 0.75rem;">
          <ChargerIcon :type="model.iconType" :variant="model.type" />
        </div>
        <p style="margin: 0; font-weight: 600; font-size: 0.9rem;">{{ model.name }}</p>
        <p style="margin: 0.25rem 0 0 0; font-size: 0.75rem; color: var(--p-text-muted-color);">
          {{ model.power }} kW · {{ model.type }}
        </p>
        <Tag v-if="model.recommended" :value="$t('common.recommended')" severity="success" style="font-size: 0.65rem; margin-top: 0.5rem;" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import Tag from 'primevue/tag'
import ChargerIcon from './ChargerIcon.vue'

export interface ChargerModel {
  id: string
  name: string
  power: number
  type: 'AC' | 'DC'
  iconType: 'wallbox' | 'pedestal' | 'pillar'
  recommended?: boolean
}

const props = defineProps<{
  modelValue: string
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', id: string): void
  (e: 'select', model: ChargerModel): void
}>()

const selectedId = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val),
})

const chargerModels: ChargerModel[] = [
  { id: 'wallbox-pulsar-plus-7_4', name: 'Wallbox Pulsar Plus', power: 7.4, type: 'AC', iconType: 'wallbox' },
  { id: 'pedestal-11', name: 'Pedestal 11kW', power: 11, type: 'AC', iconType: 'pedestal' },
  { id: 'wallbox-copper-sb-22', name: 'Wallbox Copper SB', power: 22, type: 'AC', iconType: 'wallbox' },
  { id: 'pedestal-22', name: 'Pedestal 22kW', power: 22, type: 'AC', iconType: 'pedestal' },
  { id: 'fastned-50', name: 'Fastned 50kW', power: 50, type: 'DC', iconType: 'pillar' },
  { id: 'ionity-150', name: 'IONITY 150kW', power: 150, type: 'DC', iconType: 'pillar' },
  { id: 'tesla-supercharger-250', name: 'Tesla Supercharger', power: 250, type: 'DC', iconType: 'pillar' },
]

const selectModel = (model: ChargerModel) => {
  selectedId.value = model.id
  emit('select', model)
}
</script>