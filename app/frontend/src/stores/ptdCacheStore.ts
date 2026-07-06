import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { listPTDs } from '@/api/endpoints'
import type { PTDBase } from '@/types'

const CACHE_KEY = 'ptd_cache_v1'
const CACHE_TIMESTAMP_KEY = 'ptd_cache_timestamp_v1'
const CACHE_TTL_MS = 1000 * 60 * 60 * 24 // 24 horas

function loadFromStorage(): PTDBase[] | null {
  try {
    const cached = localStorage.getItem(CACHE_KEY)
    const timestamp = localStorage.getItem(CACHE_TIMESTAMP_KEY)
    if (!cached || !timestamp) return null
    const age = Date.now() - parseInt(timestamp, 10)
    if (age > CACHE_TTL_MS) {
      localStorage.removeItem(CACHE_KEY)
      localStorage.removeItem(CACHE_TIMESTAMP_KEY)
      return null
    }
    return JSON.parse(cached) as PTDBase[]
  } catch {
    return null
  }
}

function saveToStorage(items: PTDBase[]) {
  try {
    localStorage.setItem(CACHE_KEY, JSON.stringify(items))
    localStorage.setItem(CACHE_TIMESTAMP_KEY, String(Date.now()))
  } catch (e) {
    console.warn('Failed to cache PTDs:', e)
  }
}

export const usePTDCacheStore = defineStore('ptdCache', () => {
  // State
  const items = ref<PTDBase[]>(loadFromStorage() || [])
  const loading = ref(false)
  const lastFetch = ref<number | null>(
    localStorage.getItem(CACHE_TIMESTAMP_KEY)
      ? parseInt(localStorage.getItem(CACHE_TIMESTAMP_KEY)!, 10)
      : null
  )

  // Getters
  const isCached = computed(() => items.value.length > 0)
  const cacheAge = computed(() => {
    if (!lastFetch.value) return Infinity
    return Date.now() - lastFetch.value
  })
  const isStale = computed(() => cacheAge.value > CACHE_TTL_MS)

  // Actions
  async function fetch(force = false): Promise<PTDBase[]> {
    // Se temos cache válido e não é force, retornar cache
    if (!force && items.value.length > 0 && !isStale.value) {
      return items.value
    }

    // Se já estamos a carregar, esperar
    if (loading.value) {
      await new Promise(resolve => {
        const check = setInterval(() => {
          if (!loading.value) {
            clearInterval(check)
            resolve(undefined)
          }
        }, 50)
      })
      return items.value
    }

    loading.value = true
    try {
      const response = await listPTDs({})
      items.value = response.data.items
      lastFetch.value = Date.now()
      saveToStorage(items.value)
      return items.value
    } catch (error) {
      console.error('Failed to fetch PTDs:', error)
      // Se falhar mas temos cache, usar cache mesmo stale
      if (items.value.length > 0) {
        return items.value
      }
      throw error
    } finally {
      loading.value = false
    }
  }

  function invalidate() {
    items.value = []
    lastFetch.value = null
    localStorage.removeItem(CACHE_KEY)
    localStorage.removeItem(CACHE_TIMESTAMP_KEY)
  }

  function getDistricts(): string[] {
    const districtMap = new Map<string, Set<string>>()
    items.value.forEach((item) => {
      const district = item.distrito || ''
      const municipality = item.concelho || ''
      if (!districtMap.has(district)) districtMap.set(district, new Set())
      districtMap.get(district)?.add(municipality)
    })
    return Array.from(districtMap.keys()).sort()
  }

  function getConcelhos(distrito: string | null): string[] {
    if (!distrito) {
      return Array.from(new Set(items.value.map(i => i.concelho))).sort()
    }
    const municipalities = new Set<string>()
    items.value.forEach(item => {
      if (item.distrito === distrito) {
        municipalities.add(item.concelho || '')
      }
    })
    return Array.from(municipalities).sort()
  }

  function getPTDsByRegion(distrito: string | null, concelho: string | null): PTDBase[] {
    return items.value.filter(item => {
      const matchesDistrict = !distrito || item.distrito === distrito
      const matchesMunicipality = !concelho || item.concelho === concelho
      return matchesDistrict && matchesMunicipality
    })
  }

  return {
    items,
    loading,
    isCached,
    isStale,
    fetch,
    invalidate,
    getDistricts,
    getConcelhos,
    getPTDsByRegion,
  }
})
