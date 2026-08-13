<template>
  <div class="page">
    <section class="hero">
      <div>
        <p class="eyebrow">RBAC técnico</p>
        <h2>Matriz de acesso institucional</h2>
        <p>
          Visão técnica da segregação de funções, permissões por módulo e restrições
          mandatórias aplicadas ao ambiente interno da CEA INVESTIMENTOS.
        </p>
      </div>
    </section>

    <section>
      <h3 class="section-title">Matriz RBAC</h3>
      <div class="rbac-table">
        <div class="rbac-row rbac-row--head">
          <span>Função</span>
          <span>Investimentos</span>
          <span>Crédito</span>
          <span>Tesouraria</span>
          <span>Compliance</span>
          <span>ESG</span>
        </div>
        <div class="rbac-row" v-for="row in matrix" :key="row.role">
          <span>{{ row.role }}</span>
          <span>{{ row.investments }}</span>
          <span>{{ row.credit }}</span>
          <span>{{ row.treasury }}</span>
          <span>{{ row.compliance }}</span>
          <span>{{ row.esg }}</span>
        </div>
      </div>
    </section>

    <section class="grid-2">
      <article class="panel">
        <small>Regras técnicas</small>
        <h3>Controles obrigatórios</h3>
        <ul class="list">
          <li v-for="rule in technicalRules" :key="rule">{{ rule }}</li>
        </ul>
      </article>

      <article class="panel">
        <small>Escopos por camada</small>
        <h3>Mapeamento institucional</h3>
        <div class="timeline-list">
          <div class="timeline-item" v-for="layer in layers" :key="layer.name">
            <strong>{{ layer.name }}</strong>
            <span>{{ layer.scope }}</span>
          </div>
        </div>
      </article>
    </section>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { fetchRbacMatrix } from '../../services/liceuApi'

const matrix = ref([])
const technicalRules = ref([])
const layers = ref([])

onMounted(async () => {
  const data = await fetchRbacMatrix()
  matrix.value = data.matrix
  technicalRules.value = data.technical_rules
  layers.value = data.layers
})
</script>

<style scoped>
.rbac-table {
  display: grid;
  gap: 8px;
  margin-top: 20px;
}

.rbac-row {
  display: grid;
  grid-template-columns: 1.1fr repeat(5, 0.9fr);
  gap: 12px;
  padding: 12px 14px;
  border-radius: 12px;
  background: rgba(31, 59, 99, 0.05);
}

.rbac-row--head {
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

.timeline-item span {
  color: var(--muted);
}

@media (max-width: 1000px) {
  .rbac-row {
    grid-template-columns: 1fr;
  }
}
</style>
