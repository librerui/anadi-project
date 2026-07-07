<template>
  <div>
    <div style="margin-bottom: 1.5rem;">
      <h1 style="font-size: 1.875rem; font-weight: bold;">{{ $t('dashboard.title') }}</h1>
      <p style="color: var(--p-text-muted-color);">{{ $t('dashboard.welcome') }}</p>
    </div>

    <!-- Quick Action Cards -->
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1rem; margin-bottom: 2rem;">
      <Card class="dashboard-card" @click="$router.push('/predict')" style="cursor: pointer;">
        <template #content>
          <div style="display: flex; align-items: center; gap: 1rem;">
            <div style="width: 48px; height: 48px; border-radius: 0.75rem; background: var(--p-primary-100); display: flex; align-items: center; justify-content: center;">
              <i class="pi pi-bolt" style="font-size: 1.25rem; color: var(--p-primary-color);"></i>
            </div>
            <div>
              <h3 style="margin: 0; font-size: 1rem; font-weight: 600;">{{ $t('nav.predict') }}</h3>
              <p style="margin: 0.25rem 0 0 0; font-size: 0.875rem; color: var(--p-text-muted-color);">{{ $t('dashboard.cards.predict') }}</p>
            </div>
          </div>
        </template>
      </Card>

      <Card class="dashboard-card" @click="$router.push('/simulate')" style="cursor: pointer;">
        <template #content>
          <div style="display: flex; align-items: center; gap: 1rem;">
            <div style="width: 48px; height: 48px; border-radius: 0.75rem; background: var(--p-orange-100); display: flex; align-items: center; justify-content: center;">
              <i class="pi pi-chart-scatter" style="font-size: 1.25rem; color: var(--p-orange-500);"></i>
            </div>
            <div>
              <h3 style="margin: 0; font-size: 1rem; font-weight: 600;">{{ $t('nav.simulate') }}</h3>
              <p style="margin: 0.25rem 0 0 0; font-size: 0.875rem; color: var(--p-text-muted-color);">{{ $t('dashboard.cards.simulate') }}</p>
            </div>
          </div>
        </template>
      </Card>

      <Card class="dashboard-card" @click="$router.push('/regional')" style="cursor: pointer;">
        <template #content>
          <div style="display: flex; align-items: center; gap: 1rem;">
            <div style="width: 48px; height: 48px; border-radius: 0.75rem; background: var(--p-green-100); display: flex; align-items: center; justify-content: center;">
              <i class="pi pi-map" style="font-size: 1.25rem; color: var(--p-green-500);"></i>
            </div>
            <div>
              <h3 style="margin: 0; font-size: 1rem; font-weight: 600;">{{ $t('nav.regional') }}</h3>
              <p style="margin: 0.25rem 0 0 0; font-size: 0.875rem; color: var(--p-text-muted-color);">{{ $t('dashboard.cards.regional') }}</p>
            </div>
          </div>
        </template>
      </Card>

      <Card class="dashboard-card" @click="$router.push('/health')" style="cursor: pointer;">
        <template #content>
          <div style="display: flex; align-items: center; gap: 1rem;">
            <div style="width: 48px; height: 48px; border-radius: 0.75rem; background: var(--p-purple-100); display: flex; align-items: center; justify-content: center;">
              <i class="pi pi-heart" style="font-size: 1.25rem; color: var(--p-purple-500);"></i>
            </div>
            <div>
              <h3 style="margin: 0; font-size: 1rem; font-weight: 600;">{{ $t('nav.health') }}</h3>
              <p style="margin: 0.25rem 0 0 0; font-size: 0.875rem; color: var(--p-text-muted-color);">{{ $t('dashboard.cards.health') }}</p>
            </div>
          </div>
        </template>
      </Card>
    </div>

    <!-- Stats Row -->
    <h2 style="font-size: 1.25rem; font-weight: 600; margin-bottom: 1rem;">{{ $t('dashboard.quick_info') }}</h2>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 1rem; margin-bottom: 2rem;">
      <Card>
        <template #content>
          <div style="text-align: center;">
            <p style="font-size: 0.875rem; color: var(--p-text-muted-color); margin-bottom: 0.5rem;">{{ $t('dashboard.stats.system_status') }}</p>
            <Tag :value="systemStatus" :severity="systemStatusSeverity" style="font-size: 0.9rem;" />
          </div>
        </template>
      </Card>

      <Card>
        <template #content>
          <div style="text-align: center;">
            <p style="font-size: 0.875rem; color: var(--p-text-muted-color); margin-bottom: 0.5rem;">{{ $t('dashboard.stats.predictions_today') }}</p>
            <p style="font-size: 1.5rem; font-weight: bold; color: var(--p-primary-color); margin: 0;">{{ dashboardStore.predictionsToday }}</p>
          </div>
        </template>
      </Card>

      <Card>
        <template #content>
          <div style="text-align: center;">
            <p style="font-size: 0.875rem; color: var(--p-text-muted-color); margin-bottom: 0.5rem;">{{ $t('dashboard.stats.simulations_run') }}</p>
            <p style="font-size: 1.5rem; font-weight: bold; color: var(--p-orange-500); margin: 0;">{{ dashboardStore.simulationsToday }}</p>
          </div>
        </template>
      </Card>

      <Card>
        <template #content>
          <div style="text-align: center;">
            <p style="font-size: 0.875rem; color: var(--p-text-muted-color); margin-bottom: 0.5rem;">{{ $t('dashboard.stats.regional_analyses') }}</p>
            <p style="font-size: 1.5rem; font-weight: bold; color: var(--p-green-500); margin: 0;">{{ dashboardStore.regionalAnalysesToday }}</p>
          </div>
        </template>
      </Card>

      <Card>
        <template #content>
          <div style="text-align: center;">
            <p style="font-size: 0.875rem; color: var(--p-text-muted-color); margin-bottom: 0.5rem;">{{ $t('dashboard.stats.ptds_analysed') }}</p>
            <p style="font-size: 1.5rem; font-weight: bold; color: var(--p-purple-500); margin: 0;">{{ dashboardStore.ptdsAnalysed }}</p>
          </div>
        </template>
      </Card>

      <Card>
        <template #content>
          <div style="text-align: center;">
            <p style="font-size: 0.875rem; color: var(--p-text-muted-color); margin-bottom: 0.5rem;">{{ $t('dashboard.stats.models_loaded') }}</p>
            <p style="font-size: 1.5rem; font-weight: bold; color: var(--p-blue-500); margin: 0;">{{ dashboardStore.modelsLoaded }}</p>
          </div>
        </template>
      </Card>
    </div>

    <!-- Recent Activity -->
    <h2 style="font-size: 1.25rem; font-weight: 600; margin-bottom: 1rem;">{{ $t('dashboard.recent_activity') }}</h2>
    <Card>
      <template #content>
        <div v-if="dashboardStore.recentActivity.length === 0" style="text-align: center; padding: 2rem; color: var(--p-text-muted-color);">
          <i class="pi pi-inbox" style="font-size: 2rem; margin-bottom: 0.5rem; display: block;"></i>
          <p>{{ $t('dashboard.no_activity') }}</p>
        </div>

        <div v-else>
          <div
            v-for="(item, index) in dashboardStore.recentActivity"
            :key="index"
            style="display: flex; align-items: center; gap: 1rem; padding: 0.75rem 0;"
            :style="{ borderBottom: index === dashboardStore.recentActivity.length - 1 ? 'none' : '1px solid var(--p-surface-200)' }"
          >
            <div style="width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0;"
              :style="{ background: activityIconBg(item.type) }"
            >
              <i :class="activityIcon(item.type)" :style="{ color: activityIconColor(item.type), fontSize: '0.875rem' }"></i>
            </div>
            <div style="flex: 1; min-width: 0;">
              <p style="margin: 0; font-weight: 500; font-size: 0.9rem;">{{ $t(item.actionKey) }}</p>
              <p style="margin: 0.15rem 0 0 0; font-size: 0.8rem; color: var(--p-text-muted-color);">{{ $t(item.detailKey, item.detailParams) }}</p>
            </div>
            <span style="font-size: 0.75rem; color: var(--p-text-muted-color); white-space: nowrap;">{{ formatTime(item.timestamp) }}</span>
          </div>
        </div>
      </template>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import Card from 'primevue/card'
import Tag from 'primevue/tag'
import { useDashboardStore } from '@/stores/dashboardStore'

const { t } = useI18n()
const dashboardStore = useDashboardStore()

// ── System Status ──
const systemStatus = computed(() => {
  return dashboardStore.modelsReady ? t('health.status.ready') : t('health.status.checking')
})

const systemStatusSeverity = computed((): 'success' | 'warn' => {
  return dashboardStore.modelsReady ? 'success' : 'warn'
})

// ── Activity Helpers ──
const activityIcon = (type: string) => {
  if (type === 'prediction') return 'pi pi-bolt'
  if (type === 'simulation') return 'pi pi-chart-scatter'
  return 'pi pi-map'
}

const activityIconBg = (type: string) => {
  if (type === 'prediction') return 'var(--p-primary-100)'
  if (type === 'simulation') return 'var(--p-orange-100)'
  return 'var(--p-green-100)'
}

const activityIconColor = (type: string) => {
  if (type === 'prediction') return 'var(--p-primary-color)'
  if (type === 'simulation') return 'var(--p-orange-500)'
  return 'var(--p-green-500)'
}

const formatTime = (timestamp: number) => {
  const diff = Date.now() - timestamp
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)

  if (diff < 60000) return t('dashboard.time.just_now')
  if (minutes < 60) return t('dashboard.time.minutes_ago', { count: minutes })
  if (hours < 24) return t('dashboard.time.hours_ago', { count: hours })
  return t('dashboard.time.days_ago', { count: days })
}
</script>

<style scoped>
.dashboard-card {
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.dashboard-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}
</style>