<template>
  <div class="page">
    <section class="hero">
      <div>
        <p class="eyebrow">Portal do Colaborador</p>
        <h2>Treinamentos</h2>
        <p>Capacitação contínua para equipes internas CEA.</p>
      </div>
    </section>

    <section>
      <h3 class="section-title">Trilhas</h3>
      <div class="grid-2">
        <article class="card" v-for="track in tracks" :key="track.title">
          <small>{{ track.level }}</small>
          <h3>{{ track.title }}</h3>
          <p>{{ track.description }}</p>
          <span class="tag info">{{ track.duration }}</span>
        </article>
      </div>
    </section>
  </div>
</template>

<script setup>
const tracks = [
  {
    level: 'Obrigatório',
    title: 'KYC / AML',
    description: 'Boas práticas de prevenção e monitoramento de risco.',
    duration: '2h',
  },
  {
    level: 'Essencial',
    title: 'ESG',
    description: 'Princípios ESG aplicados à operação financeira e crédito.',
    duration: '1h30',
  },
  {
    level: 'Funcional',
    title: 'Produtos financeiros',
    description: 'Portfólio CEA, originação, alocação e retorno.',
    duration: '2h15',
  },
  {
    level: 'Compliance',
    title: 'Compliance',
    description: 'Atualizações regulatórias e governança interna.',
    duration: '1h45',
  },
]
</script>
