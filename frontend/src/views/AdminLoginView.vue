<template>
  <div class="page">
    <section class="hero">
      <div>
        <p class="eyebrow">/admin/login</p>
        <h2>Acesso institucional com MFA e segregação por perfil.</h2>
        <p>
          Este ponto de entrada concentra usuários internos de crédito, risco, compliance,
          tesouraria, jurídico, auditoria e administração.
        </p>
      </div>

      <div class="hero-grid">
        <div class="card">
          <small>Usuários</small>
          <div class="stat-value">10 iniciais</div>
          <span class="tag info">Controle restrito</span>
        </div>
        <div class="card">
          <small>Autenticação</small>
          <div class="stat-value">JWT + MFA</div>
          <span class="tag warning">RBAC</span>
        </div>
      </div>
    </section>

    <section class="grid-2">
      <article class="panel">
        <small>Login institucional</small>
        <h3>Credenciais e segundo fator</h3>

        <form v-if="!isAuthenticated && !auth.state.mfaRequired" class="form-grid" @submit.prevent="handleLogin">
          <label>
            Usuário
            <input v-model="form.username" type="text" />
          </label>
          <label>
            Senha
            <input v-model="form.password" type="password" />
          </label>
          <button class="primary-btn" type="submit" :disabled="auth.state.loading">
            {{ auth.state.loading ? 'Entrando...' : 'Acessar' }}
          </button>
        </form>

        <form v-else-if="auth.state.mfaRequired" class="form-grid" @submit.prevent="handleVerifyMfa">
          <label>
            Código MFA
            <input v-model="form.code" maxlength="6" type="text" />
          </label>
          <div class="card">
            <small>Ambiente demo</small>
            <p>Exemplo interno: <strong>admin / admin123</strong> com código <strong>999000</strong>.</p>
          </div>
          <button class="primary-btn" type="submit" :disabled="auth.state.loading">
            {{ auth.state.loading ? 'Validando...' : 'Confirmar MFA' }}
          </button>
        </form>

        <div v-else class="card">
          <p><strong>Perfil autenticado:</strong> {{ auth.state.userRole }}</p>
          <div class="actions">
            <RouterLink class="primary-btn" :to="resolveDestination()">Abrir painel</RouterLink>
            <button class="secondary-btn secondary-btn-dark" type="button" @click="auth.logout">Encerrar sessão</button>
          </div>
        </div>

        <p v-if="auth.state.error"><strong>Erro:</strong> {{ auth.state.error }}</p>
      </article>

      <article class="panel">
        <small>Perfis previstos</small>
        <h3>RBAC institucional</h3>
        <ul class="list">
          <li>admin;</li>
          <li>analista_credito;</li>
          <li>compliance;</li>
          <li>tesouraria;</li>
          <li>colaborador.</li>
        </ul>

        <div class="card" style="margin-top: 16px;">
          <small>Credenciais demo internas</small>
          <div class="demo-users">
            <div v-for="user in demoUsers" :key="user.username" class="demo-user">
              <strong>{{ user.username }}</strong>
              <span>Senha: {{ user.password }}</span>
              <span>MFA: {{ user.mfa }}</span>
              <span>Perfil: {{ user.role }}</span>
            </div>
          </div>
        </div>
      </article>
    </section>
  </div>
</template>

<script setup>
import { computed, reactive } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()
const isAuthenticated = computed(() => auth.isAuthenticated.value)

const form = reactive({
  username: 'admin',
  password: 'admin123',
  code: '999000',
})

const demoUsers = [
  { username: 'admin', password: 'admin123', mfa: '999000', role: 'admin' },
  { username: 'analista_credito', password: 'credito123', mfa: '224466', role: 'analista_credito' },
  { username: 'compliance', password: 'compliance123', mfa: '778899', role: 'compliance' },
  { username: 'tesouraria', password: 'tesouraria123', mfa: '554433', role: 'tesouraria' },
  { username: 'colaborador', password: 'colaborador123', mfa: '667788', role: 'colaborador' },
  { username: 'risk_manager', password: 'risk123', mfa: '313131', role: 'risk_manager' },
  { username: 'governance', password: 'gov123', mfa: '414141', role: 'governance' },
  { username: 'diretoria', password: 'board123', mfa: '515151', role: 'diretoria' },
]

const resolveDestination = () => {
  const redirect = route.query.redirect
  if (typeof redirect === 'string' && redirect) {
    return redirect
  }

  return ['analista_credito', 'compliance', 'tesouraria', 'colaborador'].includes(auth.state.userRole)
    ? '/colaborador'
    : '/admin'
}

const handleLogin = async () => {
  try {
    await auth.login(form.username, form.password)

    if (auth.isAuthenticated.value) {
      await router.push(resolveDestination())
    }
  } catch {
    // O estado de erro ja e preenchido pelo store.
  }
}

const handleVerifyMfa = async () => {
  try {
    await auth.verifyMfa(form.code)
    await router.push(resolveDestination())
  } catch {
    // O estado de erro ja e preenchido pelo store.
  }
}
</script>

<style scoped>
.demo-users {
  display: grid;
  gap: 10px;
  margin-top: 12px;
}

.demo-user {
  display: grid;
  gap: 2px;
  padding: 12px 14px;
  border: 1px solid rgba(31, 59, 99, 0.12);
  border-radius: 14px;
  background: rgba(31, 59, 99, 0.04);
}

.demo-user strong {
  color: var(--deep);
  font-size: 0.95rem;
}

.demo-user span {
  color: var(--muted);
  font-size: 0.84rem;
}
</style>