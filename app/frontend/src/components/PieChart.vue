<template>
  <div style="position: relative; height: 300px; width: 100%;">
    <Pie :data="safeData" :options="options" />
  </div>
</template>

<script setup lang="ts">
import { computed, defineProps } from 'vue'
import { Pie } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement, CategoryScale } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale)

const props = defineProps<{
  data: {
    labels: string[]
    datasets: Array<{
      data: number[]
      backgroundColor: string[]
      hoverBackgroundColor?: string[]
    }>
  }
}>()

// FIX: Map CSS variable colors to actual hex colors for canvas rendering
const cssColorMap: Record<string, string> = {
  'var(--p-red-500)': '#ef4444',
  'var(--p-orange-500)': '#f97316',
  'var(--p-green-500)': '#22c55e',
  'var(--p-blue-500)': '#3b82f6',
  'var(--p-surface-200)': '#e5e7eb',
  'var(--p-surface-100)': '#f3f4f6',
  'var(--p-surface-0)': '#ffffff',
}

const resolveColor = (color: string): string => {
  return cssColorMap[color] || color
}

const safeData = computed(() => {
  if (!props.data || !props.data.datasets || !props.data.datasets.length) {
    return { labels: [], datasets: [] }
  }

  return {
    labels: props.data.labels,
    datasets: props.data.datasets.map((dataset) => ({
      ...dataset,
      backgroundColor: dataset.backgroundColor.map(resolveColor),
      hoverBackgroundColor: (dataset.hoverBackgroundColor || dataset.backgroundColor).map(resolveColor),
    })),
  }
})

const options = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { position: 'bottom' as const },
  },
}
</script>