<template>
  <div class="page">
    <section class="hero app-preview-hero">
      <div>
        <p class="eyebrow">Telas do App CEA</p>
        <h2>Preview visual das principais telas</h2>
        <p>
          Home, Investir, Projetos e Carteira em linguagem fintech, com navegação inferior
          fixa e foco em clareza operacional.
        </p>
      </div>
    </section>

    <section class="phone-grid">
      <article class="app-shell">
        <header class="app-header">
          <strong>CEA Investimentos</strong>
          <small>Home</small>
        </header>
        <main class="app-content">
          <div class="welcome">Ola, Joao!</div>
          <div class="saldo-card">
            <small>Saldo Investido</small>
            <strong>R$ 125.750,00</strong>
          </div>
          <div class="line-stat">
            <span>Rentabilidade Mensal</span>
            <strong class="up">+1,42%</strong>
          </div>
          <div class="quick-actions">
            <button>Investir</button>
            <button>Financiamento</button>
            <button>Minha Carteira</button>
            <button>Suporte</button>
          </div>
          <div class="project-card">
            <strong>Projeto Green Residence</strong>
            <span>80% em andamento</span>
          </div>
          <div class="payment-card">
            <small>Proximo Pagamento</small>
            <strong>R$ 2.500,00</strong>
          </div>
        </main>
        <footer class="bottom-nav">
          <button class="active">Home</button>
          <button>Investir</button>
          <button>Projetos</button>
          <button>Carteira</button>
          <button>Perfil</button>
        </footer>
      </article>

      <article class="app-shell">
        <header class="app-header">
          <strong>CEA Investimentos</strong>
          <small>Investir</small>
        </header>
        <main class="app-content">
          <div class="section-title-app">Opcoes de Investimento</div>
          <div class="list-card" v-for="item in investProducts" :key="item.name">
            <strong>{{ item.name }}</strong>
            <span>Rentabilidade {{ item.yield }}</span>
            <span>Risco {{ item.risk }}</span>
            <button>Investir</button>
          </div>
        </main>
        <footer class="bottom-nav">
          <button>Home</button>
          <button class="active">Investir</button>
          <button>Projetos</button>
          <button>Carteira</button>
          <button>Perfil</button>
        </footer>
      </article>

      <article class="app-shell">
        <header class="app-header">
          <strong>CEA Investimentos</strong>
          <small>Projetos</small>
        </header>
        <main class="app-content">
          <div class="section-title-app">Meus Projetos</div>
          <div class="list-card" v-for="project in projects" :key="project.name">
            <strong>{{ project.name }}</strong>
            <span>{{ project.progress }}</span>
            <span>Valor investido {{ project.invested }}</span>
            <button>Ver Detalhes</button>
          </div>
        </main>
        <footer class="bottom-nav">
          <button>Home</button>
          <button>Investir</button>
          <button class="active">Projetos</button>
          <button>Carteira</button>
          <button>Perfil</button>
        </footer>
      </article>

      <article class="app-shell">
        <header class="app-header">
          <strong>CEA Investimentos</strong>
          <small>Carteira</small>
        </header>
        <main class="app-content">
          <div class="section-title-app">Minha Carteira</div>
          <div class="wallet-card">
            <small>Alocacao Atual</small>
            <div class="donut"></div>
            <div class="wallet-lines">
              <span>Patrimonio <strong>R$ 125.750,00</strong></span>
              <span>Rentabilidade <strong class="up">+14,5%</strong></span>
              <span>Rendimentos <strong>R$ 1.750,00</strong></span>
            </div>
            <button>Extrato</button>
          </div>
        </main>
        <footer class="bottom-nav">
          <button>Home</button>
          <button>Investir</button>
          <button>Projetos</button>
          <button class="active">Carteira</button>
          <button>Perfil</button>
        </footer>
      </article>
    </section>
  </div>
</template>

<script setup>
const investProducts = [
  { name: 'Fundo Imobiliario', yield: '9,5% a.a.', risk: 'Moderado' },
  { name: 'CRA Infraestrutura', yield: '11,2% a.a.', risk: 'Baixo' },
  { name: 'Debentures', yield: '12,5% a.a.', risk: 'Medio' },
]

const projects = [
  { name: 'Green Residence', progress: '80% concluido', invested: 'R$ 40.000,00' },
  { name: 'Complexo Empresarial', progress: '65% concluido', invested: 'R$ 30.000,00' },
]
</script>

<style scoped>
.app-preview-hero {
  display: block;
  padding: 28px;
}

.phone-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(250px, 1fr));
  gap: 16px;
  margin-top: 18px;
}

.app-shell {
  min-height: 640px;
  border-radius: 24px;
  background: #f7faff;
  border: 8px solid #0d2b52;
  box-shadow: 0 20px 40px rgba(13, 43, 82, 0.2);
  display: grid;
  grid-template-rows: auto 1fr auto;
  overflow: hidden;
}

.app-header {
  padding: 14px;
  background: #0d2b52;
  color: #fff;
  display: grid;
  gap: 4px;
}

.app-header small {
  color: #c8d8ef;
}

.app-content {
  padding: 10px;
  display: grid;
  gap: 8px;
  align-content: start;
}

.welcome,
.section-title-app {
  font-size: 0.95rem;
  color: #0d2b52;
  font-weight: 700;
}

.list-card {
  background: #fff;
  border: 1px solid #d7dde7;
  border-radius: 12px;
  padding: 10px;
  display: grid;
  gap: 4px;
}

.list-card strong {
  color: #0d2b52;
}

.list-card span {
  color: #6c7685;
  font-size: 0.84rem;
}

.saldo-card {
  border-radius: 12px;
  padding: 10px;
  background: linear-gradient(135deg, #1452a7, #2f7be0);
  color: #fff;
  display: grid;
  gap: 4px;
}

.saldo-card small {
  color: #d9e7ff;
}

.saldo-card strong {
  font-size: 1.1rem;
}

.line-stat {
  display: flex;
  justify-content: space-between;
  border-radius: 10px;
  background: #ffffff;
  border: 1px solid #d7dde7;
  padding: 8px 10px;
  font-size: 0.82rem;
  color: #6c7685;
}

.up {
  color: #2d9b53;
}

.list-card button,
.quick-actions button,
.wallet-card button {
  border: 0;
  border-radius: 10px;
  padding: 8px 10px;
  background: #1f3b63;
  color: #fff;
  font-weight: 700;
}

.quick-actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

.project-card,
.payment-card,
.wallet-card {
  background: #fff;
  border: 1px solid #d7dde7;
  border-radius: 12px;
  padding: 10px;
  display: grid;
  gap: 4px;
}

.project-card span {
  color: #2d9b53;
  font-weight: 700;
  font-size: 0.9rem;
}

.donut {
  width: 118px;
  height: 118px;
  margin: 4px auto;
  border-radius: 50%;
  background: conic-gradient(#1452a7 0 45%, #1f67c8 45% 70%, #d7a928 70% 85%, #8fb4e8 85% 100%);
  position: relative;
}

.donut::after {
  content: '';
  position: absolute;
  inset: 22px;
  border-radius: 50%;
  background: #fff;
}

.wallet-lines {
  display: grid;
  gap: 4px;
}

.wallet-lines span {
  display: flex;
  justify-content: space-between;
  font-size: 0.82rem;
  color: #6c7685;
}

.bottom-nav {
  border-top: 1px solid #d7dde7;
  background: #fff;
  display: grid;
  grid-template-columns: repeat(5, 1fr);
}

.bottom-nav button {
  border: 0;
  padding: 10px 6px;
  background: transparent;
  font-size: 0.77rem;
  color: #6c7685;
  font-weight: 700;
}

.bottom-nav button.active {
  color: #0d2b52;
}

@media (max-width: 1260px) {
  .phone-grid {
    grid-template-columns: repeat(2, minmax(250px, 1fr));
  }
}

@media (max-width: 760px) {
  .phone-grid {
    grid-template-columns: 1fr;
  }
}
</style>
