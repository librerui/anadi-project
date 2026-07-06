<template>
  <div>
    <div style="margin-bottom: 1.5rem;">
      <h1 style="font-size: 1.875rem; font-weight: bold;">{{ $t('health.title') }}</h1>
    </div>

    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem; margin-bottom: 1.5rem;">
      <Card>
        <template #title>
          <div style="display: flex; align-items: center; gap: 0.5rem;">
            <i class="pi pi-server"></i>
            <span>{{ $t('health.service') }}</span>
          </div>
        </template>
        <template #content>
          <div style="display: flex; align-items: center; gap: 0.75rem;">
            <Tag :severity="healthStatus ? 'success' : 'danger'" :value="healthStatus ? 'Pass' : 'Fail'" />
            <span style="color: var(--p-text-muted-color);">{{ healthDetail }}</span>
          </div>
          <ProgressBar v-if="loadingHealth" mode="indeterminate" style="margin-top: 0.75rem; height: 6px;" />
        </template>
      </Card>

      <Card>
        <template #title>
          <div style="display: flex; align-items: center; gap: 0.5rem;">
            <i class="pi pi-check-circle"></i>
            <span>{{ $t('health.readiness') }}</span>
          </div>
        </template>
        <template #content>
          <div style="display: flex; align-items: center; gap: 0.75rem; flex-wrap: wrap;">
            <Tag :severity="readyStatus ? 'success' : 'danger'" :value="readyStatus ? 'Ready' : 'Unavailable'" />
            <span style="color: var(--p-text-muted-color);">{{ readyDetail }}</span>
            <Button 
              :label="$t('health.reload')" 
              icon="pi pi-refresh" 
              size="small" 
              severity="secondary"
              :loading="reloading"
              @click="reload" 
            />
          </div>
          <ProgressBar v-if="loadingReady" mode="indeterminate" style="margin-top: 0.75rem; height: 6px;" />
        </template>
      </Card>
    </div>

    <Divider />

    <Card>
      <template #title>
        <div style="display: flex; align-items: center; gap: 0.5rem;">
          <i class="pi pi-chart-bar"></i>
          <span>{{ $t('health.feature_importance') }}</span>
        </div>
      </template>
      <template #content>
        <div style="display: flex; gap: 0.75rem; align-items: flex-end; margin-bottom: 1rem; flex-wrap: wrap;">
          <div style="display: flex; flex-direction: column; gap: 0.25rem;">
            <label style="font-weight: 500;">{{ $t('health.profile_label', 'Profile') }}</label>
            <Dropdown v-model="importanceProfile" :options="profiles" :placeholder="t('health.select_profile')" style="width: 12rem;" />
          </div>
          <Button :label="t('health.load')" icon="pi pi-search" @click="loadFeatureImportance" :loading="loadingFeatures" />
        </div>

        <div v-if="importanceData" style="background: var(--p-surface-100); border-radius: 0.5rem; padding: 1rem;">
          <div v-for="(importances, modelName) in importanceData" :key="modelName" style="margin-bottom: 1.5rem;">
            <h4 style="margin-bottom: 0.75rem; font-weight: 600;">{{ modelName }}</h4>
            <BarChart :data="getChartData(importances)" style="max-height: 300px;" />
          </div>
        </div>
        
        <div v-else style="color: var(--p-text-muted-color); text-align: center; padding: 2rem; background: var(--p-surface-100); border-radius: 0.5rem;">
          <i class="pi pi-chart-bar" style="font-size: 2rem; display: block; margin-bottom: 0.5rem;"></i>
          <p>{{ t('health.feature_importance_empty') }}</p>
        </div>
      </template>
    </Card>

    <Toast />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useToast } from 'primevue/usetoast'
import Card from 'primevue/card'
import Tag from 'primevue/tag'
import Button from 'primevue/button'
import Divider from 'primevue/divider'
import Dropdown from 'primevue/dropdown'
import Toast from 'primevue/toast'
import ProgressBar from 'primevue/progressbar'
import BarChart from '@/components/BarChart.vue'
import { getHealth, getReady, reloadModels, getFeatureImportance } from '@/api/endpoints'

const toast = useToast()
const { t } = useI18n()

const healthStatus = ref(false)
const healthDetail = ref('')
const readyStatus = ref(false)
const readyDetail = ref('')
const loadingHealth = ref(false)
const loadingReady = ref(false)
const reloading = ref(false)
const loadingFeatures = ref(false)

const profiles = ['leve', 'regular', 'pesado']
const importanceProfile = ref('leve')
const importanceData = ref<Record<string, Record<string, number>> | null>(null)

const loadHealth = async () => {
  loadingHealth.value = true
  try {
    const res = await getHealth()
    healthStatus.value = res.data.status === 'pass'
    healthDetail.value = res.data.detail
  } catch {
    healthStatus.value = false
    healthDetail.value = 'Service unavailable'
  } finally {
    loadingHealth.value = false
  }
}

const loadReady = async () => {
  loadingReady.value = true
  try {
    const res = await getReady()
    readyStatus.value = res.data.status === 'pass'
    readyDetail.value = res.data.detail
  } catch {
    readyStatus.value = false
    readyDetail.value = 'Models not ready'
  } finally {
    loadingReady.value = false
  }
}

const reload = async () => {
  reloading.value = true
  try {
    await reloadModels(importanceProfile.value)
    toast.add({ severity: 'success', summary: t('common.success'), detail: 'Models reloaded', life: 3000 })
    await loadReady()
  } catch (error: any) {
    toast.add({ severity: 'error', summary: t('common.error'), detail: error.message, life: 5000 })
  } finally {
    reloading.value = false
  }
}

const loadFeatureImportance = async () => {
  loadingFeatures.value = true
  try {
    const res = await getFeatureImportance(importanceProfile.value)
    importanceData.value = res.data.feature_importances
  } catch (error: any) {
    toast.add({ severity: 'error', summary: t('common.error'), detail: error.message, life: 5000 })
  } finally {
    loadingFeatures.value = false
  }
}

const getChartData = (importances: Record<string, number>) => {
  const labels = Object.keys(importances)
  const data = Object.values(importances)
  const colors = labels.map((_, i) => `hsl(${200 + (i * 30) % 160}, 70%, 60%)`)
  return { 
    labels, 
    datasets: [{ 
      label: 'Importance', 
      data, 
      backgroundColor: colors,
      borderColor: colors.map(c => c.replace('60%', '40%')),
      borderWidth: 1
    }] 
  }
}

onMounted(() => {
  loadHealth()
  loadReady()
})
</script>