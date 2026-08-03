<template>
  <div class="container">
    <h2 class="screen-title">Tokenização</h2>
    <p class="screen-subtitle">Fracionamento digital de investimentos por token</p>

    <section class="card">
      <h3>Mercado de tokens</h3>
      <div v-if="!market.length" class="empty">Nenhum ativo tokenizado no momento.</div>
      <div v-for="t in market" :key="t.token_id" class="token-row">
        <div>
          <strong>{{ t.token_symbol }}</strong>
          <small>{{ t.project_id }} · disponibilidade {{ t.available_supply }}/{{ t.total_supply }}</small>
        </div>
        <div class="right">
          <strong>{{ formatBRL(t.price_brl) }}</strong>
          <button class="buy" @click="openBuy(t)">Comprar</button>
        </div>
      </div>
    </section>

    <section class="card">
      <h3>Minha carteira tokenizada</h3>
      <div v-if="!portfolio.length" class="empty">Sem posições em tokens.</div>
      <div v-for="p in portfolio" :key="p.token_id" class="position-row">
        <div>
          <strong>{{ p.token_symbol }}</strong>
          <small>{{ p.project_id }}</small>
        </div>
        <div class="right">
          <strong>{{ p.quantity }} un.</strong>
          <small>{{ formatBRL(p.mark_value) }}</small>
        </div>
      </div>
    </section>

    <section v-if="buying" class="card">
      <h3>Comprar {{ buying.token_symbol }}</h3>
      <label class="field">
        <span>Quantidade</span>
        <input v-model.number="qty" type="number" min="1" />
      </label>
      <p class="total">Total: {{ formatBRL((qty || 0) * buying.price_brl) }}</p>
      <button class="cta" :disabled="loading || !qty" @click="confirmBuy">
        {{ loading ? 'Executando...' : 'Confirmar compra' }}
      </button>
      <p v-if="msg" class="ok">{{ msg }}</p>
      <p v-if="err" class="error">{{ err }}</p>
    </section>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { buyToken, fetchTokenMarket, fetchTokenPortfolio } from '../services/api.js'

const market = ref([])
const portfolio = ref([])
const buying = ref(null)
const qty = ref(1)
const loading = ref(false)
const msg = ref('')
const err = ref('')

function formatBRL(v) {
  return (v ?? 0).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}

async function loadAll() {
  const [m, p] = await Promise.allSettled([fetchTokenMarket(), fetchTokenPortfolio()])
  market.value = m.status === 'fulfilled' ? (m.value.items ?? []) : []
  portfolio.value = p.status === 'fulfilled' ? (p.value.items ?? []) : []
}

function openBuy(t) {
  buying.value = t
  qty.value = 1
  err.value = ''
  msg.value = ''
}

async function confirmBuy() {
  loading.value = true
  err.value = ''
  msg.value = ''
  try {
    const res = await buyToken(buying.value.token_id, qty.value)
    msg.value = `Compra confirmada: ordem ${res.order_id}`
    await loadAll()
  } catch (e) {
    err.value = e.message
  } finally {
    loading.value = false
  }
}

onMounted(loadAll)
</script>

<style scoped>
.card { background: #fff; border: 1px solid var(--cea-border); border-radius: 16px; padding: 18px; margin-bottom: 12px; display: grid; gap: 10px; }
h3 { margin: 0; color: var(--cea-blue); font-size: 0.95rem; }
.token-row, .position-row { display: flex; justify-content: space-between; align-items: center; gap: 10px; padding: 8px 0; border-bottom: 1px solid #eef3fb; }
.token-row:last-child, .position-row:last-child { border-bottom: none; }
strong { color: var(--cea-text); font-size: 0.9rem; }
small { color: var(--cea-muted); font-size: 0.76rem; display: block; }
.right { text-align: right; }
.buy { margin-top: 5px; border: 1px solid var(--cea-border); background: #f5f8ff; color: var(--cea-blue); border-radius: 10px; padding: 6px 10px; font-weight: 700; cursor: pointer; }
.field { display: grid; gap: 5px; font-size: 0.82rem; color: var(--cea-muted); }
.field input { border: 1px solid var(--cea-border); border-radius: 10px; padding: 10px; background: #f8fbff; }
.total { margin: 0; color: var(--cea-text); font-weight: 700; }
.cta { border: none; border-radius: 12px; background: linear-gradient(135deg, var(--cea-blue), var(--cea-blue-2)); color: #fff; padding: 12px; font-weight: 800; cursor: pointer; }
.ok { color: #166534; margin: 0; font-size: 0.82rem; }
.error { color: #b91c1c; margin: 0; font-size: 0.82rem; }
.empty { color: var(--cea-muted); font-size: 0.86rem; }
</style>
