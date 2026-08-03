<template>
  <div class="page">
    <section class="hero">
      <div>
        <p class="eyebrow">Comitê de crédito</p>
        <h2>Fila decisória e governança de aprovação</h2>
        <p>
          Ambiente institucional para leitura do pipeline crítico, composição do comitê,
          regras de aprovação dupla e agenda de deliberação.
        </p>
      </div>
      <div class="hero-grid">
        <div class="card" v-for="item in summary" :key="item.label">
          <small>{{ item.label }}</small>
          <div class="stat-value">{{ item.value }}</div>
          <span class="tag warning">{{ item.caption }}</span>
        </div>
      </div>
    </section>

    <section class="grid-2">
      <article class="panel">
        <small>Membros do comitê</small>
        <h3>Composição</h3>
        <div class="committee-grid">
          <div class="committee-member" v-for="member in members" :key="member.name">
            <strong>{{ member.name }}</strong>
            <span>{{ member.role }}</span>
            <small>{{ member.vote }}</small>
          </div>
        </div>
      </article>

      <article class="panel">
        <small>Regras decisórias</small>
        <h3>Governança de aprovação</h3>
        <ul class="list">
          <li v-for="rule in rules" :key="rule">{{ rule }}</li>
        </ul>
      </article>
    </section>

    <section>
      <h3 class="section-title">Fila do comitê</h3>
      <div class="committee-table">
        <div class="committee-row committee-row--head">
          <span>Projeto</span>
          <span>Valor</span>
          <span>Status</span>
          <span>Dupla aprovação</span>
        </div>
        <div class="committee-row" v-for="item in queue" :key="item.project">
          <span>{{ item.project }}</span>
          <span>{{ item.value }}</span>
          <span>{{ item.status }}</span>
          <span>{{ item.double_approval ? 'Sim' : 'Não' }}</span>
        </div>
      </div>
    </section>

    <section class="grid-2">
      <article class="panel">
        <small>Agenda</small>
        <h3>Rotina do comitê</h3>
        <ul class="list">
          <li v-for="agenda in schedule" :key="agenda.time + agenda.activity">{{ agenda.time }} — {{ agenda.activity }}</li>
        </ul>
      </article>

      <article class="panel">
        <small>Encaminhamento</small>
        <h3>Fluxo de aprovação</h3>
        <div class="flow-chain">
          <div v-for="step in flow" :key="step" class="flow-step">{{ step }}</div>
        </div>
      </article>
    </section>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { fetchCreditCommittee } from '../../services/liceuApi'

const summary = ref([])
const members = ref([])
const rules = ref([])
const queue = ref([])
const schedule = ref([])
const flow = ref([])

onMounted(async () => {
  const data = await fetchCreditCommittee()
  summary.value = data.summary
  members.value = data.members
  rules.value = data.rules
  queue.value = data.queue
  schedule.value = data.schedule
  flow.value = data.flow
})
</script>

<style scoped>
.committee-grid {
  display: grid;
  gap: 10px;
  margin-top: 12px;
}

.committee-member {
  display: grid;
  gap: 2px;
  padding: 12px 14px;
  border-radius: 12px;
  background: rgba(31, 59, 99, 0.05);
}

.committee-member strong {
  color: var(--deep);
}

.committee-member span,
.committee-member small {
  color: var(--muted);
}

.committee-table {
  display: grid;
  gap: 8px;
  margin-top: 20px;
}

.committee-row {
  display: grid;
  grid-template-columns: 1.3fr 0.8fr 0.8fr 0.8fr;
  gap: 12px;
  padding: 12px 14px;
  border-radius: 12px;
  background: rgba(31, 59, 99, 0.05);
}

.committee-row--head {
  font-weight: 700;
  color: var(--deep);
  background: rgba(13, 43, 82, 0.08);
}

.flow-chain {
  display: grid;
  gap: 10px;
  margin-top: 12px;
}

.flow-step {
  padding: 12px 14px;
  border-left: 3px solid var(--gold);
  background: rgba(31, 59, 99, 0.04);
  border-radius: 0 12px 12px 0;
  color: var(--deep);
  font-weight: 600;
}

@media (max-width: 800px) {
  .committee-row {
    grid-template-columns: 1fr;
  }
}
</style>
