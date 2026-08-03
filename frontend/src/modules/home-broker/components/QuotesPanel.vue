<template>
  <div class="grid-4">
    <div v-for="asset in assets" :key="asset.id" class="card">
      <div class="asset-symbol">{{ asset.symbol }}</div>
      <div class="asset-price">R$ {{ Number(asset.price).toFixed(2) }}</div>
      <div class="asset-yield">Yield: {{ asset.yield }}%</div>
      <small>Risco: {{ asset.risk }}</small>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useBrokerStore } from '../store'

const store = useBrokerStore()
const { assets } = storeToRefs(store)

onMounted(() => {
  store.loadAssets()
})
</script>

<style scoped>
.asset-symbol {
  font-weight: 700;
}

.asset-price {
  margin-top: 6px;
  font-size: 1.05rem;
}

.asset-yield {
  margin-top: 4px;
  color: var(--primary);
  font-weight: 600;
}
</style>
