<template>
  <div class="container">
    <h2 class="screen-title">Compliance PIX</h2>
    <p class="screen-subtitle">KPIs, auditoria e reconciliação operacional em um único painel</p>

    <div v-if="!canView" class="blocked">
      Seu perfil não possui permissão para este dashboard.
    </div>

    <template v-else>
      <section class="card reconcile-card">
        <div>
          <h3>Reconciliação Manual</h3>
          <small>
            Última execução: {{ reconcileStatus.last_run ? formatDate(reconcileStatus.last_run) : 'nunca' }}
            · Intervalo automático: {{ reconcileStatus.interval_seconds || 300 }}s
          </small>
        </div>
        <button
          class="run"
          :disabled="reconciling || !canReconcile"
          @click="runReconcile"
        >
          {{ reconciling ? 'Processando...' : 'Rodar reconciliação agora' }}
        </button>
        <p v-if="reconcileMsg" class="ok">{{ reconcileMsg }}</p>
      </section>

      <section class="kpi-grid">
        <article class="kpi">
          <small>Volume PIX diário</small>
          <strong>{{ formatBRL(kpis.pix_volume_diario) }}</strong>
        </article>
        <article class="kpi">
          <small>Ticket médio</small>
          <strong>{{ formatBRL(kpis.ticket_medio) }}</strong>
        </article>
        <article class="kpi">
          <small>Conversão investimento</small>
          <strong>{{ kpis.conversao_investimento_pct ?? 0 }}%</strong>
        </article>
        <article class="kpi">
          <small>Saldo médio carteira</small>
          <strong>{{ formatBRL(kpis.saldo_medio_carteira) }}</strong>
        </article>
        <article class="kpi">
          <small>Liquidez</small>
          <strong>{{ kpis.liquidez_pct ?? 0 }}%</strong>
        </article>
        <article class="kpi">
          <small>Wallet bloqueado total</small>
          <strong>{{ formatBRL(kpis.wallet_bloqueado_total) }}</strong>
        </article>
      </section>

      <section class="card">
        <div class="audit-head">
          <h3>Auditoria PIX</h3>
          <button class="refresh" :disabled="loadingAudit" @click="loadAudit">
            {{ loadingAudit ? 'Atualizando...' : 'Atualizar' }}
          </button>
        </div>

        <div v-if="!audit.length" class="empty">Nenhum evento de auditoria disponível.</div>

        <div v-for="item in audit" :key="item.id" class="audit-row">
          <div>
            <strong>{{ item.action }}</strong>
            <small>{{ item.user }} · txid {{ item.txid }}</small>
          </div>
          <div class="right">
            <small>{{ item.ip }}</small>
            <small>{{ formatDate(item.timestamp) }}</small>
          </div>
        </div>
      </section>

      <p v-if="errorMsg" class="error">{{ errorMsg }}</p>
    </template>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { auth } from '../store/auth.js'
import {
  fetchPixAudit,
  fetchPixKpis,
  fetchPixReconcileStatus,
  runPixReconcile,
} from '../services/api.js'

const kpis = ref({})
const audit = ref([])
const reconcileStatus = ref({})

const loadingAudit = ref(false)
const reconciling = ref(false)
const errorMsg = ref('')
const reconcileMsg = ref('')

const canView = computed(() => ['admin', 'tesouraria', 'risk_manager', 'governance', 'compliance'].includes(auth.role))
const canReconcile = computed(() => ['admin', 'tesouraria', 'risk_manager', 'governance'].includes(auth.role))

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

async function loadKpis() {
  try {
    kpis.value = await fetchPixKpis()
  } catch {
    kpis.value = {}
  }
}

async function loadAudit() {
  loadingAudit.value = true
  try {
    const data = await fetchPixAudit()
    audit.value = (data.items ?? []).slice(0, 80)
  } catch {
    audit.value = []
  } finally {
    loadingAudit.value = false
  }
}

async function loadReconcileStatus() {
  try {
    reconcileStatus.value = await fetchPixReconcileStatus()
  } catch {
    reconcileStatus.value = {}
  }
}

async function runReconcile() {
  if (!canReconcile.value) return
  reconciling.value = true
  errorMsg.value = ''
  reconcileMsg.value = ''
  try {
    const res = await runPixReconcile()
    reconcileMsg.value = `Concluído: ${res.reconciled} conciliado(s), ${res.expired} expirado(s), ${res.already_processed} já processado(s).`
    await Promise.all([loadReconcileStatus(), loadKpis(), loadAudit()])
  } catch (e) {
    errorMsg.value = e.message
  } finally {
    reconciling.value = false
  }
}

onMounted(async () => {
  if (!canView.value) return
  await Promise.all([loadKpis(), loadAudit(), loadReconcileStatus()])
})
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

.card {
  background: #fff;
  border: 1px solid var(--cea-border);
  border-radius: 16px;
  padding: 14px;
  margin-bottom: 12px;
}

.reconcile-card {
  display: grid;
  gap: 10px;
}

h3 {
  margin: 0;
  color: var(--cea-blue);
  font-size: 0.94rem;
}

.reconcile-card small {
  color: var(--cea-muted);
}

.run {
  border: none;
  border-radius: 10px;
  background: linear-gradient(135deg, var(--cea-blue), var(--cea-blue-2));
  color: #fff;
  padding: 10px;
  font-weight: 800;
  cursor: pointer;
}

.run:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

.kpi-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin-bottom: 12px;
}

.kpi {
  background: #fff;
  border: 1px solid var(--cea-border);
  border-radius: 14px;
  padding: 12px;
  display: grid;
  gap: 4px;
}

.kpi small { font-size: 0.74rem; color: var(--cea-muted); }
.kpi strong { font-size: 0.95rem; color: var(--cea-text); }

.audit-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.refresh {
  border: 1px solid var(--cea-border);
  background: #f5f8ff;
  color: var(--cea-blue);
  border-radius: 8px;
  padding: 6px 10px;
  font-weight: 700;
  cursor: pointer;
}

.audit-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
  border-bottom: 1px solid #eef3fb;
  padding: 8px 0;
}

.audit-row:last-child { border-bottom: none; }
.audit-row strong { color: var(--cea-text); font-size: 0.84rem; display: block; }
.audit-row small { color: var(--cea-muted); font-size: 0.75rem; display: block; }
.right { text-align: right; }

.ok { color: #166534; font-size: 0.85rem; font-weight: 700; margin: 0; }
.error { color: #b91c1c; font-size: 0.85rem; font-weight: 700; }
.empty { color: var(--cea-muted); font-size: 0.86rem; }
</style>
