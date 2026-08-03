<template>
  <article class="panel">
    <small>Watchlist</small>
    <h3>Ativos disponíveis</h3>

    <div class="watchlist">
      <button
        v-for="asset in assets"
        :key="asset.id"
        class="watch-item"
        type="button"
        @click="$emit('select', asset)"
      >
        <strong>{{ asset.symbol }}</strong>
        <span>R$ {{ Number(asset.price).toFixed(2) }}</span>
      </button>
    </div>
  </article>
</template>

<script setup>
import { onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useBrokerStore } from '../store'

defineEmits(['select'])

const store = useBrokerStore()
const { assets } = storeToRefs(store)

onMounted(async () => {
  if (!assets.value.length) {
    await store.loadAssets()
  }
})
</script>

<style scoped>
.watchlist {
  display: grid;
  gap: 10px;
}

.watch-item {
  display: flex;
  justify-content: space-between;
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 10px;
  background: #fff;
}
</style>
