<template>
  <div class="page institutional-page" :class="{ 'institutional-page--dark': isDarkMode }">
    <section class="hero institutional-hero">
      <div>
        <p class="eyebrow">Institucional CEA</p>
        <h2>Arquitetura corporativa para investimentos, governanca e conformidade operacional.</h2>
        <p>
          A CEA Investimentos opera com disciplina institucional, conectando mercado de capitais, credito,
          acompanhamento de projetos e governanca em um modelo de instituicao financeira digital.
        </p>
        <div class="actions">
          <RouterLink to="/interplanetary/ecossistema" class="secondary-btn institutional-action-link">
            Abrir ecossistema interplanetario
          </RouterLink>
          <button type="button" class="secondary-btn institutional-theme-toggle" @click="toggleDarkMode">
            {{ isDarkMode ? 'Modo claro institucional' : 'Modo escuro institucional' }}
          </button>
        </div>
      </div>

      <div class="hero-grid">
        <div class="card">
          <small>Governanca</small>
          <div class="stat-value">360°</div>
          <span class="tag info">Visibilidade executiva</span>
        </div>
        <div class="card">
          <small>Conformidade</small>
          <div class="stat-value">KYC + AML</div>
          <span class="tag warning">Controles ativos</span>
        </div>
      </div>
    </section>

    <MissionVisionValues :dark-mode="isDarkMode" />

    <nav class="institutional-quick-nav" aria-label="Atalhos institucionais">
      <RouterLink
        v-for="item in governanceCards"
        :key="`quick-${item.slug}`"
        class="institutional-quick-nav__item"
        :to="`/institucional/${item.slug}`"
      >
        <span class="institutional-quick-nav__icon" v-html="item.icon"></span>
        <span>{{ item.title }}</span>
      </RouterLink>
    </nav>

    <section class="institutional-suite">
      <div class="institutional-suite__header">
        <p class="eyebrow">Governanca + Compliance</p>
        <h3>Pilares institucionais com aparencia de banco digital</h3>
        <p>
          A estrutura da CEA Investimentos organiza política, risco, protecao de dados, auditoria e decisao
          executiva em um modelo claro, rastreavel e preparado para escala regulada.
        </p>
      </div>

      <div class="institutional-suite__grid">
        <RouterLink
          v-for="(item, index) in governanceCards"
          :key="item.title"
          class="institutional-card"
          :to="`/institucional/${item.slug}`"
          :style="{ animationDelay: `${index * 80}ms` }"
        >
          <div class="institutional-card__icon" v-html="item.icon"></div>
          <div class="institutional-card__content">
            <small>{{ item.category }}</small>
            <h4>{{ item.title }}</h4>
            <p>{{ item.description }}</p>
            <ul>
              <li v-for="point in item.points" :key="point">{{ point }}</li>
            </ul>
          </div>
        </RouterLink>
      </div>
    </section>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import MissionVisionValues from '../components/MissionVisionValues.vue'
import { institutionalPolicies as governanceCards } from '../data/institutionalPolicies'
import { useInstitutionalTheme } from '../composables/useInstitutionalTheme'

const { isDarkMode, toggleDarkMode } = useInstitutionalTheme()
</script>

<style scoped>
.institutional-page {
  padding-bottom: 48px;
}

.institutional-theme-toggle {
  background: rgba(255, 255, 255, 0.14);
  color: var(--white);
  border: 1px solid rgba(255, 255, 255, 0.32);
}

.institutional-action-link {
  text-decoration: none;
}

.institutional-hero {
  margin-bottom: 28px;
}

.institutional-suite {
  margin-top: 32px;
  padding: 34px;
  border-radius: 24px;
  background:
    radial-gradient(circle at top right, rgba(200, 169, 106, 0.16), transparent 24%),
    linear-gradient(180deg, rgba(13, 43, 82, 0.03), rgba(13, 43, 82, 0.01));
  border: 1px solid rgba(13, 43, 82, 0.08);
}

.institutional-quick-nav {
  display: none;
}

.institutional-suite__header {
  margin-bottom: 24px;
}

.institutional-suite__header h3 {
  margin: 8px 0 12px;
  font-size: clamp(1.8rem, 3vw, 2.4rem);
  color: var(--deep);
}

.institutional-suite__header p {
  margin: 0;
  max-width: 72ch;
  color: var(--muted);
}

.institutional-suite__grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 18px;
}

.institutional-card {
  display: grid;
  grid-template-columns: 64px 1fr;
  gap: 16px;
  padding: 22px;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.96);
  border: 1px solid rgba(13, 43, 82, 0.08);
  box-shadow: 0 14px 34px rgba(13, 43, 82, 0.07);
  animation: card-enter 0.65s ease both;
  transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
  text-decoration: none;
}

.institutional-card:hover {
  transform: translateY(-4px);
  border-color: rgba(31, 59, 99, 0.18);
  box-shadow: 0 18px 38px rgba(13, 43, 82, 0.12);
}

.institutional-card__icon {
  width: 64px;
  height: 64px;
  border-radius: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(13, 43, 82, 0.08), rgba(200, 169, 106, 0.22));
  color: var(--deep);
}

.institutional-card__icon :deep(svg) {
  width: 30px;
  height: 30px;
  stroke: currentColor;
  stroke-width: 1.8;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.institutional-card__content small {
  display: inline-block;
  margin-bottom: 8px;
  color: var(--gold);
  font-size: 0.76rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.institutional-card__content h4 {
  margin: 0 0 10px;
  color: var(--deep);
  font-size: 1.12rem;
}

.institutional-card__content p {
  margin: 0 0 12px;
  color: var(--muted);
}

.institutional-card__content ul {
  margin: 0;
  padding-left: 18px;
  color: var(--muted);
}

.institutional-card__content li + li {
  margin-top: 6px;
}

.institutional-page--dark {
  color: #d7e0ec;
}

.institutional-page--dark .institutional-hero {
  background: linear-gradient(135deg, #071a33 0%, #0d2b52 55%, #143a70 100%);
  box-shadow: 0 24px 44px rgba(3, 10, 20, 0.45);
}

.institutional-page--dark .institutional-suite {
  background:
    radial-gradient(circle at top right, rgba(200, 169, 106, 0.2), transparent 24%),
    linear-gradient(180deg, rgba(7, 20, 40, 0.86), rgba(7, 20, 40, 0.82));
  border-color: rgba(113, 144, 187, 0.3);
}

.institutional-page--dark .institutional-suite__header h3,
.institutional-page--dark .institutional-card__content h4,
.institutional-page--dark .institutional-quick-nav__item {
  color: #e8eef7;
}

.institutional-page--dark .institutional-suite__header p,
.institutional-page--dark .institutional-card__content p,
.institutional-page--dark .institutional-card__content ul,
.institutional-page--dark .institutional-card__content small {
  color: #b4c5d8;
}

.institutional-page--dark .institutional-card {
  background: rgba(11, 30, 56, 0.92);
  border-color: rgba(113, 144, 187, 0.25);
  box-shadow: 0 16px 34px rgba(0, 0, 0, 0.35);
}

.institutional-page--dark .institutional-card__icon {
  background: linear-gradient(135deg, rgba(30, 65, 112, 0.45), rgba(200, 169, 106, 0.32));
  color: #f3f7fc;
}

@keyframes card-enter {
  from {
    opacity: 0;
    transform: translateY(16px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 980px) {
  .institutional-suite__grid {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 720px) {
  .institutional-quick-nav {
    position: sticky;
    top: 8px;
    z-index: 12;
    display: flex;
    gap: 10px;
    overflow-x: auto;
    padding: 10px;
    border-radius: 16px;
    background: rgba(255, 255, 255, 0.92);
    border: 1px solid rgba(13, 43, 82, 0.08);
    box-shadow: 0 8px 20px rgba(13, 43, 82, 0.08);
    -webkit-overflow-scrolling: touch;
  }

  .institutional-quick-nav__item {
    flex: 0 0 auto;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 12px;
    border-radius: 999px;
    text-decoration: none;
    font-size: 0.82rem;
    font-weight: 600;
    color: var(--deep);
    background: linear-gradient(180deg, #eef2f7 0%, #e6edf5 100%);
    border: 1px solid rgba(13, 43, 82, 0.08);
    white-space: nowrap;
  }

  .institutional-quick-nav__icon {
    width: 18px;
    height: 18px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    color: var(--deep);
  }

  .institutional-quick-nav__icon :deep(svg) {
    width: 16px;
    height: 16px;
    stroke: currentColor;
    stroke-width: 1.8;
    stroke-linecap: round;
    stroke-linejoin: round;
  }

  .institutional-suite {
    padding: 24px 18px;
  }

  .institutional-suite__grid {
    grid-template-columns: 1fr;
  }

  .institutional-card {
    grid-template-columns: 1fr;
  }
}
</style>
