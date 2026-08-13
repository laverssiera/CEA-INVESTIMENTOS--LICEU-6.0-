<template>
  <div class="continental-dashboard">
    <header class="hero-panel">
      <div>
        <p class="eyebrow">CEA / LICEU / CONTINENTAL</p>
        <h1>Dashboard Continental de Investimentos</h1>
        <p class="subtitle">
          JOHN decide, ECONOTECH calcula o impacto, CEA aloca capital e LICEU governa o processo.
        </p>
      </div>
      <div class="hero-actions">
        <div class="status-badge" :class="dashboard.overview.status">
          {{ dashboard.overview.status === 'approved' ? 'Aprovado' : dashboard.overview.status }}
        </div>
        <button class="refresh-button" type="button" :disabled="isLoading" @click="loadDashboard">
          {{ isLoading ? 'Atualizando...' : 'Atualizar dados' }}
        </button>
      </div>
    </header>

    <p class="connection-status" :class="dataSource" role="status" aria-live="polite">
      <span class="connection-indicator"></span>
      {{ connectionMessage }}
    </p>

    <section class="kpi-grid">
      <article v-for="item in KPI_ITEMS" :key="item.label" class="kpi-card">
        <span>{{ item.label }}</span>
        <strong>{{ item.value }}</strong>
      </article>
    </section>

    <section class="panel-grid two-columns">
      <article class="panel">
        <h2>Decisão estratégica</h2>
        <div class="decision-row">
          <span class="tag">{{ dashboard.decision.decision }}</span>
          <span>Owner: {{ dashboard.decision.decision_owner }}</span>
        </div>
        <p class="metric-line"><strong>Score:</strong> {{ dashboard.decision.decision_score }}</p>
        <p class="metric-line"><strong>Governança:</strong> {{ dashboard.decision.governance }}</p>
        <p class="summary">{{ dashboard.decision.summary }}</p>
      </article>

      <article class="panel">
        <h2>Risco</h2>
        <p class="metric-line"><strong>Score:</strong> {{ dashboard.risk.score }}</p>
        <p class="metric-line"><strong>Classificação:</strong> {{ dashboard.risk.classification }}</p>
        <p class="metric-line"><strong>Confiança:</strong> {{ dashboard.risk.confidence_interval.join(' - ') }}</p>
        <p class="metric-line"><strong>Owner:</strong> {{ dashboard.risk.decision_owner }}</p>
      </article>
    </section>

    <section class="panel-grid two-columns">
      <article class="panel">
        <h2>Alocação por categoria</h2>
        <div class="bar-list">
          <div v-for="row in dashboard.allocation.allocations" :key="row.category" class="bar-row">
            <div class="bar-header">
              <span>{{ row.category }}</span>
              <strong>{{ row.percentage * 100 }}%</strong>
            </div>
            <div class="bar-track">
              <div class="bar-fill" :style="{ width: `${row.percentage * 100}%` }"></div>
            </div>
            <small>{{ formatCurrency(row.amount) }}</small>
          </div>
        </div>
      </article>

      <article class="panel">
        <h2>Impacto financeiro</h2>
        <p class="metric-line"><strong>NPV:</strong> {{ formatCurrency(dashboard.finance.npv) }}</p>
        <p class="metric-line"><strong>IRR:</strong> {{ dashboard.finance.irr }}</p>
        <p class="metric-line"><strong>Payback:</strong> {{ dashboard.finance.payback_period }} anos</p>
        <p class="metric-line"><strong>ROI:</strong> {{ dashboard.finance.roi }}</p>
        <p class="metric-line"><strong>Owner:</strong> {{ dashboard.finance.owner }}</p>
      </article>
    </section>

    <section class="panel-grid two-columns">
      <article class="panel">
        <h2>Portfólio continental</h2>
        <div class="portfolio-summary">
          <span>Valor inicial</span>
          <strong>{{ formatCurrency(dashboard.portfolio.total_initial_value) }}</strong>
        </div>
        <ul class="country-list">
          <li v-for="(value, country) in dashboard.portfolio.by_country" :key="country">
            <span>{{ country }}</span>
            <strong>{{ formatCurrency(value) }}</strong>
          </li>
        </ul>
      </article>

      <article class="panel">
        <h2>Dados para gráficos</h2>
        <div class="mini-chart" v-for="item in dashboard.chart_data.allocation_by_category" :key="item.category">
          <div class="mini-chart-label">
            <span>{{ item.category }}</span>
            <strong>{{ item.value }}%</strong>
          </div>
          <div class="mini-track">
            <div class="mini-fill" :style="{ width: `${item.value}%` }"></div>
          </div>
        </div>
      </article>
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import api from '../services/api'

const fallbackDashboard = {
  overview: {
    status: 'approved',
    decision_owner: 'John',
    governance: 'LICEU',
    region: 'Continental',
    summary: 'JOHN decide, ECONOTECH calcula o impacto, CEA aloca capital e LICEU governa.'
  },
  kpis: {
    decision_score: 0.81,
    risk_score: 0.62,
    roi: 1.42,
    npv: 13234443.42,
    total_capital: 100000000,
    total_initial_value: 100000000
  },
  decision: {
    decision: 'approve',
    decision_owner: 'John',
    governance: 'LICEU',
    decision_score: 0.81,
    summary: 'JOHN decide pela aprovação, revisão ou deferimento com governança LICEU.'
  },
  allocation: {
    total_capital: 100000000,
    risk_profile: 'Moderate',
    region: 'Continental',
    decision_owner: 'CEA',
    governance: 'LICEU',
    allocations: [
      { category: 'Fixed Income', percentage: 0.5, amount: 50000000.0 },
      { category: 'Infrastructure', percentage: 0.3, amount: 30000000.0 },
      { category: 'Alternative', percentage: 0.2, amount: 20000000.0 }
    ]
  },
  portfolio: {
    portfolio_id: 'ceda1b25-9f0d-4bc6-9d0f-9c3f6c936e7e',
    owner_id: 'cea-continental-01',
    region: 'Continental',
    status: 'active',
    decision_owner: 'CEA',
    governance: 'LICEU',
    total_initial_value: 100000000.0,
    by_country: {
      BR: 32000000,
      CL: 24000000,
      AR: 18000000,
      PE: 26000000
    }
  },
  finance: {
    npv: 13234443.42,
    irr: 0.2474,
    payback_period: 3,
    total_return: 121000000.0,
    roi: 1.42,
    owner: 'ECONOTECH',
    governance: 'LICEU',
    decision_owner: 'John'
  },
  risk: {
    score: 0.62,
    classification: 'Medium',
    confidence_interval: [0.57, 0.67],
    decision_owner: 'John',
    governance: 'LICEU'
  },
  chart_data: {
    allocation_by_category: [
      { category: 'Fixed Income', value: 50 },
      { category: 'Infrastructure', value: 30 },
      { category: 'Alternative', value: 20 }
    ]
  }
}

const dashboard = ref({ ...fallbackDashboard })
const isLoading = ref(false)
const dataSource = ref('loading')
const lastUpdatedAt = ref(null)

const connectionMessage = computed(() => {
  if (isLoading.value) return 'Atualizando dados da decisão continental...'
  if (dataSource.value === 'fallback') return 'Dados de contingência exibidos: a API continental está indisponível.'
  if (!lastUpdatedAt.value) return 'Aguardando a primeira atualização.'

  return `Dados reais atualizados às ${lastUpdatedAt.value.toLocaleTimeString('pt-BR', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  })}.`
})

const buildDashboard = (payload) => {
  const decision = payload.decision || {}
  const allocation = payload.allocation || {}
  const portfolio = payload.portfolio || {}
  const finance = payload.finance || {}
  const risk = payload.risk || {}

  const byCountry = portfolio.by_country || Object.fromEntries(
    (portfolio.assets || []).map((asset) => [asset.country, (asset.value || 0)]),
  )

  const summary = {
    overview: {
      status: decision.decision === 'approve' ? 'approved' : 'review',
      decision_owner: decision.decision_owner || 'John',
      governance: decision.governance || 'LICEU',
      region: allocation.region || 'Continental',
      summary: 'JOHN decide, ECONOTECH calcula o impacto, CEA aloca capital e LICEU governa.'
    },
    kpis: {
      decision_score: decision.decision_score || 0.81,
      risk_score: risk.score || 0.62,
      roi: finance.roi || 1.42,
      npv: finance.npv || 13234443.42,
      total_capital: allocation.total_capital || 100000000,
      total_initial_value: portfolio.total_initial_value || 100000000,
    },
    decision: {
      decision: decision.decision || 'approve',
      decision_owner: decision.decision_owner || 'John',
      governance: decision.governance || 'LICEU',
      decision_score: decision.decision_score || 0.81,
      summary: decision.summary || 'JOHN decide pela aprovação, revisão ou deferimento com governança LICEU.'
    },
    allocation: {
      total_capital: allocation.total_capital || 100000000,
      risk_profile: allocation.risk_profile || 'Moderate',
      region: allocation.region || 'Continental',
      decision_owner: allocation.decision_owner || 'CEA',
      governance: allocation.governance || 'LICEU',
      allocations: allocation.allocations || fallbackDashboard.allocation.allocations,
    },
    portfolio: {
      portfolio_id: portfolio.portfolio_id || 'continental-live',
      owner_id: portfolio.owner_id || 'cea-continental-01',
      region: portfolio.region || 'Continental',
      status: portfolio.status || 'active',
      decision_owner: portfolio.decision_owner || 'CEA',
      governance: portfolio.governance || 'LICEU',
      total_initial_value: portfolio.total_initial_value || 100000000.0,
      by_country: byCountry,
      assets: portfolio.assets || fallbackDashboard.portfolio.assets,
    },
    finance: {
      npv: finance.npv || 13234443.42,
      irr: finance.irr || 0.2474,
      payback_period: finance.payback_period || 3,
      total_return: finance.total_return || 121000000.0,
      roi: finance.roi || 1.42,
      owner: finance.owner || 'ECONOTECH',
      governance: finance.governance || 'LICEU',
      decision_owner: finance.decision_owner || 'John',
    },
    risk: {
      score: risk.score || 0.62,
      classification: risk.classification || 'Medium',
      confidence_interval: risk.confidence_interval || [0.57, 0.67],
      decision_owner: risk.decision_owner || 'John',
      governance: risk.governance || 'LICEU',
    },
    chart_data: {
      allocation_by_category: (allocation.allocations || fallbackDashboard.allocation.allocations).map((row) => ({
        category: row.category,
        value: Math.round((Number(row.percentage) || 0) * 100),
      })),
    },
  }

  return summary
}

const loadDashboard = async () => {
  isLoading.value = true
  dataSource.value = 'loading'

  try {
    const requestData = {
      project: {
        name: 'Continental Grid',
        location: 'South America',
        project_type: 'infraestrutura',
        strategic_importance: 0.82,
        budget: 25000000,
        complexity: 7,
      },
      market_signal: {
        risk_score: 0.32,
        economic_impact: 0.88,
        region: 'Continental',
      },
      capital_allocation: {
        total_capital: 100000000,
        risk_profile: 'Moderate',
        region: 'Continental',
      },
      portfolio: {
        owner_id: 'cea-continental-01',
        region: 'Continental',
        assets: [
          { asset_id: 'C-PORT-001', value: 32000000, segment: 'infraestrutura', country: 'BR' },
          { asset_id: 'C-PORT-002', value: 24000000, segment: 'mercados', country: 'CL' },
          { asset_id: 'C-PORT-003', value: 18000000, segment: 'fundos', country: 'AR' },
          { asset_id: 'C-PORT-004', value: 26000000, segment: 'governos', country: 'PE' },
        ],
      },
      project_finance: {
        cash_flows: [-50000000, 18000000, 20000000, 22000000, 24000000, 25000000],
        discount_rate: 0.1,
      },
      risk: {
        location: 'South America',
        complexity: 7,
        budget: 25000000,
      },
    }

    const [decision, allocation, portfolio, finance, risk] = await Promise.all([
      api.post('/api/john/cea/continental/decision', {
        project: requestData.project,
        market_signal: requestData.market_signal,
      }),
      api.post('/api/john/cea/continental/allocate', requestData.capital_allocation),
      api.post('/api/john/cea/continental/portfolio', requestData.portfolio),
      api.post('/api/john/cea/continental/finance', requestData.project_finance),
      api.post('/api/john/cea/continental/risk', requestData.risk),
    ])

    const coalition = {
      decision: decision.data?.result || decision.data,
      allocation: allocation.data?.result || allocation.data,
      portfolio: portfolio.data?.result || portfolio.data,
      finance: finance.data?.result || finance.data,
      risk: risk.data?.result || risk.data,
    }

    dashboard.value = buildDashboard(coalition)
    dataSource.value = 'live'
    lastUpdatedAt.value = new Date()
  } catch (error) {
    console.warn('Continental dashboard fallback activated:', error)
    dashboard.value = fallbackDashboard
    dataSource.value = 'fallback'
  } finally {
    isLoading.value = false
  }
}

const KPI_ITEMS = computed(() => [
  { label: 'Decision score', value: dashboard.value.kpis.decision_score },
  { label: 'Risk score', value: dashboard.value.kpis.risk_score },
  { label: 'ROI', value: `${dashboard.value.kpis.roi}` },
  { label: 'NPV', value: formatCurrency(dashboard.value.kpis.npv) },
  { label: 'Capital', value: formatCurrency(dashboard.value.kpis.total_capital) },
])

onMounted(() => {
  loadDashboard()
})

function formatCurrency(value) {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
    maximumFractionDigits: 2,
  }).format(Number(value))
}
</script>

<style scoped>
.continental-dashboard {
  width: min(1200px, calc(100% - 32px));
  margin: 32px auto 56px;
  color: #112033;
}

.hero-panel {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  align-items: center;
  background: linear-gradient(135deg, #0f172a, #183850);
  color: white;
  border-radius: 22px;
  padding: 28px 32px;
  box-shadow: 0 18px 40px rgba(15, 23, 42, 0.18);
}

.eyebrow {
  margin: 0 0 8px;
  font-size: 0.76rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  opacity: 0.8;
  text-transform: uppercase;
}

.hero-panel h1 {
  margin: 0;
  font-size: clamp(2rem, 2.8vw, 3rem);
}

.subtitle {
  margin: 12px 0 0;
  max-width: 700px;
  line-height: 1.5;
  color: rgba(255,255,255,0.82);
}

.status-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 110px;
  height: 42px;
  padding: 0 18px;
  border-radius: 999px;
  background: rgba(255,255,255,0.12);
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.status-badge.approved {
  background: rgba(47, 204, 114, 0.2);
  color: #b9f7d4;
}

.hero-actions {
  display: grid;
  justify-items: end;
  gap: 10px;
}

.refresh-button {
  min-height: 38px;
  padding: 0 14px;
  border: 1px solid rgba(255, 255, 255, 0.45);
  border-radius: 6px;
  background: transparent;
  color: #fff;
  cursor: pointer;
  font: inherit;
  font-weight: 700;
}

.refresh-button:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.12);
}

.refresh-button:disabled {
  cursor: wait;
  opacity: 0.65;
}

.connection-status {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 14px 0 0;
  color: #446071;
  font-size: 0.9rem;
}

.connection-status.fallback {
  color: #9a5b12;
}

.connection-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #1b8d5c;
}

.connection-status.loading .connection-indicator {
  background: #1677a7;
  animation: status-pulse 1s ease-in-out infinite;
}

.connection-status.fallback .connection-indicator {
  background: #b26b12;
}

@keyframes status-pulse {
  50% { opacity: 0.35; }
}

.kpi-grid {
  margin-top: 24px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px;
}

.kpi-card,
.panel {
  background: rgba(255,255,255,0.94);
  border: 1px solid #e3eaf3;
  border-radius: 18px;
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.04);
}

.kpi-card {
  padding: 18px 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.kpi-card span {
  color: #4d6480;
  font-size: 0.82rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.kpi-card strong {
  font-size: clamp(1.2rem, 2vw, 1.8rem);
  color: #10233f;
}

.panel-grid {
  margin-top: 20px;
  display: grid;
  gap: 20px;
}

.two-columns {
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
}

.panel {
  padding: 22px 20px;
}

.panel h2 {
  margin: 0 0 18px;
  font-size: 1.2rem;
}

.decision-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
  font-weight: 600;
}

.tag {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 6px 12px;
  border-radius: 999px;
  background: #e8f5ee;
  color: #1d7b4f;
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
}

.metric-line {
  margin: 8px 0;
  color: #1b2d3d;
}

.summary {
  margin-top: 16px;
  line-height: 1.6;
  color: #42516c;
}

.bar-list {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.bar-row {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.bar-header {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  font-size: 0.9rem;
  color: #233752;
}

.bar-track,
.mini-track {
  width: 100%;
  height: 12px;
  background: #edf2f9;
  border-radius: 999px;
  overflow: hidden;
}

.bar-fill,
.mini-fill {
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(90deg, #3b82f6, #0ea5e9);
}

.mini-chart {
  margin-bottom: 14px;
}

.mini-chart-label {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 8px;
  color: #2d3f58;
}

.portfolio-summary {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 12px 14px;
  border-radius: 12px;
  background: #f4f8ff;
  margin-bottom: 18px;
}

.country-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.country-list li {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  padding: 10px 12px;
  border-radius: 10px;
  background: #f8fafc;
}

@media (max-width: 720px) {
  .hero-panel {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
