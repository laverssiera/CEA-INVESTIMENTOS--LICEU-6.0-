<template>
  <div class="card">
    <h3>{{ title }}</h3>
    <p>Rentabilidade {{ yield }}</p>
    <small>Risco Moderado</small>
    <button>Investir</button>
  </div>
</template>

<script setup>
defineProps(['title', 'yield'])
</script>

<style scoped>
.card {
  background: var(--cea-card);
  padding: 16px;
  border-radius: 12px;
  margin-bottom: 12px;
  border: 1px solid var(--cea-border);
  display: grid;
  gap: 8px;
  box-shadow: 0 8px 16px rgba(13, 60, 143, 0.08);
  transition: transform 180ms ease, box-shadow 180ms ease;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 22px rgba(13, 60, 143, 0.12);
}

.card p {
  color: var(--cea-muted);
}

.card small {
  color: #2f7b45;
  font-weight: 700;
}

.card button {
  border: none;
  border-radius: 10px;
  background: var(--cea-blue);
  color: white;
  padding: 10px;
  font-weight: 700;
  cursor: pointer;
}

.card button:hover {
  transform: translateY(-1px);
}

.card button:active {
  transform: translateY(0);
}
</style>
