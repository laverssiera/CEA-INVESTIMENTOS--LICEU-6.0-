<template>
  <article class="panel">
    <small>Carteira</small>
    <h3>Posição consolidada do cliente</h3>

    <div class="grid-3">
      <div class="card">
        <small>Patrimônio</small>
        <div class="stat-value">{{ currency(summary.portfolio_value_brl) }}</div>
      </div>
      <div class="card">
        <small>Rentabilidade mensal</small>
        <div class="stat-value">{{ summary.monthly_yield_pct }}%</div>
      </div>
      <div class="card">
        <small>Projetos ativos</small>
        <div class="stat-value">{{ summary.active_projects?.length || 0 }}</div>
      </div>
    </div>

    <ul class="list" v-if="summary.wallet?.length">
      <li v-for="item in summary.wallet" :key="item.name">
        <strong>{{ item.name }}</strong> — {{ item.percentage }}% ({{ currency(item.value_brl) }})
      </li>
    </ul>
  </article>
</template>

<script setup>
defineProps({
  summary: {
    type: Object,
    default: () => ({}),
  },
})

const currency = (value) =>
  new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
    maximumFractionDigits: 0,
  }).format(Number(value || 0))
</script>
