<template>
  <div class="container">
    <h2 class="screen-title">Marketplace de Projetos</h2>
    <p class="screen-subtitle">Vitrine de oportunidades com captação aberta</p>

    <section class="cards-grid">
      <article class="project-card" v-for="p in projects" :key="p.project_id">
        <div class="pc-head">
          <h3>{{ p.title }}</h3>
          <span class="tag" :class="p.status">{{ p.status }}</span>
        </div>
        <p class="category">{{ p.category }}</p>

        <div class="metrics">
          <div><small>Meta</small><strong>{{ formatBRL(p.target_raise) }}</strong></div>
          <div><small>Captado</small><strong>{{ formatBRL(p.raised) }}</strong></div>
          <div><small>Yield est.</small><strong>{{ p.annual_yield_est }}% a.a.</strong></div>
          <div><small>Ticket mínimo</small><strong>{{ formatBRL(p.minimum_ticket) }}</strong></div>
        </div>

        <div class="bar-wrap">
          <div class="bar"><span :style="{ width: progressPct(p) + '%' }"></span></div>
          <small>{{ progressPct(p) }}% da captação</small>
        </div>

        <label class="ticket">
          <span>Investir (R$)</span>
          <input v-model.number="tickets[p.project_id]" type="number" :min="p.minimum_ticket" step="100" />
        </label>

        <button class="cta" :disabled="loadingId === p.project_id" @click="invest(p)">
          {{ loadingId === p.project_id ? 'Processando...' : 'Investir agora' }}
        </button>
      </article>
    </section>

    <section class="orders card">
      <h3>Minhas ordens</h3>
      <div v-if="!orders.length" class="empty">Nenhuma ordem no marketplace.</div>
      <div v-for="o in orders" :key="o.order_id" class="order-row">
        <div>
          <strong>{{ o.project_id }}</strong>
          <small>{{ formatDate(o.created_at) }}</small>
        </div>
        <span>{{ formatBRL(o.amount) }}</span>
      </div>
    </section>

    <p v-if="msg" class="ok">{{ msg }}</p>
    <p v-if="err" class="error">{{ err }}</p>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { fetchMarketplaceOrders, fetchMarketplaceProjects, investMarketplaceProject } from '../services/api.js'

const projects = ref([])
const orders = ref([])
const tickets = ref({})
const loadingId = ref('')
const msg = ref('')
const err = ref('')

function formatBRL(v) {
  return (v ?? 0).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}

function formatDate(iso) {
  return iso ? new Date(iso).toLocaleString('pt-BR', { day: '2-digit', month: '2-digit', year: '2-digit', hour: '2-digit', minute: '2-digit' }) : ''
}

function progressPct(p) {
  if (!p.target_raise) return 0
  return Math.min(100, Math.round((p.raised / p.target_raise) * 100))
}

async function loadData() {
  const [prj, ord] = await Promise.allSettled([fetchMarketplaceProjects(), fetchMarketplaceOrders()])
  projects.value = prj.status === 'fulfilled' ? (prj.value.items ?? []) : []
  orders.value = ord.status === 'fulfilled' ? (ord.value.items ?? []) : []
}

async function invest(project) {
  loadingId.value = project.project_id
  msg.value = ''
  err.value = ''
  try {
    const amount = Number(tickets.value[project.project_id] || project.minimum_ticket)
    const res = await investMarketplaceProject(project.project_id, amount)
    msg.value = `Ordem ${res.order_id} confirmada em ${project.title}.`
    await loadData()
  } catch (e) {
    err.value = e.message
  } finally {
    loadingId.value = ''
  }
}

onMounted(loadData)
</script>

<style scoped>
.cards-grid { display: grid; gap: 12px; }
.project-card { background: #fff; border: 1px solid var(--cea-border); border-radius: 16px; padding: 16px; display: grid; gap: 10px; }
.pc-head { display: flex; justify-content: space-between; align-items: center; gap: 8px; }
h3 { margin: 0; color: var(--cea-blue); font-size: 0.96rem; }
.tag { font-size: 0.72rem; font-weight: 800; border-radius: 999px; padding: 4px 10px; text-transform: uppercase; }
.tag.open { background: #dcfce7; color: #166534; }
.tag.funded { background: #e0e7ff; color: #3730a3; }
.category { margin: 0; font-size: 0.8rem; color: var(--cea-muted); }
.metrics { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
.metrics small { font-size: 0.72rem; color: var(--cea-muted); display: block; }
.metrics strong { font-size: 0.82rem; color: var(--cea-text); }
.bar-wrap { display: grid; gap: 5px; }
.bar { height: 8px; border-radius: 999px; background: #e5e7eb; overflow: hidden; }
.bar span { display: block; height: 100%; background: linear-gradient(135deg, var(--cea-blue), var(--cea-blue-2)); }
.bar-wrap small { font-size: 0.75rem; color: var(--cea-muted); }
.ticket { display: grid; gap: 5px; font-size: 0.8rem; color: var(--cea-muted); }
.ticket input { border: 1px solid var(--cea-border); border-radius: 10px; padding: 9px; background: #f8fbff; }
.cta { border: none; border-radius: 12px; background: linear-gradient(135deg, var(--cea-blue), var(--cea-blue-2)); color: #fff; padding: 12px; font-weight: 800; cursor: pointer; }
.card { background: #fff; border: 1px solid var(--cea-border); border-radius: 16px; padding: 16px; margin-top: 12px; }
.order-row { display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid #eef3fb; }
.order-row:last-child { border-bottom: none; }
.order-row strong { font-size: 0.86rem; color: var(--cea-text); display: block; }
.order-row small { font-size: 0.75rem; color: var(--cea-muted); }
.order-row span { font-weight: 700; color: var(--cea-blue); }
.ok { color: #166534; margin: 10px 2px 0; font-size: 0.83rem; }
.error { color: #b91c1c; margin: 10px 2px 0; font-size: 0.83rem; }
.empty { color: var(--cea-muted); font-size: 0.86rem; }
</style>
