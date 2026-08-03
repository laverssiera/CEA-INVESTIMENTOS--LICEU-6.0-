<template>
  <div class="container">
    <h2 class="screen-title">Minha Carteira</h2>
    <p class="screen-subtitle">Visão consolidada de desempenho e diversificação</p>

    <!-- Carteira Digital PIX -->
    <div class="wallet-card">
      <div class="wallet-left">
        <small>Carteira Digital</small>
        <h2>{{ formatBRL(walletBalance) }}</h2>
        <span class="wallet-status">{{ wsConnected ? '● ao vivo' : '○ atualizando...' }}</span>
      </div>
      <router-link to="/deposit" class="deposit-btn">
        <span>＋</span> Depositar PIX
      </router-link>
    </div>

    <div class="balance-summary">
      <small>Patrimônio Total</small>
      <h1>R$ 125.750,00</h1>
      <span class="yield">+1,42% este mês</span>
    </div>

    <!-- Gráfico de alocação -->
    <div class="chart-card">
      <h3>Alocação por Classe</h3>
      <div class="chart-wrap">
        <Doughnut :data="chartData" :options="chartOptions" />
      </div>
      <ul class="legend">
        <li v-for="(item, i) in allocation" :key="i">
          <i :style="{ background: item.color }"></i>
          <span>{{ item.label }}</span>
          <strong>{{ item.pct }}%</strong>
        </li>
      </ul>
    </div>

    <!-- Missões Civilizacionais -->
    <div class="missions-section" v-if="missionPortfolio">
      <h3>Missões Civilizacionais</h3>
      <div v-for="m in missionPortfolio.assets" :key="m.id" class="mission-card">
        <div class="mission-header">
          <strong>{{ m.name }}</strong>
          <span class="category-badge">{{ m.category }}</span>
        </div>
        <div class="mission-body">
          <div class="stat">
            <small>Avaliação</small>
            <span>{{ formatBRL(m.valuation) }}</span>
          </div>
          <div class="stat">
            <small>Impacto</small>
            <span>{{ (m.impact_civilizational_score * 100).toFixed(0) }}%</span>
          </div>
          <div class="status-pill" :class="m.funding_status.toLowerCase()">
            {{ m.funding_status }}
          </div>
        </div>
      </div>
    </div>

    <!-- Posições -->
    <div class="positions">
      <h3>Posições Ativas</h3>
      <div class="position-row" v-for="p in positions" :key="p.label">
        <div>
          <strong>{{ p.label }}</strong>
          <small>{{ p.type }}</small>
        </div>
        <div class="right">
          <strong>{{ p.value }}</strong>
          <small :class="p.yield.startsWith('+') ? 'pos' : 'neg'">{{ p.yield }}</small>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { Doughnut } from 'vue-chartjs'
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
} from 'chart.js'
import { fetchWalletBalance, connectWalletSocket, fetchMissionPortfolio } from '../services/api.js'
import { auth } from '../store/auth.js'

ChartJS.register(ArcElement, Tooltip, Legend)

const walletBalance = ref(0)
const missionPortfolio = ref(null)
const wsConnected = ref(false)
let _ws = null

function formatBRL(v) {
  return (v ?? 0).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}

onMounted(async () => {
  try {
    const [wData, mData] = await Promise.all([
      fetchWalletBalance(),
      fetchMissionPortfolio()
    ])
    walletBalance.value = wData.balance ?? 0
    missionPortfolio.value = mData
  } catch { /* usa zeros */ }

    _ws = connectWalletSocket(auth.name ?? 'demo', (msg) => {
      if (msg.event === 'wallet.updated' || msg.event === 'wallet_updated') {
      walletBalance.value = msg.balance ?? walletBalance.value
    }
  })
  if (_ws) {
    _ws.onopen = () => { wsConnected.value = true }
    _ws.onclose = () => { wsConnected.value = false }
  }
})

onBeforeUnmount(() => {
  _ws?.close()
})

const allocation = [
  { label: 'Imobiliário', pct: 45, color: '#0d3c8f' },
  { label: 'Infraestrutura', pct: 30, color: '#1f66dc' },
  { label: 'Crédito Privado', pct: 15, color: '#d4aa3a' },
  { label: 'Renda Fixa', pct: 10, color: '#a5b4d0' },
]

const chartData = {
  labels: allocation.map((a) => a.label),
  datasets: [
    {
      data: allocation.map((a) => a.pct),
      backgroundColor: allocation.map((a) => a.color),
      borderWidth: 0,
      hoverOffset: 6,
    },
  ],
}

const chartOptions = {
  cutout: '68%',
  plugins: {
    legend: { display: false },
    tooltip: {
      callbacks: {
        label: (ctx) => ` ${ctx.label}: ${ctx.parsed}%`,
      },
    },
  },
}

const positions = [
  { label: 'Green Residence', type: 'Imobiliário', value: 'R$ 40.000', yield: '+9,8% a.a.' },
  { label: 'Fundo Infra BR', type: 'Infraestrutura', value: 'R$ 30.000', yield: '+11,2% a.a.' },
  { label: 'CRI CEA', type: 'Crédito', value: 'R$ 20.000', yield: '+8,5% a.a.' },
  { label: 'Tesouro IPCA+', type: 'Renda Fixa', value: 'R$ 12.000', yield: '+6,2% a.a.' },
]
</script>

<style scoped>
h2 {
  margin-bottom: 0;
}

h3 {
  color: var(--cea-blue);
  font-size: 0.96rem;
  margin-bottom: 12px;
}

.balance-summary {
  background: linear-gradient(135deg, var(--cea-blue), var(--cea-blue-2));
  color: #fff;
  border-radius: 16px;
  padding: 20px;
  display: grid;
  gap: 4px;
  margin-bottom: 14px;
  box-shadow: 0 12px 24px rgba(13, 60, 143, 0.22);
}

.balance-summary small {
  color: #d9e6ff;
  font-size: 0.82rem;
}

.balance-summary h1 {
  font-size: 1.7rem;
}

.yield {
  color: #8ff3ac;
  font-size: 0.86rem;
  font-weight: 700;
}

.chart-card {
  background: #fff;
  border: 1px solid var(--cea-border);
  border-radius: 16px;
  padding: 18px;
  margin-bottom: 14px;
  box-shadow: 0 6px 14px rgba(13, 60, 143, 0.07);
}

.chart-wrap {
  max-width: 180px;
  margin: 0 auto 16px;
}

.legend {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 8px;
}

.legend li {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.88rem;
}

.legend i {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}

.legend span {
  flex: 1;
  color: var(--cea-muted);
}

.legend strong {
  color: var(--cea-text);
}

.missions-section {
  margin-top: 2rem;
  background: rgba(255, 255, 255, 0.05);
  padding: 1rem;
  border-radius: 12px;
}

.mission-card {
  background: rgba(255, 255, 255, 0.03);
  margin-bottom: 1rem;
  padding: 1rem;
  border-radius: 8px;
  border-left: 4px solid #1f66dc;
}

.mission-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.category-badge {
  font-size: 0.7rem;
  background: #1f66dc;
  padding: 2px 6px;
  border-radius: 4px;
}

.mission-body {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat {
  display: flex;
  flex-direction: column;
}

.stat small {
  font-size: 0.6rem;
  color: #a5b4d0;
}

.status-pill {
  font-size: 0.7rem;
  padding: 4px 8px;
  border-radius: 12px;
  background: #333;
}

.status-pill.operational { background: #1a5c1a; }
.status-pill.partially_funded { background: #5c5c1a; }
.status-pill.awaiting_funds { background: #5c1a1a; }

.positions {
  background: #fff;
  border: 1px solid var(--cea-border);
  border-radius: 16px;
  padding: 18px;
  box-shadow: 0 6px 14px rgba(13, 60, 143, 0.07);
}

.position-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #f0f4fa;
}

.position-row:last-child {
  border-bottom: none;
}

.position-row > div {
  display: grid;
  gap: 2px;
}

.position-row strong {
  font-size: 0.9rem;
  color: var(--cea-text);
}

.position-row small {
  font-size: 0.78rem;
  color: var(--cea-muted);
}

.right {
  text-align: right;
}

.pos {
  color: #16a34a;
  font-weight: 700;
}

.neg {
  color: #dc2626;
  font-weight: 700;
}

/* ── Carteira Digital ── */
.wallet-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: linear-gradient(135deg, #0d2f6e, #101e3a);
  border-radius: 16px;
  padding: 18px 20px;
  margin-bottom: 14px;
  box-shadow: 0 12px 24px rgba(10, 20, 60, 0.28);
}

.wallet-left {
  display: grid;
  gap: 4px;
}

.wallet-left small {
  color: #8faed4;
  font-size: 0.78rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.wallet-left h2 {
  color: #fff;
  font-size: 1.42rem;
  font-family: Sora, sans-serif;
  margin: 0;
}

.wallet-status {
  font-size: 0.73rem;
  color: #4dde7a;
  font-weight: 700;
}

.deposit-btn {
  display: flex;
  align-items: center;
  gap: 5px;
  background: #1f66dc;
  color: #fff;
  border-radius: 12px;
  padding: 10px 16px;
  font-size: 0.84rem;
  font-weight: 800;
  text-decoration: none;
  box-shadow: 0 6px 14px rgba(31, 102, 220, 0.35);
  white-space: nowrap;
}

.deposit-btn:hover {
  transform: translateY(-1px);
  background: #2b7bf0;
}

.deposit-btn span {
  font-size: 1.08rem;
  font-weight: 900;
}
</style>

