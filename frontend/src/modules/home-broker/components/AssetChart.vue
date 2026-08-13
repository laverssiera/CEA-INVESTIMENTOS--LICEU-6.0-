<template>
  <article class="panel">
    <small>Asset Chart</small>
    <h3>{{ asset ? asset.name : 'Selecione um ativo' }}</h3>

    <div v-if="asset" class="chart-placeholder">
      <div class="bar" v-for="(point, idx) in trend" :key="idx" :style="{ height: `${point}%` }"></div>
    </div>
    <p v-else>Escolha um ativo na watchlist para ver comportamento de preço.</p>
  </article>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  asset: {
    type: Object,
    default: null,
  },
})

const trend = computed(() => {
  const base = props.asset?.yield || 10
  return [40, 62, 48, 74, 57, 80, 66].map((point) => Math.min(95, Math.max(20, point + base / 2 - 8)))
})
</script>

<style scoped>
.chart-placeholder {
  display: flex;
  gap: 8px;
  align-items: flex-end;
  height: 180px;
  margin-top: 12px;
}

.bar {
  flex: 1;
  background: linear-gradient(180deg, var(--gold), var(--primary));
  border-radius: 6px 6px 2px 2px;
}
</style>
