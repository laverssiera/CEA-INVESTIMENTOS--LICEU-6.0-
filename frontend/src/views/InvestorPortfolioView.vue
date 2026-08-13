<template>
  <div class="page">
    <section class="hero">
      <div>
        <p class="eyebrow">/investidor/carteira</p>
        <h2>Carteira consolidada com visão de liquidez, duração e rentabilidade.</h2>
        <p>
          A camada de portfólio foi organizada para exibir exposição em crédito, caixa e ativos
          de suporte à operação das obras.
        </p>
      </div>

      <div class="hero-grid">
        <div class="card">
          <small>Patrimônio total</small>
          <div class="stat-value">{{ formatBrl(portfolio.portfolio_value_brl) }}</div>
          <span class="tag info">{{ portfolio.liquidity_label || '...' }}</span>
        </div>
        <div class="card">
          <small>Rentabilidade mensal</small>
          <div class="stat-value">{{ portfolio.monthly_yield_pct || '--' }}%</div>
          <span class="tag warning">Mês corrente</span>
        </div>
      </div>
    </section>

    <section class="grid-3">
      <article v-for="item in portfolio.wallet || []" :key="item.name" class="card">
        <small>{{ item.name }}</small>
        <div class="stat-value">{{ item.percentage }}%</div>
        <p>{{ formatBrl(item.value_brl) }}</p>
      </article>
    </section>

    <h3 class="section-title">Projetos ativos</h3>
    <section class="grid-3">
      <article v-for="proj in portfolio.active_projects || []" :key="proj.name" class="card">
        <small>{{ proj.status }}</small>
        <h4>{{ proj.name }}</h4>
        <p>Avanço: {{ proj.progress }}%</p>
      </article>
    </section>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { fetchDashboardPortfolio } from '../services/liceuApi'

const portfolio = ref({ wallet: [], active_projects: [], portfolio_value_brl: 0 })

const formatBrl = (value) =>
  value ? `R$ ${(value / 1_000_000).toFixed(2).replace('.', ',')} mi` : '--'

onMounted(async () => {
  try {
    portfolio.value = await fetchDashboardPortfolio()
  } catch (e) {
    console.error(e)
  }
})
</script>