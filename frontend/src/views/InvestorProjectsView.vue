<template>
  <div class="page">
    <section class="hero">
      <div>
        <p class="eyebrow">/investidor/projetos</p>
        <h2>Projetos em captação, execução e decisão de capital.</h2>
        <p>
          Cada projeto combina risco, CAPEX, OPEX, fluxo de caixa, NPV, IRR, payback, ROI e impacto estratégico.
        </p>
      </div>

      <div class="hero-grid">
        <div class="card">
          <small>Pipeline</small>
          <div class="stat-value">{{ projects.length }} ativos</div>
          <span class="tag info">Originação contínua</span>
        </div>
        <div class="card">
          <small>Decisão líder</small>
          <div class="stat-value">{{ topProjectLabel }}</div>
          <span class="tag warning">Ranking por capital score</span>
        </div>
      </div>
    </section>

    <section class="grid-3">
      <article v-for="project in projects" :key="project.project_name" class="card project-card">
        <div class="project-head">
          <div>
            <small>{{ project.rank ? `Rank ${project.rank}` : 'Projeto' }}</small>
            <h3>{{ project.project_name }}</h3>
          </div>
          <span class="tag" :class="project.decision === 'fund' ? 'success' : project.decision === 'review' ? 'warning' : 'info'">
            {{ project.decision }}
          </span>
        </div>

        <p>{{ project.location }}</p>

        <div class="metrics">
          <div><strong>CAPEX:</strong> {{ formatCurrency(project.capex) }}</div>
          <div><strong>OPEX:</strong> {{ formatCurrency(project.opex) }}</div>
          <div><strong>NPV:</strong> {{ formatCurrency(project.npv) }}</div>
          <div><strong>IRR:</strong> {{ formatPercent(project.irr) }}</div>
          <div><strong>Payback:</strong> {{ project.payback }} anos</div>
          <div><strong>ROI:</strong> {{ formatPercent(project.roi) }}</div>
          <div><strong>Risco:</strong> {{ project.risk?.level }} ({{ formatPercent(project.risk?.score) }})</div>
          <div><strong>Impacto:</strong> {{ formatPercent(project.impacto_estrategico?.score) }}</div>
        </div>

        <p class="summary">{{ project.impacto_estrategico?.summary }}</p>
      </article>
    </section>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { fetchEarthProjectExamples } from '../services/api'

const projects = ref([])

const topProjectLabel = ref('—')

const formatCurrency = (value) => {
  const amount = Number(value || 0)
  return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL', maximumFractionDigits: 0 }).format(amount)
}

const formatPercent = (value) => `${(Number(value || 0) * 100).toFixed(1)}%`

onMounted(async () => {
  try {
    const response = await fetchEarthProjectExamples()
    if (response?.projects?.length) {
      projects.value = response.projects
      topProjectLabel.value = response.recommended_project?.project_name || response.projects[0].project_name
    }
  } catch (e) {
    console.error(e)
  }
})
</script>

<style scoped>
.project-card {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.project-head {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: flex-start;
}

.metrics {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px 14px;
  font-size: 0.92rem;
  color: var(--muted);
}

.summary {
  margin-top: 4px;
  color: var(--deep);
}

@media (max-width: 720px) {
  .metrics {
    grid-template-columns: 1fr;
  }

  .project-head {
    flex-direction: column;
  }
}
</style>