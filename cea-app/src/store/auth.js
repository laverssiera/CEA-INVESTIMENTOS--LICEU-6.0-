import { reactive, computed } from 'vue'

const STORAGE_KEY = 'cea.auth'

function load() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : null
  } catch {
    return null
  }
}

function save(data) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(data))
}

const _state = load()

export const auth = reactive({
  token: _state?.token ?? null,
  role: _state?.role ?? null,
  name: _state?.name ?? null,
  investorType: _state?.investorType ?? 'PF',

  get isAuthenticated() {
    return !!this.token
  },

  setAuth({ token, role, name, investorType = 'PF' }) {
    this.token = token
    this.role = role
    this.name = name
    this.investorType = investorType
    save({ token, role, name, investorType })
  },

  logout() {
    this.token = null
    this.role = null
    this.name = null
    this.investorType = 'PF'
    localStorage.removeItem(STORAGE_KEY)
  },
})
