<template>
  <div class="container">
    <h2 class="screen-title">Rendimentos</h2>
    <p class="screen-subtitle">Pagamentos automáticos por projeto investido</p>

    <!-- Total recebido -->
    <div class="summary-banner">
      <div>
        <small>Total recebido</small>
        <h2>{{ formatBRL(totalReceived) }}</h2>
      </div>
      <div>
        <small>Próximo pagamento</small>
        <h2 class="next">{{ nextLabel }}</h2>
      </div>
    </div>

    <!-- Tabs -->
    <div class="tabs">
      <button :class="{ active: tab === 'received' }" @click="tab = 'received'">Recebidos</button>
      <button :class="{ active: tab === 'schedules' }" @click="tab = 'schedules'">Agendamentos</button>
      <button v-if="isAdmin" :class="{ active: tab === 'admin' }" @click="tab = 'admin'">Admin</button>
    </div>

    <!-- Rendimentos recebidos -->
    <section v-if="tab === 'received'">
      <div v-if="!payments.length" class="empty">Nenhum rendimento recebido ainda.</div>
      <div class="yield-item" v-for="p in payments" :key="p.payment_id">
        <div class="yi-left">
          <div class="yi-icon">◈</div>
          <div>
            <strong>{{ p.project_id }}</strong>
            <small>{{ formatDate(p.paid_at) }}</small>
          </div>
        </div>
        <div class="yi-right">
          <span class="credit">+ {{ formatBRL(p.my_amount) }}</span>
          <small>{{ p.investors?.find(i => i.user_id === userId)?.rate ?? '—' }}% a.m.</small>
        </div>
      </div>
    </section>

    <!-- Agendamentos ativos -->
    <section v-else-if="tab === 'schedules'">
      <div v-if="!schedules.length" class="empty">Nenhum agendamento ativo.</div>
      <div class="sched-item" v-for="s in schedules" :key="s.schedule_id">
        <div class="si-header">
          <strong>{{ s.project_id }}</strong>
          <span class="badge" :class="s.active ? 'active' : 'inactive'">
            {{ s.active ? 'Ativo' : 'Inativo' }}
          </span>
        </div>
        <div class="si-details">
          <span>{{ s.rate }}% · {{ freqLabel(s.frequency) }}</span>
          <span>{{ s.investors?.length ?? 0 }} investidores</span>
        </div>
        <div class="si-last" v-if="s.last_paid_at">
          Último pagamento: {{ formatDate(s.last_paid_at) }}
        </div>
        <button v-if="isAdmin" class="pay-btn" @click="triggerPay(s.schedule_id)">
          Disparar pagamento
        </button>
      </div>
    </section>

    <!-- Admin: novo agendamento -->
    <section v-else-if="tab === 'admin'" class="admin-section">
      <div class="card">
        <h3>Criar agendamento de rendimentos</h3>

        <label class="field">
          <span>ID do Projeto</span>
          <input v-model="schedForm.project_id" placeholder="PROJ-2026-A1" />
        </label>

        <label class="field">
          <span>Taxa (% a.m.)</span>
          <input v-model="schedForm.rate" type="number" step="0.01" min="0.01" placeholder="1.20" />
        </label>

        <label class="field">
          <span>Frequência</span>
          <select v-model="schedForm.frequency">
            <option value="monthly">Mensal</option>
            <option value="weekly">Semanal</option>
            <option value="daily">Diária</option>
          </select>
        </label>

        <div class="investors-header">
          <strong>Investidores e capital</strong>
          <button class="add-btn" @click="addInvestor">+ Adicionar</button>
        </div>

        <div class="inv-row" v-for="(inv, i) in schedForm.investors" :key="i">
          <input v-model="inv.user_id" placeholder="user_id" />
          <input v-model="inv.principal" type="number" step="100" min="1" placeholder="Capital R$" />
          <button class="rm-btn" @click="schedForm.investors.splice(i, 1)" :disabled="schedForm.investors.length <= 1">✕</button>
        </div>

        <button class="cta" :disabled="!canCreateSched || schedLoading" @click="createSchedule">
          {{ schedLoading ? 'Criando...' : 'Criar agendamento' }}
        </button>

        <p v-if="schedError" class="error">{{ schedError }}</p>
        <p v-if="schedSuccess" class="ok-msg">{{ schedSuccess }}</p>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { auth } from '../store/auth.js'

const BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const tab = ref('received')
const payments = ref([])
const schedules = ref([])
const userId = computed(() => auth.name ?? 'demo')
const isAdmin = computed(() => auth.role === 'admin' || auth.role === 'tesouraria' || auth.role === 'risk_manager')

const totalReceived = computed(() => payments.value.reduce((s, p) => s + (p.my_amount ?? 0), 0))
const nextLabel = computed(() => {
  const active = schedules.value.filter((s) => s.active)
  if (!active.length) return '—'
  return 'No agendamento'
})

const schedForm = ref({
  project_id: '',
  rate: '',
  frequency: 'monthly',
  investors: [{ user_id: '', principal: '' }],
})
const schedLoading = ref(false)
const schedError = ref('')
const schedSuccess = ref('')

const canCreateSched = computed(() => {
  return schedForm.value.project_id.trim() &&
    parseFloat(schedForm.value.rate) > 0 &&
    schedForm.value.investors.every((i) => i.user_id.trim() && parseFloat(i.principal) > 0)
})

function freqLabel(f) {
  return { monthly: 'Mensal', weekly: 'Semanal', daily: 'Diária' }[f] ?? f
}

function formatBRL(v) {
  return (v ?? 0).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}

function formatDate(iso) {
  return iso ? new Date(iso).toLocaleString('pt-BR', { day: '2-digit', month: '2-digit', year: '2-digit', hour: '2-digit', minute: '2-digit' }) : ''
}

function getToken() {
  try { return JSON.parse(localStorage.getItem('cea.auth') ?? '{}').token } catch { return null }
}

function authHeaders() {
  const t = getToken()
  return { 'Content-Type': 'application/json', ...(t ? { Authorization: `Bearer ${t}` } : {}) }
}

function addInvestor() { schedForm.value.investors.push({ user_id: '', principal: '' }) }

onMounted(async () => {
  const [p, s] = await Promise.allSettled([
    fetch(`${BASE}/api/yields/payments`, { headers: authHeaders() }),
    fetch(`${BASE}/api/yields/schedules`, { headers: authHeaders() }),
  ])
  if (p.status === 'fulfilled' && p.value.ok) {
    const d = await p.value.json(); payments.value = d.items ?? []
  }
  if (s.status === 'fulfilled' && s.value.ok) {
    const d = await s.value.json(); schedules.value = d.items ?? []
  }
})

async function triggerPay(scheduleId) {
  try {
    const res = await fetch(`${BASE}/api/yields/pay`, {
      method: 'POST',
      headers: authHeaders(),
      body: JSON.stringify({ schedule_id: scheduleId }),
    })
    if (!res.ok) throw new Error((await res.json().catch(() => ({}))).detail || 'Erro')
    const d = await res.json()
    alert(`Rendimentos pagos para ${d.investors_paid} investidores!`)
    // recarregar
    const r = await fetch(`${BASE}/api/yields/payments`, { headers: authHeaders() })
    if (r.ok) { const dd = await r.json(); payments.value = dd.items ?? [] }
  } catch (err) {
    alert(err.message)
  }
}

async function createSchedule() {
  schedLoading.value = true
  schedError.value = ''
  schedSuccess.value = ''
  try {
    const body = {
      project_id: schedForm.value.project_id.trim(),
      rate: parseFloat(schedForm.value.rate),
      frequency: schedForm.value.frequency,
      investors: schedForm.value.investors.map((i) => ({
        user_id: i.user_id.trim(),
        principal: parseFloat(i.principal),
      })),
    }
    const res = await fetch(`${BASE}/api/yields/schedule`, {
      method: 'POST',
      headers: authHeaders(),
      body: JSON.stringify(body),
    })
    if (!res.ok) {
      const err = await res.json().catch(() => ({}))
      throw new Error(err.detail || `Erro ${res.status}`)
    }
    const d = await res.json()
    schedSuccess.value = `Agendamento ${d.schedule_id} criado!`
    schedules.value.unshift(d)
    schedForm.value = { project_id: '', rate: '', frequency: 'monthly', investors: [{ user_id: '', principal: '' }] }
  } catch (err) {
    schedError.value = err.message
  } finally {
    schedLoading.value = false
  }
}
</script>

<style scoped>
h3 { font-size: 0.96rem; color: var(--cea-blue); margin: 0; }

.summary-banner {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1px;
  background: var(--cea-border);
  border: 1px solid var(--cea-border);
  border-radius: 16px;
  overflow: hidden;
  margin-bottom: 16px;
}

.summary-banner > div {
  background: #fff;
  padding: 16px;
  display: grid;
  gap: 4px;
}

.summary-banner small { font-size: 0.75rem; color: var(--cea-muted); text-transform: uppercase; letter-spacing: 0.04em; }
.summary-banner h2 { font-family: Sora, sans-serif; font-size: 1.2rem; color: var(--cea-text); margin: 0; }
.next { color: var(--cea-blue-2); }

/* ── Tabs ── */
.tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}
.tabs button {
  flex: 1;
  border: 1px solid var(--cea-border);
  border-radius: 999px;
  background: #f5f8ff;
  color: var(--cea-muted);
  padding: 9px;
  font-size: 0.84rem;
  font-weight: 700;
  cursor: pointer;
}
.tabs button.active {
  background: var(--cea-blue);
  color: #fff;
  border-color: var(--cea-blue);
}

/* ── Itens ── */
.yield-item, .sched-item {
  background: #fff;
  border: 1px solid var(--cea-border);
  border-radius: 14px;
  padding: 14px;
  margin-bottom: 8px;
  box-shadow: 0 2px 6px rgba(13,60,143,0.05);
}

.yield-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.yi-left { display: flex; align-items: center; gap: 10px; }
.yi-icon {
  width: 36px; height: 36px;
  border-radius: 50%;
  background: #fef9c3;
  color: #ca8a04;
  display: flex; align-items: center; justify-content: center;
  font-size: 1rem;
}
.yi-left strong { font-size: 0.88rem; color: var(--cea-text); display: block; }
.yi-left small  { font-size: 0.76rem; color: var(--cea-muted); }
.yi-right { text-align: right; }
.yi-right small { font-size: 0.76rem; color: var(--cea-muted); display: block; }

.credit { color: #16a34a; font-weight: 700; font-size: 0.95rem; }

.si-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }
.si-header strong { font-size: 0.9rem; color: var(--cea-text); }

.badge { font-size: 0.72rem; font-weight: 800; padding: 3px 10px; border-radius: 999px; }
.badge.active   { background: #dcfce7; color: #166534; }
.badge.inactive { background: #f3f4f6; color: #6b7280; }

.si-details { display: flex; gap: 16px; font-size: 0.82rem; color: var(--cea-muted); margin-bottom: 6px; }
.si-last { font-size: 0.78rem; color: var(--cea-muted); }

.pay-btn {
  margin-top: 10px;
  width: 100%;
  border: 1px solid var(--cea-blue);
  border-radius: 10px;
  background: #e8f0ff;
  color: var(--cea-blue);
  padding: 10px;
  font-weight: 800;
  font-size: 0.85rem;
  cursor: pointer;
}
.pay-btn:hover { background: #d0e4ff; }

/* ── Admin ── */
.card {
  background: #fff;
  border: 1px solid var(--cea-border);
  border-radius: 18px;
  padding: 20px;
  display: grid;
  gap: 14px;
  box-shadow: 0 8px 20px rgba(13, 60, 143, 0.08);
}

.field { display: grid; gap: 5px; font-size: 0.85rem; color: var(--cea-muted); }
.field input, .field select {
  border: 1px solid var(--cea-border);
  border-radius: 10px;
  padding: 10px 12px;
  font-size: 0.9rem;
  background: #f8fbff;
  color: var(--cea-text);
}

.investors-header { display: flex; justify-content: space-between; align-items: center; }
.investors-header strong { font-size: 0.88rem; color: var(--cea-text); }

.add-btn {
  font-size: 0.8rem;
  font-weight: 800;
  color: var(--cea-blue-2);
  background: #e8f0ff;
  border: none;
  border-radius: 8px;
  padding: 5px 10px;
  cursor: pointer;
}

.inv-row {
  display: flex;
  gap: 8px;
  align-items: center;
}
.inv-row input {
  flex: 1;
  border: 1px solid var(--cea-border);
  border-radius: 10px;
  padding: 8px 10px;
  font-size: 0.86rem;
  background: #f8fbff;
}

.rm-btn {
  color: #ef4444;
  background: #fee2e2;
  border: none;
  border-radius: 8px;
  width: 30px; height: 30px;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer;
}
.rm-btn:disabled { opacity: 0.3; cursor: not-allowed; }

.cta {
  border: none;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--cea-blue), var(--cea-blue-2));
  color: #fff;
  padding: 13px;
  font-weight: 800;
  cursor: pointer;
  box-shadow: 0 8px 18px rgba(13, 60, 143, 0.22);
}
.cta:disabled { opacity: 0.5; cursor: not-allowed; }
.cta:hover:not(:disabled) { transform: translateY(-1px); }

.error  { color: #b91c1c; font-size: 0.86rem; font-weight: 700; margin: 0; }
.ok-msg { color: #166534; font-size: 0.86rem; font-weight: 700; margin: 0; }

.empty {
  text-align: center;
  color: var(--cea-muted);
  padding: 32px 0;
  font-size: 0.9rem;
}
</style>
