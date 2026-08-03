<template>
  <div class="page">
    <section class="hero">
      <div>
        <p class="eyebrow">/investidor/projetos</p>
        <h2>Projetos em captação, execução e acompanhamento operacional.</h2>
        <p>
          Cada projeto combina estágio de obra, necessidade de funding, risco estimado e
          potencial de retorno esperado para o investidor.
        </p>
      </div>

      <div class="hero-grid">
        <div class="card">
          <small>Pipeline</small>
          <div class="stat-value">12 ativos</div>
          <span class="tag info">Originação contínua</span>
        </div>
        <div class="card">
          <small>Status médio</small>
          <div class="stat-value">Execução</div>
          <span class="tag warning">Monitoramento ativo</span>
        </div>
      </div>
    </section>

    <section class="grid-3">
      <article v-for="project in projects" :key="project.name" class="card">
        <small>{{ project.stage }}</small>
        <h3>{{ project.name }}</h3>
        <p>{{ project.location }}</p>
        <p><strong>Captação:</strong> {{ project.amount }}</p>
        <p><strong>Retorno estimado:</strong> {{ project.yield }}</p>
      </article>
    </section>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { fetchAssetsProjects } from '../services/liceuApi'

const projects = ref([
  { name: 'Residencial Nova Linha', stage: 'Captação', location: 'Campinas / SP', amount: 'R$ 18 mi', yield: 'CDI + 4,2%' },
  { name: 'Hub Logístico Litoral', stage: 'Execução', location: 'Santos / SP', amount: 'R$ 26 mi', yield: 'IPCA + 8,4%' },
  { name: 'Parque Industrial Vale', stage: 'Monitoramento', location: 'Betim / MG', amount: 'R$ 31 mi', yield: 'CDI + 5,1%' },
])

onMounted(async () => {
  try {
    const assets = await fetchAssetsProjects()
    if (assets?.active_projects?.length) {
      projects.value = assets.active_projects.map((name, i) => ({
        name,
        stage: ['Captação', 'Execução', 'Monitoramento', 'Pré-operação'][i % 4],
        location: '—',
        amount: `R$ ${((assets.valuation_brl / 1_000_000) / assets.active_projects.length).toFixed(0)} mi`,
        yield: 'CDI + 4%',
      }))
    }
  } catch (e) {
    console.error(e)
  }
})
</script>