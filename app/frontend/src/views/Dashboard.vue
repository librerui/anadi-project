<template>
  <div>
    <div style="margin-bottom: 2rem;">
      <h1 style="font-size: 1.875rem; font-weight: bold; margin-bottom: 0.5rem;">{{ t('dashboard.title') }}</h1>
      <p style="color: var(--p-text-muted-color);">{{ t('dashboard.welcome') }}</p>
    </div>

    <!-- Navigation Cards -->
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem; margin-bottom: 2rem;">
      <Card @click="goTo('/predict')" style="cursor: pointer;">
        <template #title>
          <div style="display: flex; align-items: center; gap: 0.5rem;">
            <i class="pi pi-chart-line" style="font-size: 1.5rem;"></i>
            <span>{{ t('nav.predict') }}</span>
          </div>
        </template>
        <template #content>
          <p style="color: var(--p-text-muted-color); margin-bottom: 1rem;">{{ t('dashboard.cards.predict') }}</p>
          <Button :label="t('nav.predict')" icon="pi pi-arrow-right" iconPos="right" style="width: 100%;" />
        </template>
      </Card>

      <Card @click="goTo('/simulate')" style="cursor: pointer;">
        <template #title>
          <div style="display: flex; align-items: center; gap: 0.5rem;">
            <i class="pi pi-cog" style="font-size: 1.5rem;"></i>
            <span>{{ t('nav.simulate') }}</span>
          </div>
        </template>
        <template #content>
          <p style="color: var(--p-text-muted-color); margin-bottom: 1rem;">{{ t('dashboard.cards.simulate') }}</p>
          <Button :label="t('nav.simulate')" icon="pi pi-arrow-right" iconPos="right" severity="warning" style="width: 100%;" />
        </template>
      </Card>

      <Card @click="goTo('/health')" style="cursor: pointer;">
        <template #title>
          <div style="display: flex; align-items: center; gap: 0.5rem;">
            <i class="pi pi-heart" style="font-size: 1.5rem;"></i>
            <span>{{ t('nav.health') }}</span>
          </div>
        </template>
        <template #content>
          <p style="color: var(--p-text-muted-color); margin-bottom: 1rem;">{{ t('dashboard.cards.health') }}</p>
          <Button :label="t('nav.health')" icon="pi pi-arrow-right" iconPos="right" severity="success" style="width: 100%;" />
        </template>
      </Card>
    </div>

    <!-- Quick Stats -->
    <Card style="margin-bottom: 2rem;">
      <template #title>
        <div style="display: flex; align-items: center; gap: 0.5rem;">
          <i class="pi pi-chart-bar"></i>
          <span>{{ t('dashboard.quick_info') }}</span>
        </div>
      </template>
      <template #content>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">

          <!-- System Status -->
          <div style="
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0.75rem;
            padding: 1.5rem;
            border-radius: 0.75rem;
            background: var(--p-surface-100);
            border-top: 4px solid var(--p-primary-color);
            text-align: center;
          ">
            <div style="
              width: 56px;
              height: 56px;
              border-radius: 50%;
              background: var(--p-primary-color);
              display: flex;
              align-items: center;
              justify-content: center;
            ">
              <i class="pi pi-server" style="color: white; font-size: 1.5rem;"></i>
            </div>
            <div>
              <p style="font-size: 0.875rem; color: var(--p-text-muted-color); margin-bottom: 0.5rem;">{{ t('dashboard.stats.system_status') }}</p>
              <Tag :severity="systemStatus ? 'success' : 'danger'" :value="systemStatus ? 'UP' : 'DOWN'" style="font-size: 1rem; padding: 0.4rem 1rem;" />
            </div>
          </div>

          <!-- Predictions Today -->
          <div style="
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0.75rem;
            padding: 1.5rem;
            border-radius: 0.75rem;
            background: var(--p-surface-100);
            border-top: 4px solid var(--p-orange-500);
            text-align: center;
          ">
            <div style="
              width: 56px;
              height: 56px;
              border-radius: 50%;
              background: var(--p-orange-500);
              display: flex;
              align-items: center;
              justify-content: center;
            ">
              <i class="pi pi-chart-line" style="color: white; font-size: 1.5rem;"></i>
            </div>
            <div>
              <p style="font-size: 0.875rem; color: var(--p-text-muted-color); margin-bottom: 0.25rem;">{{ t('dashboard.stats.predictions_today') }}</p>
              <p style="font-size: 2rem; font-weight: bold; color: var(--p-orange-500);">{{ dashboardStore.predictionsToday }}</p>
            </div>
          </div>

          <!-- Simulations Today -->
          <div style="
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0.75rem;
            padding: 1.5rem;
            border-radius: 0.75rem;
            background: var(--p-surface-100);
            border-top: 4px solid var(--p-green-500);
            text-align: center;
          ">
            <div style="
              width: 56px;
              height: 56px;
              border-radius: 50%;
              background: var(--p-green-500);
              display: flex;
              align-items: center;
              justify-content: center;
            ">
              <i class="pi pi-cog" style="color: white; font-size: 1.5rem;"></i>
            </div>
            <div>
              <p style="font-size: 0.875rem; color: var(--p-text-muted-color); margin-bottom: 0.25rem;">{{ t('dashboard.stats.simulations_run') }}</p>
              <p style="font-size: 2rem; font-weight: bold; color: var(--p-green-500);">{{ dashboardStore.simulationsToday }}</p>
            </div>
          </div>

          <!-- Models Loaded -->
          <div style="
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0.75rem;
            padding: 1.5rem;
            border-radius: 0.75rem;
            background: var(--p-surface-100);
            border-top: 4px solid var(--p-purple-500);
            text-align: center;
          ">
            <div style="
              width: 56px;
              height: 56px;
              border-radius: 50%;
              background: var(--p-purple-500);
              display: flex;
              align-items: center;
              justify-content: center;
            ">
              <i class="pi pi-box" style="color: white; font-size: 1.5rem;"></i>
            </div>
            <div>
              <p style="font-size: 0.875rem; color: var(--p-text-muted-color); margin-bottom: 0.25rem;">{{ t('dashboard.stats.models_loaded') }}</p>
              <p style="font-size: 2rem; font-weight: bold; color: var(--p-purple-500);">{{ dashboardStore.modelsLoaded }}</p>
            </div>
          </div>

        </div>
      </template>
    </Card>

    <!-- Recent Activity -->
    <Card>
      <template #title>
        <div style="display: flex; align-items: center; gap: 0.5rem;">
          <i class="pi pi-history"></i>
          <span>{{ t('dashboard.recent_activity') }}</span>
        </div>
      </template>
      <template #content>
        <div v-if="dashboardStore.recentActivity.length > 0">
          <div
            v-for="(activity, index) in dashboardStore.recentActivity"
            :key="activity.id"
            style="
              display: flex;
              align-items: center;
              justify-content: space-between;
              padding: 0.75rem 0;
            "
            :style="{ borderBottom: index === dashboardStore.recentActivity.length - 1 ? 'none' : '1px solid var(--p-surface-200)' }"
          >
            <div style="display: flex; align-items: center; gap: 0.75rem;">
              <span :style="{ width: '10px', height: '10px', borderRadius: '50%', background: activity.color, display: 'inline-block', flexShrink: 0 }"></span>
              <span style="font-weight: 500;">{{ t(activity.actionKey) }}</span>
              <span style="color: var(--p-text-muted-color); font-size: 0.875rem;"> &nbsp;&nbsp;&nbsp;&nbsp; {{ formatDetail(activity) }}</span>
            </div>
            <span style="color: var(--p-text-muted-color); font-size: 0.8rem; white-space: nowrap;">{{ formatTime(activity.timestamp) }}</span>
          </div>
        </div>
        <div v-else style="text-align: center; color: var(--p-text-muted-color); padding: 2rem;">
          <i class="pi pi-inbox" style="font-size: 2rem; display: block; margin-bottom: 0.5rem;"></i>
          <p>{{ t('dashboard.no_activity') }}</p>
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