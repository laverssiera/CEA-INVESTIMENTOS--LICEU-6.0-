import { computed, ref } from 'vue'

const STORAGE_KEY = 'cea.institutional.dark'
const isDarkMode = ref(false)
let initialized = false

const readSystemPreference = () => {
  if (typeof window === 'undefined' || typeof window.matchMedia !== 'function') return false
  return window.matchMedia('(prefers-color-scheme: dark)').matches
}

const initializeTheme = () => {
  if (initialized || typeof window === 'undefined') return

  const saved = window.localStorage.getItem(STORAGE_KEY)
  if (saved === 'true' || saved === 'false') {
    isDarkMode.value = saved === 'true'
  } else {
    isDarkMode.value = readSystemPreference()
  }

  initialized = true
}

const setDarkMode = (value) => {
  isDarkMode.value = Boolean(value)
  if (typeof window !== 'undefined') {
    window.localStorage.setItem(STORAGE_KEY, String(isDarkMode.value))
  }
}

const toggleDarkMode = () => {
  setDarkMode(!isDarkMode.value)
}

export const useInstitutionalTheme = () => {
  initializeTheme()

  return {
    isDarkMode,
    isLightMode: computed(() => !isDarkMode.value),
    setDarkMode,
    toggleDarkMode,
  }
}
