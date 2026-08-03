<template>
  <div class="page policy-page" :class="{ 'policy-page--dark': isDarkMode }">
    <section class="hero policy-hero" v-if="policy">
      <div>
        <p class="eyebrow">{{ policy.category }}</p>
        <h2>{{ policy.title }}</h2>
        <p>{{ policy.description }}</p>
        <div class="actions">
          <button type="button" class="secondary-btn policy-theme-toggle" @click="toggleDarkMode">
            {{ isDarkMode ? 'Modo claro institucional' : 'Modo escuro institucional' }}
          </button>
          <RouterLink class="secondary-btn" to="/institucional">Voltar ao institucional</RouterLink>
        </div>
      </div>

      <div class="hero-grid">
        <div class="card policy-summary-card">
          <small>Pilares</small>
          <ul class="policy-highlight-list">
            <li v-for="highlight in policy.highlights" :key="highlight">{{ highlight }}</li>
          </ul>
        </div>
        <div class="card policy-summary-card">
          <small>Controles</small>
          <ul class="policy-highlight-list">
            <li v-for="point in policy.points" :key="point">{{ point }}</li>
          </ul>
        </div>
      </div>
    </section>

    <section v-if="policy" class="policy-content">
      <article v-for="section in policy.sections" :key="section.heading" class="panel policy-panel">
        <h3>{{ section.heading }}</h3>
        <p>{{ section.text }}</p>
      </article>
    </section>

    <section v-if="policy" class="policy-navigation grid-3">
      <RouterLink
        v-for="item in relatedPolicies"
        :key="item.slug"
        class="card card-link policy-nav-card"
        :to="`/institucional/${item.slug}`"
      >
        <small>{{ item.category }}</small>
        <h3>{{ item.title }}</h3>
        <p>{{ item.description }}</p>
      </RouterLink>
    </section>

    <section v-else class="panel policy-empty">
      <h3>Conteudo institucional nao encontrado</h3>
      <p>O pilar solicitado nao esta disponivel nesta rota.</p>
      <RouterLink class="primary-btn" to="/institucional">Ir para a pagina institucional</RouterLink>
    </section>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import { institutionalPolicyMap, institutionalPolicies } from '../data/institutionalPolicies'
import { useInstitutionalTheme } from '../composables/useInstitutionalTheme'

const route = useRoute()
const { isDarkMode, toggleDarkMode } = useInstitutionalTheme()

const policy = computed(() => institutionalPolicyMap[route.params.slug])
const relatedPolicies = computed(() => institutionalPolicies.filter((item) => item.slug !== route.params.slug))
</script>

<style scoped>
.policy-page {
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding-bottom: 48px;
}

.policy-hero {
  margin-bottom: 0;
}

.policy-theme-toggle {
  background: rgba(255, 255, 255, 0.14);
  color: var(--white);
  border: 1px solid rgba(255, 255, 255, 0.32);
}

.policy-summary-card {
  min-height: 100%;
}

.policy-highlight-list {
  margin: 12px 0 0;
  padding-left: 18px;
}

.policy-highlight-list li + li {
  margin-top: 8px;
}

.policy-content {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 18px;
}

.policy-panel h3 {
  margin-top: 0;
  color: var(--deep);
}

.policy-panel p {
  margin-bottom: 0;
  color: var(--muted);
}

.policy-nav-card h3 {
  margin: 8px 0 10px;
  color: var(--deep);
}

.policy-nav-card p {
  margin: 0;
  color: var(--muted);
}

.policy-empty {
  display: flex;
  flex-direction: column;
  gap: 16px;
  align-items: flex-start;
}

.policy-page--dark {
  color: #d7e0ec;
}

.policy-page--dark .policy-hero {
  background: linear-gradient(135deg, #071a33 0%, #0d2b52 55%, #143a70 100%);
  box-shadow: 0 24px 44px rgba(3, 10, 20, 0.45);
}

.policy-page--dark .policy-panel,
.policy-page--dark .policy-nav-card,
.policy-page--dark .policy-summary-card,
.policy-page--dark .policy-empty {
  background: rgba(11, 30, 56, 0.92);
  border-color: rgba(113, 144, 187, 0.28);
  box-shadow: 0 16px 32px rgba(0, 0, 0, 0.35);
}

.policy-page--dark .policy-panel h3,
.policy-page--dark .policy-nav-card h3,
.policy-page--dark .policy-empty h3 {
  color: #e8eef7;
}

.policy-page--dark .policy-panel p,
.policy-page--dark .policy-nav-card p,
.policy-page--dark .policy-highlight-list,
.policy-page--dark .policy-empty p,
.policy-page--dark .policy-nav-card small {
  color: #b4c5d8;
}

@media (max-width: 980px) {
  .policy-content {
    grid-template-columns: 1fr;
  }
}
</style>
