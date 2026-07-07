import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

type ThemePreset = 'aura' | 'lara' | 'nora' | 'material'
type ColorScheme = 'light' | 'dark'

export const useThemeStore = defineStore('theme', () => {
  // State
  const preset = ref<ThemePreset>('aura')
  const colorScheme = ref<ColorScheme>('light')

  // Getters
  const isDark = computed(() => colorScheme.value === 'dark')
  const currentPreset = computed(() => preset.value)

  // Actions
  function setPreset(newPreset: ThemePreset) {
    preset.value = newPreset
    persist()
    applyTheme()
  }

  function toggleColorScheme() {
    colorScheme.value = colorScheme.value === 'light' ? 'dark' : 'light'
    persist()
    applyTheme()
  }

  function setColorScheme(scheme: ColorScheme) {
    colorScheme.value = scheme
    persist()
    applyTheme()
  }

  function applyTheme() {
    const html = document.documentElement
    if (colorScheme.value === 'dark') {
      html.classList.add('my-app-dark')
    } else {
      html.classList.remove('my-app-dark')
    }
  }

  function persist() {
    localStorage.setItem('ptd-theme-preset', preset.value)
    localStorage.setItem('ptd-theme-scheme', colorScheme.value)
  }

  function load() {
    try {
      const savedPreset = localStorage.getItem('ptd-theme-preset') as ThemePreset | null
      const savedScheme = localStorage.getItem('ptd-theme-scheme') as ColorScheme | null
      if (savedPreset && ['aura', 'lara', 'nora', 'material'].includes(savedPreset)) {
        preset.value = savedPreset
      }
      if (savedScheme && ['light', 'dark'].includes(savedScheme)) {
        colorScheme.value = savedScheme
      }
      applyTheme()
    } catch {
      // Ignore
    }
  }

  // Load on init
  load()

  return {
    preset,
    colorScheme,
    isDark,
    currentPreset,
    setPreset,
    toggleColorScheme,
    setColorScheme,
    applyTheme,
  }
})
