import { computed, reactive } from 'vue'
import { loginRequest, refreshTokenRequest, setAccessToken, verifyMfaRequest } from '../services/liceuApi'

const REFRESH_TOKEN_KEY = 'cea.refreshToken'
const USER_ROLE_KEY = 'cea.userRole'

const state = reactive({
  token: typeof window !== 'undefined' ? localStorage.getItem('cea.accessToken') || '' : '',
  refreshToken: typeof window !== 'undefined' ? localStorage.getItem(REFRESH_TOKEN_KEY) || '' : '',
  mfaRequired: false,
  userRole: typeof window !== 'undefined' ? localStorage.getItem(USER_ROLE_KEY) || 'guest' : 'guest',
  challengeId: '',
  userName: '',
  loading: false,
  error: '',
})

const persistState = () => {
  if (typeof window === 'undefined') return

  setAccessToken(state.token)

  if (state.refreshToken) {
    localStorage.setItem(REFRESH_TOKEN_KEY, state.refreshToken)
  } else {
    localStorage.removeItem(REFRESH_TOKEN_KEY)
  }

  if (state.userRole) {
    localStorage.setItem(USER_ROLE_KEY, state.userRole)
  } else {
    localStorage.removeItem(USER_ROLE_KEY)
  }
}

export const useAuthStore = () => {
  const isAuthenticated = computed(() => Boolean(state.token))

  const login = async (username: string, password: string) => {
    state.loading = true
    state.error = ''

    try {
      const response = await loginRequest(username, password)
      state.userName = username
      state.userRole = response.user_role || 'investidor'
      state.challengeId = response.challenge_id || ''
      state.mfaRequired = Boolean(response.mfa_required)
      persistState()
      return response
    } catch (error: any) {
      state.error = error?.response?.data?.detail || 'Falha no login'
      throw error
    } finally {
      state.loading = false
    }
  }

  const verifyMfa = async (code: string) => {
    state.loading = true
    state.error = ''

    try {
      const response = await verifyMfaRequest(state.challengeId, code)
      state.token = response.access_token || ''
      state.refreshToken = response.refresh_token || ''
      state.userRole = response.role || state.userRole
      state.mfaRequired = false
      state.challengeId = ''
      persistState()
      return response
    } catch (error: any) {
      state.error = error?.response?.data?.detail || 'Falha na verificação MFA'
      throw error
    } finally {
      state.loading = false
    }
  }

  const refreshSession = async () => {
    if (!state.refreshToken) return null

    state.loading = true
    state.error = ''
    try {
      const response = await refreshTokenRequest(state.refreshToken)
      state.token = response.access_token || state.token
      persistState()
      return response
    } catch (error: any) {
      state.error = error?.response?.data?.detail || 'Não foi possível renovar a sessão'
      logout()
      throw error
    } finally {
      state.loading = false
    }
  }

  const logout = () => {
    state.token = ''
    state.refreshToken = ''
    state.mfaRequired = false
    state.userRole = 'guest'
    state.challengeId = ''
    state.error = ''
    persistState()
  }

  return {
    state,
    isAuthenticated,
    login,
    verifyMfa,
    refreshSession,
    logout,
  }
}
