<template>
  <div>
    <div style="margin-bottom: 1.5rem;">
      <h1 style="font-size: 1.5rem; font-weight: bold; margin-bottom: 0.25rem;">{{ t('dashboard.title') }}</h1>
      <p style="color: var(--p-text-muted-color); font-size: 0.875rem;">{{ t('dashboard.welcome') }}</p>
    </div>

    <!-- Navigation Cards -->
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1rem; margin-bottom: 1.5rem;">
      <div @click="goTo('/predict')" style="cursor: pointer;">
        <Card>
          <template #title>
            <div style="display: flex; align-items: center; gap: 0.5rem;">
              <i class="pi pi-chart-line" style="font-size: 1.5rem; color: var(--p-primary-color);"></i>
              <span>{{ t('nav.predict') }}</span>
            </div>
          </template>
          <template #content>
            <p style="color: var(--p-text-muted-color); margin-bottom: 1rem; font-size: 0.875rem;">{{ t('dashboard.cards.predict') }}</p>
            <Button :label="t('nav.predict')" icon="pi pi-arrow-right" iconPos="right" style="width: 100%;" size="small" />
          </template>
        </Card>
      </div>

      <div @click="goTo('/simulate')" style="cursor: pointer;">
        <Card>
          <template #title>
            <div style="display: flex; align-items: center; gap: 0.5rem;">
              <i class="pi pi-cog" style="font-size: 1.5rem; color: var(--p-orange-500);"></i>
              <span>{{ t('nav.simulate') }}</span>
            </div>
          </template>
          <template #content>
            <p style="color: var(--p-text-muted-color); margin-bottom: 1rem; font-size: 0.875rem;">{{ t('dashboard.cards.simulate') }}</p>
            <Button :label="t('nav.simulate')" icon="pi pi-arrow-right" iconPos="right" severity="warning" style="width: 100%;" size="small" />
          </template>
        </Card>
      </div>

      <div @click="goTo('/health')" style="cursor: pointer;">
        <Card>
          <template #title>
            <div style="display: flex; align-items: center; gap: 0.5rem;">
              <i class="pi pi-heart" style="font-size: 1.5rem; color: var(--p-green-500);"></i>
              <span>{{ t('nav.health') }}</span>
            </div>
          </template>
          <template #content>
            <p style="color: var(--p-text-muted-color); margin-bottom: 1rem; font-size: 0.875rem;">{{ t('dashboard.cards.health') }}</p>
            <Button :label="t('nav.health')" icon="pi pi-arrow-right" iconPos="right" severity="success" style="width: 100%;" size="small" />
          </template>
        </Card>
      </div>

      <div @click="goTo('/regional')" style="cursor: pointer;">
        <Card>
          <template #title>
            <div style="display: flex; align-items: center; gap: 0.5rem;">
              <i class="pi pi-map" style="font-size: 1.5rem; color: var(--p-cyan-500);"></i>
              <span>{{ t('nav.regional') }}</span>
            </div>
          </template>
          <template #content>
            <p style="color: var(--p-text-muted-color); margin-bottom: 1rem; font-size: 0.875rem;">{{ t('dashboard.cards.regional') }}</p>
            <Button :label="t('nav.regional')" icon="pi pi-arrow-right" iconPos="right" severity="info" style="width: 100%;" size="small" />
          </template>
        </Card>
      </div>
    </div>

    <!-- Quick Stats + Recent Activity - Side by Side -->
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1.5rem;">
      <!-- Quick Stats (Left) -->
      <Card>
        <template #title>
          <div style="display: flex; align-items: center; gap: 0.5rem;">
            <i class="pi pi-chart-bar"></i>
            <span>{{ t('dashboard.quick_info') }}</span>
          </div>
        </template>
        <template #content>
          <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.6rem;">
            <div style="padding: 0.75rem; border-radius: 0.5rem; background: var(--p-surface-100); border-left: 3px solid var(--p-primary-color);">
              <p style="font-size: 0.7rem; color: var(--p-text-muted-color); margin-bottom: 0.15rem;">{{ t('dashboard.stats.system_status') }}</p>
              <Tag :severity="systemStatus ? 'success' : 'danger'" :value="systemStatus ? 'UP' : 'DOWN'" style="font-size: 0.8rem;" />
            </div>
            <div style="padding: 0.75rem; border-radius: 0.5rem; background: var(--p-surface-100); border-left: 3px solid var(--p-orange-500);">
              <p style="font-size: 0.7rem; color: var(--p-text-muted-color); margin-bottom: 0.15rem;">{{ t('dashboard.stats.predictions_today') }}</p>
              <p style="font-size: 1.1rem; font-weight: 700; color: var(--p-orange-500);">{{ dashboardStore.predictionsToday }}</p>
            </div>
            <div style="padding: 0.75rem; border-radius: 0.5rem; background: var(--p-surface-100); border-left: 3px solid var(--p-green-500);">
              <p style="font-size: 0.7rem; color: var(--p-text-muted-color); margin-bottom: 0.15rem;">{{ t('dashboard.stats.simulations_run') }}</p>
              <p style="font-size: 1.1rem; font-weight: 700; color: var(--p-green-500);">{{ dashboardStore.simulationsToday }}</p>
            </div>
            <div style="padding: 0.75rem; border-radius: 0.5rem; background: var(--p-surface-100); border-left: 3px solid var(--p-purple-500);">
              <p style="font-size: 0.7rem; color: var(--p-text-muted-color); margin-bottom: 0.15rem;">{{ t('dashboard.stats.models_loaded') }}</p>
              <p style="font-size: 1.1rem; font-weight: 700; color: var(--p-purple-500);">{{ dashboardStore.modelsLoaded }}</p>
            </div>
            <div style="padding: 0.75rem; border-radius: 0.5rem; background: var(--p-surface-100); border-left: 3px solid var(--p-cyan-500);">
              <p style="font-size: 0.7rem; color: var(--p-text-muted-color); margin-bottom: 0.15rem;">{{ t('dashboard.stats.regional_analyses') }}</p>
              <p style="font-size: 1.1rem; font-weight: 700; color: var(--p-cyan-500);">{{ dashboardStore.regionalAnalysesToday }}</p>
            </div>
            <div style="padding: 0.75rem; border-radius: 0.5rem; background: var(--p-surface-100); border-left: 3px solid var(--p-pink-500);">
              <p style="font-size: 0.7rem; color: var(--p-text-muted-color); margin-bottom: 0.15rem;">{{ t('dashboard.stats.ptds_analysed') }}</p>
              <p style="font-size: 1.1rem; font-weight: 700; color: var(--p-pink-500);">{{ dashboardStore.ptdsAnalysed }}</p>
            </div>
          </div>
        </template>
      </Card>

      <!-- Recent Activity (Right) -->
      <Card>
        <template #title>
          <div style="display: flex; align-items: center; gap: 0.5rem;">
            <i class="pi pi-history"></i>
            <span>{{ t('dashboard.recent_activity') }}</span>
          </div>
        </template>
        <template #content>
          <div v-if="dashboardStore.recentActivity.length > 0" style="max-height: 220px; overflow-y: auto;">
            <div
              v-for="(activity, index) in dashboardStore.recentActivity"
              :key="activity.id"
              style="display: flex; align-items: center; justify-content: space-between; padding: 0.4rem 0;"
              :style="{ borderBottom: index === dashboardStore.recentActivity.length - 1 ? 'none' : '1px solid var(--p-surface-200)' }"
            >
              <div style="display: flex; align-items: center; gap: 0.5rem; min-width: 0;">
                <span :style="{ width: '8px', height: '8px', borderRadius: '50%', background: activity.color, display: 'inline-block', flexShrink: 0 }"></span>
                <span style="font-weight: 500; font-size: 0.8rem; white-space: nowrap;">{{ t(activity.actionKey) }}</span>
                <span style="color: var(--p-text-muted-color); font-size: 0.75rem; overflow: hidden; text-overflow: ellipsis;">{{ formatDetail(activity) }}</span>
              </div>
              <span style="color: var(--p-text-muted-color); font-size: 0.7rem; white-space: nowrap; flex-shrink: 0; margin-left: 0.5rem;">{{ formatTime(activity.timestamp) }}</span>
            </div>
          </div>
          <div v-else style="text-align: center; color: var(--p-text-muted-color); padding: 1.5rem;">
            <i class="pi pi-inbox" style="font-size: 1.5rem; display: block; margin-bottom: 0.5rem;"></i>
            <p style="font-size: 0.875rem;">{{ t('dashboard.no_activity') }}</p>
          </div>
        </template>
      </Card>
    </div>

    <!-- Extra Metrics Row -->
    <Card>
      <template #title>
        <div style="display: flex; align-items: center; gap: 0.5rem;">
          <i class="pi pi-chart-pie"></i>
          <span>{{ t('dashboard.insights') }}</span>
        </div>
      </template>
      <template #content>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
          <div style="text-align: center; padding: 1rem; background: var(--p-surface-100); border-radius: 0.5rem;">
            <p style="font-size: 0.75rem; color: var(--p-text-muted-color); margin-bottom: 0.25rem;">{{ t('dashboard.avg_prediction_time') }}</p>
            <p style="font-size: 1.25rem; font-weight: 700; color: var(--p-primary-color);">{{ dashboardStore.avgPredictionTime }}ms</p>
          </div>
          <div style="text-align: center; padding: 1rem; background: var(--p-surface-100); border-radius: 0.5rem;">
            <p style="font-size: 0.75rem; color: var(--p-text-muted-color); margin-bottom: 0.25rem;">{{ t('dashboard.most_used_model') }}</p>
            <p style="font-size: 1.25rem; font-weight: 700; color: var(--p-primary-color);">{{ dashboardStore.mostUsedModel }}</p>
          </div>
          <div style="text-align: center; padding: 1rem; background: var(--p-surface-100); border-radius: 0.5rem;">
            <p style="font-size: 0.75rem; color: var(--p-text-muted-color); margin-bottom: 0.25rem;">{{ t('dashboard.top_region') }}</p>
            <p style="font-size: 1.25rem; font-weight: 700; color: var(--p-primary-color);">{{ dashboardStore.topRegion }}</p>
          </div>
          <div style="text-align: center; padding: 1rem; background: var(--p-surface-100); border-radius: 0.5rem;">
            <p style="font-size: 0.75rem; color: var(--p-text-muted-color); margin-bottom: 0.25rem;">{{ t('dashboard.success_rate') }}</p>
            <p style="font-size: 1.25rem; font-weight: 700; color: var(--p-primary-color);">{{ dashboardStore.successRate }}%</p>
          </div>
        </div>
      </template>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import Card from 'primevue/card'
import Button from 'primevue/button'
import Tag from 'primevue/tag'
import { useDashboardStore, type ActivityItem } from '@/stores/dashboardStore'

const { t } = useI18n()
const router = useRouter()
const dashboardStore = useDashboardStore()

function formatDetail(activity: ActivityItem): string {
  const params: Record<string, string | number> = { ...activity.detailParams }
  if (typeof params.task === 'string') {
    params.task = t(params.task)
  }
  return t(activity.detailKey, params)
}

const goTo = (path: string) => {
  router.push(path)
}

const systemStatus = computed(() => dashboardStore.systemHealth >= 80)

function formatTime(timestamp: number): string {
  const diff = Date.now() - timestamp
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)

  if (minutes < 1) return t('dashboard.time.just_now')
  if (minutes < 60) return t('dashboard.time.minutes_ago', { count: minutes })
  if (hours < 24) return t('dashboard.time.hours_ago', { count: hours })
  return t('dashboard.time.days_ago', { count: days })
}
</script>
