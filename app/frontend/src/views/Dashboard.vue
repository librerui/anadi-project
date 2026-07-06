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

      <Card @click="goTo('/regional')" style="cursor: pointer;">
        <template #title>
          <div style="display: flex; align-items: center; gap: 0.5rem;">
            <i class="pi pi-map" style="font-size: 1.5rem;"></i>
            <span>{{ t('nav.regional') }}</span>
          </div>
        </template>
        <template #content>
          <p style="color: var(--p-text-muted-color); margin-bottom: 1rem;">{{ t('dashboard.cards.regional') }}</p>
          <Button :label="t('nav.regional')" icon="pi pi-arrow-right" iconPos="right" severity="info" style="width: 100%;" />
        </template>
      </Card>
    </div>

    <!-- Quick Stats + Recent Activity side by side, compact -->
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap: 1rem; align-items: start;">

      <!-- Quick Stats -->
      <Card :pt="{ body: { style: 'padding: 0.85rem 1rem;' } }">
        <template #title>
          <div style="display: flex; align-items: center; gap: 0.4rem; font-size: 0.95rem;">
            <i class="pi pi-chart-bar" style="font-size: 0.9rem;"></i>
            <span>{{ t('dashboard.quick_info') }}</span>
          </div>
        </template>
        <template #content>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(110px, 1fr)); gap: 0.5rem;">

            <!-- System Status -->
            <div style="
              padding: 0.5rem 0.6rem;
              border-radius: 0.4rem;
              background: var(--p-surface-100);
              border-left: 3px solid var(--p-primary-color);
            ">
              <p style="font-size: 0.7rem; color: var(--p-text-muted-color); margin-bottom: 0.25rem;">{{ t('dashboard.stats.system_status') }}</p>
              <Tag :severity="systemStatus ? 'success' : 'danger'" :value="systemStatus ? 'UP' : 'DOWN'" style="font-size: 0.75rem;" />
            </div>

            <!-- Predictions Today -->
            <div style="
              padding: 0.5rem 0.6rem;
              border-radius: 0.4rem;
              background: var(--p-surface-100);
              border-left: 3px solid var(--p-orange-500);
            ">
              <p style="font-size: 0.7rem; color: var(--p-text-muted-color); margin-bottom: 0.15rem;">{{ t('dashboard.stats.predictions_today') }}</p>
              <p style="font-size: 1.05rem; font-weight: 700; color: var(--p-orange-500);">{{ dashboardStore.predictionsToday }}</p>
            </div>

            <!-- Simulations Today -->
            <div style="
              padding: 0.5rem 0.6rem;
              border-radius: 0.4rem;
              background: var(--p-surface-100);
              border-left: 3px solid var(--p-green-500);
            ">
              <p style="font-size: 0.7rem; color: var(--p-text-muted-color); margin-bottom: 0.15rem;">{{ t('dashboard.stats.simulations_run') }}</p>
              <p style="font-size: 1.05rem; font-weight: 700; color: var(--p-green-500);">{{ dashboardStore.simulationsToday }}</p>
            </div>

            <!-- Models Loaded -->
            <div style="
              padding: 0.5rem 0.6rem;
              border-radius: 0.4rem;
              background: var(--p-surface-100);
              border-left: 3px solid var(--p-purple-500);
            ">
              <p style="font-size: 0.7rem; color: var(--p-text-muted-color); margin-bottom: 0.15rem;">{{ t('dashboard.stats.models_loaded') }}</p>
              <p style="font-size: 1.05rem; font-weight: 700; color: var(--p-purple-500);">{{ dashboardStore.modelsLoaded }}</p>
            </div>

          </div>
        </template>
      </Card>

      <!-- Recent Activity -->
      <Card :pt="{ body: { style: 'padding: 0.85rem 1rem;' } }">
        <template #title>
          <div style="display: flex; align-items: center; gap: 0.4rem; font-size: 0.95rem;">
            <i class="pi pi-history" style="font-size: 0.9rem;"></i>
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
                padding: 0.35rem 0;
                gap: 0.5rem;
              "
              :style="{ borderBottom: index === dashboardStore.recentActivity.length - 1 ? 'none' : '1px solid var(--p-surface-200)' }"
            >
              <div style="display: flex; align-items: center; gap: 0.4rem; min-width: 0;">
                <span :style="{ width: '7px', height: '7px', borderRadius: '50%', background: activity.color, display: 'inline-block', flexShrink: 0 }"></span>
                <span style="font-weight: 500; font-size: 0.8rem; white-space: nowrap;">{{ t(activity.actionKey) }}</span>
                <span style="color: var(--p-text-muted-color); font-size: 0.75rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{{ formatDetail(activity) }}</span>
              </div>
              <span style="color: var(--p-text-muted-color); font-size: 0.7rem; white-space: nowrap; flex-shrink: 0;">{{ formatTime(activity.timestamp) }}</span>
            </div>
          </div>
          <div v-else style="text-align: center; color: var(--p-text-muted-color); padding: 1.25rem;">
            <i class="pi pi-inbox" style="font-size: 1.5rem; display: block; margin-bottom: 0.4rem;"></i>
            <p style="font-size: 0.8rem;">{{ t('dashboard.no_activity') }}</p>
          </div>
        </template>
      </Card>

    </div>
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