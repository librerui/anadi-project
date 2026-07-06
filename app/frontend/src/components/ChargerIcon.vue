<template>
  <svg v-if="type === 'wallbox'" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
    <rect x="18" y="8" width="28" height="40" rx="4" :fill="bodyColor" />
    <rect x="22" y="14" width="20" height="12" rx="2" fill="#ffffff" opacity="0.85" />
    <circle cx="32" cy="34" r="4" :fill="accentColor" />
    <path d="M46 44 C 52 44, 54 48, 54 54" stroke="#94a3b8" stroke-width="2.5" fill="none" stroke-linecap="round" />
    <circle cx="54" cy="56" r="3" :fill="accentColor" />
    <rect x="14" y="48" width="36" height="4" rx="2" fill="#475569" />
  </svg>

  <svg v-else-if="type === 'pedestal'" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
    <rect x="24" y="6" width="16" height="34" rx="3" :fill="bodyColor" />
    <rect x="27" y="11" width="10" height="8" rx="1.5" fill="#ffffff" opacity="0.85" />
    <circle cx="32" cy="26" r="3.5" :fill="accentColor" />
    <rect x="18" y="40" width="28" height="6" rx="2" fill="#334155" />
    <path d="M40 48 C 47 48, 49 52, 49 58" stroke="#94a3b8" stroke-width="2.5" fill="none" stroke-linecap="round" />
    <circle cx="49" cy="59" r="3" :fill="accentColor" />
  </svg>

  <svg v-else viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
    <rect x="20" y="4" width="24" height="46" rx="4" :fill="bodyColor" />
    <rect x="24" y="10" width="16" height="16" rx="2" fill="#ffffff" opacity="0.85" />
    <text x="32" y="21" text-anchor="middle" font-size="8" font-weight="700" fill="#0f172a">DC</text>
    <circle cx="32" cy="36" r="4" :fill="accentColor" />
    <rect x="16" y="50" width="32" height="6" rx="2" fill="#334155" />
    <path d="M44 40 C 52 40, 55 45, 55 53" stroke="#94a3b8" stroke-width="3" fill="none" stroke-linecap="round" />
    <circle cx="55" cy="55" r="3.5" :fill="accentColor" />
  </svg>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  type: 'wallbox' | 'pedestal' | 'pillar'
  variant?: 'AC' | 'DC'
}>()

const bodyColor = computed(() => (props.variant === 'DC' ? '#1e293b' : '#334155'))
const accentColor = computed(() => (props.variant === 'DC' ? '#ef4444' : '#22c55e'))
</script>
