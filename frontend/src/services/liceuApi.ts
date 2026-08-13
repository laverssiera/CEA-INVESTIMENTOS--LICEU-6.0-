import axios, { type InternalAxiosRequestConfig } from 'axios'

const ACCESS_TOKEN_KEY = 'cea.accessToken'
type ApiPayload = Record<string, unknown>

export const liceuApi = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  timeout: 10000,
})

/**
 * Integração com o Monólito CEA e Gateway Cognitivo
 */
export const ceaApi = {
  // LICEU (Projetos e Sync)
  projects: {
    ingest: async (payload: ApiPayload) => (await liceuApi.post('/cea/project/ingest', payload)).data,
    update: async (payload: ApiPayload) => (await liceuApi.post('/cea/project/update', payload)).data,
    status: async (id: string) => (await liceuApi.get(`/cea/project/${id}/status`)).data,
    funding: async (payload: ApiPayload) => (await liceuApi.post('/cea/project/funding', payload)).data,
    sync: async (payload: ApiPayload) => (await liceuApi.post('/cea/liceu/sync', payload)).data,
  },
  // John Monolith / Cognition
  cognition: {
    ingest: async (payload: ApiPayload) => (await liceuApi.post('/cea/john/ingest', payload)).data,
    decision: async (payload: ApiPayload) => (await liceuApi.post('/cea/john/decision', payload)).data,
    context: async (payload: ApiPayload) => (await liceuApi.post('/cea/john/context', payload)).data,
    health: async () => (await liceuApi.get('/cea/john/health')).data,
  },
  // Finanças e Crédito
  finance: {
    analyze: async (payload: ApiPayload) => (await liceuApi.post('/cea/investment/analyze', payload)).data,
    evaluateCredit: async (payload: ApiPayload) => (await liceuApi.post('/cea/credit/evaluate', payload)).data,
  }
}

export const authApi = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  timeout: 10000,
})

let accessToken = typeof window !== 'undefined' ? localStorage.getItem(ACCESS_TOKEN_KEY) || '' : ''

export const setAccessToken = (token = '') => {
  accessToken = token

  if (typeof window === 'undefined') return

  if (token) {
    localStorage.setItem(ACCESS_TOKEN_KEY, token)
  } else {
    localStorage.removeItem(ACCESS_TOKEN_KEY)
  }
}

const attachToken = (config: InternalAxiosRequestConfig) => {
  if (accessToken) {
    config.headers = config.headers || {}
    config.headers.Authorization = `Bearer ${accessToken}`
  }
  return config
}

liceuApi.interceptors.request.use(attachToken)
authApi.interceptors.request.use(attachToken)

export const fetchEngineeringProduction = async () => (await liceuApi.get('/engineering/production')).data
export const fetchFinanceCashflow = async () => (await liceuApi.get('/finance/cashflow')).data
export const fetchAssetsProjects = async () => (await liceuApi.get('/assets/projects')).data
export const fetchDataAnalytics = async () => (await liceuApi.get('/data/analytics')).data
export const fetchLiceuOverview = async () => (await liceuApi.get('/liceu/overview')).data
export const fetchMarketIndicators = async () => (await liceuApi.get('/market/indicators')).data
export const fetchMarketRecommendation = async () => (await liceuApi.get('/market/recommendation')).data
export const fetchMarketAlerts = async () => (await liceuApi.get('/market/alerts')).data
export const fetchSecurityPosture = async () => (await liceuApi.get('/security/posture')).data
export const simulateMarketAllocation = async (payload: ApiPayload) => (await liceuApi.post('/market/simulate', payload)).data
export const fetchDashboardPortfolio = async () => (await liceuApi.get('/dashboard/portfolio')).data
export const fetchGovernanceDashboard = async () => (await liceuApi.get('/governance/dashboard')).data
export const fetchCreditCommittee = async () => (await liceuApi.get('/credit/committee')).data
export const fetchRbacMatrix = async () => (await liceuApi.get('/security/rbac-matrix')).data
export const fetchAutomationSchedules = async () => (await liceuApi.get('/jobs/schedules')).data
export const fetchOrchestrationJobs = async () => (await liceuApi.get('/orchestration/jobs')).data
export const runOrchestrationJob = async (jobName: string) => (await liceuApi.post(`/orchestration/run/${jobName}`)).data
export const fetchOrchestrationLogs = async () => (await liceuApi.get('/orchestration/logs')).data
export const fetchOrchestrationEvents = async () => (await liceuApi.get('/orchestration/events')).data
export const fetchNotificationLogs = async () => (await liceuApi.get('/notifications/logs')).data
export const fetchDocumentLogs = async () => (await liceuApi.get('/documents/logs')).data
export const fetchCreditScore = async (payload: ApiPayload) => (await liceuApi.post('/credit/score', payload)).data
export const fetchCreditScorePreview = async () => (await liceuApi.get('/credit/score')).data
export const fetchComplianceCheck = async (payload: ApiPayload) => (await liceuApi.post('/compliance/check', payload)).data
export const fetchMlDecision = async (payload: ApiPayload) => (await authApi.post('/ml/decision', payload)).data

export const fetchInterplanetaryEcosystem = async () =>
  (await authApi.get('/interplanetary/ecosystem')).data

export const activateInterplanetaryDomain = async (domainId: string) =>
  (await authApi.post(`/interplanetary/ecosystem/${domainId}/activate`)).data

export const submitFinancingRequest = async (payload: ApiPayload) =>
  (await liceuApi.post('/financing/request', payload)).data

export const submitCareersApplication = async (payload: ApiPayload) =>
  (await liceuApi.post('/careers/apply', payload)).data

export const loginRequest = async (username: string, password: string) => {
  const { data } = await authApi.post('/auth/login', { username, password })
  return data
}

export const verifyMfaRequest = async (challengeId: string, code: string) => {
  const { data } = await authApi.post('/auth/mfa/verify', {
    challenge_id: challengeId,
    code,
  })

  if (data.access_token) {
    setAccessToken(data.access_token)
  }

  return data
}

export const refreshTokenRequest = async (refreshToken: string) => {
  const { data } = await authApi.post('/auth/refresh', {
    refresh_token: refreshToken,
  })

  if (data.access_token) {
    setAccessToken(data.access_token)
  }

  return data
}
