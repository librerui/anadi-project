<template>
  <div>
    <div style="margin-bottom: 1.5rem;">
      <h1 style="font-size: 1.875rem; font-weight: bold;">{{ $t('prediction.title') }}</h1>
      <p style="color: var(--p-text-muted-color);">{{ $t('prediction.subtitle') }}</p>
    </div>

    <Card style="margin-bottom: 1rem;">
      <template #title>
        <div style="display: flex; align-items: center; gap: 0.5rem;">
          <i class="pi pi-sliders-h"></i>
          <span>{{ $t('prediction.configuration') }}</span>
        </div>
      </template>
      <template #content>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1rem;">
          <!-- Profile with descriptive labels -->
          <div style="display: flex; flex-direction: column; gap: 0.25rem; min-width: 0;">
            <label for="profile" style="font-weight: 500;">{{ $t('prediction.profile') }}</label>
            <Dropdown id="profile" v-model="form.profile" :options="profileOptions" optionLabel="label" optionValue="value" :placeholder="t('prediction.select_profile')" fluid>
              <template #option="slotProps">
                <div style="display: flex; flex-direction: column; gap: 0.15rem;">
                  <span style="font-weight: 600;">{{ slotProps.option.label }}</span>
                  <span style="font-size: 0.75rem; color: var(--p-text-muted-color);">{{ slotProps.option.description }}</span>
                </div>
              </template>
            </Dropdown>
          </div>
          <!-- Version selector -->
          <div style="display: flex; flex-direction: column; gap: 0.25rem; min-width: 0;">
            <label for="version" style="font-weight: 500;">{{ $t('prediction.version') }}</label>
            <Dropdown id="version" v-model="form.version" :options="versionOptions" optionLabel="label" optionValue="value" :placeholder="t('prediction.select_version')" showClear fluid>
              <template #option="slotProps">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                  <span>{{ slotProps.option.label }}</span>
                  <Tag v-if="slotProps.option.recommended" :value="$t('common.recommended')" severity="success" style="font-size: 0.7rem;" />
                </div>
              </template>
            </Dropdown>
          </div>
        </div>
      </template>
    </Card>

    <!-- PTD Selection + Map -->
    <Card style="margin-bottom: 1rem;">
      <template #title>
        <div style="display: flex; align-items: center; gap: 0.5rem;">
          <i class="pi pi-map-marker"></i>
          <span>{{ $t('prediction.ptd_selection') }}</span>
        </div>
      </template>
      <template #content>
        <PTDSelector
          ref="ptdSelectorRef"
          idPrefix="pred_"
          v-model="selectedPTD"
          @select="onPTDSelected"
          @encodedChange="onEncodedChange"
        />
      </template>
    </Card>

    <TabView v-model:activeIndex="activeTab" @update:activeIndex="onTabChange">
      <TabPanel>
        <template #header>
          <div style="display: flex; align-items: center; gap: 0.4rem; white-space: nowrap;">
            <i class="pi pi-tags"></i>
            <span>{{ $t('prediction.classification_tab') }}</span>
          </div>
        </template>

        <form @submit.prevent="onSubmit('classification')">
          <Card style="margin-bottom: 1rem;">
            <template #title>
              <div style="display: flex; align-items: center; gap: 0.5rem;">
                <i class="pi pi-cog"></i>
                <span>{{ $t('prediction.model') }}</span>
              </div>
            </template>
            <template #content>
              <div style="display: flex; flex-direction: column; gap: 0.25rem; max-width: 320px; min-width: 0;">
                <Dropdown id="model_classification" v-model="form.model_name" :options="modelOptions.classification" optionLabel="label" optionValue="value" :placeholder="t('prediction.select_model')" fluid>
                  <template #option="slotProps">
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                      <span>{{ slotProps.option.label }}</span>
                      <Tag v-if="slotProps.option.recommended" :value="$t('common.recommended')" severity="success" style="font-size: 0.7rem;" />
                    </div>
                  </template>
                </Dropdown>
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
                <div v-for="(value, key) in form.features" :key="key" style="display: flex; flex-direction: column; gap: 0.25rem; min-width: 0;">
                  <label :for="'c_' + key" style="font-size: 0.875rem; font-weight: 500;">
                    {{ key }} <span v-if="featureUnit(key)" style="color: var(--p-text-muted-color); font-weight: 400;">({{ featureUnit(key) }})</span>
                  </label>
                  <InputNumber :id="'c_' + key" v-model="form.features[key]" mode="decimal" :min="0" :step="0.5" fluid showButtons :minFractionDigits="1" />
                </div>
              </div>
            </template>
          </Card>

          <div style="display: flex; justify-content: flex-end;">
            <Button type="submit" :label="$t('prediction.submit')" icon="pi pi-check" :loading="submittingClassification" />
          </div>
        </form>

        <div ref="resultClassificationRef" v-if="resultClassification" style="margin-top: 2rem;">
          <Card>
            <template #title>
              <div style="display: flex; align-items: center; gap: 0.5rem;">
                <i class="pi pi-check-circle" style="color: var(--p-green-500);"></i>
                <span>{{ $t('prediction.result') }}</span>
              </div>
            </template>
            <template #content>
              <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; margin-bottom: 1.5rem;">
                <div style="background: var(--p-surface-100); padding: 1rem; border-radius: 0.5rem; text-align: center; min-width: 0;">
                  <p style="font-size: 0.875rem; color: var(--p-text-muted-color); margin-bottom: 0.25rem;">{{ $t('prediction.predicted_class') }}</p>
                  <Tag :value="resultClassification.prediction" :severity="classSeverity(resultClassification.prediction)" style="font-size: 1.25rem; padding: 0.5rem 1rem; margin-top: 0.25rem;" />
                </div>
                <div style="background: var(--p-surface-100); padding: 1rem; border-radius: 0.5rem; text-align: center; min-width: 0;">
                  <p style="font-size: 0.875rem; color: var(--p-text-muted-color); margin-bottom: 0.25rem;">{{ $t('prediction.model_used') }}</p>
                  <p style="font-weight: 600;">{{ resultClassification.model_name }}</p>
                </div>
                <div style="background: var(--p-surface-100); padding: 1rem; border-radius: 0.5rem; text-align: center; min-width: 0;">
                  <p style="font-size: 0.875rem; color: var(--p-text-muted-color); margin-bottom: 0.25rem;">{{ $t('prediction.model_version') }}</p>
                  <p style="font-weight: 600;">{{ resultClassification.version || 'default' }}</p>
                </div>
                <div style="background: var(--p-surface-100); padding: 1rem; border-radius: 0.5rem; text-align: center; min-width: 0;">
                  <p style="font-size: 0.875rem; color: var(--p-text-muted-color); margin-bottom: 0.25rem;">{{ $t('prediction.profile_used') }}</p>
                  <p style="font-weight: 600;">{{ resultClassification.profile }}</p>
                </div>
              </div>

              <div v-if="primaryProbability !== null" style="max-width: 320px; margin: 0 auto 1.5rem auto;">
                <GaugeChart :value="primaryProbability" :label="t('prediction.confidence') + ': ' + resultClassification.prediction" :thresholds="{ low: 0.4, medium: 0.75 }" />
              </div>

              <div v-if="resultClassification.raw_scores && Object.keys(resultClassification.raw_scores).length">
                <Divider />
                <h4 style="margin-bottom: 1rem;">{{ $t('prediction.raw_scores') }}</h4>
                <div style="background: var(--p-surface-100); border-radius: 0.5rem; padding: 1rem;">
                  <div v-for="(score, className) in resultClassification.raw_scores" :key="className" style="margin-bottom: 0.75rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.25rem;">
                      <Tag :value="className" :severity="classSeverity(className)" style="font-size: 0.85rem;" />
                      <span style="font-weight: 600;">{{ (score * 100).toFixed(1) }}%</span>
                    </div>
                    <div style="height: 24px; background: var(--p-surface-200); border-radius: 12px; overflow: hidden;">
                      <div :style="{ height: '100%', width: (score * 100) + '%', background: classColor(className), borderRadius: '12px', transition: 'width 0.5s ease', minWidth: score > 0 ? '4px' : '0' }" />
                    </div>
                  </div>
                </div>
              </div>
            </template>
          </Card>
        </div>
      </TabPanel>

      <TabPanel>
        <template #header>
          <div style="display: flex; align-items: center; gap: 0.4rem; white-space: nowrap;">
            <i class="pi pi-chart-line"></i>
            <span>{{ $t('prediction.regression_tab') }}</span>
          </div>
        </template>

        <form @submit.prevent="onSubmit('regression')">
          <Card style="margin-bottom: 1rem;">
            <template #title>
              <div style="display: flex; align-items: center; gap: 0.5rem;">
                <i class="pi pi-cog"></i>
                <span>{{ $t('prediction.model') }}</span>
              </div>
            </template>
            <template #content>
              <div style="display: flex; flex-direction: column; gap: 0.25rem; max-width: 320px; min-width: 0;">
                <Dropdown id="model_regression" v-model="form.model_name" :options="modelOptions.regression" optionLabel="label" optionValue="value" :placeholder="t('prediction.select_model')" fluid>
                  <template #option="slotProps">
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                      <span>{{ slotProps.option.label }}</span>
                      <Tag v-if="slotProps.option.recommended" :value="$t('common.recommended')" severity="success" style="font-size: 0.7rem;" />
                    </div>
                  </template>
                </Dropdown>
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
                <div v-for="(value, key) in form.features" :key="key" style="display: flex; flex-direction: column; gap: 0.25rem; min-width: 0;">
                  <label :for="'r_' + key" style="font-size: 0.875rem; font-weight: 500;">
                    {{ key }} <span v-if="featureUnit(key)" style="color: var(--p-text-muted-color); font-weight: 400;">({{ featureUnit(key) }})</span>
                  </label>
                  <InputNumber :id="'r_' + key" v-model="form.features[key]" mode="decimal" :min="0" :step="0.5" fluid showButtons :minFractionDigits="1" />
                </div>
              </div>
            </template>
          </Card>

          <Card style="margin-bottom: 1rem;">
            <template #title>
              <div style="display: flex; align-items: center; gap: 0.5rem;">
                <i class="pi pi-plug"></i>
                <span>{{ $t('prediction.charger_simulation') }}</span>
              </div>
            </template>
            <template #content>
              <ChargerModelPicker v-model="form.charger_model_id" @select="onChargerModelSelect" style="margin-bottom: 1.25rem;" />

              <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                <div style="display: flex; flex-direction: column; gap: 0.25rem; min-width: 0;">
                  <label style="font-weight: 500;">{{ $t('prediction.charger_power') }} ({{ $t('prediction.units.kw') }})</label>
                  <InputNumber v-model="form.charger_power" :min="0" :step="0.5" fluid showButtons :minFractionDigits="1" />
                </div>
                <div style="display: flex; flex-direction: column; gap: 0.25rem; min-width: 0;">
                  <label for="n_chargers" style="font-weight: 500;">{{ $t('prediction.number_of_chargers') }}</label>
                  <InputNumber id="n_chargers" v-model="form.n_chargers" :min="1" :step="1" fluid showButtons />
                </div>
                <div style="display: flex; flex-direction: column; gap: 0.25rem; min-width: 0;">
                  <label for="utilization_factor" style="font-weight: 500;">{{ $t('prediction.utilization_factor') }} ({{ $t('prediction.units.ratio') }})</label>
                  <InputNumber id="utilization_factor" v-model="form.utilization_factor" :min="0" :max="1" :step="0.05" fluid showButtons :minFractionDigits="2" />
                </div>
              </div>

              <div style="margin-top: 1rem; display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem;">
                <div style="background: var(--p-surface-100); padding: 1rem; border-radius: 0.5rem; min-width: 0;">
                  <p style="margin: 0 0 0.5rem 0; font-size: 0.875rem; color: var(--p-text-muted-color);">{{ $t('prediction.total_charger_load') }}</p>
                  <p style="font-weight: 600;">{{ totalChargerLoad.toFixed(2) }} {{ $t('prediction.units.kw') }}</p>
                </div>
                <div style="background: var(--p-surface-100); padding: 1rem; border-radius: 0.5rem; min-width: 0;">
                  <p style="margin: 0 0 0.5rem 0; font-size: 0.875rem; color: var(--p-text-muted-color);">{{ $t('prediction.supported_chargers') }}</p>
                  <p style="font-weight: 600;">{{ supportedChargersCount }} {{ $t('prediction.units.units') }}</p>
                </div>
              </div>
            </template>
          </Card>

          <Card style="margin-bottom: 1rem;">
            <template #title>
              <div style="display: flex; align-items: center; gap: 0.5rem;">
                <i class="pi pi-shield"></i>
                <span>{{ $t('prediction.grid_security') }}</span>
              </div>
            </template>
            <template #content>
              <p style="margin: 0 0 1rem 0; color: var(--p-text-muted-color);">{{ $t('prediction.grid_security_hint') }}</p>
              <p style="margin: 0 0 1rem 0; font-size: 0.8rem; color: var(--p-text-muted-color);">
                {{ $t('prediction.capacity_base') }}: <strong>{{ gridCapacityBase.toFixed(1) }} {{ $t('prediction.units.kva') }}</strong>
                &nbsp;•&nbsp;
                {{ $t('prediction.current_setup') }}: <strong>{{ form.n_chargers }} × {{ form.charger_power }} {{ $t('prediction.units.kw') }}</strong>
              </p>
              <GridSecurityChart :base-capacity="gridCapacityBase" :charger-power="form.charger_power" :utilization-factor="form.utilization_factor" :current-chargers="form.n_chargers" />
            </template>
          </Card>

          <div style="display: flex; justify-content: flex-end;">
            <Button type="submit" :label="$t('prediction.submit')" icon="pi pi-check" :loading="submittingRegression" />
          </div>
        </form>

        <div ref="resultRegressionRef" v-if="resultRegression" style="margin-top: 2rem;">
          <Card>
            <template #title>
              <div style="display: flex; align-items: center; gap: 0.5rem;">
                <i class="pi pi-check-circle" style="color: var(--p-green-500);"></i>
                <span>{{ $t('prediction.result') }}</span>
              </div>
            </template>
            <template #content>
              <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem;">
                <div style="background: var(--p-surface-100); padding: 1rem; border-radius: 0.5rem; text-align: center; min-width: 0;">
                  <p style="font-size: 0.875rem; color: var(--p-text-muted-color); margin-bottom: 0.25rem;">{{ $t('prediction.predicted_value') }}</p>
                  <p style="font-size: 1.75rem; font-weight: bold; color: var(--p-primary-color);">{{ Number(resultRegression.prediction).toFixed(2) }} {{ $t('prediction.units.kw') }}</p>
                </div>
                <div style="background: var(--p-surface-100); padding: 1rem; border-radius: 0.5rem; text-align: center; min-width: 0;">
                  <p style="font-size: 0.875rem; color: var(--p-text-muted-color); margin-bottom: 0.25rem;">{{ $t('prediction.model_used') }}</p>
                  <p style="font-weight: 600;">{{ resultRegression.model_name }}</p>
                </div>
                <div style="background: var(--p-surface-100); padding: 1rem; border-radius: 0.5rem; text-align: center; min-width: 0;">
                  <p style="font-size: 0.875rem; color: var(--p-text-muted-color); margin-bottom: 0.25rem;">{{ $t('prediction.model_version') }}</p>
                  <p style="font-weight: 600;">{{ resultRegression.version || 'default' }}</p>
                </div>
                <div style="background: var(--p-surface-100); padding: 1rem; border-radius: 0.5rem; text-align: center; min-width: 0;">
                  <p style="font-size: 0.875rem; color: var(--p-text-muted-color); margin-bottom: 0.25rem;">{{ $t('prediction.profile_used') }}</p>
                  <p style="font-weight: 600;">{{ resultRegression.profile }}</p>
                </div>
              </div>
            </template>
          </Card>
        </div>
      </TabPanel>
    </TabView>

    <Toast />
  </div>
</template>

<script setup lang="ts">
import { usePredictionStore } from '@/stores/predictionStore'
import { usePTDCacheStore } from '@/stores/ptdCacheStore'
import { reactive, ref, computed, nextTick } from 'vue'
import type { Ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useToast } from 'primevue/usetoast'
import Dropdown from 'primevue/dropdown'
import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import Button from 'primevue/button'
import Card from 'primevue/card'
import Divider from 'primevue/divider'
import Toast from 'primevue/toast'
import Tag from 'primevue/tag'
import TabView from 'primevue/tabview'
import TabPanel from 'primevue/tabpanel'
import GaugeChart from '@/components/GaugeChart.vue'
import ChargerModelPicker from '@/components/ChargerModelPicker.vue'
import GridSecurityChart from '@/components/GridSecurityChart.vue'
import PTDSelector from '@/components/PTDSelector.vue'
import { predict } from '@/api/endpoints'
import type { PredictionResponse, PTDBase } from '@/types'
import { getChargerModel, type ChargerModel } from '@/data/chargerModels'

const predictionStore = usePredictionStore()
const ptdCache = usePTDCacheStore()

const toast = useToast()
const { t } = useI18n()

// ── Profile options with descriptive labels ──
const profileOptions = computed(() => [
  { value: 'leve', label: t('prediction.profile_leve'), description: t('prediction.profile_leve_desc') },
  { value: 'regular', label: t('prediction.profile_regular'), description: t('prediction.profile_regular_desc') },
  { value: 'pesado', label: t('prediction.profile_pesado'), description: t('prediction.profile_pesado_desc') },
])

// ── Version options ──
const versionOptions = [
  { value: '', label: t('prediction.version_latest'), recommended: true },
  { value: '20260630195806', label: '20260630195806' },
]

const modelOptions: Record<'classification' | 'regression', { label: string; value: string; recommended?: boolean }[]> = {
  classification: [
    { label: 'NeuralNet', value: 'NeuralNet', recommended: true },
    { label: 'Decision_Tree', value: 'Decision_Tree', recommended: true },
    { label: 'SVM', value: 'SVM' },
    { label: 'KNN', value: 'KNN' },
  ],
  regression: [
    { label: 'NeuralNet', value: 'NeuralNet', recommended: true },
    { label: 'Tree', value: 'Tree', recommended: true },
    { label: 'Linear', value: 'Linear' },
    { label: 'SVM', value: 'SVM' },
  ],
}

const featureUnitKeys: Record<string, string> = {
  'Potência instalada [kVA]': 'kva',
  'P_IP_Total': 'kw',
  'P_IP_Inef': 'kw',
  'LED_Ratio': 'ratio',
  'N_Luminarias': 'units',
  'N_Lampadas': 'units',
  'Cap_per_Cliente': 'kva',
  'N_Clientes': 'clients',
}

const featureUnit = (key: string) => {
  const unitKey = featureUnitKeys[key]
  return unitKey ? t(`prediction.units.${unitKey}`) : ''
}

const form = reactive({
  profile: 'leve',
  version: '' as string,
  model_name: 'NeuralNet',
  distrito: null as string | null,
  concelho: null as string | null,
  ptd_id: null as string | null,
  charger_model_id: 'wallbox-pulsar-plus-7_4' as string,
  charger_power: 7.4,
  n_chargers: 2,
  utilization_factor: 0.7,
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
  } as Record<string, number>,
})

const activeTab = ref(0)
const onTabChange = (index: number) => {
  const task = index === 0 ? 'classification' : 'regression'
  const models = modelOptions[task]
  if (models && models.length && !models.some(m => m.value === form.model_name)) {
    form.model_name = models[0].value
  }
}

const onChargerModelSelect = (charger: ChargerModel) => {
  form.charger_power = charger.power
}

const resultClassificationRef = ref<HTMLElement | null>(null)
const resultClassification = ref<PredictionResponse | null>(null)
const resultRegressionRef = ref<HTMLElement | null>(null)
const resultRegression = ref<PredictionResponse | null>(null)
const submittingClassification = ref(false)
const submittingRegression = ref(false)

const selectedPTD = ref<PTDBase | null>(null)

const onEncodedChange = (values: { distrito_enc: number | null; concelho_enc: number | null }) => {
  if (values.distrito_enc != null) form.features['Distrito_enc'] = values.distrito_enc
  if (values.concelho_enc != null) form.features['Concelho_enc'] = values.concelho_enc
}

const onPTDSelected = (ptd: PTDBase) => {
  selectedPTD.value = ptd
  normalizePTD(ptd)
}

const totalChargerLoad = computed(() => form.n_chargers * form.charger_power * form.utilization_factor)
const gridCapacityBase = computed(() => form.features['Potência instalada [kVA]'] || 50)

const supportedChargersCount = computed(() => {
  const singleChargerEffectiveLoad = form.charger_power * form.utilization_factor
  if (singleChargerEffectiveLoad <= 0) return 0
  return Math.max(0, Math.floor(gridCapacityBase.value / singleChargerEffectiveLoad))
})

const primaryProbability = computed(() => {
  if (!resultClassification.value?.raw_scores || !resultClassification.value?.prediction) return null
  return resultClassification.value.raw_scores[resultClassification.value.prediction] ?? null
})

const scrollToResults = (refEl: Ref<HTMLElement | null>) => {
  if (refEl.value) refEl.value.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

const classSeverity = (value: string): 'success' | 'warn' | 'danger' | 'info' => {
  if (value === 'alto' || value === 'high') return 'danger'
  if (value === 'medio' || value === 'medium') return 'warn'
  if (value === 'baixo' || value === 'low') return 'success'
  return 'info'
}

const classColor = (value: string) => {
  if (value === 'alto' || value === 'high') return '#ef4444'
  if (value === 'medio' || value === 'medium') return '#f97316'
  if (value === 'baixo' || value === 'low') return '#22c55e'
  return '#6b7280'
}

const normalizePTD = (ptd: PTDBase) => {
  form.distrito = ptd.distrito
  form.concelho = ptd.concelho
  form.ptd_id = ptd.codigo_instalacao
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

const onSubmit = async (task: 'classification' | 'regression') => {
  const submittingRef = task === 'classification' ? submittingClassification : submittingRegression
  submittingRef.value = true
  try {
    const payload = {
      profile: form.profile,
      version: form.version || undefined,
      task,
      model_name: form.model_name,
      features: form.features,
    }
    const response = await predict(payload)

    if (task === 'classification') {
      resultClassification.value = response.data
      await nextTick()
      scrollToResults(resultClassificationRef)
    } else {
      resultRegression.value = response.data
      await nextTick()
      scrollToResults(resultRegressionRef)
    }

    predictionStore.addRecord({
      profile: form.profile,
      version: form.version,
      task,
      model_name: form.model_name,
      features: { ...form.features },
      prediction: response.data.prediction,
      raw_scores: response.data.raw_scores,
      confidence: task === 'classification' ? (primaryProbability.value ?? undefined) : undefined,
    })

    toast.add({ severity: 'success', summary: t('common.success'), detail: 'Prediction completed', life: 3000 })
  } catch (error: any) {
    toast.add({ severity: 'error', summary: t('common.error'), detail: error.response?.data?.detail || error.message, life: 5000 })
  } finally {
    submittingRef.value = false
  }
}
</script>

<style scoped>
:deep(.p-inputnumber),
:deep(.p-inputnumber-input),
:deep(.p-dropdown) {
  width: 100% !important;
  min-width: 0;
}
:deep(.p-inputnumber-input) {
  width: 100% !important;
}
:deep(.p-dropdown-label) {
  width: 100%;
}
</style>