import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface PredictionRecord {
  id: string
  timestamp: number
  profile: string
  version: string
  task: string
  model_name: string
  features: Record<string, number>
  prediction: string | number
  raw_scores?: Record<string, number>
  confidence?: number
}

export const usePredictionStore = defineStore('prediction', () => {
  // State
  const history = ref<PredictionRecord[]>([])
  const favorites = ref<PredictionRecord[]>([])

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
  function addRecord(record: Omit<PredictionRecord, 'id' | 'timestamp'>) {
    const newRecord: PredictionRecord = {
      ...record,
      id: crypto.randomUUID(),
      timestamp: Date.now(),
    }
    history.value.unshift(newRecord)
    // Keep only last 100 records
    if (history.value.length > 100) {
      history.value = history.value.slice(0, 100)
    }
    persist()
  }

  function addToFavorites(record: PredictionRecord) {
    if (!favorites.value.find(f => f.id === record.id)) {
      favorites.value.push(record)
      persist()
    }
  }

  function removeFromFavorites(id: string) {
    favorites.value = favorites.value.filter(f => f.id !== id)
    persist()
  }

  function clearHistory() {
    history.value = []
    persist()
  }

  function deleteRecord(id: string) {
    history.value = history.value.filter(h => h.id !== id)
    favorites.value = favorites.value.filter(f => f.id !== id)
    persist()
  }

  // Persistence
  function persist() {
    localStorage.setItem('ptd-prediction-history', JSON.stringify(history.value))
    localStorage.setItem('ptd-prediction-favorites', JSON.stringify(favorites.value))
  }

  function load() {
    try {
      const savedHistory = localStorage.getItem('ptd-prediction-history')
      const savedFavorites = localStorage.getItem('ptd-prediction-favorites')
      if (savedHistory) history.value = JSON.parse(savedHistory)
      if (savedFavorites) favorites.value = JSON.parse(savedFavorites)
    } catch {
      // Ignore parse errors
    }
  }

  // Load on init
  load()

  return {
    history,
    favorites,
    sortedHistory,
    todayCount,
    totalCount,
    addRecord,
    addToFavorites,
    removeFromFavorites,
    clearHistory,
    deleteRecord,
  }
})