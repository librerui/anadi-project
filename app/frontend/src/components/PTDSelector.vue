<template>
  <div>
    <!-- District / Municipality / PTD selectors -->
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
      <div style="display: flex; flex-direction: column; gap: 0.25rem; min-width: 0;">
        <label :for="idPrefix + 'distrito'" style="font-weight: 500;">{{ resolvedDistrictLabel }}</label>
        <Dropdown
          :id="idPrefix + 'distrito'"
          v-model="selectedDistrito"
          :options="districts"
          :placeholder="resolvedDistrictPlaceholder"
          style="width: 100%;"
          @change="onDistritoChange"
          showClear
        />
      </div>

      <div style="display: flex; flex-direction: column; gap: 0.25rem; min-width: 0;">
        <label :for="idPrefix + 'concelho'" style="font-weight: 500;">{{ resolvedMunicipalityLabel }}</label>
        <Dropdown
          :id="idPrefix + 'concelho'"
          v-model="selectedConcelho"
          :options="concelhos"
          :placeholder="resolvedMunicipalityPlaceholder"
          style="width: 100%;"
          @change="onConcelhoChange"
          showClear
          :disabled="!selectedDistrito"
        />
      </div>

      <div style="display: flex; flex-direction: column; gap: 0.25rem; min-width: 0;">
        <label :for="idPrefix + 'ptd'" style="font-weight: 500;">{{ resolvedPtdLabel }}</label>
        <Dropdown
          :id="idPrefix + 'ptd'"
          v-model="selectedPTDId"
          :options="ptdSelectOptions"
          optionLabel="label"
          optionValue="value"
          :placeholder="resolvedPtdPlaceholder"
          style="width: 100%;"
          :disabled="!canSelectPTD"
          showClear
          @change="onPTDChange"
        />
      </div>
    </div>

    <!-- Selected PTD Info Card -->
    <div v-if="selectedPTD" style="margin-top: 1rem; display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem;">
      <div style="background: var(--p-surface-100); padding: 1rem; border-radius: 0.5rem;">
        <p style="margin: 0 0 0.5rem 0; font-weight: 600;">{{ selectedPTD.codigo_instalacao }}</p>
        <p style="margin: 0.25rem 0;">{{ selectedPTD.distrito }} / {{ selectedPTD.concelho }}</p>
        <p style="margin: 0.25rem 0;">{{ $t('prediction.installed_power') }}: {{ selectedPTD.potencia_instalada }} {{ $t('prediction.units.kva') }}</p>
        <p style="margin: 0.25rem 0;">{{ $t('prediction.customers') }}: {{ selectedPTD.n_clientes }} {{ $t('prediction.units.clients') }}</p>
      </div>
    </div>

    <!-- Map -->
    <div style="margin-top: 1.5rem;">
      <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 0.75rem; margin-bottom: 1rem;">
        <p style="margin: 0; color: var(--p-text-muted-color);">{{ $t('prediction.map_hint') }}</p>
        <div style="display: flex; align-items: center; gap: 0.5rem;">
          <label :for="idPrefix + 'map_count'" style="font-weight: 500; font-size: 0.875rem; white-space: nowrap;">{{ $t('prediction.map_count_label') }}</label>
          <InputNumber :id="idPrefix + 'map_count'" v-model="mapPointLimit" :min="10" :max="1000" :step="10" showButtons style="width: 10rem;" />
        </div>
      </div>
      <div style="display: grid; gap: 1rem; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); align-items: start;">
        <div style="border: 1px solid var(--p-surface-300); border-radius: 0.75rem; padding: 0.5rem; background: var(--p-surface-0); overflow: hidden;">
          <div ref="mapContainer" style="height: 360px; width: 100%; border-radius: 0.6rem;"></div>
        </div>

        <div style="display: flex; flex-direction: column; gap: 0.75rem;">
          <div style="background: var(--p-surface-100); padding: 1rem; border-radius: 0.75rem;">
            <p style="margin: 0 0 0.25rem 0; font-size: 0.875rem; color: var(--p-text-muted-color);">{{ $t('prediction.map_showing') }}</p>
            <p style="margin: 0; font-weight: 700;">{{ mapPTDs.length }} {{ $t('prediction.map_points') }}</p>
          </div>

          <div v-if="selectedPTD" style="background: var(--p-surface-100); padding: 1rem; border-radius: 0.75rem;">
            <p style="margin: 0 0 0.25rem 0; font-weight: 700;">{{ selectedPTD.codigo_instalacao }}</p>
            <p style="margin: 0.2rem 0;">{{ selectedPTD.distrito }} / {{ selectedPTD.concelho }}</p>
            <p style="margin: 0.2rem 0;">{{ $t('prediction.installed_power') }}: {{ selectedPTD.potencia_instalada }} {{ $t('prediction.units.kva') }}</p>
            <p style="margin: 0.2rem 0;">{{ $t('prediction.customers') }}: {{ selectedPTD.n_clientes }} {{ $t('prediction.units.clients') }}</p>
            <Button type="button" severity="secondary" class="p-button-sm" style="margin-top: 0.5rem;" @click="applySelectedPTD">
              {{ $t('prediction.map_apply') }}
            </Button>
          </div>

          <div style="background: var(--p-surface-100); padding: 1rem; border-radius: 0.75rem;">
            <p style="margin: 0 0 0.5rem 0; font-weight: 700; font-size: 0.875rem;">{{ $t('prediction.map_legend_title') }}</p>
            <div style="display: flex; flex-direction: column; gap: 0.4rem; font-size: 0.8rem; color: var(--p-text-muted-color);">
              <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="width: 12px; height: 12px; border-radius: 50%; background: #16a34a; display: inline-block;"></span>
                <span>{{ $t('prediction.legend_good') }}</span>
              </div>
              <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="width: 12px; height: 12px; border-radius: 50%; background: #3b82f6; display: inline-block;"></span>
                <span>{{ $t('prediction.legend_moderate') }}</span>
              </div>
              <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="width: 12px; height: 12px; border-radius: 50%; background: #f59e0b; display: inline-block;"></span>
                <span>{{ $t('prediction.legend_low') }}</span>
              </div>
              <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="width: 12px; height: 12px; border-radius: 50%; background: #dc2626; display: inline-block;"></span>
                <span>{{ $t('prediction.legend_negative') }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, onBeforeUnmount } from 'vue'
import { useI18n } from 'vue-i18n'
import Dropdown from 'primevue/dropdown'
import InputNumber from 'primevue/inputnumber'
import Button from 'primevue/button'
import { listPTDs } from '@/api/endpoints'
import type { PTDBase } from '@/types'
import L from 'leaflet'

const { t } = useI18n()

const props = withDefaults(defineProps<{
  idPrefix?: string
  districtLabel?: string
  municipalityLabel?: string
  ptdLabel?: string
  districtPlaceholder?: string
  municipalityPlaceholder?: string
  ptdPlaceholder?: string
  modelValue?: PTDBase | null
}>(), {
  idPrefix: '',
  districtLabel: undefined,
  municipalityLabel: undefined,
  ptdLabel: undefined,
  districtPlaceholder: undefined,
  municipalityPlaceholder: undefined,
  ptdPlaceholder: undefined,
  modelValue: null,
})

const emit = defineEmits<{
  (e: 'update:modelValue', ptd: PTDBase | null): void
  (e: 'select', ptd: PTDBase): void
  // NEW: Emit encoded values when distrito/concelho changes (even without PTD selection)
  (e: 'encodedChange', values: { distrito_enc: number | null; concelho_enc: number | null }): void
}>()

const resolvedDistrictLabel = computed(() => props.districtLabel ?? t('prediction.district'))
const resolvedMunicipalityLabel = computed(() => props.municipalityLabel ?? t('prediction.municipality'))
const resolvedPtdLabel = computed(() => props.ptdLabel ?? t('prediction.ptd'))
const resolvedDistrictPlaceholder = computed(() => props.districtPlaceholder ?? t('prediction.select_district'))
const resolvedMunicipalityPlaceholder = computed(() => props.municipalityPlaceholder ?? t('prediction.select_municipality'))
const resolvedPtdPlaceholder = computed(() => props.ptdPlaceholder ?? t('prediction.select_ptd'))

// Internal state
const selectedDistrito = ref<string | null>(null)
const selectedConcelho = ref<string | null>(null)
const selectedPTDId = ref<string | null>(null)
const loadingPTDs = ref(false)
const districts = ref<string[]>([])
const concelhos = ref<string[]>([])
const ptdCache = ref<PTDBase[]>([])
const districtMunicipalities = ref<Record<string, string[]>>({})
const ptdOptions = ref<PTDBase[]>([])

// Map state
const mapPointLimit = ref(220)
const mapCenter = ref<[number, number]>([39.5, -8.0])
const mapZoom = ref(7)
const portugalBounds = ref<[number, number][]>([[36.9, -9.5], [42.2, -6.2]])
const mapTileUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
const mapAttribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
const mapContainer = ref<HTMLDivElement | null>(null)
let mapInstance: L.Map | null = null
let markerLayer: L.LayerGroup | null = null

// Computed
const ptdSelectOptions = computed(() =>
  ptdOptions.value.map((ptd) => ({
    label: `${ptd.codigo_instalacao} — ${ptd.concelho}`,
    value: ptd.codigo_instalacao,
  }))
)

const selectedPTD = computed(() =>
  ptdOptions.value.find((item) => item.codigo_instalacao === selectedPTDId.value) || null
)

const canSelectPTD = computed(
  () => !!selectedDistrito.value && !!selectedConcelho.value && !loadingPTDs.value
)

// Map PTDs - filtered by current distrito/concelho selection
const mapPTDs = computed(() => {
  let filtered = ptdCache.value.filter((ptd) =>
    typeof ptd.latitude === 'number' && typeof ptd.longitude === 'number'
  )

  if (selectedDistrito.value) {
    filtered = filtered.filter(p => p.distrito === selectedDistrito.value)
  }
  if (selectedConcelho.value) {
    filtered = filtered.filter(p => p.concelho === selectedConcelho.value)
  }

  return filtered.slice(0, mapPointLimit.value)
})

const mapMarkers = computed(() =>
  mapPTDs.value.map((ptd) => ({
    id: ptd.codigo_instalacao,
    lat: ptd.latitude,
    lng: ptd.longitude,
    ptd,
  }))
)

const getFolgaColor = (value?: number | null) => {
  if (typeof value !== 'number' || Number.isNaN(value)) return '#2563eb'
  if (value < 0) return '#dc2626'
  if (value < 0.3) return '#f59e0b'
  if (value < 0.7) return '#3b82f6'
  return '#16a34a'
}

const renderMapMarkers = () => {
  if (!mapInstance) return
  if (!markerLayer) {
    markerLayer = L.layerGroup().addTo(mapInstance)
  } else {
    markerLayer.clearLayers()
  }

  mapMarkers.value.forEach((marker) => {
    const popupContent = `<div style="min-width: 180px;"><strong>${marker.ptd.codigo_instalacao}</strong><div>${marker.ptd.distrito} / ${marker.ptd.concelho}</div><div>${t('prediction.installed_power')}: ${marker.ptd.potencia_instalada} ${t('prediction.units.kva')}</div><div>Folga: ${marker.ptd.pfolga_ptd ?? 'n/a'}</div></div>`
    const leafletMarker = L.circleMarker([marker.lat as number, marker.lng as number], {
      radius: 4,
      fillColor: getFolgaColor(marker.ptd.pfolga_ptd),
      color: '#ffffff',
      weight: 1.5,
      opacity: 1,
      fillOpacity: 0.9,
    })
      .bindPopup(popupContent)
      .on('click', () => {
        selectedPTDId.value = marker.ptd.codigo_instalacao
        emit('update:modelValue', marker.ptd)
        emit('select', marker.ptd)
      })

    markerLayer?.addLayer(leafletMarker)
  })
}

// NEW: Get encoded values for current selection
const getEncodedValues = (): { distrito_enc: number | null; concelho_enc: number | null } => {
  // Find any PTD with matching distrito to get distrito_enc
  const distritoPTD = ptdCache.value.find(p => p.distrito === selectedDistrito.value)
  const concelhoPTD = ptdCache.value.find(p => 
    p.distrito === selectedDistrito.value && p.concelho === selectedConcelho.value
  )

  return {
    distrito_enc: distritoPTD?.distrito_enc ?? null,
    concelho_enc: concelhoPTD?.concelho_enc ?? null,
  }
}

// Methods
const buildDistrictCache = (items: PTDBase[]) => {
  const districtMap = new Map<string, Set<string>>()

  items.forEach((item) => {
    const district = item.distrito || ''
    const municipality = item.concelho || ''

    if (!districtMap.has(district)) {
      districtMap.set(district, new Set())
    }
    districtMap.get(district)?.add(municipality)
  })

  districts.value = Array.from(districtMap.keys()).sort()
  districtMunicipalities.value = Object.fromEntries(
    Array.from(districtMap.entries()).map(([district, municipalities]) => [
      district,
      Array.from(municipalities).sort(),
    ])
  )

  if (selectedDistrito.value) {
    concelhos.value = districtMunicipalities.value[selectedDistrito.value] || []
  } else {
    concelhos.value = Array.from(new Set(items.map((item) => item.concelho))).sort()
  }
}

const applyCachedPTDFilters = () => {
  ptdOptions.value = ptdCache.value.filter((item) => {
    const matchesDistrict = !selectedDistrito.value || item.distrito === selectedDistrito.value
    const matchesMunicipality = !selectedConcelho.value || item.concelho === selectedConcelho.value
    return matchesDistrict && matchesMunicipality
  })

  if (selectedDistrito.value) {
    concelhos.value = districtMunicipalities.value[selectedDistrito.value] || []
  } else {
    concelhos.value = Array.from(new Set(ptdCache.value.map((item) => item.concelho))).sort()
  }
}

const loadPTDs = async () => {
  loadingPTDs.value = true
  try {
    if (!ptdCache.value.length) {
      const response = await listPTDs({})
      ptdCache.value = response.data.items
      buildDistrictCache(ptdCache.value)
    }
    applyCachedPTDFilters()
  } catch (error: any) {
    console.error('Failed to load PTDs:', error)
  } finally {
    loadingPTDs.value = false
  }
}

const onDistritoChange = async () => {
  selectedConcelho.value = null
  selectedPTDId.value = null
  await loadPTDs()

  // NEW: Emit encoded values even without PTD selection
  const encoded = getEncodedValues()
  emit('encodedChange', encoded)
  emit('update:modelValue', null)
}

const onConcelhoChange = async () => {
  selectedPTDId.value = null
  await loadPTDs()

  // NEW: Emit encoded values even without PTD selection
  const encoded = getEncodedValues()
  emit('encodedChange', encoded)
  emit('update:modelValue', null)
}

const onPTDChange = () => {
  const ptd = selectedPTD.value
  if (ptd) {
    emit('update:modelValue', ptd)
    emit('select', ptd)
  }
}

const applySelectedPTD = () => {
  if (selectedPTD.value) {
    emit('update:modelValue', selectedPTD.value)
    emit('select', selectedPTD.value)
  }
}

// Watch external modelValue changes
watch(
  () => props.modelValue,
  (ptd) => {
    if (ptd) {
      selectedDistrito.value = ptd.distrito
      selectedConcelho.value = ptd.concelho
      selectedPTDId.value = ptd.codigo_instalacao
    } else if (!selectedDistrito.value && !selectedConcelho.value) {
      selectedPTDId.value = null
    }
  },
  { immediate: true }
)

// Watch map markers and re-render
watch(mapMarkers, () => {
  renderMapMarkers()
}, { deep: true })

// Lifecycle
onMounted(() => {
  loadPTDs().then(() => {
    // Initialize map after PTDs are loaded
    if (!mapContainer.value) return

    mapInstance = L.map(mapContainer.value, {
      center: mapCenter.value,
      zoom: mapZoom.value,
      minZoom: 6,
      maxZoom: 12,
      zoomControl: true,
      scrollWheelZoom: true,
      maxBounds: portugalBounds.value,
      maxBoundsViscosity: 1.0,
    })

    L.tileLayer(mapTileUrl, { attribution: mapAttribution }).addTo(mapInstance)
    markerLayer = L.layerGroup().addTo(mapInstance)

    renderMapMarkers()
    mapInstance.fitBounds(portugalBounds.value)
    setTimeout(() => mapInstance?.invalidateSize(), 0)
  })
})

onBeforeUnmount(() => {
  mapInstance?.remove()
  mapInstance = null
  markerLayer = null
})

// Expose for parent access
defineExpose({
  selectedPTD,
  selectedDistrito,
  selectedConcelho,
  getEncodedValues,
})
</script>