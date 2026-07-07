import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { usePredictionStore } from './predictionStore'
import { useSimulationStore } from './simulationStore'
import { useRegionalStore } from './regionalStore'

export interface ActivityItem {
  id: string
  type: 'prediction' | 'simulation' | 'regional'
  actionKey: string
  detailKey: string
  detailParams: Record<string, string | number>
  timestamp: number
  color: string
}

export const useDashboardStore = defineStore('dashboard', () => {
  const predictionStore = usePredictionStore()
  const simulationStore = useSimulationStore()
  const regionalStore = useRegionalStore()

  // State
  const systemHealth = ref(94)
  const modelsLoaded = ref(8)
  const serviceStatus = ref<'pass' | 'fail' | 'unknown'>('unknown')
  const lastChecked = ref<number | null>(null)

  // Getters
  const recentActivity = computed((): ActivityItem[] => {
    const activities: ActivityItem[] = []

    predictionStore.sortedHistory.slice(0, 5).forEach(p => {
      activities.push({
        id: p.id,
        type: 'prediction',
        actionKey: 'dashboard.activity.prediction',
        detailKey: 'dashboard.activity.profile_detail',
        detailParams: {
          task: p.task === 'classification' ? 'dashboard.activity.task_classification' : 'dashboard.activity.task_regression',
          profile: p.profile,
        },
        timestamp: p.timestamp,
        color: 'var(--p-primary-color)',
      })
    })

    simulationStore.sortedHistory.slice(0, 5).forEach(s => {
      activities.push({
        id: s.id,
        type: 'simulation',
        actionKey: 'dashboard.activity.simulation',
        detailKey: 'dashboard.activity.simulation_detail',
        detailParams: { count: s.iterations },
        timestamp: s.timestamp,
        color: 'var(--p-orange-500)',
      })
    })

    regionalStore.sortedHistory.slice(0, 5).forEach(r => {
      activities.push({
        id: r.id,
        type: 'regional',
        actionKey: 'dashboard.activity.regional',
        detailKey: 'dashboard.activity.regional_detail',
        detailParams: {
          count: r.ptdCount,
          region: r.region,
        },
        timestamp: r.timestamp,
        color: 'var(--p-green-500)',
      })
    })

    // Sort by timestamp descending, take top 10
    return activities
      .sort((a, b) => b.timestamp - a.timestamp)
      .slice(0, 10)
  })

  const predictionsToday = computed(() => predictionStore.todayCount)
  const simulationsToday = computed(() => simulationStore.todayCount)
  const regionalAnalysesToday = computed(() => regionalStore.todayCount)
  const ptdsAnalysed = computed(() => regionalStore.totalPtdCount)

  const modelsReady = computed(() => {
    return serviceStatus.value === 'pass' && modelsLoaded.value > 0
  })

  // Actions
  function setSystemHealth(value: number) {
    systemHealth.value = Math.max(0, Math.min(100, value))
  }

  function setModelsLoaded(value: number) {
    modelsLoaded.value = value
  }

  function setServiceStatus(status: 'pass' | 'fail') {
    serviceStatus.value = status
    lastChecked.value = Date.now()
  }

  return {
    systemHealth,
    modelsLoaded,
    serviceStatus,
    lastChecked,
    recentActivity,
    predictionsToday,
    simulationsToday,
    regionalAnalysesToday,
    ptdsAnalysed,
    modelsReady,
    setSystemHealth,
    setModelsLoaded,
    setServiceStatus,
  }
})
