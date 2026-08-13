<template>
  <div class="page">
    <section class="hero">
      <div>
        <p class="eyebrow">/investir</p>
        <h2>Inteligência de mercado para suportar decisões de investimento e caixa.</h2>
        <p>
          O painel cruza CDI, SELIC, IPCA, curva de juros, liquidez e risco de projeto para
          sugerir alocações objetivas, auditáveis e reforçadas por decision tree ML.
        </p>
      </div>
      <div class="hero-grid">
        <div class="card">
          <small>Recomendação atual</small>
          <div class="stat-value">{{ recommendation.expected_return }}</div>
          <span class="tag low">Risco {{ recommendation.risk_level }}</span>
        </div>
        <div class="card">
          <small>ML allocation</small>
          <div class="stat-value">{{ mlDecision.allocation || 'N/D' }}</div>
          <span class="tag info">Conf. {{ mlDecision.confidence || '--' }}</span>
        </div>
      </div>
    </section>

    <MarketTicker :indicators="indicators" />

    <h3 class="section-title">Painel de mercado</h3>
    <section class="grid-4">
      <StatCard label="CDI" :value="`${indicators.cdi}%`" trend="ao vivo" />
      <StatCard label="SELIC" :value="`${indicators.selic}%`" trend="macro" tone="warning" />
      <StatCard label="IPCA" :value="`${indicators.ipca}%`" trend="inflação" />
      <StatCard label="Tesouro Selic" :value="`${indicators.tesouro_selic}%`" trend="benchmark" tone="info" />
    </section>

    <section class="grid-2">
      <YieldCurve :curve="yieldCurve" />
      <DecisionTreePanel :recommendation="recommendation" />
    </section>

    <h3 class="section-title">Recomendações inteligentes</h3>
    <section class="grid-3">
      <article v-for="item in recommendation.allocation" :key="item.asset" class="card">
        <small>Alocação sugerida</small>
        <div class="stat-value">{{ item.percentage }}%</div>
        <strong>{{ item.asset }}</strong>
      </article>
    </section>

    <section class="grid-2">
      <article class="panel">
        <small>Simulador de alocação</small>
        <h3>Testar cenário</h3>
        <form class="form-grid" @submit.prevent="simulateScenario">
          <label>
            Caixa disponível
            <input v-model.number="form.cash_balance" min="1" step="1000" type="number" />
          </label>
          <label>
            Prazo da obra (dias)
            <input v-model.number="form.project_horizon_days" min="1" max="720" type="number" />
          </label>
          <label>
            Liquidez
            <select v-model="form.liquidity_need">
              <option value="alta">Alta</option>
              <option value="média">Média</option>
              <option value="baixa">Baixa</option>
            </select>
          </label>
          <label>
            Risco
            <select v-model="form.risk_profile">
              <option value="baixo">Baixo</option>
              <option value="moderado">Moderado</option>
              <option value="alto">Alto</option>
            </select>
          </label>
          <button class="primary-btn" type="submit">Gerar recomendação</button>
        </form>

        <ul class="list" v-if="simulation.rationale?.length">
          <li v-for="item in simulation.rationale" :key="item">{{ item }}</li>
        </ul>
        <p v-if="simulation.projected_monthly_income_brl">
          <strong>Rendimento mensal estimado:</strong> R$ {{ simulation.projected_monthly_income_brl }}
        </p>
      </article>

      <article class="panel">
        <small>Alertas inteligentes</small>
        <h3>Eventos monitorados</h3>
        <div v-for="alert in alerts" :key="alert.title" class="alert">
          <span class="tag" :class="alert.level">{{ alert.level }}</span>
          <p><strong>{{ alert.title }}</strong></p>
          <p>{{ alert.message }}</p>
        </div>
      </article>
    </section>

    <SecurityChecklist :security-data="securityData" />
  </div>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'
import DecisionTreePanel from '../components/DecisionTreePanel.vue'
import MarketTicker from '../components/MarketTicker.vue'
import SecurityChecklist from '../components/SecurityChecklist.vue'
import StatCard from '../components/StatCard.vue'
import YieldCurve from '../components/YieldCurve.vue'
import {
  fetchMarketAlerts,
  fetchMarketIndicators,
  fetchMarketRecommendation,
  fetchMlDecision,
  fetchSecurityPosture,
  simulateMarketAllocation,
} from '../services/liceuApi'

const indicators = ref({
  cdi: 13.45,
  selic: 13.75,
  ipca: 4.31,
  tesouro_selic: 13.22,
  liquidez: 'Alta',
})
const recommendation = ref({ allocation: [], risk_level: 'baixo', expected_return: 'CDI + 0.4%' })
const simulation = ref({})
const alerts = ref([])
const securityData = ref({})
const yieldCurve = ref([12.9, 13.1, 13.35, 13.48, 13.62])
const mlDecision = ref({})
const form = ref({
  cash_balance: 12400000,
  project_horizon_days: 45,
  liquidity_need: 'alta',
  risk_profile: 'baixo',
})

let socket

const connectSocket = () => {
  const wsUrl = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws/market'
  socket = new WebSocket(wsUrl)

  socket.onmessage = (event) => {
    const payload = JSON.parse(event.data)
    indicators.value = payload.indicators
  }

  socket.onerror = () => {
    socket?.close()
  }
}

const loadDashboard = async () => {
  try {
    const [market, reco, alertsData, security, ml] = await Promise.all([
      fetchMarketIndicators(),
      fetchMarketRecommendation(),
      fetchMarketAlerts(),
      fetchSecurityPosture(),
      fetchMlDecision({
        project_term_days: 45,
        interest_rate: 13.75,
        cash_balance: 12400000,
        risk_index: 35,
      }),
    ])

    indicators.value = market.indicators
    yieldCurve.value = market.yield_curve
    recommendation.value = reco
    simulation.value = reco
    alerts.value = alertsData.items
    securityData.value = security
    mlDecision.value = ml
  } catch (error) {
    console.error(error)
  }
}

const simulateScenario = async () => {
  simulation.value = await simulateMarketAllocation(form.value)
  recommendation.value = simulation.value
  mlDecision.value = await fetchMlDecision({
    project_term_days: form.value.project_horizon_days,
    interest_rate: indicators.value.selic,
    cash_balance: form.value.cash_balance,
    risk_index: form.value.risk_profile === 'alto' ? 70 : form.value.risk_profile === 'moderado' ? 45 : 25,
  })
}

onMounted(async () => {
  await loadDashboard()
  connectSocket()
})

onBeforeUnmount(() => {
  socket?.close()
})
</script>
