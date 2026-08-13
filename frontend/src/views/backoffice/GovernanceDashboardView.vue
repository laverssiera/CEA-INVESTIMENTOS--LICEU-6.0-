<template>
  <div class="page">
    <section class="hero">
      <div>
        <p class="eyebrow">Governança institucional</p>
        <h2>Dashboard de governança e controles</h2>
        <p>
          Visão consolidada da estrutura institucional, SLAs operacionais, indicadores-chave
          e trilha de controle para comitês, risco, auditoria e ESG governance.
        </p>
      </div>

      <div class="hero-grid">
        <div class="card" v-for="item in summary" :key="item.label">
          <small>{{ item.label }}</small>
          <div class="stat-value">{{ item.value }}</div>
          <span class="tag info">{{ item.caption }}</span>
        </div>
      </div>
    </section>

    <section>
      <h3 class="section-title">Camadas operacionais</h3>
      <div class="grid-3">
        <article class="card" v-for="layer in layers" :key="layer.title">
          <small>{{ layer.tag }}</small>
          <h3>{{ layer.title }}</h3>
          <p>{{ layer.description }}</p>
          <ul class="list">
            <li v-for="role in layer.roles" :key="role">{{ role }}</li>
          </ul>
        </article>
      </div>
    </section>

    <section class="grid-2">
      <article class="panel">
        <small>SLA institucional</small>
        <h3>Monitoramento operacional</h3>
        <div class="governance-table">
          <div class="governance-row governance-row--head">
            <span>Processo</span>
            <span>SLA</span>
          </div>
          <div class="governance-row" v-for="sla in slas" :key="sla.process">
            <span>{{ sla.process }}</span>
            <span>{{ sla.target }}</span>
          </div>
        </div>
      </article>

      <article class="panel">
        <small>Indicadores operacionais</small>
        <h3>Painel institucional</h3>
        <div class="grid-2" style="margin-top: 12px;">
          <article class="stat-card" v-for="metric in metrics" :key="metric.label">
            <small>{{ metric.label }}</small>
            <div class="stat-value">{{ metric.value }}</div>
          </article>
        </div>
      </article>
    </section>

    <section class="grid-2">
      <article class="panel">
        <small>Trilha de auditoria</small>
        <h3>Eventos recentes</h3>
        <div class="timeline-list">
          <div class="timeline-item" v-for="event in auditTrail" :key="event.timestamp + event.action">
            <strong>{{ event.action }}</strong>
            <span>{{ event.user }} · {{ event.module }}</span>
            <small>{{ event.timestamp }}</small>
          </div>
        </div>
      </article>

      <article class="panel">
        <small>Controles mandatórios</small>
        <h3>Governança ativa</h3>
        <ul class="list">
          <li v-for="control in controls" :key="control">{{ control }}</li>
        </ul>
      </article>
    </section>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { fetchGovernanceDashboard } from '../../services/liceuApi'

const summary = ref([])
const layers = ref([])
const slas = ref([])
const metrics = ref([])
const auditTrail = ref([])
const controls = ref([])

onMounted(async () => {
  const data = await fetchGovernanceDashboard()
  summary.value = data.summary
  layers.value = data.layers
  slas.value = data.sla
  metrics.value = data.metrics
  auditTrail.value = data.audit_trail
  controls.value = data.controls
})
</script>

<style scoped>
.governance-table {
  display: grid;
  gap: 8px;
  margin-top: 12px;
}

.governance-row {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 12px;
  padding: 12px 14px;
  border-radius: 12px;
  background: rgba(31, 59, 99, 0.05);
}

.governance-row--head {
  font-weight: 700;
  color: var(--deep);
  background: rgba(13, 43, 82, 0.08);
}

.timeline-list {
  display: grid;
  gap: 10px;
  margin-top: 12px;
}

.timeline-item {
  display: grid;
  gap: 4px;
  padding: 12px 14px;
  border-left: 3px solid var(--gold);
  background: rgba(31, 59, 99, 0.04);
  border-radius: 0 12px 12px 0;
}

.timeline-item strong {
  color: var(--deep);
}

.timeline-item span,
.timeline-item small {
  color: var(--muted);
}
</style>
