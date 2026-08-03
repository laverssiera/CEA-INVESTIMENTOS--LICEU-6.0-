<template>
  <div class="page">
    <section class="hero">
      <div>
        <p class="eyebrow">Portal do Colaborador</p>
        <h2>Documentos internos</h2>
        <p>Base institucional para políticas e procedimentos operacionais.</p>
      </div>
    </section>

    <section>
      <h3 class="section-title">Biblioteca</h3>
      <div class="grid-2">
        <article class="card" v-for="doc in docs" :key="doc.title">
          <small>{{ doc.category }}</small>
          <h3>{{ doc.title }}</h3>
          <p>{{ doc.description }}</p>
          <span class="tag info">{{ doc.version }}</span>
        </article>
      </div>
    </section>
  </div>
</template>

<script setup>
const docs = [
  {
    category: 'Governança',
    title: 'Políticas internas',
    description: 'Normas institucionais de operação e segurança.',
    version: 'v2.1',
  },
  {
    category: 'Compliance',
    title: 'Manual compliance',
    description: 'Diretrizes de conduta e aderência regulatória.',
    version: 'v3.0',
  },
  {
    category: 'Crédito',
    title: 'Procedimentos de crédito',
    description: 'Fluxos e critérios para análise e aprovação.',
    version: 'v1.9',
  },
  {
    category: 'Sustentabilidade',
    title: 'ESG guidelines',
    description: 'Princípios ESG aplicados nas operações da CEA.',
    version: 'v1.4',
  },
]
</script>
