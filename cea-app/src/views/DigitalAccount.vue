<template>
  <div class="container">
    <h2 class="screen-title">Conta Digital CEA</h2>
    <p class="screen-subtitle">Sua conta de investimentos com carteira digital integrada</p>

    <!-- Cabeçalho da conta -->
    <div class="account-header" v-if="account">
      <div class="account-badge">
        <span class="bank-logo">CEA</span>
        <div>
          <p class="bank-name">CEA Investimentos</p>
          <p class="acc-info">Ag {{ account.agency }} · C/C {{ account.account_number }}</p>
        </div>
      </div>
      <div class="balance-block">
        <small>Saldo disponível</small>
        <h1>{{ formatBRL(account.balance) }}</h1>
        <span class="updated">Atualizado {{ timeAgo(account.updated_at) }}</span>
      </div>
      <div class="quick-actions">
        <router-link to="/deposit" class="qa-btn green">
          <span>↓</span> Depositar
        </router-link>
        <router-link to="/withdraw" class="qa-btn red">
          <span>↑</span> Sacar
        </router-link>
      </div>
    </div>

    <div v-if="account" class="balance-metrics">
      <div>
        <small>Disponível</small>
        <strong>{{ formatBRL(account.balance) }}</strong>
      </div>
      <div>
        <small>Bloqueado</small>
        <strong>{{ formatBRL(account.locked || 0) }}</strong>
      </div>
      <div>
        <small>Total</small>
        <strong>{{ formatBRL(account.total || account.balance) }}</strong>
      </div>
    </div>

    <!-- Filtros de extrato -->
    <div class="filters">
      <button
        v-for="f in filters"
        :key="f.value"
        :class="{ active: activeFilter === f.value }"
        @click="activeFilter = f.value"
      >{{ f.label }}</button>
    </div>

    <!-- Extrato -->
    <div class="statement" v-if="!loadingStatement">
      <div v-if="filteredEntries.length === 0" class="empty">
        Nenhuma movimentação encontrada.
      </div>

      <div
        v-for="entry in filteredEntries"
        :key="entry.id"
        class="entry"
        :class="entry.type"
      >
        <div class="entry-icon">{{ typeIcon(entry.type) }}</div>
        <div class="entry-info">
          <strong>{{ entry.label }}</strong>
          <small>{{ formatDate(entry.at) }}</small>
        </div>
        <div class="entry-amount" :class="entry.sign === '+' ? 'credit' : 'debit'">
          {{ entry.sign }} {{ formatBRL(entry.amount) }}
        </div>
      </div>
    </div>

    <div v-else class="loading">Carregando extrato...</div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'

const BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const account = ref(null)
const entries = ref([])
const loadingStatement = ref(true)
const activeFilter = ref('all')

const filters = [
  { label: 'Tudo', value: 'all' },
  { label: 'Depósitos', value: 'deposit' },
  { label: 'Saques', value: 'withdraw' },
  { label: 'Rendimentos', value: 'yield' },
  { label: 'Splits', value: 'split' },
]

const filteredEntries = computed(() =>
  activeFilter.value === 'all'
    ? entries.value
    : entries.value.filter((e) => e.type === activeFilter.value)
)

function getToken() {
  try { return JSON.parse(localStorage.getItem('cea.auth') ?? '{}').token } catch { return null }
}

function authHeaders() {
  const t = getToken()
  return { 'Content-Type': 'application/json', ...(t ? { Authorization: `Bearer ${t}` } : {}) }
}

function formatBRL(v) {
  return (v ?? 0).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}

function formatDate(iso) {
  if (!iso) return ''
  return new Date(iso).toLocaleString('pt-BR', {
    day: '2-digit', month: '2-digit', year: '2-digit',
    hour: '2-digit', minute: '2-digit',
  })
}

function timeAgo(iso) {
  if (!iso) return ''
  const diff = Date.now() - new Date(iso).getTime()
  if (diff < 60_000) return 'agora mesmo'
  if (diff < 3_600_000) return `há ${Math.floor(diff / 60_000)} min`
  return `há ${Math.floor(diff / 3_600_000)}h`
}

const TYPE_ICONS = {
  deposit: '↓', withdraw: '↑', yield: '◈', split: '⊕',
}
function typeIcon(type) { return TYPE_ICONS[type] ?? '·' }

onMounted(async () => {
  const [det, stm] = await Promise.allSettled([
    fetch(`${BASE}/api/account/details`, { headers: authHeaders() }),
    fetch(`${BASE}/api/account/statement`, { headers: authHeaders() }),
  ])

  if (det.status === 'fulfilled' && det.value.ok) {
    account.value = await det.value.json()
  } else {
    // fallback demo
    account.value = { agency: '0001', account_number: '0123456-7', bank_name: 'CEA Investimentos', balance: 0, updated_at: new Date().toISOString() }
  }

  if (stm.status === 'fulfilled' && stm.value.ok) {
    const data = await stm.value.json()
    entries.value = data.entries ?? []
    if (account.value) {
      account.value.balance = data.balance ?? account.value.balance
      account.value.locked = data.locked ?? account.value.locked ?? 0
      account.value.total = data.total ?? (account.value.balance + (account.value.locked || 0))
    }
  }

  loadingStatement.value = false
})
</script>

<style scoped>
.account-header {
  background: linear-gradient(160deg, #061d50, #0d3c8f 60%, #1f66dc);
  border-radius: 20px;
  padding: 22px;
  display: grid;
  gap: 18px;
  box-shadow: 0 16px 32px rgba(6, 29, 80, 0.3);
  margin-bottom: 16px;
}

.account-badge {
  display: flex;
  align-items: center;
  gap: 12px;
}

.bank-logo {
  background: rgba(255,255,255,0.15);
  color: #fff;
  font-family: Sora, sans-serif;
  font-weight: 900;
  font-size: 0.88rem;
  padding: 8px 10px;
  border-radius: 10px;
  letter-spacing: 0.06em;
}

.bank-name { color: #fff; font-weight: 700; font-size: 0.88rem; margin: 0 0 2px; }
.acc-info { color: #8faed4; font-size: 0.78rem; margin: 0; }

.balance-block { display: grid; gap: 3px; }
.balance-block small { color: #8faed4; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.05em; }
.balance-block h1 { color: #fff; font-family: Sora, sans-serif; font-size: 1.7rem; margin: 0; }
.updated { color: #5a8ccc; font-size: 0.73rem; }

.quick-actions { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }

.balance-metrics {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 1px;
  background: var(--cea-border);
  border: 1px solid var(--cea-border);
  border-radius: 14px;
  overflow: hidden;
  margin-bottom: 14px;
}

.balance-metrics > div {
  background: #fff;
  padding: 10px 12px;
  display: grid;
  gap: 2px;
}

.balance-metrics small {
  font-size: 0.72rem;
  color: var(--cea-muted);
  text-transform: uppercase;
}

.balance-metrics strong {
  font-size: 0.88rem;
  color: var(--cea-text);
}

.qa-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  border-radius: 12px;
  padding: 11px;
  font-weight: 800;
  font-size: 0.88rem;
  text-decoration: none;
}

.qa-btn.green { background: rgba(22, 163, 74, 0.2); color: #4ade80; }
.qa-btn.red   { background: rgba(220, 38, 38, 0.2); color: #f87171; }
.qa-btn:hover { filter: brightness(1.15); }
.qa-btn span  { font-size: 1.1rem; }

/* ── Filtros ── */
.filters {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  padding-bottom: 4px;
  margin-bottom: 14px;
  scrollbar-width: none;
}

.filters button {
  flex-shrink: 0;
  border: 1px solid var(--cea-border);
  border-radius: 999px;
  background: #f5f8ff;
  color: var(--cea-muted);
  padding: 7px 14px;
  font-size: 0.82rem;
  font-weight: 700;
  cursor: pointer;
}

.filters button.active {
  background: var(--cea-blue);
  color: #fff;
  border-color: var(--cea-blue);
}

/* ── Extrato ── */
.statement { display: grid; gap: 4px; }

.entry {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 14px;
  background: #fff;
  border: 1px solid var(--cea-border);
  border-radius: 14px;
  box-shadow: 0 2px 6px rgba(13, 60, 143, 0.05);
}

.entry-icon {
  width: 38px; height: 38px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  flex-shrink: 0;
}

.entry.deposit .entry-icon  { background: #dcfce7; color: #16a34a; }
.entry.withdraw .entry-icon { background: #fee2e2; color: #dc2626; }
.entry.yield .entry-icon    { background: #fef9c3; color: #ca8a04; }
.entry.split .entry-icon    { background: #e0f2fe; color: #0284c7; }

.entry-info { flex: 1; }
.entry-info strong { font-size: 0.88rem; color: var(--cea-text); display: block; }
.entry-info small  { font-size: 0.76rem; color: var(--cea-muted); }

.entry-amount { font-weight: 800; font-size: 0.92rem; white-space: nowrap; }
.credit { color: #16a34a; }
.debit  { color: #dc2626; }

.empty {
  text-align: center;
  color: var(--cea-muted);
  padding: 32px 0;
  font-size: 0.9rem;
}

.loading {
  text-align: center;
  color: var(--cea-muted);
  padding: 32px 0;
  font-size: 0.9rem;
}
</style>
