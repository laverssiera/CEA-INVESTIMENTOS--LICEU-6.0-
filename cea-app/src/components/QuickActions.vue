<template>
  <div class="actions">
    <button
      v-for="item in items"
      :key="item.label"
      :class="{ active: isActive(item.to) }"
      @click="goTo(item.to)"
    >
      <span>{{ item.icon }}</span>{{ item.label }}
    </button>
  </div>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router'

const router = useRouter()
const route = useRoute()

const items = [
  { label: 'Contratos',   icon: '✎', to: '/contracts' },
  { label: 'Tokenização', icon: '◉', to: '/tokenization' },
  { label: 'Wallet',      icon: '⊞', to: '/wallet' },
  { label: 'Marketplace', icon: '▣', to: '/marketplace' },
]

function goTo(path) {
  router.push(path)
}

function isActive(path) {
  return route.path === path
}
</script>

<style scoped>
.actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin: 20px 0;
}

button {
  padding: 14px;
  border: none;
  border-radius: 12px;
  background: var(--cea-blue);
  color: white;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 7px;
  box-shadow: 0 10px 18px rgba(13, 60, 143, 0.24);
  cursor: pointer;
}

button.active {
  background: linear-gradient(135deg, var(--cea-blue), var(--cea-blue-2));
  box-shadow: 0 14px 22px rgba(13, 60, 143, 0.32);
}

button span {
  color: var(--cea-gold);
}

button:hover {
  transform: translateY(-2px);
  box-shadow: 0 14px 22px rgba(13, 60, 143, 0.28);
}

button:active {
  transform: translateY(0);
}
</style>
