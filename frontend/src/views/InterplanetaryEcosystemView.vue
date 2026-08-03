<template>
  <div class="page">
    <section class="hero">
      <div>
        <p class="eyebrow">Interplanetary Finance</p>
        <h2>Ecossistema operacional CEA para banco, investimento, exchanges e seguro espacial.</h2>
        <p>
          Catálogo de domínios interplanetários com estado operacional persistido e trilha de ativação.
          A ativação respeita RBAC por domínio.
        </p>
      </div>

      <div class="hero-grid">
        <div class="card stat-card">
          <small>Domínios mapeados</small>
          <div class="stat-value">{{ domains.length }}</div>
          <span class="tag info">Catálogo vivo</span>
        </div>
        <div class="card stat-card">
          <small>Ativos no runtime</small>
          <div class="stat-value">{{ activeCount }}</div>
          <span class="tag success">Status real</span>
        </div>
      </div>
    </section>

    <section>
      <h3 class="section-title">Domínios interplanetários</h3>
      <div class="domain-grid">
        <article class="domain-card" v-for="domain in domains" :key="domain.id">
          <div class="domain-head">
            <div>
              <small>{{ domain.type }}</small>
              <h4>{{ domain.name }}</h4>
            </div>
            <span class="status-chip" :class="chipClass(domain.status)">
              {{ domain.status }}
            </span>
          </div>

          <p class="domain-description">{{ domain.description }}</p>

          <div class="meta-row">
            <span><strong>Subject:</strong> {{ domain.subject }}</span>
            <span><strong>Última ativação:</strong> {{ formatDate(domain.last_activation_at) }}</span>
          </div>

          <button
            class="activate-button"
            :disabled="!canActivate || activating === domain.id"
            @click="activateDomain(domain.id)"
          >
            {{ activating === domain.id ? 'Ativando...' : 'Ativar domínio' }}
          </button>
        </article>
      </div>
      <p class="hint" v-if="!canActivate">
        Perfil atual sem permissão de ativação. Faça login com papel de backoffice autorizado.
      </p>
      <p class="error" v-if="errorMessage">{{ errorMessage }}</p>
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { activateInterplanetaryDomain, fetchInterplanetaryEcosystem } from '../services/liceuApi'

const domains = ref([])
const activating = ref('')
const errorMessage = ref('')

const ALLOWED_ROLES = ['admin', 'risk_manager', 'governance', 'diretoria', 'tesouraria']
const currentRole = (localStorage.getItem('cea.userRole') || 'guest').toLowerCase()
const canActivate = computed(() => ALLOWED_ROLES.includes(currentRole))
const activeCount = computed(() => domains.value.filter((item) => item.active).length)

const loadDomains = async () => {
  errorMessage.value = ''
  try {
    const response = await fetchInterplanetaryEcosystem()
    domains.value = response.items || []
  } catch (error) {
    errorMessage.value = error?.response?.data?.detail || 'Falha ao carregar ecossistema interplanetário.'
  }
}

const activateDomain = async (domainId) => {
  if (!canActivate.value) return

  activating.value = domainId
  errorMessage.value = ''
  try {
    await activateInterplanetaryDomain(domainId)
    await loadDomains()
  } catch (error) {
    errorMessage.value = error?.response?.data?.detail || 'Não foi possível ativar o domínio.'
  } finally {
    activating.value = ''
  }
}

const chipClass = (status) => {
  if (status === 'active') return 'status-chip--active'
  if (status === 'maintenance') return 'status-chip--maintenance'
  return 'status-chip--planned'
}

const formatDate = (value) => {
  if (!value) return 'nunca'
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return 'nunca'
  return date.toLocaleString('pt-BR')
}

onMounted(loadDomains)
</script>

<style scoped>
.domain-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
  margin-top: 20px;
}

.domain-card {
  border-radius: 16px;
  border: 1px solid rgba(13, 43, 82, 0.16);
  background: linear-gradient(165deg, rgba(255, 255, 255, 0.98) 0%, rgba(239, 245, 255, 0.84) 100%);
  padding: 16px;
  box-shadow: 0 8px 22px rgba(13, 43, 82, 0.08);
}

.domain-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.domain-head h4 {
  margin: 4px 0 0;
  color: var(--deep);
}

.domain-description {
  margin: 12px 0;
  color: var(--muted);
}

.meta-row {
  display: grid;
  gap: 6px;
  color: var(--muted);
  font-size: 0.88rem;
}

.status-chip {
  border-radius: 999px;
  padding: 6px 10px;
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.status-chip--active {
  color: #075228;
  background: rgba(53, 184, 120, 0.18);
}

.status-chip--maintenance {
  color: #7a4b00;
  background: rgba(255, 176, 32, 0.22);
}

.status-chip--planned {
  color: #0d2b52;
  background: rgba(13, 43, 82, 0.12);
}

.activate-button {
  margin-top: 12px;
  width: 100%;
  border: none;
  border-radius: 10px;
  padding: 10px 12px;
  background: var(--deep);
  color: #fff;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s ease, opacity 0.2s ease;
}

.activate-button:hover:not(:disabled) {
  transform: translateY(-1px);
}

.activate-button:disabled {
  cursor: not-allowed;
  opacity: 0.58;
}

.hint {
  margin-top: 14px;
  color: var(--muted);
}

.error {
  margin-top: 14px;
  color: #a11313;
  font-weight: 600;
}

@media (max-width: 980px) {
  .domain-grid {
    grid-template-columns: 1fr;
  }
}
</style>
