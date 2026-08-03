<template>
  <div class="page">
    <section class="hero">
      <div>
        <p class="eyebrow">Portal do Colaborador</p>
        <h2>Painel interno operacional CEA</h2>
        <p>
          Área dedicada para execução diária das atividades de crédito, compliance,
          tesouraria e comunicação institucional.
        </p>
      </div>
      <div class="hero-grid">
        <div class="card">
          <small>Colaborador</small>
          <div class="stat-value">{{ collaborator.name }}</div>
          <span class="tag info">{{ collaborator.role }}</span>
        </div>
        <div class="card">
          <small>Unidade</small>
          <div class="stat-value">{{ collaborator.unit }}</div>
          <span class="tag warning">Notificações: {{ collaborator.notifications }}</span>
        </div>
      </div>
    </section>

    <section>
      <h3 class="section-title">Dashboard</h3>
      <div class="grid-4">
        <article class="stat-card">
          <small>Tarefas do dia</small>
          <div class="stat-value">18</div>
        </article>
        <article class="stat-card">
          <small>Solicitações pendentes</small>
          <div class="stat-value">12</div>
        </article>
        <article class="stat-card">
          <small>Alertas compliance</small>
          <div class="stat-value">4</div>
        </article>
        <article class="stat-card">
          <small>Comunicados internos</small>
          <div class="stat-value">6</div>
        </article>
      </div>
    </section>

    <section class="grid-2">
      <article class="panel">
        <small>Tarefas</small>
        <h3>Atividades prioritárias</h3>
        <ul class="list">
          <li>Aprovação de crédito;</li>
          <li>Revisão KYC;</li>
          <li>Follow-up de clientes;</li>
          <li>Análise de projetos.</li>
        </ul>
        <div class="actions">
          <RouterLink class="primary-btn" to="/colaborador/tarefas">Abrir tarefas</RouterLink>
        </div>
      </article>

      <article class="panel">
        <small>Documentos internos</small>
        <h3>Base de consulta</h3>
        <ul class="list">
          <li>Políticas internas;</li>
          <li>Manual de compliance;</li>
          <li>Procedimentos de crédito;</li>
          <li>ESG guidelines.</li>
        </ul>
        <div class="actions">
          <RouterLink class="primary-btn" to="/colaborador/documentos">Abrir documentos</RouterLink>
        </div>
      </article>
    </section>

    <section class="grid-2">
      <article class="panel">
        <small>Comunicados</small>
        <h3>Últimas atualizações</h3>
        <ul class="list">
          <li>Avisos da diretoria</li>
          <li>Atualizações regulatórias</li>
          <li>Atualizações LICEU</li>
        </ul>
        <div class="actions">
          <RouterLink class="secondary-btn secondary-btn-dark" to="/colaborador/comunicados">Ver comunicados</RouterLink>
        </div>
      </article>

      <article class="panel">
        <small>Treinamentos</small>
        <h3>Trilhas recomendadas</h3>
        <ul class="list">
          <li>KYC / AML</li>
          <li>ESG</li>
          <li>Produtos financeiros</li>
          <li>Compliance</li>
        </ul>
        <div class="actions">
          <RouterLink class="secondary-btn secondary-btn-dark" to="/colaborador/treinamentos">Abrir treinamentos</RouterLink>
        </div>
      </article>
    </section>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'

const collaborator = {
  name: 'Usuário Interno',
  role: 'Colaborador',
  unit: 'São Paulo',
  notifications: 5,
}
</script>
