<template>
  <div class="page">
    <section class="hero">
      <div>
        <p class="eyebrow">Acesso</p>
        <h2>Escolha o ambiente de entrada conforme seu perfil operacional.</h2>
        <p>
          O ecossistema foi separado em jornadas para investidor, cliente e usuários internos,
          respeitando autenticação, governança e segregação de acesso.
        </p>
      </div>

      <div class="hero-grid">
        <div class="card">
          <small>Camadas</small>
          <div class="stat-value">3 portais</div>
          <span class="tag info">Público, cliente e admin</span>
        </div>
        <div class="card">
          <small>Segurança</small>
          <div class="stat-value">JWT + MFA</div>
          <span class="tag warning">RBAC ativo</span>
        </div>
      </div>
    </section>

    <section class="grid-3">
      <RouterLink class="card card-link" to="/investidor/dashboard">
        <small>Investidor</small>
        <h3>Portal do investidor</h3>
        <p>Carteira, rentabilidade, compliance e dados de projetos disponíveis.</p>
      </RouterLink>
      <RouterLink class="card card-link" to="/cliente/dashboard">
        <small>Cliente</small>
        <h3>Área do cliente</h3>
        <p>Status de financiamento, documentos, relatórios e comunicação.</p>
      </RouterLink>
      <RouterLink class="card card-link" to="/admin/login">
        <small>Institucional</small>
        <h3>Login interno</h3>
        <p>Acesso ao backoffice de crédito, risco, tesouraria, compliance e auditoria.</p>
      </RouterLink>
    </section>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>