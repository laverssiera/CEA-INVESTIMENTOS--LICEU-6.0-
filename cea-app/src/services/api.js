const BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function getToken() {
  try {
    const raw = localStorage.getItem('cea.auth')
    return raw ? JSON.parse(raw).token : null
  } catch {
    return null
  }
}

async function request(method, path, body) {
  const token = getToken()
  const headers = { 'Content-Type': 'application/json' }
  if (token) headers['Authorization'] = `Bearer ${token}`

  const res = await fetch(`${BASE}${path}`, {
    method,
    headers,
    body: body !== undefined ? JSON.stringify(body) : undefined,
  })

  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || `Erro ${res.status}`)
  }
  return res.json()
}

const get = (path) => request('GET', path)
const post = (path, body) => request('POST', path, body)

// ── Autenticação ─────────────────────────────────────────────────────────────
export const loginApi = (username, password) =>
  post('/auth/login', { username, password })

export const verifyMfa = (challengeId, code) =>
  post('/auth/mfa/verify', { challenge_id: challengeId, code })

export const refreshToken = (token) =>
  post('/auth/refresh', { refresh_token: token })

// ── Investidor ────────────────────────────────────────────────────────────────
export const fetchPortfolio = () => get('/api/dashboard/portfolio')
export const fetchMissionPortfolio = () => get('/interplanetary/portfolio/')
export const fetchPositions = () => get('/api/investments/positions')
export const fetchProducts = () => get('/api/investments/products')
export const signupInvestor = (data) => post('/api/investor/signup', data)
export const submitKyc = (data) => post('/api/investor/kyc', data)
export const submitSuitability = (data) => post('/api/investor/suitability', data)
export const fetchSuitability = () => get('/api/investor/suitability')

// ── Integração CEA / LICEU / Cognição ──────────────────────────────────────────
export const ceaApi = {
  // LICEU & Projetos
  ingestProject: (data) => post('/api/cea/project/ingest', data),
  updateProject: (data) => post('/api/cea/project/update', data),
  getProjectStatus: (id) => get(`/api/cea/project/${id}/status`),
  fundingProject: (data) => post('/api/cea/project/funding', data),
  syncLiceu: (data) => post('/api/cea/liceu/sync', data),

  // Cognição (John Monolith)
  cognitionIngest: (data) => post('/api/cea/john/ingest', data),
  cognitionDecision: (data) => post('/api/cea/john/decision', data),
  cognitionContext: (data) => post('/api/cea/john/context', data),
  cognitionHealth: () => get('/api/cea/john/health'),

  // Inteligência Financeira
  analyzeInvestment: (data) => post('/api/cea/investment/analyze', data),
  evaluateCredit: (data) => post('/api/cea/credit/evaluate', data),
}

// ── Suporte ───────────────────────────────────────────────────────────────────
export const submitSupportTicket = ({ subject, message, email }) =>
  post('/api/support/tickets', { subject, message, email })

// ── PIX ───────────────────────────────────────────────────────────────────────
export const createPixCharge = ({ amount, userId = 'demo', description }) =>
  post('/api/pix/create', { amount, user_id: userId, description })

export const getPixStatus = (txid) => get(`/api/pix/status/${txid}`)

// ── Carteira ──────────────────────────────────────────────────────────────────
export const fetchWalletBalance = () => get('/api/wallet/balance')

/**
 * Conecta ao WebSocket de atualizacoes da carteira.
 * Retorna a instancia WebSocket para que o caller possa fechar.
 * @param {string} userId
 * @param {(data: object) => void} onMessage
 */
export function connectWalletSocket(userId, onMessage) {
  const wsBase = (import.meta.env.VITE_API_URL || 'http://localhost:8000')
    .replace(/^http/, 'ws')
  const ws = new WebSocket(`${wsBase}/ws/wallet/${userId}`)
  ws.onmessage = (e) => {
    try { onMessage(JSON.parse(e.data)) } catch { /* ignore */ }
  }
  return ws
}

// ── Saque PIX ─────────────────────────────────────────────────────────────────
export const pixWithdraw = ({ amount, userId, pixKey, keyType, mfaCode }) =>
  post('/api/pix/withdraw', {
    amount,
    user_id: userId,
    pix_key: pixKey,
    key_type: keyType,
    mfa_code: mfaCode,
  })

export const fetchWithdrawals = () => get('/api/pix/withdrawals')
export const fetchPendingWithdrawals = () => get('/api/pix/withdrawals/pending')
export const approvePixWithdraw = (wid) => post(`/api/pix/withdraw/approve/${wid}`)
export const rejectPixWithdraw = (wid) => post(`/api/pix/withdraw/reject/${wid}`)
export const runPixReconcile = () => post('/api/pix/reconcile')
export const fetchPixReconcileStatus = () => get('/api/pix/reconcile/status')
export const fetchPixAudit = () => get('/api/pix/audit')
export const fetchPixKpis = () => get('/api/pix/kpis')

// ── Conta Digital ─────────────────────────────────────────────────────────────
export const fetchAccountDetails = () => get('/api/account/details')
export const fetchAccountStatement = () => get('/api/account/statement')

// ── Split ─────────────────────────────────────────────────────────────────────
export const executeProjectSplit = (data) => post('/api/projects/split', data)
export const fetchProjectSplits = () => get('/api/projects/splits')

// ── Rendimentos ───────────────────────────────────────────────────────────────
export const fetchYieldPayments = () => get('/api/yields/payments')
export const fetchYieldSchedules = () => get('/api/yields/schedules')
export const createYieldSchedule = (data) => post('/api/yields/schedule', data)
export const triggerYieldPayment = (scheduleId) => post('/api/yields/pay', { schedule_id: scheduleId })

// ── Contratos Digitais ───────────────────────────────────────────────────────
export const createContract = (data) => post('/api/contracts/create', data)
export const signContract = (contractId, signatureToken) =>
  post('/api/contracts/sign', { contract_id: contractId, signature_token: signatureToken })
export const fetchContracts = () => get('/api/contracts')
export const fetchContractById = (contractId) => get(`/api/contracts/${contractId}`)

// ── Tokenização ──────────────────────────────────────────────────────────────
export const createTokenAsset = (data) => post('/api/tokens/create', data)
export const fetchTokenMarket = () => get('/api/tokens/market')
export const buyToken = (tokenId, quantity) => post('/api/tokens/buy', { token_id: tokenId, quantity })
export const fetchTokenPortfolio = () => get('/api/tokens/portfolio')

// ── Wallet Interna ───────────────────────────────────────────────────────────
export const walletTransfer = (data) => post('/api/wallet/transfer', data)
export const fetchWalletTransfers = () => get('/api/wallet/transfers')

// ── Marketplace ──────────────────────────────────────────────────────────────
export const fetchMarketplaceProjects = () => get('/api/marketplace/projects')
export const createMarketplaceProject = (data) => post('/api/marketplace/projects', data)
export const investMarketplaceProject = (projectId, amount) =>
  post('/api/marketplace/invest', { project_id: projectId, amount })
export const fetchMarketplaceOrders = () => get('/api/marketplace/orders')

