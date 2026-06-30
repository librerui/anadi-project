<template>
  <div>
    <div style="margin-bottom: 1.5rem;">
      <h1 style="font-size: 1.875rem; font-weight: bold;">{{ $t('simulation.title') }}</h1>
    </div>

    <form @submit.prevent="onSubmit">
      <Card style="margin-bottom: 1rem;">
        <template #title>
          <div style="display: flex; align-items: center; gap: 0.5rem;">
            <i class="pi pi-sliders-h"></i>
            <span>{{ $t('simulation.configuration') }}</span>
          </div>
        </template>
        <template #content>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
            <div style="display: flex; flex-direction: column; gap: 0.25rem;">
              <label for="profile" style="font-weight: 500;">{{ $t('simulation.profile') }}</label>
              <Dropdown id="profile" v-model="form.profile" :options="profiles" style="width: 100%;" />
            </div>
            <div style="display: flex; flex-direction: column; gap: 0.25rem;">
              <label for="version" style="font-weight: 500;">{{ $t('simulation.version') }}</label>
              <InputText id="version" v-model="form.version" placeholder="Optional" style="width: 100%;" />
            </div>
            <div style="display: flex; flex-direction: column; gap: 0.25rem;">
              <label for="model" style="font-weight: 500;">{{ $t('simulation.model') }}</label>
              <Dropdown id="model" v-model="form.model_name" :options="classificationModels" style="width: 100%;" />
            </div>
            <div style="display: flex; flex-direction: column; gap: 0.25rem;">
              <label for="overload_class" style="font-weight: 500;">{{ $t('simulation.overload_class') }}</label>
              <Dropdown id="overload_class" v-model="form.overload_class" :options="overloadClasses" optionLabel="label" optionValue="value" style="width: 100%;" />
            </div>
          </div>
        </template>
      </Card>

      <Card style="margin-bottom: 1rem;">
        <template #title>
          <div style="display: flex; align-items: center; gap: 0.5rem;">
            <i class="pi pi-cog"></i>
            <span>{{ $t('simulation.parameters') }}</span>
          </div>
        </template>
        <template #content>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
            <div style="display: flex; flex-direction: column; gap: 0.25rem;">
              <label for="iterations" style="font-weight: 500;">{{ $t('simulation.iterations') }}</label>
              <InputNumber id="iterations" v-model="form.iterations" :min="100" :max="100000" style="width: 100%;" showButtons />
            </div>
            <div style="display: flex; flex-direction: column; gap: 0.25rem;">
              <label for="noise" style="font-weight: 500;">{{ $t('simulation.noise_scale') }}</label>
              <InputNumber id="noise" v-model="form.noise_scale" :min="0.01" :step="0.01" style="width: 100%;" showButtons :minFractionDigits="2" />
            </div>
            <div style="display: flex; flex-direction: column; gap: 0.25rem;">
              <label for="seed" style="font-weight: 500;">{{ $t('simulation.seed') }}</label>
              <InputNumber id="seed" v-model="form.seed" :min="0" style="width: 100%;" showButtons />
            </div>
          </div>
        </template>
      </Card>

      <Card style="margin-bottom: 1rem;">
        <template #title>
          <div style="display: flex; align-items: center; gap: 0.5rem;">
            <i class="pi pi-list"></i>
            <span>{{ $t('simulation.features') }}</span>
          </div>
        </template>
        <template #content>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
            <div v-for="(value, key) in form.features" :key="key" style="display: flex; flex-direction: column; gap: 0.25rem;">
              <label :for="key" style="font-size: 0.875rem; font-weight: 500;">{{ key }}</label>
              <InputNumber :id="key" v-model="form.features[key]" mode="decimal" :min="0" :step="0.5" style="width: 100%;" showButtons :minFractionDigits="1" />
            </div>
          </div>
        </template>
      </Card>

      <div style="display: flex; justify-content: flex-end;">
        <Button type="submit" :label="$t('simulation.submit')" icon="pi pi-play" severity="warning" :loading="submitting" />
      </div>
    </form>

    <div v-if="result" style="margin-top: 2rem;">
      <Card>
        <template #title>
          <div style="display: flex; align-items: center; gap: 0.5rem;">
            <i class="pi pi-check-circle" style="color: var(--p-green-500);"></i>
            <span>{{ $t('simulation.result') }}</span>
          </div>
        </template>
        <template #content>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin-bottom: 1rem;">
            <div style="background: var(--p-surface-100); padding: 0.75rem; border-radius: 0.5rem; text-align: center;">
              <p style="font-size: 0.875rem; color: var(--p-text-muted-color); margin-bottom: 0.25rem;">{{ $t('simulation.overload_probability') }}</p>
              <p style="font-size: 1.5rem; font-weight: bold;" :style="{ color: getProbabilityColor(result.overload_probability) }">
                {{ (result.overload_probability * 100).toFixed(1) }}%
              </p>
            </div>
            <div style="background: var(--p-surface-100); padding: 0.75rem; border-radius: 0.5rem; text-align: center;">
              <p style="font-size: 0.875rem; color: var(--p-text-muted-color); margin-bottom: 0.25rem;">Iterations</p>
              <p style="font-weight: 600;">{{ result.iterations }}</p>
            </div>
            <div style="background: var(--p-surface-100); padding: 0.75rem; border-radius: 0.5rem; text-align: center;">
              <p style="font-size: 0.875rem; color: var(--p-text-muted-color); margin-bottom: 0.25rem;">Model</p>
              <p style="font-weight: 600;">{{ result.model_name }}</p>
            </div>
            <div style="background: var(--p-surface-100); padding: 0.75rem; border-radius: 0.5rem; text-align: center;">
              <p style="font-size: 0.875rem; color: var(--p-text-muted-color); margin-bottom: 0.25rem;">Version</p>
              <p style="font-weight: 600;">{{ result.version || 'default' }}</p>
            </div>
          </div>

          <div v-if="result.distribution" style="margin-top: 1rem;">
            <Divider />
            <h4 style="margin-bottom: 0.75rem;">{{ $t('simulation.distribution') }}</h4>
            <div style="display: flex; justify-content: center; background: var(--p-surface-100); border-radius: 0.5rem; padding: 1rem;">
              <div style="max-width: 400px; width: 100%;">
                <PieChart :data="pieData" />
              </div>
            </div>
          </div>
        </template>
      </Card>
    </div>

    <Toast />
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useToast } from 'primevue/usetoast'
import Dropdown from 'primevue/dropdown'
import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import Button from 'primevue/button'
import Card from 'primevue/card'
import Divider from 'primevue/divider'
import Toast from 'primevue/toast'
import PieChart from '@/components/PieChart.vue'
import { simulate } from '@/api/endpoints'
import type { SimulationResponse } from '@/types'
import { useSimulationStore } from '@/stores/simulationStore'

const simulationStore = useSimulationStore()

const toast = useToast()
const { t } = useI18n()

const profiles = ['leve', 'regular', 'pesado']
const classificationModels = ['Decision_Tree', 'NeuralNet', 'SVM', 'KNN']
const overloadClasses = [
  { label: 'Baixo', value: 'baixo' },
  { label: 'Médio', value: 'medio' },
  { label: 'Alto', value: 'alto' }
]

const form = reactive({
  profile: 'leve',
  version: '',
  model_name: 'Decision_Tree',
  features: {
    'Potência instalada [kVA]': 15.5,
    'P_IP_Total': 123.4,
    'P_IP_Inef': 56.7,
    'LED_Ratio': 0.8,
    'N_Luminarias': 50,
    'N_Lampadas': 100,
    'Cap_per_Cliente': 2.5,
    'Distrito_enc': 3,
    'Concelho_enc': 5,
    'N_Clientes': 4,
  },
  iterations: 1000,
  noise_scale: 0.1,
  overload_class: 'alto',
  seed: 42,
})

const result = ref<SimulationResponse | null>(null)
const submitting = ref(false)

const getProbabilityColor = (prob: number) => {
  if (prob < 0.3) return 'var(--p-green-500)'
  if (prob < 0.7) return 'var(--p-orange-500)'
  return 'var(--p-red-500)'
}

const pieData = computed(() => {
  if (!result.value?.distribution) return null
  const labels = Object.keys(result.value.distribution)
  const data = Object.values(result.value.distribution)
  const colors = ['#42A5F5', '#FFA726', '#66BB6A', '#EF5350', '#AB47BC']
  return {
    labels,
    datasets: [
      {
        data,
        backgroundColor: colors.slice(0, labels.length),
        hoverBackgroundColor: colors.slice(0, labels.length),
      },
    ],
  }
})

const onSubmit = async () => {
  submitting.value = true
  try {
    const payload = {
      profile: form.profile,
      version: form.version || undefined,
      task: 'classification' as const,
      model_name: form.model_name,
      features: form.features,
      iterations: form.iterations,
      noise_scale: form.noise_scale,
      overload_class: form.overload_class,
      seed: form.seed || undefined,
    }
    const response = await simulate(payload)
    result.value = response.data
    
    simulationStore.addRecord({
      profile: form.profile,
      version: form.version,
      model_name: form.model_name,
      overload_class: form.overload_class,
      iterations: form.iterations,
      noise_scale: form.noise_scale,
      features: { ...form.features },
      overload_probability: response.data.overload_probability,
      distribution: response.data.distribution,
    })
    
    toast.add({ severity: 'success', summary: t('common.success'), detail: 'Simulation completed', life: 3000 })
  } catch (error: any) {
    toast.add({
      severity: 'error',
      summary: t('common.error'),
      detail: error.response?.data?.detail || error.message,
      life: 5000,
    })
  } finally {
    submitting.value = false
  }
}
</script>