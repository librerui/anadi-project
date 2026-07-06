<template>
  <div>
    <div style="margin-bottom: 1.5rem;">
      <h1 style="font-size: 1.875rem; font-weight: bold;">{{ $t('simulation.title') }}</h1>
      <p style="color: var(--p-text-muted-color);">{{ $t('simulation.subtitle') }}</p>
    </div>

    <form @submit.prevent="onSubmit">
      <!-- Configuration -->
      <Card style="margin-bottom: 1rem;">
        <template #title>
          <div style="display: flex; align-items: center; gap: 0.5rem;">
            <i class="pi pi-sliders-h"></i>
            <span>{{ $t('simulation.configuration') }}</span>
          </div>
        </template>
        <template #content>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
            <div style="display: flex; flex-direction: column; gap: 0.25rem; min-width: 0;">
              <label for="profile" style="font-weight: 500;">{{ $t('simulation.profile') }}</label>
              <Dropdown id="profile" v-model="form.profile" :options="profiles" :placeholder="t('simulation.select_profile')" style="width: 100%;" />
            </div>
            <div style="display: flex; flex-direction: column; gap: 0.25rem; min-width: 0;">
              <label for="version" style="font-weight: 500;">{{ $t('simulation.version') }}</label>
              <InputText id="version" v-model="form.version" :placeholder="t('simulation.optional_placeholder')" style="width: 100%;" />
            </div>
            <div style="display: flex; flex-direction: column; gap: 0.25rem; min-width: 0;">
              <label for="model" style="font-weight: 500;">{{ $t('simulation.model') }}</label>
              <Dropdown id="model" v-model="form.model_name" :options="classificationModels" style="width: 100%;" />
            </div>
          </div>
        </template>
      </Card>

      <!-- PTD Selection + Map -->
      <Card style="margin-bottom: 1rem;">
        <template #title>
          <div style="display: flex; align-items: center; gap: 0.5rem;">
            <i class="pi pi-map-marker"></i>
            <span>{{ $t('simulation.ptd_selection') }}</span>
          </div>
        </template>
        <template #content>
          <PTDSelector
            idPrefix="sim_"
            v-model="selectedPTD"
            @select="onPTDSelected"
            @encodedChange="onEncodedChange"
          />

          <!-- Show synced encoded values -->
          <div style="margin-top: 1rem; padding: 0.75rem 1rem; background: var(--p-surface-100); border-radius: 0.5rem; display: flex; gap: 1.5rem; flex-wrap: wrap; font-size: 0.875rem;">
            <div>
              <span style="color: var(--p-text-muted-color);">Distrito_enc:</span>
              <span style="font-weight: 600; margin-left: 0.5rem;">{{ form.features['Distrito_enc'] }}</span>
            </div>
            <div>
              <span style="color: var(--p-text-muted-color);">Concelho_enc:</span>
              <span style="font-weight: 600; margin-left: 0.5rem;">{{ form.features['Concelho_enc'] }}</span>
            </div>
            <div>
              <span style="color: var(--p-text-muted-color);">N_Clientes:</span>
              <span style="font-weight: 600; margin-left: 0.5rem;">{{ form.features['N_Clientes'] }}</span>
            </div>
          </div>
        </template>
      </Card>

      <!-- Scenario Selector -->
      <Card style="margin-bottom: 1rem;">
        <template #title>
          <div style="display: flex; align-items: center; gap: 0.5rem;">
            <i class="pi pi-bullseye"></i>
            <span>{{ $t('simulation.scenario_title') }}</span>
          </div>
        </template>
        <template #content>
          <p style="margin: 0 0 1rem 0; color: var(--p-text-muted-color);">
            {{ $t('simulation.scenario_hint') }}
          </p>

          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 0.75rem;">
            <div
              v-for="cls in overloadClasses"
              :key="cls.value"
              @click="form.overload_class = cls.value"
              style="cursor: pointer; padding: 1rem; border-radius: 0.75rem; border: 2px solid transparent; text-align: center; transition: all 0.2s;"
              :style="{
                background: form.overload_class === cls.value ? cls.selectedBg : 'var(--p-surface-100)',
                borderColor: form.overload_class === cls.value ? cls.color : 'transparent',
                boxShadow: form.overload_class === cls.value ? '0 2px 8px ' + cls.shadow : 'none',
              }"
            >
              <i :class="cls.icon" style="font-size: 1.5rem; margin-bottom: 0.5rem; display: block;" :style="{ color: cls.color }"></i>
              <p style="margin: 0; font-weight: 600; font-size: 0.95rem;">{{ cls.label }}</p>
              <p style="margin: 0.25rem 0 0 0; font-size: 0.75rem; color: var(--p-text-muted-color);">{{ cls.description }}</p>
            </div>
          </div>
        </template>
      </Card>

      <!-- Parameters -->
      <Card style="margin-bottom: 1rem;">
        <template #title>
          <div style="display: flex; align-items: center; gap: 0.5rem;">
            <i class="pi pi-cog"></i>
            <span>{{ $t('simulation.parameters') }}</span>
          </div>
        </template>
        <template #content>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
            <div style="display: flex; flex-direction: column; gap: 0.25rem; min-width: 0;">
              <label for="iterations" style="font-weight: 500;">{{ $t('simulation.iterations') }}</label>
              <InputNumber id="iterations" v-model="form.iterations" :min="100" :max="100000" style="width: 100%;" showButtons />
            </div>
            <div style="display: flex; flex-direction: column; gap: 0.25rem; min-width: 0;">
              <label for="noise" style="font-weight: 500;">{{ $t('simulation.noise_scale') }}</label>
              <InputNumber id="noise" v-model="form.noise_scale" :min="0.01" :step="0.01" style="width: 100%;" showButtons :minFractionDigits="2" />
            </div>
            <div style="display: flex; flex-direction: column; gap: 0.25rem; min-width: 0;">
              <label for="seed" style="font-weight: 500;">{{ $t('simulation.seed') }}</label>
              <InputNumber id="seed" v-model="form.seed" :min="0" style="width: 100%;" showButtons />
            </div>
          </div>
        </template>
      </Card>

      <!-- Features -->
      <Card style="margin-bottom: 1rem;">
        <template #title>
          <div style="display: flex; align-items: center; gap: 0.5rem;">
            <i class="pi pi-list"></i>
            <span>{{ $t('simulation.features') }}</span>
          </div>
        </template>
        <template #content>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
            <div v-for="(value, key) in form.features" :key="key" style="display: flex; flex-direction: column; gap: 0.25rem; min-width: 0;">
              <label :for="key" style="font-size: 0.875rem; font-weight: 500;">{{ key }}</label>
              <InputNumber :id="key" v-model="form.features[key]" mode="decimal" :min="0" :step="0.5" style="width: 100%;" showButtons :minFractionDigits="1" />
            </div>
          </div>
        </template>
      </Card>

      <div style="display: flex; justify-content: flex-end;">
        <Button type="submit" :label="submitLabel" icon="pi pi-play" :severity="selectedScenarioSeverity" :loading="submitting" />
      </div>
    </form>

    <!-- Results -->
    <div ref="resultRef" v-if="result" style="margin-top: 2rem;">
      <Card>
        <template #title>
          <div style="display: flex; align-items: center; gap: 0.5rem;">
            <i class="pi pi-check-circle" :style="{ color: selectedScenarioColor }"></i>
            <span>{{ $t('simulation.result') }}</span>
          </div>
        </template>
        <template #content>
          <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1.5rem; padding: 0.75rem 1rem; background: var(--p-surface-100); border-radius: 0.5rem;">
            <span style="font-size: 0.875rem; color: var(--p-text-muted-color);">{{ $t('simulation.simulated_scenario') }}:</span>
            <Tag :value="selectedScenarioLabel" :severity="selectedScenarioSeverity" />
          </div>

          <Message :severity="detectionSeverity" :closable="false" style="margin-bottom: 1.5rem;">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
              <i :class="detectionIcon"></i>
              <span>{{ detectionBannerText }}</span>
            </div>
          </Message>

          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin-bottom: 1.5rem;">
            <div style="background: var(--p-surface-100); padding: 0.75rem; border-radius: 0.5rem; text-align: center; min-width: 0;">
              <p style="font-size: 0.875rem; color: var(--p-text-muted-color); margin-bottom: 0.25rem;">{{ $t('simulation.iterations') }}</p>
              <p style="font-weight: 600;">{{ result.iterations.toLocaleString() }}</p>
            </div>
            <div style="background: var(--p-surface-100); padding: 0.75rem; border-radius: 0.5rem; text-align: center; min-width: 0;">
              <p style="font-size: 0.875rem; color: var(--p-text-muted-color); margin-bottom: 0.25rem;">{{ $t('simulation.model') }}</p>
              <p style="font-weight: 600;">{{ result.model_name }}</p>
            </div>
            <div style="background: var(--p-surface-100); padding: 0.75rem; border-radius: 0.5rem; text-align: center; min-width: 0;">
              <p style="font-size: 0.875rem; color: var(--p-text-muted-color); margin-bottom: 0.25rem;">{{ $t('simulation.version') }}</p>
              <p style="font-weight: 600;">{{ result.version || 'default' }}</p>
            </div>
            <div style="background: var(--p-surface-100); padding: 0.75rem; border-radius: 0.5rem; text-align: center; min-width: 0;">
              <p style="font-size: 0.875rem; color: var(--p-text-muted-color); margin-bottom: 0.25rem;">{{ $t('simulation.dominant_class') }}</p>
              <p style="font-weight: 600;">{{ dominantClass }}</p>
            </div>
          </div>

          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; align-items: start;">
            <div>
              <h4 style="margin-bottom: 0.75rem; text-align: center;">
                {{ $t('simulation.detection_rate') }}: {{ selectedScenarioLabel }}
              </h4>
              <GaugeChart
                :value="selectedClassProbability"
                :label="$t('simulation.probability_detected')"
                :thresholds="{ low: 0.3, medium: 0.7 }"
              />
              <p style="text-align: center; font-size: 0.875rem; color: var(--p-text-muted-color); margin-top: 0.5rem;">
                {{ $t('simulation.detection_rate_hint') }}
              </p>
            </div>

            <div>
              <h4 style="margin-bottom: 0.75rem; text-align: center;">{{ $t('simulation.overload_probability') }}</h4>
              <GaugeChart
                :value="result.overload_probability"
                :label="overloadClassLabel(result.overload_class)"
                :thresholds="{ low: 0.3, medium: 0.7 }"
              />
            </div>

            <div v-if="result.distribution">
              <h4 style="margin-bottom: 0.75rem; text-align: center;">{{ $t('simulation.distribution') }}</h4>
              <div style="display: flex; justify-content: center; background: var(--p-surface-100); border-radius: 0.5rem; padding: 1rem;">
                <div style="max-width: 320px; width: 100%;">
                  <PieChart :data="pieData" />
                </div>
              </div>
            </div>
          </div>

          <div v-if="result.distribution" style="margin-top: 1.5rem;">
            <Divider />
            <h4 style="margin-bottom: 1rem;">{{ $t('simulation.detection_breakdown') }}</h4>
            <div style="background: var(--p-surface-100); border-radius: 0.5rem; padding: 1rem;">
              <div style="display: grid; grid-template-columns: auto 1fr auto; gap: 0.5rem 1rem; align-items: center; margin-bottom: 0.75rem;">
                <span style="font-weight: 600; font-size: 0.875rem;">{{ $t('simulation.true_class') }}</span>
                <span></span>
                <span style="font-weight: 600; font-size: 0.875rem;">{{ $t('simulation.detected_probability') }}</span>
              </div>

              <div
                v-for="(prob, className) in result.distribution"
                :key="className"
                style="display: grid; grid-template-columns: auto 1fr auto; gap: 0.5rem 1rem; align-items: center; padding: 0.5rem 0; border-top: 1px solid var(--p-surface-200);"
                :style="{ background: String(className) === form.overload_class ? 'rgba(59, 130, 246, 0.08)' : 'transparent', borderRadius: '0.25rem', margin: '0 -0.5rem', padding: '0.5rem' }"
              >
                <Tag 
                  :value="overloadClassLabel(String(className))" 
                  :severity="classSeverity(String(className))"
                  style="font-size: 0.8rem;"
                />
                <div style="height: 20px; background: var(--p-surface-200); border-radius: 10px; overflow: hidden;">
                  <div :style="{
                    height: '100%',
                    width: (prob * 100) + '%',
                    background: classColor(String(className)),
                    borderRadius: '10px',
                    transition: 'width 0.5s ease',
                    minWidth: prob > 0 ? '4px' : '0',
                  }" />
                </div>
                <span style="font-weight: 600; font-size: 0.9rem; white-space: nowrap;">{{ (prob * 100).toFixed(1) }}%</span>
              </div>
            </div>
          </div>

          <div v-if="result.distribution" style="margin-top: 1.5rem;">
            <Divider />
            <h4 style="margin-bottom: 1rem;">{{ $t('simulation.summary_statistics') }}</h4>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 1rem;">
              <div style="background: var(--p-surface-100); padding: 0.75rem; border-radius: 0.5rem; text-align: center; min-width: 0;">
                <p style="font-size: 0.8rem; color: var(--p-text-muted-color); margin-bottom: 0.25rem;">{{ $t('simulation.mean') }}</p>
                <p style="font-weight: 600;">{{ (distributionStats.mean * 100).toFixed(1) }}%</p>
              </div>
              <div style="background: var(--p-surface-100); padding: 0.75rem; border-radius: 0.5rem; text-align: center; min-width: 0;">
                <p style="font-size: 0.8rem; color: var(--p-text-muted-color); margin-bottom: 0.25rem;">{{ $t('simulation.std_dev') }}</p>
                <p style="font-weight: 600;">{{ (distributionStats.std * 100).toFixed(1) }}%</p>
              </div>
              <div style="background: var(--p-surface-100); padding: 0.75rem; border-radius: 0.5rem; text-align: center; min-width: 0;">
                <p style="font-size: 0.8rem; color: var(--p-text-muted-color); margin-bottom: 0.25rem;">{{ $t('simulation.min') }}</p>
                <p style="font-weight: 600;">{{ (distributionStats.min * 100).toFixed(1) }}%</p>
              </div>
              <div style="background: var(--p-surface-100); padding: 0.75rem; border-radius: 0.5rem; text-align: center; min-width: 0;">
                <p style="font-size: 0.8rem; color: var(--p-text-muted-color); margin-bottom: 0.25rem;">{{ $t('simulation.max') }}</p>
                <p style="font-weight: 600;">{{ (distributionStats.max * 100).toFixed(1) }}%</p>
              </div>
              <div style="background: var(--p-surface-100); padding: 0.75rem; border-radius: 0.5rem; text-align: center; min-width: 0;">
                <p style="font-size: 0.8rem; color: var(--p-text-muted-color); margin-bottom: 0.25rem;">{{ $t('simulation.risk_margin') }}</p>
                <p style="font-weight: 600;">{{ ((1 - result.overload_probability) * 100).toFixed(1) }}%</p>
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
import { reactive, ref, computed, nextTick } from 'vue'
import { useI18n } from 'vue-i18n'
import { useToast } from 'primevue/usetoast'
import Dropdown from 'primevue/dropdown'
import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import Button from 'primevue/button'
import Card from 'primevue/card'
import Divider from 'primevue/divider'
import Toast from 'primevue/toast'
import Message from 'primevue/message'
import Tag from 'primevue/tag'
import PieChart from '@/components/PieChart.vue'
import GaugeChart from '@/components/GaugeChart.vue'
import PTDSelector from '@/components/PTDSelector.vue'
import { simulate } from '@/api/endpoints'
import type { SimulationResponse, PTDBase } from '@/types'
import { useSimulationStore } from '@/stores/simulationStore'

const simulationStore = useSimulationStore()

const toast = useToast()
const { t } = useI18n()

const profiles = ['leve', 'regular', 'pesado']
const classificationModels = ['Decision_Tree', 'NeuralNet', 'SVM', 'KNN']

const overloadClasses = computed(() => [
  { 
    label: t('common.risk_low'), 
    value: 'baixo',
    description: t('simulation.scenario_low_desc'),
    icon: 'pi pi-check-circle',
    color: '#22c55e',
    selectedBg: 'rgba(34, 197, 94, 0.12)',
    shadow: 'rgba(34, 197, 94, 0.25)',
  },
  { 
    label: t('common.risk_medium'), 
    value: 'medio',
    description: t('simulation.scenario_medium_desc'),
    icon: 'pi pi-exclamation-triangle',
    color: '#f97316',
    selectedBg: 'rgba(249, 115, 22, 0.12)',
    shadow: 'rgba(249, 115, 22, 0.25)',
  },
  { 
    label: t('common.risk_high'), 
    value: 'alto',
    description: t('simulation.scenario_high_desc'),
    icon: 'pi pi-times-circle',
    color: '#ef4444',
    selectedBg: 'rgba(239, 68, 68, 0.12)',
    shadow: 'rgba(239, 68, 68, 0.25)',
  },
])

const overloadClassLabel = (value: string) => {
  const found = overloadClasses.value.find((c) => c.value === value)
  return found ? found.label : value
}

const classColor = (value: string) => {
  if (value === 'alto') return '#ef4444'
  if (value === 'medio') return '#f97316'
  return '#22c55e'
}

const classSeverity = (value: string): 'success' | 'warn' | 'danger' | 'info' => {
  if (value === 'alto') return 'danger'
  if (value === 'medio') return 'warn'
  return 'success'
}

// PTD selection
const selectedPTD = ref<PTDBase | null>(null)

const onEncodedChange = (values: { distrito_enc: number | null; concelho_enc: number | null }) => {
  if (values.distrito_enc != null) {
    form.features['Distrito_enc'] = values.distrito_enc
  }
  if (values.concelho_enc != null) {
    form.features['Concelho_enc'] = values.concelho_enc
  }
}

const onPTDSelected = (ptd: PTDBase) => {
  selectedPTD.value = ptd
  form.features['Potência instalada [kVA]'] = ptd.potencia_instalada
  form.features['P_IP_Total'] = ptd.p_ip_total ?? 0
  form.features['P_IP_Inef'] = ptd.p_ip_inef ?? 0
  form.features['LED_Ratio'] = ptd.led_ratio ?? 0
  form.features['N_Luminarias'] = ptd.n_luminarias ?? 0
  form.features['N_Lampadas'] = ptd.n_lampadas ?? 0
  form.features['Cap_per_Cliente'] = ptd.cap_per_cliente ?? 0
  form.features['N_Clientes'] = ptd.n_clientes ?? 0
  if (ptd.distrito_enc != null) form.features['Distrito_enc'] = ptd.distrito_enc
  if (ptd.concelho_enc != null) form.features['Concelho_enc'] = ptd.concelho_enc
}

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
  overload_class: 'alto' as 'baixo' | 'medio' | 'alto',
  seed: 42,
})

const resultRef = ref<HTMLElement | null>(null)
const result = ref<SimulationResponse | null>(null)
const submitting = ref(false)

const selectedScenario = computed(() => 
  overloadClasses.value.find(c => c.value === form.overload_class)
)

const selectedScenarioLabel = computed(() => 
  selectedScenario.value?.label || form.overload_class
)

const selectedScenarioColor = computed(() => 
  selectedScenario.value?.color || '#6b7280'
)

const selectedScenarioSeverity = computed((): 'success' | 'warn' | 'danger' => {
  if (form.overload_class === 'alto') return 'danger'
  if (form.overload_class === 'medio') return 'warn'
  return 'success'
})

const submitLabel = computed(() => {
  return t('simulation.run_scenario', { class: selectedScenarioLabel.value })
})

const selectedClassProbability = computed(() => {
  if (!result.value?.distribution) return 0
  return result.value.distribution[form.overload_class] || 0
})

const detectionSeverity = computed((): 'success' | 'warn' | 'error' | 'info' => {
  if (!result.value) return 'info'
  const p = selectedClassProbability.value
  if (p >= 0.7) return 'success'
  if (p >= 0.3) return 'warn'
  return 'error'
})

const detectionIcon = computed(() => {
  if (!result.value) return 'pi pi-info-circle'
  const p = selectedClassProbability.value
  if (p >= 0.7) return 'pi pi-check-circle'
  if (p >= 0.3) return 'pi pi-exclamation-triangle'
  return 'pi pi-times-circle'
})

const detectionBannerText = computed(() => {
  if (!result.value) return ''
  const p = selectedClassProbability.value
  const scenario = selectedScenarioLabel.value
  if (p >= 0.7) return t('simulation.detection_high', { class: scenario, prob: (p * 100).toFixed(1) })
  if (p >= 0.3) return t('simulation.detection_medium', { class: scenario, prob: (p * 100).toFixed(1) })
  return t('simulation.detection_low', { class: scenario, prob: (p * 100).toFixed(1) })
})

const dominantClass = computed(() => {
  if (!result.value?.distribution) return '—'
  const entries = Object.entries(result.value.distribution)
  if (!entries.length) return '—'
  const [best] = entries.sort((a, b) => b[1] - a[1])
  return overloadClassLabel(best[0])
})

const riskSeverity = computed(() => {
  if (!result.value) return 'info'
  const p = result.value.overload_probability
  if (p < 0.3) return 'success'
  if (p < 0.7) return 'warn'
  return 'error'
})

const riskIcon = computed(() => {
  if (!result.value) return 'pi pi-info-circle'
  const p = result.value.overload_probability
  if (p < 0.3) return 'pi pi-check-circle'
  if (p < 0.7) return 'pi pi-exclamation-triangle'
  return 'pi pi-times-circle'
})

const riskBannerText = computed(() => {
  if (!result.value) return ''
  const p = result.value.overload_probability
  if (p < 0.3) return t('simulation.risk_banner_low')
  if (p < 0.7) return t('simulation.risk_banner_medium')
  return t('simulation.risk_banner_high')
})

const distributionStats = computed(() => {
  const values = result.value?.distribution ? Object.values(result.value.distribution) : []
  if (!values.length) return { mean: 0, std: 0, min: 0, max: 0 }
  const mean = values.reduce((a, b) => a + b, 0) / values.length
  const variance = values.reduce((a, b) => a + (b - mean) ** 2, 0) / values.length
  return {
    mean,
    std: Math.sqrt(variance),
    min: Math.min(...values),
    max: Math.max(...values),
  }
})

const pieData = computed(() => {
  if (!result.value?.distribution) return null
  const labels = Object.keys(result.value.distribution).map((k) => overloadClassLabel(k))
  const data = Object.values(result.value.distribution)
  const colors = Object.keys(result.value.distribution).map((k) => classColor(k))
  return {
    labels,
    datasets: [
      {
        data,
        backgroundColor: colors,
        hoverBackgroundColor: colors,
      },
    ],
  }
})

const scrollToResults = () => {
  if (resultRef.value) {
    resultRef.value.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}

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
    await nextTick()
    scrollToResults()

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

    toast.add({ severity: 'success', summary: t('common.success'), detail: t('simulation.completed'), life: 3000 })
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