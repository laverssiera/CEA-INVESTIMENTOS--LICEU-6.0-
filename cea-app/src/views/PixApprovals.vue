<template>
  <div class="container">
    <h2 class="screen-title">Aprovações PIX</h2>
    <p class="screen-subtitle">Fila institucional com segregação de função</p>

    <div v-if="!canApprove" class="blocked">
      Seu perfil não possui permissão para aprovar saques PIX.
    </div>

    <template v-else>
      <div class="toolbar">
        <div class="toolbar-left">
          <button class="refresh" :disabled="loading" @click="loadQueue">
            {{ loading ? 'Atualizando...' : 'Atualizar fila' }}
          </button>
          <router-link class="compliance-link" to="/pix-compliance">Ver compliance PIX</router-link>
        </div>
        <small>{{ queue.length }} pendência(s)</small>
      </div>

      <div v-if="!queue.length" class="empty">Nenhuma solicitação pendente.</div>

      <article class="card" v-for="w in queue" :key="w.wid">
        <header>
          <strong>{{ w.wid }}</strong>
          <span class="status" :class="w.status">{{ statusLabel(w.status) }}</span>
        </header>

        <div class="grid">
          <div><small>Usuário</small><p>{{ w.user_id }}</p></div>
          <div><small>Valor</small><p>{{ formatBRL(w.amount) }}</p></div>
          <div><small>Tipo chave</small><p>{{ (w.key_type || '-').toUpperCase() }}</p></div>
          <div><small>Criado em</small><p>{{ formatDate(w.created_at) }}</p></div>
        </div>

        <div class="approvals">
          <small>Aprovações: {{ w.approval_count || 0 }}/{{ w.required_approvals || 2 }}</small>
          <ul>
            <li v-for="a in (w.approved_by || [])" :key="`${w.wid}-${a.username}-${a.approved_at}`">
              {{ a.username }} ({{ a.role }}) · {{ formatDate(a.approved_at) }}
            </li>
          </ul>
        </div>

        <div class="actions">
          <button class="approve" :disabled="actingId === w.wid" @click="approve(w.wid)">
            {{ actingId === w.wid ? 'Processando...' : 'Aprovar' }}
          </button>
          <button class="reject" :disabled="actingId === w.wid" @click="reject(w.wid)">
            Rejeitar
          </button>
        </div>
      </article>

      <p v-if="feedback" class="ok">{{ feedback }}</p>
      <p v-if="errorMsg" class="error">{{ errorMsg }}</p>
    </template>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { auth } from '../store/auth.js'
import { approvePixWithdraw, fetchPendingWithdrawals, rejectPixWithdraw } from '../services/api.js'

const queue = ref([])
const loading = ref(false)
const actingId = ref('')
const feedback = ref('')
const errorMsg = ref('')

const canApprove = computed(() => ['admin', 'tesouraria', 'risk_manager'].includes(auth.role))

function formatBRL(v) {
  return (v ?? 0).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}

function formatDate(iso) {
  if (!iso) return '-'
  return new Date(iso).toLocaleString('pt-BR', {
    day: '2-digit', month: '2-digit', year: '2-digit',
    hour: '2-digit', minute: '2-digit',
  })
}

function statusLabel(status) {
  return {
    pending_approval: 'Pendente',
    approved_stage_1: '1ª Aprovação',
    settled: 'Liquidado',
    rejected: 'Rejeitado',
  }[status] ?? status
}

async function loadQueue() {
  if (!canApprove.value) return
  loading.value = true
  errorMsg.value = ''
  try {
    const data = await fetchPendingWithdrawals()
    queue.value = data.items ?? []
  } catch (e) {
    errorMsg.value = e.message
  } finally {
    loading.value = false
  }
}

async function approve(wid) {
  actingId.value = wid
  feedback.value = ''
  errorMsg.value = ''
  try {
    const res = await approvePixWithdraw(wid)
    feedback.value = `Solicitação ${wid}: ${statusLabel(res.status)}.`
    await loadQueue()
  } catch (e) {
    errorMsg.value = e.message
  } finally {
    actingId.value = ''
  }
}

async function reject(wid) {
  actingId.value = wid
  feedback.value = ''
  errorMsg.value = ''
  try {
    const res = await rejectPixWithdraw(wid)
    feedback.value = `Solicitação ${res.wid} rejeitada.`
    await loadQueue()
  } catch (e) {
    errorMsg.value = e.message
  } finally {
    actingId.value = ''
  }
}

onMounted(loadQueue)
</script>

<style scoped>
.blocked {
  border: 1px solid #fecaca;
  background: #fff1f2;
  color: #9f1239;
  border-radius: 14px;
  padding: 14px;
  font-size: 0.9rem;
  font-weight: 600;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.toolbar-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.refresh {
  border: 1px solid var(--cea-border);
  background: #f5f8ff;
  color: var(--cea-blue);
  border-radius: 10px;
  padding: 8px 12px;
  font-weight: 700;
  cursor: pointer;
}

.compliance-link {
  border: 1px solid var(--cea-border);
  background: #ffffff;
  color: var(--cea-blue-2);
  border-radius: 10px;
  padding: 8px 10px;
  font-size: 0.82rem;
  font-weight: 700;
  text-decoration: none;
}

.toolbar small { color: var(--cea-muted); }

.empty {
  text-align: center;
  color: var(--cea-muted);
  padding: 26px 0;
}

.card {
  background: #fff;
  border: 1px solid var(--cea-border);
  border-radius: 16px;
  padding: 14px;
  display: grid;
  gap: 10px;
  margin-bottom: 10px;
}

header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

header strong { color: var(--cea-text); }

.status {
  font-size: 0.74rem;
  font-weight: 800;
  border-radius: 999px;
  padding: 4px 10px;
}

.status.pending_approval { background: #fff7ed; color: #9a3412; }
.status.approved_stage_1 { background: #eff6ff; color: #1d4ed8; }

.grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

.grid small { color: var(--cea-muted); font-size: 0.75rem; }
.grid p { margin: 0; color: var(--cea-text); font-size: 0.86rem; font-weight: 600; }

.approvals small { color: var(--cea-muted); }
.approvals ul { margin: 6px 0 0; padding-left: 18px; color: var(--cea-text); font-size: 0.8rem; }

.actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

.approve, .reject {
  border: none;
  border-radius: 10px;
  padding: 10px;
  font-weight: 800;
  cursor: pointer;
}

.approve {
  background: linear-gradient(135deg, var(--cea-blue), var(--cea-blue-2));
  color: #fff;
}

.reject {
  background: #fee2e2;
  color: #b91c1c;
}

.ok { color: #166534; font-size: 0.85rem; font-weight: 700; }
.error { color: #b91c1c; font-size: 0.85rem; font-weight: 700; }
</style>
