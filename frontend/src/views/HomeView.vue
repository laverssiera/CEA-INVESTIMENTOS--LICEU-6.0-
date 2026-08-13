<template>
  <div class="page">
    <section class="hero">
      <div>
        <p class="eyebrow">Financial Engine</p>
        <h2>Captação, funding e inteligência financeira para obras e ativos reais.</h2>
        <p>
          A CEA INVESTIMENTOS conecta investidores, clientes tomadores de financiamento,
          projetos da LICEU 6.0 e um backoffice institucional para operar como uma estrutura
          financeira digital com foco em RWA.
        </p>
        <div class="actions">
          <RouterLink class="primary-btn" to="/servicos">Acessar serviços</RouterLink>
          <RouterLink class="secondary-btn secondary-btn-dark" to="/investidor/dashboard">Portal do investidor</RouterLink>
        </div>
      </div>

      <div class="hero-grid">
        <div class="card">
          <small>Status operacional</small>
          <div class="stat-value">Multiportal</div>
          <span class="tag info">Investidor, cliente e admin</span>
        </div>
        <div class="card">
          <small>Motor de decisão</small>
          <div class="stat-value">Crédito + ML</div>
          <span class="tag warning">Liquidez e risco</span>
        </div>
      </div>
    </section>

    <h3 class="section-title">Indicadores institucionais</h3>
    <section class="grid-4">
      <StatCard label="CDI" :value="`${indicators.cdi}%`" trend="Renda fixa" />
      <StatCard label="SELIC" :value="`${indicators.selic}%`" trend="Macro" tone="warning" />
      <StatCard label="Ibovespa" :value="indicators.ibovespa" trend="Mercado" />
      <StatCard label="Dólar" :value="`R$ ${indicators.dolar}`" trend="Hedge" tone="critical" />
    </section>

    <h3 class="section-title">Jornadas da plataforma</h3>
    <section class="grid-3">
      <RouterLink class="card card-link" to="/investir">
        <small>Investimentos</small>
        <h4>Inteligência de mercado</h4>
        <p>Curva de juros, simulações, alertas e recomendação de alocação.</p>
      </RouterLink>
      <RouterLink class="card card-link" to="/financiamento">
        <small>Funding</small>
        <h4>Solicitação de financiamento</h4>
        <p>Captação de dados iniciais do projeto e entrada no pipeline de crédito.</p>
      </RouterLink>
      <RouterLink class="card card-link" to="/admin/login">
        <small>Backoffice</small>
        <h4>Operação institucional</h4>
        <p>Módulos internos para crédito, risco, tesouraria, compliance e auditoria.</p>
      </RouterLink>
    </section>

    <h3 class="section-title">Integrações via API com a LICEU 6.0</h3>
    <section class="grid-3">
      <article v-for="(module, key) in liceuOverview" :key="key" class="card">
        <small>{{ module.endpoint }}</small>
        <h4>{{ key.toUpperCase() }}</h4>
        <ul class="list">
          <li v-for="(value, itemKey) in filteredEntries(module)" :key="itemKey">
            <strong>{{ itemKey }}:</strong> {{ formatValue(value) }}
          </li>
        </ul>
      </article>
    </section>

    <h3 class="section-title">Capacidades estruturantes</h3>
    <section class="grid-3">
      <article class="card">
        <strong>Site institucional e entrada por perfil</strong>
        <p>Navegação organizada para serviços, investir, financiamento e áreas restritas.</p>
      </article>
      <article class="card">
        <strong>Portal do investidor</strong>
        <p>Dashboard, carteira, projetos e sinais de risco conectados ao backend.</p>
      </article>
      <article class="card">
        <strong>Backoffice institucional</strong>
        <p>Governança por papéis, pipeline de crédito e módulos internos operacionais.</p>
      </article>
    </section>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import StatCard from '../components/StatCard.vue'
import { fetchLiceuOverview, fetchMarketIndicators } from '../services/liceuApi'

const indicators = ref({ cdi: 13.45, selic: 13.75, ibovespa: 128450, dolar: 5.18 })
const liceuOverview = ref({})

const filteredEntries = (module) => Object.entries(module).filter(([key]) => key !== 'endpoint')

const formatValue = (value) => {
  if (Array.isArray(value)) return value.join(' · ')
  return value
}

onMounted(async () => {
  try {
    const [market, liceu] = await Promise.all([fetchMarketIndicators(), fetchLiceuOverview()])
    indicators.value = market.indicators
    liceuOverview.value = liceu
  } catch (error) {
    console.error(error)
  }
})
</script>
