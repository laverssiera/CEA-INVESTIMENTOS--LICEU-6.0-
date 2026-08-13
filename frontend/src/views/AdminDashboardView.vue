<template>
  <div class="page">
    <section class="hero">
      <div>
        <p class="eyebrow">/admin</p>
        <h2>Backoffice institucional para crédito, risco, tesouraria e compliance.</h2>
        <p>
          Esta área resume a estrutura operacional esperada para o ambiente interno com até 10
          usuários e responsabilidades segregadas por função.
        </p>
      </div>

      <div class="hero-grid">
        <div class="card">
          <small>Pipeline crédito</small>
          <div class="stat-value">27 casos</div>
          <span class="tag info">Originação ativa</span>
        </div>
        <div class="card">
          <small>Tesouraria</small>
          <div class="stat-value">R$ 48 mi</div>
          <span class="tag warning">Caixa monitorado</span>
        </div>
      </div>
    </section>

    <section class="grid-4">
      <component
        :is="module.to ? 'router-link' : 'article'"
        v-for="module in modules"
        :key="module.title"
        :to="module.to"
        class="card"
        :class="{ 'card-link': Boolean(module.to) }"
      >
        <small>{{ module.kicker }}</small>
        <h3>{{ module.title }}</h3>
        <p>{{ module.description }}</p>
      </component>
    </section>
  </div>
</template>

<script setup>
const modules = [
  {
    kicker: 'Governança',
    title: 'Dashboard governança',
    description: 'SLA institucional, auditoria, segregação e indicadores executivos.',
    to: '/admin/governanca',
  },
  {
    kicker: 'Comitê',
    title: 'Comitê de crédito',
    description: 'Fila decisória, composição do comitê e regras de dupla aprovação.',
    to: '/admin/comite-credito',
  },
  {
    kicker: 'Segurança',
    title: 'Matriz RBAC',
    description: 'Permissões por módulo, escopos técnicos e restrições mandatórias.',
    to: '/admin/rbac',
  },
  {
    kicker: 'Operações',
    title: 'Rotinas automáticas',
    description: 'Agenda de jobs, cadência operacional e calendário ESG/compliance.',
    to: '/admin/rotinas',
  },
  {
    kicker: 'Overview',
    title: 'Visão geral',
    description: 'Indicadores consolidados de funding, exposição e performance da operação.',
  },
  {
    kicker: 'Crédito',
    title: 'Pipeline de crédito',
    description: 'Triagem, comitê, garantias, documentos e evolução por etapa.',
  },
  {
    kicker: 'Mercado',
    title: 'Investimentos',
    description: 'Acompanhamento de carteira, rentabilidade, duration e recomendações.',
  },
  {
    kicker: 'Caixa',
    title: 'Tesouraria',
    description: 'Gestão de liquidez, alocação tática e proteção de caixa operacional.',
  },
  {
    kicker: 'Governança',
    title: 'Compliance',
    description: 'KYC, AML, suitability, monitoramento e trilha de auditoria.',
  },
  {
    kicker: 'Obras',
    title: 'Monitoramento',
    description: 'Acompanhamento de produção, cronograma e evolução físico-financeira.',
  },
  {
    kicker: 'BI',
    title: 'Relatórios',
    description: 'Exportação de visão executiva, operacional e regulatória.',
  },
  {
    kicker: 'Administração',
    title: 'Usuários',
    description: 'Gestão de papéis, acessos e limites para a operação inicial.',
  },
]
</script>