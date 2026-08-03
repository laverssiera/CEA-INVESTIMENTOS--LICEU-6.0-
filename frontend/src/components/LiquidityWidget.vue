<template>
  <article class="panel">
    <small>Liquidez</small>
    <h3>Caixa e fluxo financeiro</h3>

    <div class="grid-3">
      <div class="card">
        <small>Caixa disponível</small>
        <div class="stat-value">{{ currency(cashflow.cash_balance_brl) }}</div>
      </div>
      <div class="card">
        <small>Receita mensal</small>
        <div class="stat-value">{{ currency(cashflow.monthly_income_brl) }}</div>
      </div>
      <div class="card">
        <small>Despesa mensal</small>
        <div class="stat-value">{{ currency(cashflow.monthly_expenses_brl) }}</div>
      </div>
    </div>

    <p>
      <strong>Buffer de liquidez:</strong>
      {{ cashflow.liquidity_buffer_months || '--' }} meses
    </p>
  </article>
</template>

<script setup>
defineProps({
  cashflow: {
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
