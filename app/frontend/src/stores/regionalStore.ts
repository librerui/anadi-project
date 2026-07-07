import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface RegionalRecord {
  id: string
  timestamp: number
  profile: string
  version: string
  model_name: string
  region: string
  ptdCount: number
  overload_probability: number
  distribution?: Record<string, number>
}

export const useRegionalStore = defineStore('regional', () => {
  // State
  const history = ref<RegionalRecord[]>([])

  // Getters
  const sortedHistory = computed(() => 
    [...history.value].sort((a, b) => b.timestamp - a.timestamp)
  )

  const todayCount = computed(() => {
    const today = new Date().setHours(0, 0, 0, 0)
    return history.value.filter(h => h.timestamp >= today).length
  })

  const totalCount = computed(() => history.value.length)

  const totalPtdCount = computed(() => 
    history.value.reduce((sum, h) => sum + (h.ptdCount || 0), 0)
  )

  // Alias for Dashboard compatibility
  const records = computed(() => history.value)

  // Actions
  function addRecord(record: Omit<RegionalRecord, 'id' | 'timestamp'>) {
    const newRecord: RegionalRecord = {
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
    localStorage.setItem('ptd-regional-history', JSON.stringify(history.value))
  }

  function load() {
    try {
      const saved = localStorage.getItem('ptd-regional-history')
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
    totalPtdCount,
    records,
    addRecord,
    clearHistory,
    deleteRecord,
  }
})
