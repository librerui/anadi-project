import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { usePredictionStore } from './predictionStore'
import { useSimulationStore } from './simulationStore'

export interface ActivityItem {
  id: string
  type: 'prediction' | 'simulation' | 'reload'
  action: string
  detail: string
  timestamp: number
  color: string
}

export const useDashboardStore = defineStore('dashboard', () => {
  const predictionStore = usePredictionStore()
  const simulationStore = useSimulationStore()

  // State
  const systemHealth = ref(94)
  const modelsLoaded = ref(8)

  // Getters
  const recentActivity = computed((): ActivityItem[] => {
    const activities: ActivityItem[] = []

    predictionStore.sortedHistory.slice(0, 5).forEach(p => {
      activities.push({
        id: p.id,
        type: 'prediction',
        action: 'Prediction',
        detail: `${p.task === 'classification' ? 'Classification' : 'Regression'} — Profile: ${p.profile}`,
        timestamp: p.timestamp,
        color: 'var(--p-primary-color)',
      })
    })

    simulationStore.sortedHistory.slice(0, 5).forEach(s => {
      activities.push({
        id: s.id,
        type: 'simulation',
        action: 'Simulation',
        detail: `Monte Carlo — ${s.iterations.toLocaleString()} iterations`,
        timestamp: s.timestamp,
        color: 'var(--p-orange-500)',
      })
    })

    // Sort by timestamp descending, take top 10
    return activities
      .sort((a, b) => b.timestamp - a.timestamp)
      .slice(0, 10)
  })

  const predictionsToday = computed(() => predictionStore.todayCount)
  const simulationsToday = computed(() => simulationStore.todayCount)

  // Actions
  function setSystemHealth(value: number) {
    systemHealth.value = Math.max(0, Math.min(100, value))
  }

  function setModelsLoaded(value: number) {
    modelsLoaded.value = value
  }

  return {
    systemHealth,
    modelsLoaded,
    recentActivity,
    predictionsToday,
    simulationsToday,
    setSystemHealth,
    setModelsLoaded,
  }
})