<template>
  <div>
    <div style="margin-bottom: 1.5rem;">
      <h1 style="font-size: 1.875rem; font-weight: bold;">{{ $t('prediction.title') }}</h1>
    </div>

    <form @submit.prevent="onSubmit">
      <Card style="margin-bottom: 1rem;">
        <template #title>
          <div style="display: flex; align-items: center; gap: 0.5rem;">
            <i class="pi pi-sliders-h"></i>
            <span>{{ $t('prediction.configuration') }}</span>
          </div>
        </template>
        <template #content>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
            <div style="display: flex; flex-direction: column; gap: 0.25rem;">
              <label for="profile" style="font-weight: 500;">{{ $t('prediction.profile') }}</label>
              <Dropdown id="profile" v-model="form.profile" :options="profiles" placeholder="Select profile" style="width: 100%;" />
            </div>

            <div style="display: flex; flex-direction: column; gap: 0.25rem;">
              <label for="version" style="font-weight: 500;">{{ $t('prediction.version') }}</label>
              <InputText id="version" v-model="form.version" placeholder="Optional" style="width: 100%;" />
            </div>

            <div style="display: flex; flex-direction: column; gap: 0.25rem;">
              <label for="task" style="font-weight: 500;">{{ $t('prediction.task') }}</label>
              <Dropdown id="task" v-model="form.task" :options="tasks" optionLabel="label" optionValue="value" placeholder="Select task" style="width: 100%;" @change="onTaskChange" />
            </div>

            <div style="display: flex; flex-direction: column; gap: 0.25rem;">
              <label for="model" style="font-weight: 500;">{{ $t('prediction.model') }}</label>
              <Dropdown id="model" v-model="form.model_name" :options="availableModels" placeholder="Select model" style="width: 100%;" />
            </div>
          </div>
        </template>
      </Card>

      <Card style="margin-bottom: 1rem;">
        <template #title>
          <div style="display: flex; align-items: center; gap: 0.5rem;">
            <i class="pi pi-list"></i>
            <span>{{ $t('prediction.features') }}</span>
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
        <Button type="submit" :label="$t('prediction.submit')" icon="pi pi-check" :loading="submitting" />
      </div>
    </form>

    <div v-if="result" style="margin-top: 2rem;">
        <Card>
        <template #title>
            <div style="display: flex; align-items: center; gap: 0.5rem;">
            <i class="pi pi-check-circle" style="color: var(--p-green-500);"></i>
            <span>{{ $t('prediction.result') }}</span>
            </div>
        </template>
        <template #content>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; margin-bottom: 1.5rem;">
            <div style="background: var(--p-surface-100); padding: 1rem; border-radius: 0.5rem; text-align: center;">
                <p style="font-size: 0.875rem; color: var(--p-text-muted-color); margin-bottom: 0.25rem;">{{ $t('prediction.prediction') }}</p>
                <p style="font-size: 1.75rem; font-weight: bold; color: var(--p-primary-color);">{{ result.prediction }}</p>
            </div>
            <div style="background: var(--p-surface-100); padding: 1rem; border-radius: 0.5rem; text-align: center;">
                <p style="font-size: 0.875rem; color: var(--p-text-muted-color); margin-bottom: 0.25rem;">{{ $t('prediction.model_used') }}</p>
                <p style="font-weight: 600;">{{ result.model_name }}</p>
            </div>
            <div style="background: var(--p-surface-100); padding: 1rem; border-radius: 0.5rem; text-align: center;">
                <p style="font-size: 0.875rem; color: var(--p-text-muted-color); margin-bottom: 0.25rem;">Version</p>
                <p style="font-weight: 600;">{{ result.version || 'default' }}</p>
            </div>
            <div style="background: var(--p-surface-100); padding: 1rem; border-radius: 0.5rem; text-align: center;">
                <p style="font-size: 0.875rem; color: var(--p-text-muted-color); margin-bottom: 0.25rem;">Profile</p>
                <p style="font-weight: 600;">{{ result.profile }}</p>
            </div>
            </div>

            <!-- GAUGE for primary class probability -->
            <div v-if="primaryProbability !== null" style="max-width: 320px; margin: 0 auto 1.5rem auto;">
            <GaugeChart 
                :value="primaryProbability" 
                :label="'Confidence: ' + result.prediction"
                :thresholds="{ low: 0.4, medium: 0.75 }"
            />
            </div>

            <div v-if="result.raw_scores && Object.keys(result.raw_scores).length">
            <Divider />
            <h4 style="margin-bottom: 1rem;">{{ $t('prediction.raw_scores') }}</h4>
            
            <!-- Horizontal Bar Chart for all class probabilities -->
            <div style="background: var(--p-surface-100); border-radius: 0.5rem; padding: 1rem;">
                <div 
                v-for="(score, className) in result.raw_scores" 
                :key="className"
                style="margin-bottom: 0.75rem;"
                >
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                    <span style="font-weight: 500;">{{ className }}</span>
                    <span style="font-weight: 600;">{{ (score * 100).toFixed(1) }}%</span>
                </div>
                <div style="
                    height: 24px; 
                    background: var(--p-surface-200); 
                    border-radius: 12px; 
                    overflow: hidden;
                ">
                    <div :style="{
                    height: '100%',
                    width: (score * 100) + '%',
                    background: getBarColor(score),
                    borderRadius: '12px',
                    transition: 'width 0.5s ease',
                    minWidth: score > 0 ? '4px' : '0',
                    }" />
                </div>
                </div>
            </div>
            </div>
        </template>
        </Card>
    </div>
    </div>

    <Toast />
</template>

<script setup lang="ts">
import { usePredictionStore } from '@/stores/predictionStore'
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
import GaugeChart from '@/components/GaugeChart.vue'
import { predict } from '@/api/endpoints'
import type { PredictionResponse } from '@/types'

const predictionStore = usePredictionStore()

const toast = useToast()
const { t } = useI18n()

const profiles = ['leve', 'regular', 'pesado']
const tasks = [
  { label: 'Classification', value: 'classification' },
  { label: 'Regression', value: 'regression' }
]

const modelOptions = {
  classification: ['Decision_Tree', 'NeuralNet', 'SVM', 'KNN'],
  regression: ['Linear', 'Tree', 'SVM', 'NeuralNet'],
}

const form = reactive({
  profile: 'leve',
  version: '',
  task: 'classification' as 'classification' | 'regression',
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
})

const availableModels = computed(() => modelOptions[form.task] || [])

const onTaskChange = () => {
  const models = modelOptions[form.task]
  if (models && models.length) {
    form.model_name = models[0]
  }
}

const result = ref<PredictionResponse | null>(null)
const submitting = ref(false)

// Get the probability for the predicted class
const primaryProbability = computed(() => {
  if (!result.value?.raw_scores || !result.value?.prediction) return null
  return result.value.raw_scores[result.value.prediction] ?? null
})

const getBarColor = (score: number) => {
  if (score < 0.3) return 'var(--p-green-500)'
  if (score < 0.7) return 'var(--p-orange-500)'
  return 'var(--p-red-500)'
}

const onSubmit = async () => {
  submitting.value = true
  try {
    const payload = {
      profile: form.profile,
      version: form.version || undefined,
      task: form.task,
      model_name: form.model_name,
      features: form.features,
    }
    const response = await predict(payload)
    result.value = response.data
    
    predictionStore.addRecord({
      profile: form.profile,
      version: form.version,
      task: form.task,
      model_name: form.model_name,
      features: { ...form.features },
      prediction: response.data.prediction,
      raw_scores: response.data.raw_scores,
      confidence: primaryProbability.value ?? undefined,
    })
    
    toast.add({ severity: 'success', summary: t('common.success'), detail: 'Prediction completed', life: 3000 })
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