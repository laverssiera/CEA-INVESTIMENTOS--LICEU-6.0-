<template>
  <article class="panel">
    <small>Credit Intelligence Engine</small>
    <h3>Score de risco e crédito</h3>

    <div class="stat-value">{{ scoreData.score || '--' }}</div>
    <p><strong>Risco:</strong> {{ scoreData.risk || 'N/D' }}</p>
    <p><strong>Alocação recomendada:</strong> {{ scoreData.recommended_allocation || 'N/D' }}</p>

    <ul class="list" v-if="scoreData.breakdown">
      <li v-for="(value, key) in scoreData.breakdown" :key="key">
        <strong>{{ key }}:</strong> {{ value }}
      </li>
    </ul>
  </article>
</template>

<script setup>
defineProps({
  scoreData: {
    type: Object,
    default: () => ({}),
  },
})
</script>
