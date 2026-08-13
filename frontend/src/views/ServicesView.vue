<template>
  <div class="page">
    <section class="hero">
      <div>
        <p class="eyebrow">Acessar Serviços</p>
        <h2>Escolha o fluxo de entrada da operação CEA INVESTIMENTOS.</h2>
        <p>
          A navegação foi organizada por intenção: investir, captar financiamento, estruturar
          projetos ou acessar ambientes internos e institucionais.
        </p>
      </div>

      <div class="hero-grid">
        <div class="card">
          <small>Perfis atendidos</small>
          <div class="stat-value">6 jornadas</div>
          <span class="tag info">Entrada segmentada</span>
        </div>
        <div class="card">
          <small>Operação</small>
          <div class="stat-value">Full stack</div>
          <span class="tag warning">Investimento + crédito</span>
        </div>
      </div>
    </section>

    <section class="grid-3">
      <RouterLink v-for="service in services" :key="service.title" :to="service.to" class="card card-link">
        <small>{{ service.kicker }}</small>
        <h3>{{ service.title }}</h3>
        <p>{{ service.description }}</p>
      </RouterLink>
    </section>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'

const services = [
  {
    kicker: 'Pessoa física',
    title: 'Investir como investidor PF',
    description: 'Acessar onboarding, suitability, carteira, projetos e rentabilidade.',
    to: '/investidor',
  },
  {
    kicker: 'Pessoa jurídica',
    title: 'Investir como empresa',
    description: 'Entrar na camada institucional com avaliação de perfil e instrumentos estruturados.',
    to: '/investir',
  },
  {
    kicker: 'Funding',
    title: 'Solicitar financiamento',
    description: 'Iniciar o pedido de crédito para obra com dados do projeto e prazo estimado.',
    to: '/financiamento',
  },
  {
    kicker: 'Estruturação',
    title: 'Coinvestimento',
    description: 'Acessar inteligência de mercado e composições de alocação com múltiplos participantes.',
    to: '/investir',
  },
  {
    kicker: 'Projetos',
    title: 'Estruturação de projetos',
    description: 'Entrar em contato com a frente de desenho financeiro, garantias e cronograma.',
    to: '/sobre',
  },
  {
    kicker: 'Institucional',
    title: 'Investidor institucional',
    description: 'Seguir para o login institucional e backoffice com papéis avançados.',
    to: '/admin/login',
  },
]
</script>