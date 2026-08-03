<template>
  <div class="page">
    <section class="hero">
      <div>
        <p class="eyebrow">Investidor</p>
        <h2>Entrada consolidada do investidor pessoa física.</h2>
        <p>
          Esta área reúne onboarding, suitability, investimentos disponíveis, carteira e projetos
          vinculados à operação da LICEU 6.0.
        </p>
        <div class="actions">
          <RouterLink class="primary-btn" to="/investidor/dashboard">Abrir dashboard</RouterLink>
          <RouterLink class="secondary-btn secondary-btn-dark" to="/investidor/carteira">Ver carteira</RouterLink>
        </div>
      </div>

      <div class="hero-grid">
        <div class="card">
          <small>KYC</small>
          <div class="stat-value">Em fluxo</div>
          <span class="tag info">Suitability habilitado</span>
        </div>
        <div class="card">
          <small>Perfil</small>
          <div class="stat-value">Moderado</div>
          <span class="tag warning">Renda fixa + crédito</span>
        </div>
      </div>
    </section>

    <section class="grid-3">
      <RouterLink class="card card-link" to="/investidor/dashboard">
        <small>Painel principal</small>
        <h3>Dashboard</h3>
        <p>Resumo de carteira, indicadores, compliance, liquidez e inteligência de mercado.</p>
      </RouterLink>
      <RouterLink class="card card-link" to="/investidor/carteira">
        <small>Patrimônio</small>
        <h3>Carteira</h3>
        <p>Distribuição de ativos, duration, caixa disponível e rendimento esperado.</p>
      </RouterLink>
      <RouterLink class="card card-link" to="/investidor/projetos">
        <small>Originação</small>
        <h3>Projetos</h3>
        <p>Visualização dos projetos elegíveis e em acompanhamento dentro do portfólio.</p>
      </RouterLink>
    </section>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>