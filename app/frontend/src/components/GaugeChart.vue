<template>
  <div>
    <!-- Gauge -->
    <div style="position: relative; height: 220px; width: 100%; display: flex; justify-content: center;">
      <Doughnut :data="gaugeData" :options="gaugeOptions" />
      <div style="
        position: absolute;
        bottom: 20%;
        left: 50%;
        transform: translateX(-50%);
        text-align: center;
      ">
        <div style="font-size: 2rem; font-weight: bold;" :style="{ color: valueColor }">
          {{ (props.value * 100).toFixed(1) }}%
        </div>
        <div style="font-size: 0.875rem; color: var(--p-text-muted-color);">
          {{ props.label }}
        </div>
      </div>
    </div>

    <!-- Legend -->
    <div style="
      display: flex;
      justify-content: center;
      gap: 1.5rem;
      margin-top: 0.5rem;
      font-size: 0.8rem;
      color: var(--p-text-muted-color);
    ">
      <div style="display: flex; align-items: center; gap: 0.4rem;">
        <span style="
          width: 12px;
          height: 12px;
          border-radius: 2px;
          background: var(--p-green-500);
          display: inline-block;
        "></span>
        <span>Baixo</span>
      </div>
      <div style="display: flex; align-items: center; gap: 0.4rem;">
        <span style="
          width: 12px;
          height: 12px;
          border-radius: 2px;
          background: var(--p-orange-500);
          display: inline-block;
        "></span>
        <span>Médio</span>
      </div>
      <div style="display: flex; align-items: center; gap: 0.4rem;">
        <span style="
          width: 12px;
          height: 12px;
          border-radius: 2px;
          background: var(--p-red-500);
          display: inline-block;
        "></span>
        <span>Alto</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Doughnut } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, ArcElement)

const props = defineProps<{
  value: number
  label: string
  thresholds?: {
    low: number
    medium: number
  }
}>()

const thresholds = computed(() => props.thresholds ?? { low: 0.3, medium: 0.7 })

const valueColor = computed(() => {
  if (props.value < thresholds.value.low) return 'var(--p-green-500)'
  if (props.value < thresholds.value.medium) return 'var(--p-orange-500)'
  return 'var(--p-red-500)'
})

const gaugeData = computed(() => {
  const v = Math.max(0, Math.min(1, props.value))
  const empty = 1 - v
  return {
    labels: [props.label, ''],
    datasets: [{
      data: [v, empty],
      backgroundColor: [valueColor.value, 'var(--p-surface-200)'],
      borderWidth: 0,
      circumference: 180,
      rotation: 270,
    }]
  }
})

const gaugeOptions = {
  responsive: true,
  maintainAspectRatio: false,
  cutout: '75%',
  plugins: {
    legend: { display: false },
    tooltip: { enabled: false },
  },
}
</script>