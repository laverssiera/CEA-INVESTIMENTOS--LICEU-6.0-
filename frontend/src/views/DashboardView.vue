<template>
  <div class="page">
    <section class="hero">
      <div>
        <p class="eyebrow">/investidor/dashboard</p>
        <h2>Dashboard do investidor com autenticação bancária e visão consolidada da carteira.</h2>
        <p>
          A experiência do cliente agora combina autenticação bancária, score de crédito,
          compliance, market realtime e inteligência de alocação baseada na LICEU 6.0.
        </p>
      </div>

      <div class="hero-grid">
        <div class="card">
          <small>Status da sessão</small>
          <div class="stat-value">{{ isAuthenticated ? 'Protegida' : 'Pendente' }}</div>
          <span class="tag info">{{ auth.state.userRole }}</span>
        </div>
        <div class="card">
          <small>MFA</small>
          <div class="stat-value">{{ auth.state.mfaRequired ? 'Aguardando' : 'Ativo' }}</div>
          <span class="tag warning">JWT + Refresh</span>
        </div>
      </div>
    </section>

    <section class="grid-2">
      <article class="panel">
        <small>Autenticação</small>
        <h3>Login → JWT → MFA</h3>

        <form v-if="!isAuthenticated && !auth.state.mfaRequired" class="form-grid" @submit.prevent="handleLogin">
          <label>
            Usuário
            <input v-model="loginForm.username" type="text" />
          </label>
          <label>
            Senha
            <input v-model="loginForm.password" type="password" />
          </label>
          <button class="primary-btn" type="submit" :disabled="auth.state.loading">
            {{ auth.state.loading ? 'Entrando...' : 'Fazer login' }}
          </button>
        </form>

        <form v-else-if="auth.state.mfaRequired" class="form-grid" @submit.prevent="handleVerifyMfa">
          <label>
            Código MFA
            <input v-model="loginForm.code" maxlength="6" type="text" />
          </label>
          <div class="card">
            <small>Demo</small>
            <p>Use o código <strong>246810</strong> para `investidor`.</p>
          </div>
          <button class="primary-btn" type="submit" :disabled="auth.state.loading">
            {{ auth.state.loading ? 'Validando...' : 'Validar MFA' }}
          </button>
        </form>

        <div v-else class="card">
          <p><strong>Usuário autenticado:</strong> {{ auth.state.userRole }}</p>
          <div class="actions">
            <button class="primary-btn" type="button" @click="handleRefresh">Renovar token</button>
            <button class="secondary-btn" type="button" @click="handleLogout">Sair</button>
          </div>
        </div>

        <p><strong>Credenciais demo:</strong> investidor / cea123</p>
        <p v-if="auth.state.error"><strong>Erro:</strong> {{ auth.state.error }}</p>
      </article>

      <MarketTicker :indicators="liveIndicators" />
    </section>

    <template v-if="isAuthenticated">
      <section class="grid-2">
        <PortfolioCard :summary="portfolio" />
        <LiquidityWidget :cashflow="cashflow" />
      </section>

      <section class="grid-3">
        <RiskScore :score-data="creditScore" />

        <article class="panel">
          <small>Decision Tree ML</small>
          <h3>Alocação sugerida pelo modelo</h3>
          <div class="stat-value">{{ mlDecision.allocation || 'N/D' }}</div>
          <p><strong>Expected yield:</strong> {{ mlDecision.expected_yield || '--' }}%</p>
          <p><strong>Confidence:</strong> {{ mlDecision.confidence || '--' }}</p>
        </article>

        <article class="panel">
          <small>Compliance & AML</small>
          <h3>Status da análise</h3>
          <div class="stat-value">{{ compliance.status || 'N/D' }}</div>
          <ul class="list">
            <li><strong>KYC:</strong> {{ compliance.checks?.kyc ? 'OK' : 'Pendente' }}</li>
            <li><strong>AML:</strong> {{ compliance.checks?.aml ? 'OK' : 'Revisão' }}</li>
            <li><strong>Suitability:</strong> {{ compliance.checks?.suitability || 'N/D' }}</li>
          </ul>
        </article>
      </section>

      <section class="grid-2">
        <YieldChart :series="portfolio.performance_series || []" />

        <article class="panel">
          <small>LICEU APIs</small>
          <h3>Dados operacionais usados nas decisões</h3>
          <ul class="list">
            <li><strong>Produção:</strong> {{ engineering.produced_m2 }} m²</li>
            <li><strong>Avanço da obra:</strong> {{ engineering.work_progress }}%</li>
            <li><strong>Produtividade:</strong> {{ analytics.productivity }}</li>
            <li><strong>Valuation:</strong> R$ {{ assets.valuation_brl }}</li>
          </ul>
        </article>
      </section>
    </template>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, reactive, ref } from 'vue'
import LiquidityWidget from '../components/LiquidityWidget.vue'
import MarketTicker from '../components/MarketTicker.vue'
import PortfolioCard from '../components/PortfolioCard.vue'
import RiskScore from '../components/RiskScore.vue'
import YieldChart from '../components/YieldChart.vue'
import {
  fetchAssetsProjects,
  fetchComplianceCheck,
  fetchCreditScore,
  fetchDashboardPortfolio,
  fetchDataAnalytics,
  fetchEngineeringProduction,
  fetchFinanceCashflow,
  fetchMarketIndicators,
  fetchMlDecision,
} from '../services/liceuApi'
import { useAuthStore } from '../store/auth'

const auth = useAuthStore()
const isAuthenticated = computed(() => auth.isAuthenticated.value)

const loginForm = reactive({
  username: 'investidor',
  password: 'cea123',
  code: '246810',
})

const portfolio = ref({})
const cashflow = ref({})
const creditScore = ref({})
const compliance = ref({})
const mlDecision = ref({})
const engineering = ref({})
const analytics = ref({})
const assets = ref({})
const liveIndicators = ref({ cdi: 13.45, selic: 13.75, dolar: 5.18, liquidez: 'Alta' })

let socket

const loadDashboard = async () => {
  if (!isAuthenticated.value) return

  const [portfolioData, financeData, creditData, complianceData, mlData, engineeringData, analyticsData, assetsData] =
    await Promise.all([
      fetchDashboardPortfolio(),
      fetchFinanceCashflow(),
      fetchCreditScore({
        investment_history: 86,
        liquidity_work: 88,
        engineering_productivity: 92,
        project_risk: 20,
        project_term_days: 45,
      }),
      fetchComplianceCheck({
        investor_name: 'Investidor Demo',
        investment_amount: 250000,
        kyc_completed: true,
        aml_flag: false,
        suitability_profile: 'moderado',
      }),
      fetchMlDecision({
        project_term_days: 45,
        interest_rate: 13.75,
        cash_balance: 12400000,
        risk_index: 35,
      }),
      fetchEngineeringProduction(),
      fetchDataAnalytics(),
      fetchAssetsProjects(),
    ])

  portfolio.value = portfolioData
  cashflow.value = financeData
  creditScore.value = creditData
  compliance.value = complianceData
  mlDecision.value = mlData
  engineering.value = engineeringData
  analytics.value = analyticsData
  assets.value = assetsData
}

const handleLogin = async () => {
  await auth.login(loginForm.username, loginForm.password)
}

const handleVerifyMfa = async () => {
  await auth.verifyMfa(loginForm.code)
  await loadDashboard()
}

const handleRefresh = async () => {
  await auth.refreshSession()
}

const handleLogout = () => {
  auth.logout()
}

const connectSocket = () => {
  socket = new WebSocket('ws://localhost:8000/ws/market')
  socket.onmessage = (event) => {
    const payload = JSON.parse(event.data)
    liveIndicators.value = payload.indicators
  }
}

onMounted(async () => {
  try {
    const market = await fetchMarketIndicators()
    liveIndicators.value = market.indicators
  } catch (error) {
    console.error(error)
  }

  connectSocket()

  if (isAuthenticated.value) {
    await loadDashboard()
  }
})

onBeforeUnmount(() => socket?.close())
</script>
