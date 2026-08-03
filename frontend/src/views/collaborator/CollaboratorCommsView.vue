<template>
  <div class="page">
    <section class="hero">
      <div>
        <p class="eyebrow">Portal do Colaborador</p>
        <h2>Comunicados internos</h2>
        <p>Atualizações oficiais para equipes da CEA INVESTIMENTOS.</p>
      </div>
    </section>

    <section>
      <h3 class="section-title">Comunicados recentes</h3>
      <div class="grid-2">
        <article class="panel" v-for="item in items" :key="item.title">
          <small>{{ item.date }}</small>
          <h3>{{ item.title }}</h3>
          <p>{{ item.text }}</p>
          <span class="tag warning">{{ item.type }}</span>
        </article>
      </div>
    </section>
  </div>
</template>

<script setup>
const items = [
  {
    date: '13/04/2026',
    title: 'Aviso da diretoria',
    text: 'Reforço das metas operacionais para o trimestre e foco em eficiência.',
    type: 'Institucional',
  },
  {
    date: '12/04/2026',
    title: 'Atualização regulatória',
    text: 'Novas recomendações de adequação para trilhas de KYC/AML.',
    type: 'Compliance',
  },
  {
    date: '11/04/2026',
    title: 'Atualizações LICEU',
    text: 'Novos dashboards de progresso de obra já disponíveis para consulta.',
    type: 'Operação',
  },
]
</script>
