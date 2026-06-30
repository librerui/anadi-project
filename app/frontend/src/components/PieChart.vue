<template>
  <div style="position: relative; height: 300px; width: 100%;">
    <Pie :data="props.data" :options="options" />
  </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue'
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

const options = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { position: 'bottom' as const },
  },
}
</script>