<template>
  <div class="container">
    <h2 class="screen-title">Split de Pagamentos</h2>
    <p class="screen-subtitle">Distribuição automática de receitas entre investidores do projeto</p>

    <!-- Formulário de novo split -->
    <div class="card">
      <h3>Novo split</h3>

      <label class="field">
        <span>ID do Projeto</span>
        <input v-model="form.project_id" placeholder="ex: PROJ-2026-A1" />
      </label>

      <label class="field">
        <span>Valor total (R$)</span>
        <input v-model="form.total_amount" type="number" step="0.01" min="1" placeholder="0,00" />
      </label>

      <label class="field">
        <span>Descrição (opcional)</span>
        <input v-model="form.description" placeholder="Receita de aluguel — Abril/26" />
      </label>

      <div class="recipients-header">
        <strong>Destinatários</strong>
        <button class="add-btn" @click="addRecipient">+ Adicionar</button>
      </div>

      <div
        v-for="(r, i) in form.recipients"
        :key="i"
        class="recipient-row"
      >
        <input v-model="r.user_id" placeholder="user_id" class="rec-id" />
        <input v-model="r.percentage" type="number" min="0.1" max="100" step="0.1" placeholder="%" class="rec-pct" />
        <button class="rm-btn" @click="removeRecipient(i)" :disabled="form.recipients.length <= 1">✕</button>
      </div>

      <div class="pct-status" :class="pctOk ? 'ok' : 'bad'">
        Total: <strong>{{ totalPct.toFixed(1) }}%</strong>
        {{ pctOk ? '✓ correto' : '— deve somar 100%' }}
      </div>

      <button class="cta" :disabled="!canSubmit || loading" @click="doSplit">
        {{ loading ? 'Distribuindo...' : 'Executar split' }}
      </button>

      <p v-if="errorMsg" class="error">{{ errorMsg }}</p>
    </div>

    <!-- Resultado do último split -->
    <div v-if="lastResult" class="result-card">
      <h3>Split executado ✔</h3>
      <p class="split-id">ID: <code>{{ lastResult.split_id }}</code></p>
      <div class="dist-row header">
        <span>Destinatário</span><span>%</span><span>Valor</span>
      </div>
      <div class="dist-row" v-for="r in lastResult.distributed" :key="r.user_id">
        <span>{{ r.user_id }}</span>
        <span>{{ r.percentage }}%</span>
        <span class="credit">+ {{ formatBRL(r.credited) }}</span>
      </div>
    </div>

    <!-- Histórico de splits -->
    <div class="history" v-if="history.length">
      <h3>Histórico</h3>
      <div class="hist-item" v-for="s in history" :key="s.split_id">
        <div>
          <strong>{{ s.project_id }}</strong>
          <small>{{ formatDate(s.executed_at) }} · {{ s.recipients.length }} destinatários</small>
        </div>
        <span class="credit">+ {{ formatBRL(s.total_amount) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'

const BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const form = ref({
  project_id: '',
  total_amount: '',
  description: '',
  recipients: [
    { user_id: '', percentage: '' },
    { user_id: '', percentage: '' },
  ],
})

const loading = ref(false)
const errorMsg = ref('')
const lastResult = ref(null)
const history = ref([])

const totalPct = computed(() =>
  form.value.recipients.reduce((s, r) => s + (parseFloat(r.percentage) || 0), 0)
)

const pctOk = computed(() => Math.abs(totalPct.value - 100) < 0.01)

const canSubmit = computed(() => {
  const proj = form.value.project_id.trim()
  const amt = parseFloat(form.value.total_amount)
  const filled = form.value.recipients.every((r) => r.user_id.trim() && parseFloat(r.percentage) > 0)
  return proj && amt >= 1 && pctOk.value && filled
})

function addRecipient() {
  form.value.recipients.push({ user_id: '', percentage: '' })
}

function removeRecipient(i) {
  if (form.value.recipients.length > 1) {
    form.value.recipients.splice(i, 1)
  }
}

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
  return iso ? new Date(iso).toLocaleString('pt-BR', { day: '2-digit', month: '2-digit', year: '2-digit', hour: '2-digit', minute: '2-digit' }) : ''
}

async function doSplit() {
  loading.value = true
  errorMsg.value = ''
  try {
    const body = {
      project_id: form.value.project_id.trim(),
      total_amount: parseFloat(form.value.total_amount),
      description: form.value.description.trim(),
      recipients: form.value.recipients.map((r) => ({
        user_id: r.user_id.trim(),
        percentage: parseFloat(r.percentage),
      })),
    }
    const res = await fetch(`${BASE}/api/projects/split`, {
      method: 'POST',
      headers: authHeaders(),
      body: JSON.stringify(body),
    })
    if (!res.ok) {
      const err = await res.json().catch(() => ({}))
      throw new Error(err.detail || `Erro ${res.status}`)
    }
    lastResult.value = await res.json()
    await loadHistory()

    // reset form
    form.value = { project_id: '', total_amount: '', description: '', recipients: [{ user_id: '', percentage: '' }, { user_id: '', percentage: '' }] }
  } catch (err) {
    errorMsg.value = err.message
  } finally {
    loading.value = false
  }
}

async function loadHistory() {
  try {
    const res = await fetch(`${BASE}/api/projects/splits`, { headers: authHeaders() })
    if (res.ok) {
      const data = await res.json()
      history.value = data.items ?? []
    }
  } catch { /* silent */ }
}

onMounted(loadHistory)
</script>

<style scoped>
h3 { font-size: 0.96rem; color: var(--cea-blue); margin: 0; }

.card {
  background: #fff;
  border: 1px solid var(--cea-border);
  border-radius: 18px;
  padding: 20px;
  display: grid;
  gap: 14px;
  box-shadow: 0 8px 20px rgba(13, 60, 143, 0.08);
  margin-bottom: 14px;
}

.field { display: grid; gap: 5px; font-size: 0.85rem; color: var(--cea-muted); }
.field input {
  border: 1px solid var(--cea-border);
  border-radius: 10px;
  padding: 10px 12px;
  font-size: 0.9rem;
  color: var(--cea-text);
  background: #f8fbff;
}
.field input:focus { outline: none; border-color: var(--cea-blue-2); }

.recipients-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.recipients-header strong { font-size: 0.88rem; color: var(--cea-text); }

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

.recipient-row {
  display: flex;
  gap: 8px;
  align-items: center;
}

.rec-id {
  flex: 1;
  border: 1px solid var(--cea-border);
  border-radius: 10px;
  padding: 8px 10px;
  font-size: 0.86rem;
  background: #f8fbff;
  color: var(--cea-text);
}

.rec-pct {
  width: 70px;
  border: 1px solid var(--cea-border);
  border-radius: 10px;
  padding: 8px 10px;
  font-size: 0.86rem;
  background: #f8fbff;
  color: var(--cea-text);
  text-align: center;
}

.rm-btn {
  color: #ef4444;
  background: #fee2e2;
  border: none;
  border-radius: 8px;
  width: 30px; height: 30px;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer;
  font-size: 0.8rem;
}
.rm-btn:disabled { opacity: 0.3; cursor: not-allowed; }

.pct-status { font-size: 0.82rem; padding: 8px 12px; border-radius: 10px; }
.pct-status.ok  { background: #dcfce7; color: #166534; }
.pct-status.bad { background: #fee2e2; color: #991b1b; }

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

.error { color: #b91c1c; font-size: 0.86rem; font-weight: 700; margin: 0; }

/* ── Resultado ── */
.result-card {
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  border-radius: 16px;
  padding: 18px;
  display: grid;
  gap: 10px;
  margin-bottom: 14px;
}

.split-id { font-size: 0.8rem; color: var(--cea-muted); margin: 0; }
.split-id code { color: var(--cea-blue); word-break: break-all; }

.dist-row {
  display: grid;
  grid-template-columns: 1fr 60px 100px;
  gap: 8px;
  font-size: 0.84rem;
  padding: 6px 0;
  border-bottom: 1px solid #d1fae5;
}
.dist-row:last-child { border-bottom: none; }
.dist-row.header { font-weight: 800; color: var(--cea-muted); font-size: 0.78rem; text-transform: uppercase; }
.dist-row span:last-child { text-align: right; }

.credit { color: #16a34a; font-weight: 700; }

/* ── Histórico ── */
.history { display: grid; gap: 8px; }

.hist-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #fff;
  border: 1px solid var(--cea-border);
  border-radius: 12px;
  padding: 12px 14px;
}

.hist-item strong { font-size: 0.88rem; color: var(--cea-text); display: block; }
.hist-item small  { font-size: 0.76rem; color: var(--cea-muted); }
</style>
