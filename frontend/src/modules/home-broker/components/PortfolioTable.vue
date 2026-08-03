<template>
  <article class="panel">
    <small>Carteira consolidada</small>
    <h3>Posições do investidor</h3>

    <table class="portfolio-table">
      <thead>
        <tr>
          <th>Ordem</th>
          <th>Produto</th>
          <th>Valor</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in portfolio" :key="item.id">
          <td>{{ item.id }}</td>
          <td>{{ item.product_name || item.product_id }}</td>
          <td>R$ {{ Number(item.amount || 0).toFixed(2) }}</td>
          <td>{{ item.status || 'confirmed' }}</td>
        </tr>
        <tr v-if="!portfolio.length">
          <td colspan="4">Nenhuma posição registrada.</td>
        </tr>
      </tbody>
    </table>
  </article>
</template>

<script setup>
import { onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useBrokerStore } from '../store'

const store = useBrokerStore()
const { portfolio } = storeToRefs(store)

onMounted(() => {
  store.loadPortfolio()
})
</script>

<style scoped>
.portfolio-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 8px;
}

.portfolio-table th,
.portfolio-table td {
  border-bottom: 1px solid var(--border);
  text-align: left;
  padding: 10px 6px;
}
</style>
