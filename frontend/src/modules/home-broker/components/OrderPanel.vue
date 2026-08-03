<template>
  <article class="panel">
    <small>Ordem</small>
    <h3>Investir</h3>

    <div v-if="asset">
      <p><strong>{{ asset.name }}</strong></p>
      <p class="mb-2">Preço: R$ {{ Number(asset.price).toFixed(2) }}</p>
      <input v-model.number="amount" min="1" type="number" class="broker-input" placeholder="Valor do aporte" />
      <button @click="invest" class="primary-btn mt-2" type="button" :disabled="loading">
        {{ loading ? 'Enviando...' : 'Investir' }}
      </button>
      <p v-if="message" class="ok-msg">{{ message }}</p>
      <p v-if="error" class="error-msg">{{ error }}</p>
    </div>
    <p v-else>Selecione um ativo na watchlist para abrir ordem.</p>
  </article>
</template>

<script setup>
import { ref } from 'vue'
import { useBrokerStore } from '../store'

const props = defineProps(['asset'])
const amount = ref(0)
const loading = ref(false)
const error = ref('')
const message = ref('')
const store = useBrokerStore()

async function invest() {
  error.value = ''
  message.value = ''

  if (!props.asset) {
    error.value = 'Selecione um ativo.'
    return
  }

  if (!amount.value || amount.value <= 0) {
    error.value = 'Informe um valor válido.'
    return
  }

  loading.value = true
  try {
    await store.placeOrder({
      asset_id: props.asset.id,
      amount: amount.value,
    })
    message.value = 'Ordem enviada com sucesso.'
  } catch (e) {
    error.value = e?.response?.data?.detail || 'Falha ao enviar ordem.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.broker-input {
  width: 100%;
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 10px;
  background: #fcfdff;
}

.mt-2 {
  margin-top: 8px;
}

.mb-2 {
  margin-bottom: 8px;
}

.ok-msg {
  color: #1b7f3b;
  margin-top: 8px;
}

.error-msg {
  color: var(--red);
  margin-top: 8px;
}
</style>
