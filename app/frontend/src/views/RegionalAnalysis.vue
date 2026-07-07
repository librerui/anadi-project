<template>
  <div>
    <div style="margin-bottom: 1.5rem;">
      <h1 style="font-size: 1.875rem; font-weight: bold;">{{ $t('regional.title') }}</h1>
      <p style="color: var(--p-text-muted-color);">{{ $t('regional.subtitle') }}</p>
    </div>

    <!-- Configuração -->
    <Card style="margin-bottom: 1rem;">
      <template #title>
        <div style="display: flex; align-items: center; gap: 0.5rem;">
          <i class="pi pi-sliders-h"></i>
          <span>{{ $t('regional.configuration') }}</span>
        </div>
      </template>
      <template #content>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1rem;">
          <!-- Profile with descriptive labels -->
          <div style="display: flex; flex-direction: column; gap: 0.25rem; min-width: 0;">
            <label for="profile" style="font-weight: 500;">{{ $t('regional.profile') }}</label>
            <Dropdown id="profile" v-model="form.profile" :options="profileOptions" optionLabel="label" optionValue="value" :placeholder="t('regional.select_profile')" fluid>
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
            <label for="version" style="font-weight: 500;">{{ $t('regional.version') }}</label>
            <Dropdown id="version" v-model="form.version" :options="versionOptions" optionLabel="label" optionValue="value" :placeholder="t('regional.select_version')" showClear fluid>
              <template #option="slotProps">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                  <span>{{ slotProps.option.label }}</span>
                  <Tag v-if="slotProps.option.recommended" :value="$t('common.recommended')" severity="success" style="font-size: 0.7rem;" />
                </div>
              </template>
            </Dropdown>
          </div>
          <div style="display: flex; flex-direction: column; gap: 0.25rem; min-width: 0;">
            <label for="model" style="font-weight: 500;">{{ $t('regional.model') }}</label>
            <Dropdown id="model" v-model="form.model_name" :options="regressionModels" optionLabel="label" optionValue="value" fluid>
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

    <!-- Seleção de Região -->
    <Card style="margin-bottom: 1rem;">
      <template #title>
        <div style="display: flex; align-items: center; gap: 0.5rem;">
          <i class="pi pi-map-marker"></i>
          <span>{{ $t('regional.region_selection') }}</span>
        </div>
      </template>
      <template #content>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
          <div style="display: flex; flex-direction: column; gap: 0.25rem; min-width: 0;">
            <label for="distrito" style="font-weight: 500;">{{ $t('regional.district') }}</label>
            <Dropdown id="distrito" v-model="selectedDistrito" :options="districts" :placeholder="t('regional.select_district')" fluid @change="onDistritoChange" showClear />
          </div>
          <div style="display: flex; flex-direction: column; gap: 0.25rem; min-width: 0;">
            <label for="concelho" style="font-weight: 500;">{{ $t('regional.municipality') }}</label>
            <Dropdown id="concelho" v-model="selectedConcelho" :options="concelhos" :placeholder="t('regional.select_municipality')" fluid @change="onConcelhoChange" showClear :disabled="!selectedDistrito" />
          </div>
        </div>

        <div v-if="regionPTDs.length > 0" style="margin-top: 1rem; padding: 0.75rem 1rem; background: var(--p-surface-100); border-radius: 0.5rem; display: flex; gap: 1.5rem; flex-wrap: wrap; font-size: 0.875rem;">
          <div><span style="color: var(--p-text-muted-color);">{{ $t('regional.ptds_found') }}:</span><span style="font-weight: 600; margin-left: 0.5rem;">{{ regionPTDs.length }}</span></div>
          <div><span style="color: var(--p-text-muted-color);">{{ $t('regional.district') }}:</span><span style="font-weight: 600; margin-left: 0.5rem;">{{ selectedDistrito || '—' }}</span></div>
          <div><span style="color: var(--p-text-muted-color);">{{ $t('regional.municipality') }}:</span><span style="font-weight: 600; margin-left: 0.5rem;">{{ selectedConcelho || '—' }}</span></div>
        </div>
      </template>
    </Card>

    <!-- Configuração dos Carregadores -->
    <Card style="margin-bottom: 1rem;">
      <template #title>
        <div style="display: flex; align-items: center; gap: 0.5rem;">
          <i class="pi pi-plug"></i>
          <span>{{ $t('regional.charger_configuration') }}</span>
        </div>
      </template>
      <template #content>
        <ChargerModelPicker v-model="form.charger_model_id" @select="onChargerModelSelect" style="margin-bottom: 1.25rem;" />

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
          <div style="display: flex; flex-direction: column; gap: 0.25rem; min-width: 0;">
            <label style="font-weight: 500;">{{ $t('regional.charger_power') }} ({{ $t('regional.units.kw') }})</label>
            <InputNumber v-model="form.charger_power" :min="0" :step="0.5" fluid showButtons :minFractionDigits="1" />
          </div>
          <div style="display: flex; flex-direction: column; gap: 0.25rem; min-width: 0;">
            <label for="n_chargers" style="font-weight: 500;">{{ $t('regional.number_of_chargers') }}</label>
            <InputNumber id="n_chargers" v-model="form.n_chargers" :min="1" :step="1" fluid showButtons />
          </div>
          <div style="display: flex; flex-direction: column; gap: 0.25rem; min-width: 0;">
            <label for="utilization_factor" style="font-weight: 500;">{{ $t('regional.utilization_factor') }} ({{ $t('regional.units.ratio') }})</label>
            <InputNumber id="utilization_factor" v-model="form.utilization_factor" :min="0" :max="1" :step="0.05" fluid showButtons :minFractionDigits="2" />
          </div>
        </div>

        <div style="margin-top: 1rem; display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem;">
          <div style="background: var(--p-surface-100); padding: 1rem; border-radius: 0.5rem; min-width: 0;">
            <p style="margin: 0 0 0.5rem 0; font-size: 0.875rem; color: var(--p-text-muted-color);">{{ $t('regional.total_charger_load') }}</p>
            <p style="font-weight: 600;">{{ totalChargerLoad.toFixed(2) }} {{ $t('regional.units.kw') }}</p>
          </div>
          <div style="background: var(--p-surface-100); padding: 1rem; border-radius: 0.5rem; min-width: 0;">
            <p style="margin: 0 0 0.5rem 0; font-size: 0.875rem; color: var(--p-text-muted-color);">{{ $t('regional.load_per_ptd') }}</p>
            <p style="font-weight: 600;">{{ loadPerPTD.toFixed(2) }} {{ $t('regional.units.kw') }}</p>
          </div>
        </div>
      </template>
    </Card>

    <!-- Botão de análise -->
    <div style="display: flex; justify-content: flex-end; margin-bottom: 1rem;">
      <Button type="button" :label="analysisLabel" icon="pi pi-play" :loading="analysing" :disabled="!canAnalyse" @click="runRegionalAnalysis" />
    </div>

    <!-- Progresso -->
    <div v-if="analysing" style="margin-bottom: 1rem;">
      <Card>
        <template #content>
          <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 0.5rem;">
            <i class="pi pi-spinner pi-spin"></i>
            <span>{{ $t('regional.analysing_progress', { current: analysisProgress.current, total: analysisProgress.total }) }}</span>
          </div>
          <ProgressBar :value="analysisProgress.percentage" />
        </template>
      </Card>
    </div>

    <!-- Resultados -->
    <div ref="resultsRef" v-if="results.length > 0" style="margin-top: 2rem;">
      <!-- Resumo -->
      <Card style="margin-bottom: 1rem;">
        <template #title>
          <div style="display: flex; align-items: center; gap: 0.5rem;">
            <i class="pi pi-chart-bar" style="color: var(--p-primary-color);"></i>
            <span>{{ $t('regional.summary') }}</span>
          </div>
        </template>
        <template #content>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 1rem; margin-bottom: 1.5rem;">
            <div style="background: var(--p-surface-100); padding: 1rem; border-radius: 0.5rem; text-align: center; min-width: 0;"><p style="font-size: 0.875rem; color: var(--p-text-muted-color); margin-bottom: 0.25rem;">{{ $t('regional.total_ptds') }}</p><p style="font-size: 1.5rem; font-weight: bold;">{{ results.length }}</p></div>
            <div style="background: var(--p-surface-100); padding: 1rem; border-radius: 0.5rem; text-align: center; min-width: 0;"><p style="font-size: 0.875rem; color: var(--p-text-muted-color); margin-bottom: 0.25rem;">{{ $t('regional.low_risk') }}</p><p style="font-size: 1.5rem; font-weight: bold; color: #22c55e;">{{ summaryCounts.baixo }}</p></div>
            <div style="background: var(--p-surface-100); padding: 1rem; border-radius: 0.5rem; text-align: center; min-width: 0;"><p style="font-size: 0.875rem; color: var(--p-text-muted-color); margin-bottom: 0.25rem;">{{ $t('regional.medium_risk') }}</p><p style="font-size: 1.5rem; font-weight: bold; color: #f97316;">{{ summaryCounts.medio }}</p></div>
            <div style="background: var(--p-surface-100); padding: 1rem; border-radius: 0.5rem; text-align: center; min-width: 0;"><p style="font-size: 0.875rem; color: var(--p-text-muted-color); margin-bottom: 0.25rem;">{{ $t('regional.high_risk') }}</p><p style="font-size: 1.5rem; font-weight: bold; color: #ef4444;">{{ summaryCounts.alto }}</p></div>
            <div style="background: var(--p-surface-100); padding: 1rem; border-radius: 0.5rem; text-align: center; min-width: 0;"><p style="font-size: 0.875rem; color: var(--p-text-muted-color); margin-bottom: 0.25rem;">{{ $t('regional.avg_prediction') }}</p><p style="font-size: 1.5rem; font-weight: bold;">{{ avgPrediction.toFixed(2) }} {{ $t('regional.units.kw') }}</p></div>
          </div>

          <div v-if="distributionChartData" style="max-width: 400px; margin: 0 auto;">
            <h4 style="text-align: center; margin-bottom: 0.75rem;">{{ $t('regional.risk_distribution') }}</h4>
            <PieChart :data="distributionChartData" />
          </div>
        </template>
      </Card>

      <!-- Mapa -->
      <Card style="margin-bottom: 1rem;">
        <template #title>
          <div style="display: flex; align-items: center; gap: 0.5rem;">
            <i class="pi pi-map"></i>
            <span>{{ $t('regional.map_results') }}</span>
          </div>
        </template>
        <template #content>
          <div style="display: grid; gap: 1rem; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); align-items: start;">
            <div style="border: 1px solid var(--p-surface-300); border-radius: 0.75rem; padding: 0.5rem; background: var(--p-surface-0); overflow: hidden;">
              <div ref="mapContainer" style="height: 450px; width: 100%; border-radius: 0.6rem;"></div>
            </div>

            <div style="display: flex; flex-direction: column; gap: 0.75rem;">
              <div style="background: var(--p-surface-100); padding: 1rem; border-radius: 0.75rem;">
                <p style="margin: 0 0 0.5rem 0; font-weight: 700; font-size: 0.875rem;">{{ $t('regional.map_legend_title') }}</p>
                <div style="display: flex; flex-direction: column; gap: 0.4rem; font-size: 0.8rem; color: var(--p-text-muted-color);">
                  <div style="display: flex; align-items: center; gap: 0.5rem;"><span style="width: 12px; height: 12px; border-radius: 50%; background: #22c55e; display: inline-block;"></span><span>{{ $t('regional.legend_baixo') }} ({{ summaryCounts.baixo }})</span></div>
                  <div style="display: flex; align-items: center; gap: 0.5rem;"><span style="width: 12px; height: 12px; border-radius: 50%; background: #f97316; display: inline-block;"></span><span>{{ $t('regional.legend_medio') }} ({{ summaryCounts.medio }})</span></div>
                  <div style="display: flex; align-items: center; gap: 0.5rem;"><span style="width: 12px; height: 12px; border-radius: 50%; background: #ef4444; display: inline-block;"></span><span>{{ $t('regional.legend_alto') }} ({{ summaryCounts.alto }})</span></div>
                </div>
              </div>

              <div style="background: var(--p-surface-100); padding: 1rem; border-radius: 0.75rem;">
                <p style="margin: 0 0 0.25rem 0; font-weight: 700; font-size: 0.875rem;">{{ $t('regional.map_showing') }}</p>
                <p style="margin: 0; font-size: 0.875rem; color: var(--p-text-muted-color);">{{ mapResults.length }} {{ $t('regional.map_points') }}</p>
              </div>
            </div>
          </div>
        </template>
      </Card>

      <!-- Tabela de Resultados -->
      <Card>
        <template #title>
          <div style="display: flex; align-items: center; gap: 0.5rem;">
            <i class="pi pi-table"></i>
            <span>{{ $t('regional.detailed_results') }}</span>
          </div>
        </template>
        <template #content>
          <DataTable :value="results" paginator :rows="10" :rowsPerPageOptions="[5, 10, 25, 50]" sortMode="multiple" removableSort showGridlines stripedRows tableStyle="min-width: 50rem" :globalFilterFields="['ptd.codigo_instalacao', 'ptd.distrito', 'ptd.concelho', 'classification']">
            <template #header>
              <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.75rem;">
                <span style="font-weight: 600;">{{ $t('regional.results_table') }}</span>
                <div style="display: flex; gap: 0.5rem;">
                  <Button icon="pi pi-filter-slash" :label="$t('regional.clear_filters')" outlined size="small" @click="clearFilters" />
                  <Button icon="pi pi-download" :label="$t('regional.export_csv')" outlined size="small" @click="exportCSV" />
                </div>
              </div>
            </template>

            <Column field="ptd.codigo_instalacao" :header="$t('regional.ptd_code')" sortable style="min-width: 10rem">
              <template #body="{ data }"><span style="font-weight: 600; font-family: monospace;">{{ data.ptd.codigo_instalacao }}</span></template>
            </Column>
            <Column field="ptd.distrito" :header="$t('regional.district')" sortable style="min-width: 10rem" />
            <Column field="ptd.concelho" :header="$t('regional.municipality')" sortable style="min-width: 10rem" />
            <Column field="prediction" :header="$t('regional.predicted_load')" sortable style="min-width: 10rem">
              <template #body="{ data }"><span style="font-weight: 600;">{{ Number(data.prediction).toFixed(2) }} {{ $t('regional.units.kw') }}</span></template>
            </Column>
            <Column field="ptd.potencia_instalada" :header="$t('regional.installed_power')" sortable style="min-width: 10rem">
              <template #body="{ data }">{{ data.ptd.potencia_instalada }} {{ $t('regional.units.kva') }}</template>
            </Column>
            <Column field="totalLoad" :header="$t('regional.total_load')" sortable style="min-width: 10rem">
              <template #body="{ data }"><span :style="{ fontWeight: 600, color: data.totalLoad > data.ptd.potencia_instalada ? '#ef4444' : 'inherit' }">{{ data.totalLoad.toFixed(2) }} {{ $t('regional.units.kw') }}</span></template>
            </Column>
            <Column field="margin" :header="$t('regional.margin')" sortable style="min-width: 10rem">
              <template #body="{ data }"><span :style="{ fontWeight: 600, color: getMarginColor(data.margin) }">{{ (data.margin * 100).toFixed(1) }}%</span></template>
            </Column>
            <Column field="classification" :header="$t('regional.classification')" sortable style="min-width: 10rem">
              <template #body="{ data }"><Tag :value="overloadClassLabel(data.classification)" :severity="classSeverity(data.classification)" style="font-size: 0.85rem;" /></template>
            </Column>
            <Column field="supportedChargers" :header="$t('regional.supported_chargers')" sortable style="min-width: 10rem">
              <template #body="{ data }"><span style="font-weight: 600;">{{ data.supportedChargers }}</span></template>
            </Column>
            <Column :header="$t('regional.actions')" style="min-width: 8rem">
              <template #body="{ data }"><Button icon="pi pi-search" outlined rounded size="small" @click="viewPTDDetails(data)" /></template>
            </Column>
          </DataTable>
        </template>
      </Card>
    </div>

    <Toast />
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, computed, nextTick, watch, onMounted, onBeforeUnmount } from 'vue'
import type { Ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useToast } from 'primevue/usetoast'
import Dropdown from 'primevue/dropdown'
import InputNumber from 'primevue/inputnumber'
import Button from 'primevue/button'
import Card from 'primevue/card'
import Tag from 'primevue/tag'
import ProgressBar from 'primevue/progressbar'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import PieChart from '@/components/PieChart.vue'
import ChargerModelPicker from '@/components/ChargerModelPicker.vue'
import { predict } from '@/api/endpoints'
import type { PredictionResponse, PTDBase } from '@/types'
import { getChargerModel, type ChargerModel } from '@/data/chargerModels'
import { usePTDCacheStore } from '@/stores/ptdCacheStore'
import { useRegionalStore } from '@/stores/regionalStore'
import L from 'leaflet'

const { t } = useI18n()
const toast = useToast()
const ptdCache = usePTDCacheStore()
const regionalStore = useRegionalStore()

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

const regressionModels = [
  { label: 'NeuralNet', value: 'NeuralNet', recommended: true },
  { label: 'Tree', value: 'Tree', recommended: true },
  { label: 'Linear', value: 'Linear' },
  { label: 'SVM', value: 'SVM' },
]

// ── Estado do formulário ──
const form = reactive({
  profile: 'leve',
  version: '' as string,
  model_name: 'NeuralNet' as string,
  charger_model_id: 'wallbox-pulsar-plus-7_4' as string,
  charger_power: 7.4,
  n_chargers: 2,
  utilization_factor: 0.7,
})

// ── Estado da região ──
const selectedDistrito = ref<string | null>(null)
const selectedConcelho = ref<string | null>(null)
const districts = ref<string[]>([])
const concelhos = ref<string[]>([])

// ── Estado da análise ──
const analysing = ref(false)
const analysisProgress = reactive({ current: 0, total: 0, percentage: 0 })
const results = ref<RegionalResult[]>([])
const resultsRef = ref<HTMLElement | null>(null)

// ── Mapa ──
const mapContainer = ref<HTMLDivElement | null>(null)
let mapInstance: L.Map | null = null
let markerLayer: L.LayerGroup | null = null

// ── Tipos ──
interface RegionalResult {
  ptd: PTDBase
  prediction: number
  totalLoad: number
  margin: number
  classification: 'baixo' | 'medio' | 'alto'
  supportedChargers: number
}

// ── Computed ──
const totalChargerLoad = computed(() => form.n_chargers * form.charger_power * form.utilization_factor)
const loadPerPTD = computed(() => totalChargerLoad.value)
const canAnalyse = computed(() => !!selectedDistrito.value && regionPTDs.value.length > 0 && !analysing.value)
const analysisLabel = computed(() => t('regional.run_analysis', { count: regionPTDs.value.length }))
const regionPTDs = computed(() => ptdCache.getPTDsByRegion(selectedDistrito.value, selectedConcelho.value))

const summaryCounts = computed(() => {
  const counts = { baixo: 0, medio: 0, alto: 0 }
  results.value.forEach(r => { counts[r.classification]++ })
  return counts
})

const avgPrediction = computed(() => {
  if (!results.value.length) return 0
  return results.value.reduce((sum, r) => sum + r.prediction, 0) / results.value.length
})

const distributionChartData = computed(() => {
  const counts = summaryCounts.value
  const total = results.value.length
  if (!total) return null
  return {
    labels: [t('common.risk_low'), t('common.risk_medium'), t('common.risk_high')],
    datasets: [{ data: [counts.baixo, counts.medio, counts.alto], backgroundColor: ['#22c55e', '#f97316', '#ef4444'], hoverBackgroundColor: ['#22c55e', '#f97316', '#ef4444'] }],
  }
})

const mapResults = computed(() => results.value.filter(r => typeof r.ptd.latitude === 'number' && typeof r.ptd.longitude === 'number'))

// ── Helpers de classificação ──
const overloadClassLabel = (value: string) => {
  if (value === 'baixo') return t('common.risk_low')
  if (value === 'medio') return t('common.risk_medium')
  if (value === 'alto') return t('common.risk_high')
  return value
}

const classSeverity = (value: string): 'success' | 'warn' | 'danger' | 'info' => {
  if (value === 'alto') return 'danger'
  if (value === 'medio') return 'warn'
  if (value === 'baixo') return 'success'
  return 'info'
}

const getClassificationColor = (value: string) => {
  if (value === 'alto') return '#ef4444'
  if (value === 'medio') return '#f97316'
  return '#22c55e'
}

const getMarginColor = (margin: number) => {
  if (margin < 0) return '#ef4444'
  if (margin < 0.3) return '#f97316'
  return '#22c55e'
}

const classifyPTD = (prediction: number, capacity: number, totalLoad: number): 'baixo' | 'medio' | 'alto' => {
  const margin = (capacity - totalLoad) / capacity
  if (margin < 0) return 'alto'
  if (margin < 0.3) return 'medio'
  return 'baixo'
}

// ── Carregar PTDs via store ──
const loadPTDs = async () => {
  try {
    await ptdCache.fetch()
    districts.value = ptdCache.getDistricts()
    if (selectedDistrito.value) {
      concelhos.value = ptdCache.getConcelhos(selectedDistrito.value)
    }
  } catch (error: any) {
    toast.add({ severity: 'error', summary: t('common.error'), detail: error.message || 'Failed to load PTDs', life: 5000 })
  }
}

const onDistritoChange = () => {
  selectedConcelho.value = null
  if (selectedDistrito.value) {
    concelhos.value = ptdCache.getConcelhos(selectedDistrito.value)
  } else {
    concelhos.value = []
  }
}

const onConcelhoChange = () => {
  results.value = []
}

const onChargerModelSelect = (charger: ChargerModel) => {
  form.charger_power = charger.power
}

// ── Análise Regional ──
const runRegionalAnalysis = async () => {
  const ptds = regionPTDs.value
  if (!ptds.length) return

  analysing.value = true
  analysisProgress.current = 0
  analysisProgress.total = ptds.length
  analysisProgress.percentage = 0
  results.value = []

  const batchSize = 10
  const newResults: RegionalResult[] = []

  for (let i = 0; i < ptds.length; i += batchSize) {
    const batch = ptds.slice(i, i + batchSize)

    const batchPromises = batch.map(async (ptd) => {
      const features = buildFeatures(ptd)
      try {
        const response = await predict({
          profile: form.profile,
          version: form.version || undefined,
          task: 'regression',
          model_name: form.model_name,
          features,
        })

        const prediction = Number(response.data.prediction)
        const totalLoad = prediction + totalChargerLoad.value
        const capacity = ptd.potencia_instalada || 50
        const margin = (capacity - totalLoad) / capacity
        const classification = classifyPTD(prediction, capacity, totalLoad)
        const singleChargerEffectiveLoad = form.charger_power * form.utilization_factor
        const supportedChargers = singleChargerEffectiveLoad > 0 ? Math.max(0, Math.floor(capacity / singleChargerEffectiveLoad)) : 0

        return { ptd, prediction, totalLoad, margin, classification, supportedChargers }
      } catch (error) {
        return { ptd, prediction: 0, totalLoad: totalChargerLoad.value, margin: -1, classification: 'alto' as const, supportedChargers: 0 }
      }
    })

    const batchResults = await Promise.all(batchPromises)
    newResults.push(...batchResults)

    analysisProgress.current = Math.min(i + batchSize, ptds.length)
    analysisProgress.percentage = Math.round((analysisProgress.current / ptds.length) * 100)
  }

  results.value = newResults
  analysing.value = false

  // Save to store
  regionalStore.addRecord({
    profile: form.profile,
    version: form.version,
    model_name: form.model_name,
    region: selectedConcelho.value || selectedDistrito.value || 'unknown',
    ptdCount: newResults.length,
    overload_probability: 0,
  })

  await nextTick()
  if (resultsRef.value) resultsRef.value.scrollIntoView({ behavior: 'smooth', block: 'start' })

  await nextTick()
  initMap()

  toast.add({ severity: 'success', summary: t('common.success'), detail: t('regional.analysis_complete', { count: newResults.length }), life: 3000 })
}

const buildFeatures = (ptd: PTDBase): Record<string, number> => ({
  'Potência instalada [kVA]': ptd.potencia_instalada,
  'P_IP_Total': ptd.p_ip_total ?? 0,
  'P_IP_Inef': ptd.p_ip_inef ?? 0,
  'LED_Ratio': ptd.led_ratio ?? 0,
  'N_Luminarias': ptd.n_luminarias ?? 0,
  'N_Lampadas': ptd.n_lampadas ?? 0,
  'Cap_per_Cliente': ptd.cap_per_cliente ?? 0,
  'Distrito_enc': ptd.distrito_enc ?? 0,
  'Concelho_enc': ptd.concelho_enc ?? 0,
  'N_Clientes': ptd.n_clientes ?? 0,
})

// ── Mapa ──
const initMap = () => {
  if (!mapContainer.value) return
  if (mapInstance) { mapInstance.remove(); mapInstance = null; markerLayer = null }

  const validResults = mapResults.value
  if (!validResults.length) return

  const lats = validResults.map(r => r.ptd.latitude as number)
  const lngs = validResults.map(r => r.ptd.longitude as number)
  const bounds: L.LatLngBoundsExpression = [[Math.min(...lats), Math.min(...lngs)], [Math.max(...lats), Math.max(...lngs)]]

  mapInstance = L.map(mapContainer.value, { minZoom: 6, maxZoom: 15, zoomControl: true, scrollWheelZoom: true })
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors' }).addTo(mapInstance)
  markerLayer = L.layerGroup().addTo(mapInstance)

  validResults.forEach((result) => {
    const popupContent = `
      <div style="min-width: 200px;">
        <strong>${result.ptd.codigo_instalacao}</strong>
        <div>${result.ptd.distrito} / ${result.ptd.concelho}</div>
        <div>${t('regional.predicted_load')}: ${result.prediction.toFixed(2)} kW</div>
        <div>${t('regional.total_load')}: ${result.totalLoad.toFixed(2)} kW</div>
        <div>${t('regional.installed_power')}: ${result.ptd.potencia_instalada} kVA</div>
        <div>${t('regional.margin')}: ${(result.margin * 100).toFixed(1)}%</div>
        <div style="margin-top: 0.5rem; padding: 0.25rem 0.5rem; border-radius: 0.25rem; background: ${getClassificationColor(result.classification)}22; color: ${getClassificationColor(result.classification)}; font-weight: 600; display: inline-block;">${overloadClassLabel(result.classification)}</div>
      </div>
    `
    const marker = L.circleMarker([result.ptd.latitude as number, result.ptd.longitude as number], { radius: 6, fillColor: getClassificationColor(result.classification), color: '#ffffff', weight: 2, opacity: 1, fillOpacity: 0.9 })
      .bindPopup(popupContent)
    markerLayer?.addLayer(marker)
  })

  mapInstance.fitBounds(bounds, { padding: [30, 30] })
  setTimeout(() => mapInstance?.invalidateSize(), 100)
}

// ── Tabela ──
const clearFilters = () => {}

const exportCSV = () => {
  const headers = [t('regional.ptd_code'), t('regional.district'), t('regional.municipality'), t('regional.predicted_load'), t('regional.installed_power'), t('regional.total_load'), t('regional.margin'), t('regional.classification'), t('regional.supported_chargers')]
  const rows = results.value.map(r => [r.ptd.codigo_instalacao, r.ptd.distrito, r.ptd.concelho, r.prediction.toFixed(2), r.ptd.potencia_instalada, r.totalLoad.toFixed(2), (r.margin * 100).toFixed(1) + '%', overloadClassLabel(r.classification), r.supportedChargers])
  const csvContent = [headers, ...rows].map(row => row.map(cell => `"${String(cell).replace(/"/g, '""')}"`).join(',')).join('')
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.download = `regional_analysis_${selectedDistrito.value || 'all'}_${new Date().toISOString().slice(0, 10)}.csv`
  link.click()
  URL.revokeObjectURL(link.href)
}

const viewPTDDetails = (result: RegionalResult) => {
  toast.add({ severity: 'info', summary: result.ptd.codigo_instalacao, detail: `${t('regional.predicted_load')}: ${result.prediction.toFixed(2)} kW | ${t('regional.classification')}: ${overloadClassLabel(result.classification)}`, life: 5000 })
}

// ── Lifecycle ──
onMounted(() => { loadPTDs() })
onBeforeUnmount(() => { mapInstance?.remove(); mapInstance = null; markerLayer = null })

watch(() => results.value.length, async (newLen, oldLen) => {
  if (newLen > 0 && newLen !== oldLen) { await nextTick(); initMap() }
})
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