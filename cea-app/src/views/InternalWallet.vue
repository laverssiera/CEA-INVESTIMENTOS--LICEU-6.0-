<template>
  <div class="container">
    <h2 class="screen-title">Wallet Interna</h2>
    <p class="screen-subtitle">Transferências entre contas CEA com liquidação instantânea</p>

    <div class="balance-box">
      <small>Saldo atual</small>
      <h2>{{ formatBRL(balance) }}</h2>
      <small>Bloqueado: {{ formatBRL(locked) }}</small>
      <span>{{ wsOnline ? 'ao vivo' : 'offline' }}</span>
    </div>

    <section class="card">
      <h3>Nova transferência</h3>
      <label class="field">
        <span>Destinatário (user_id)</span>
        <input v-model="toUserId" placeholder="ex: investor_pj" />
      </label>
      <label class="field">
        <span>Valor (R$)</span>
        <input v-model.number="amount" type="number" min="1" step="0.01" />
      </label>
      <label class="field">
        <span>Descrição</span>
        <input v-model="description" placeholder="Repasse de parceria" />
      </label>
      <button class="cta" :disabled="loading || !toUserId || !amount" @click="sendTransfer">
        {{ loading ? 'Enviando...' : 'Transferir' }}
      </button>
      <p v-if="msg" class="ok">{{ msg }}</p>
      <p v-if="err" class="error">{{ err }}</p>
    </section>

    <section class="card">
      <h3>Histórico</h3>
      <div v-if="!transfers.length" class="empty">Sem transferências registradas.</div>
      <div v-for="t in transfers" :key="t.transfer_id" class="tx-row">
        <div>
          <strong>{{ t.from_user_id === userId ? 'Enviado para' : 'Recebido de' }} {{ t.from_user_id === userId ? t.to_user_id : t.from_user_id }}</strong>
          <small>{{ formatDate(t.created_at) }}</small>
        </div>
        <span :class="t.from_user_id === userId ? 'debit' : 'credit'">
          {{ t.from_user_id === userId ? '-' : '+' }} {{ formatBRL(t.amount) }}
        </span>
      </div>
    </section>
  </div>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { auth } from '../store/auth.js'
import { connectWalletSocket, fetchWalletBalance, fetchWalletTransfers, walletTransfer } from '../services/api.js'

const userId = auth.name ?? 'demo'
const balance = ref(0)
const locked = ref(0)
const wsOnline = ref(false)
let ws = null

const toUserId = ref('')
const amount = ref(null)
const description = ref('')
const loading = ref(false)
const msg = ref('')
const err = ref('')
const transfers = ref([])

function formatBRL(v) {
  return (v ?? 0).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}

function formatDate(iso) {
  return iso ? new Date(iso).toLocaleString('pt-BR', { day: '2-digit', month: '2-digit', year: '2-digit', hour: '2-digit', minute: '2-digit' }) : ''
}

async function loadData() {
  const [b, t] = await Promise.allSettled([fetchWalletBalance(), fetchWalletTransfers()])
  balance.value = b.status === 'fulfilled' ? (b.value.balance ?? 0) : 0
  locked.value = b.status === 'fulfilled' ? (b.value.locked ?? 0) : 0
  transfers.value = t.status === 'fulfilled' ? (t.value.items ?? []) : []
}

async function sendTransfer() {
  loading.value = true
  msg.value = ''
  err.value = ''
  try {
    const res = await walletTransfer({
      to_user_id: toUserId.value,
      amount: amount.value,
      description: description.value,
    })
    msg.value = `Transferência concluída: ${res.transfer_id}`
    toUserId.value = ''
    amount.value = null
    description.value = ''
    await loadData()
  } catch (e) {
    err.value = e.message
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await loadData()
  ws = connectWalletSocket(userId, (data) => {
    if (data.event === 'wallet.updated' || data.event === 'wallet_updated' || data.event === 'wallet_balance') {
      balance.value = data.balance ?? balance.value
      locked.value = data.locked ?? locked.value
    }
  })
  if (ws) {
    ws.onopen = () => { wsOnline.value = true }
    ws.onclose = () => { wsOnline.value = false }
  }
})

onBeforeUnmount(() => ws?.close())
</script>

<style scoped>
.balance-box { background: linear-gradient(135deg, #0d2f6e, #101e3a); border-radius: 16px; padding: 16px; color: #fff; margin-bottom: 12px; }
.balance-box small { color: #8faed4; font-size: 0.76rem; }
.balance-box h2 { margin: 4px 0; font-family: Sora, sans-serif; }
.balance-box span { color: #4ade80; font-size: 0.75rem; }
.card { background: #fff; border: 1px solid var(--cea-border); border-radius: 16px; padding: 18px; margin-bottom: 12px; display: grid; gap: 10px; }
h3 { margin: 0; color: var(--cea-blue); font-size: 0.95rem; }
.field { display: grid; gap: 5px; font-size: 0.82rem; color: var(--cea-muted); }
.field input { border: 1px solid var(--cea-border); border-radius: 10px; padding: 10px; background: #f8fbff; }
.cta { border: none; border-radius: 12px; background: linear-gradient(135deg, var(--cea-blue), var(--cea-blue-2)); color: #fff; padding: 12px; font-weight: 800; cursor: pointer; }
.tx-row { display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid #eef3fb; }
.tx-row:last-child { border-bottom: none; }
.tx-row strong { display: block; font-size: 0.88rem; color: var(--cea-text); }
.tx-row small { color: var(--cea-muted); font-size: 0.75rem; }
.credit { color: #16a34a; font-weight: 700; }
.debit { color: #dc2626; font-weight: 700; }
.ok { color: #166534; margin: 0; font-size: 0.82rem; }
.error { color: #b91c1c; margin: 0; font-size: 0.82rem; }
.empty { color: var(--cea-muted); font-size: 0.86rem; }
</style>
