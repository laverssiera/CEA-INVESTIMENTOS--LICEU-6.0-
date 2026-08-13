<template>
  <div class="page">
    <section class="hero">
      <div>
        <p class="eyebrow">Portal do Colaborador</p>
        <h2>Tarefas internas</h2>
        <p>Gestão de backlog operacional por área e prioridade.</p>
      </div>
    </section>

    <section>
      <h3 class="section-title">Fila de tarefas</h3>
      <div class="grid-2">
        <article class="panel" v-for="task in tasks" :key="task.title">
          <small>{{ task.area }}</small>
          <h3>{{ task.title }}</h3>
          <p>{{ task.description }}</p>
          <span class="tag" :class="task.tagClass">{{ task.priority }}</span>
        </article>
      </div>
    </section>
  </div>
</template>

<script setup>
const tasks = [
  {
    area: 'Crédito',
    title: 'Aprovação de crédito',
    description: 'Validar dossiê de financiamento e checklist regulatório.',
    priority: 'Alta',
    tagClass: 'critical',
  },
  {
    area: 'Compliance',
    title: 'Revisão KYC',
    description: 'Atualização cadastral e monitoramento de inconsistências.',
    priority: 'Alta',
    tagClass: 'warning',
  },
  {
    area: 'Relacionamento',
    title: 'Follow-up clientes',
    description: 'Contato com clientes com pendências documentais.',
    priority: 'Média',
    tagClass: 'info',
  },
  {
    area: 'Investimentos',
    title: 'Análise de projetos',
    description: 'Avaliar performance e evolução das operações alocadas.',
    priority: 'Média',
    tagClass: 'info',
  },
]
</script>
