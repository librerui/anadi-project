import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface SimulationRecord {
  id: string
  timestamp: number
  profile: string
  version: string
  model_name: string
  overload_class: string
  iterations: number
  noise_scale: number
  features: Record<string, number>
  overload_probability: number
  distribution: Record<string, number>
}

export const useSimulationStore = defineStore('simulation', () => {
  // State
  const history = ref<SimulationRecord[]>([])

  // Getters
  const sortedHistory = computed(() => 
    [...history.value].sort((a, b) => b.timestamp - a.timestamp)
  )
  
  const todayCount = computed(() => {
    const today = new Date().setHours(0, 0, 0, 0)
    return history.value.filter(h => h.timestamp >= today).length
  })

  const totalCount = computed(() => history.value.length)

  // Actions
  function addRecord(record: Omit<SimulationRecord, 'id' | 'timestamp'>) {
    const newRecord: SimulationRecord = {
      ...record,
      id: crypto.randomUUID(),
      timestamp: Date.now(),
    }
    history.value.unshift(newRecord)
    if (history.value.length > 50) {
      history.value = history.value.slice(0, 50)
    }
    persist()
  }

  function clearHistory() {
    history.value = []
    persist()
  }

  function deleteRecord(id: string) {
    history.value = history.value.filter(h => h.id !== id)
    persist()
  }

  // Persistence
  function persist() {
    localStorage.setItem('ptd-simulation-history', JSON.stringify(history.value))
  }

  function load() {
    try {
      const saved = localStorage.getItem('ptd-simulation-history')
      if (saved) history.value = JSON.parse(saved)
    } catch {
      // Ignore parse errors
    }
  }

  load()

  return {
    history,
    sortedHistory,
    todayCount,
    totalCount,
    addRecord,
    clearHistory,
    deleteRecord,
  }
})