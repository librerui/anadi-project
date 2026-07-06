<template>
  <div>
    <div style="position: relative; height: 280px; width: 100%;">
      <Line :data="chartData" :options="chartOptions" />
    </div>
    <div style="display: flex; justify-content: center; gap: 1.25rem; margin-top: 0.75rem; flex-wrap: wrap; font-size: 0.8rem; color: var(--p-text-muted-color);">
      <div style="display: flex; align-items: center; gap: 0.4rem;">
        <span style="width: 12px; height: 12px; border-radius: 2px; background: #16a34a; display: inline-block;"></span>
        <span>{{ $t('prediction.legend_good') }}</span>
      </div>
      <div style="display: flex; align-items: center; gap: 0.4rem;">
        <span style="width: 12px; height: 12px; border-radius: 2px; background: #3b82f6; display: inline-block;"></span>
        <span>{{ $t('prediction.legend_moderate') }}</span>
      </div>
      <div style="display: flex; align-items: center; gap: 0.4rem;">
        <span style="width: 12px; height: 12px; border-radius: 2px; background: #f59e0b; display: inline-block;"></span>
        <span>{{ $t('prediction.legend_low') }}</span>
      </div>
      <div style="display: flex; align-items: center; gap: 0.4rem;">
        <span style="width: 12px; height: 12px; border-radius: 2px; background: #dc2626; display: inline-block;"></span>
        <span>{{ $t('prediction.legend_negative') }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
  Filler,
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, LineElement, PointElement, CategoryScale, LinearScale, Filler)

const { t } = useI18n()

const props = defineProps<{
  baseCapacity: number // kVA/kW capacity available at the PTD
  chargerPower: number // kW per charger
  utilizationFactor: number // 0..1
  currentChargers: number
  maxChargers?: number
}>()

const marginColor = (pct: number) => {
  if (pct < 0) return '#dc2626'
  if (pct < 30) return '#f59e0b'
  if (pct < 70) return '#3b82f6'
  return '#16a34a'
}

const points = computed(() => {
  const max = Math.max(props.maxChargers ?? 0, props.currentChargers * 2, 10)
  const capacity = props.baseCapacity > 0 ? props.baseCapacity : 50
  const result: { n: number; margin: number }[] = []
  for (let n = 0; n <= max; n++) {
    const load = n * props.chargerPower * props.utilizationFactor
    const margin = ((capacity - load) / capacity) * 100
    result.push({ n, margin })
  }
  return result
})

const chartData = computed(() => ({
  labels: points.value.map((p) => String(p.n)),
  datasets: [
    {
      label: t('prediction.grid_margin'),
      data: points.value.map((p) => Math.round(p.margin * 10) / 10),
      borderColor: '#3b82f6',
      backgroundColor: 'rgba(59, 130, 246, 0.12)',
      fill: true,
      tension: 0.25,
      pointRadius: points.value.map((p) => (p.n === props.currentChargers ? 6 : 0)),
      pointHoverRadius: 6,
      pointBackgroundColor: points.value.map((p) => marginColor(p.margin)),
      segment: {
        borderColor: (ctx: any) => marginColor(points.value[ctx.p1DataIndex]?.margin ?? 0),
      },
    },
  ],
}))

const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: {
      callbacks: {
        label: (ctx: any) => `${t('prediction.grid_margin')}: ${ctx.parsed.y}%`,
      },
    },
  },
  scales: {
    x: {
      title: { display: true, text: t('prediction.chargers_axis') },
    },
    y: {
      title: { display: true, text: t('prediction.margin_axis') },
      suggestedMin: -20,
      suggestedMax: 100,
    },
  },
}))
</script>
