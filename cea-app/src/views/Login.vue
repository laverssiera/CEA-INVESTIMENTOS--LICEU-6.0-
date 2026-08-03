<template>
  <div class="login-screen">
    <div class="card">
      <div class="logo">
        <span>CEA</span>
        <small>Investimentos</small>
      </div>

      <!-- Etapa 1 — Credenciais -->
      <form v-if="step === 1" @submit.prevent="doLogin">
        <h2>Entrar na sua conta</h2>
        <p class="hint">Acesse sua carteira de investimentos</p>

        <label>
          Usuário
          <input v-model="username" type="text" required autocomplete="username" placeholder="ex.: investidor" />
        </label>

        <label>
          Senha
          <input v-model="password" type="password" required autocomplete="current-password" placeholder="••••••" />
        </label>

        <label class="tipo-label">
          Tipo de conta
          <select v-model="investorType">
            <option value="PF">Pessoa Física</option>
            <option value="PJ">Pessoa Jurídica</option>
          </select>
        </label>

        <button type="submit" :disabled="loading">
          {{ loading ? 'Verificando...' : 'Continuar' }}
        </button>

        <p v-if="errorMsg" class="error">{{ errorMsg }}</p>

        <p class="demo-hint">
          Demo PF: <code>investidor / cea123</code><br />
          Demo Admin: <code>admin / admin123</code>
        </p>
      </form>

      <!-- Etapa 2 — MFA -->
      <form v-else @submit.prevent="doMfa">
        <h2>Verificação de segurança</h2>
        <p class="hint">Digite o código de autenticação em duas etapas</p>

        <label>
          Código MFA
          <input
            v-model="mfaCode"
            type="text"
            inputmode="numeric"
            maxlength="6"
            required
            placeholder="ex.: 246810"
            autofocus
          />
        </label>

        <button type="submit" :disabled="loading">
          {{ loading ? 'Verificando...' : 'Acessar' }}
        </button>

        <button type="button" class="back-btn" @click="step = 1">Voltar</button>

        <p v-if="errorMsg" class="error">{{ errorMsg }}</p>

        <p class="demo-hint">Demo PF: <code>246810</code> · Admin: <code>999000</code></p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { loginApi, verifyMfa } from '../services/api.js'
import { auth } from '../store/auth.js'

const router = useRouter()

const step = ref(1)
const username = ref('')
const password = ref('')
const investorType = ref('PF')
const mfaCode = ref('')
const challengeId = ref('')
const loading = ref(false)
const errorMsg = ref('')

async function doLogin() {
  loading.value = true
  errorMsg.value = ''
  try {
    const res = await loginApi(username.value, password.value)
    if (res.mfa_required) {
      challengeId.value = res.challenge_id
      step.value = 2
    } else {
      // sem MFA (não esperado no backend atual mas tratado por robustez)
      auth.setAuth({ token: res.access_token, role: res.role ?? 'investor_pf', name: username.value, investorType: investorType.value })
      router.push('/')
    }
  } catch (err) {
    errorMsg.value = err.message || 'Credenciais inválidas.'
  } finally {
    loading.value = false
  }
}

async function doMfa() {
  loading.value = true
  errorMsg.value = ''
  try {
    const res = await verifyMfa(challengeId.value, mfaCode.value)
    auth.setAuth({
      token: res.access_token,
      role: res.role ?? 'investor_pf',
      name: username.value,
      investorType: investorType.value,
    })
    router.push('/')
  } catch (err) {
    errorMsg.value = err.message || 'Código inválido. Tente novamente.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-screen {
  min-height: 100dvh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px 16px;
}

.card {
  width: min(400px, 100%);
  background: #fff;
  border-radius: 20px;
  padding: 32px 24px;
  box-shadow: 0 16px 40px rgba(13, 60, 143, 0.14);
  border: 1px solid var(--cea-border);
  display: grid;
  gap: 20px;
}

.logo {
  display: grid;
  justify-items: center;
  gap: 2px;
}

.logo span {
  font-family: Sora, sans-serif;
  font-size: 1.6rem;
  font-weight: 800;
  color: var(--cea-blue);
  letter-spacing: 0.08em;
}

.logo small {
  color: var(--cea-gold);
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

form {
  display: grid;
  gap: 14px;
}

h2 {
  color: var(--cea-blue);
  font-size: 1.1rem;
  margin: 0;
}

.hint {
  color: var(--cea-muted);
  font-size: 0.88rem;
  margin: -8px 0 0;
}

label {
  display: grid;
  gap: 6px;
  font-size: 0.88rem;
  font-weight: 700;
  color: var(--cea-text);
}

input,
select {
  border: 1px solid var(--cea-border);
  border-radius: 10px;
  padding: 11px 13px;
  font: inherit;
  color: var(--cea-text);
  background: #fff;
}

input:focus,
select:focus {
  outline: 2px solid rgba(31, 102, 220, 0.22);
  border-color: rgba(31, 102, 220, 0.45);
}

button[type='submit'] {
  border: none;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--cea-blue), var(--cea-blue-2));
  color: #fff;
  padding: 13px;
  font-weight: 800;
  font-size: 0.95rem;
  cursor: pointer;
  box-shadow: 0 8px 18px rgba(13, 60, 143, 0.24);
}

button[type='submit']:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

button[type='submit']:hover:not(:disabled) {
  transform: translateY(-1px);
}

.back-btn {
  border: 1px solid var(--cea-border);
  border-radius: 12px;
  background: transparent;
  color: var(--cea-muted);
  padding: 10px;
  font-weight: 700;
  cursor: pointer;
}

.tipo-label select {
  background: #f7faff;
}

.error {
  color: #b91c1c;
  font-size: 0.86rem;
  font-weight: 700;
  margin: 0;
}

.demo-hint {
  color: var(--cea-muted);
  font-size: 0.78rem;
  text-align: center;
  margin: 0;
  line-height: 1.7;
}

.demo-hint code {
  font-family: monospace;
  background: #f0f4ff;
  padding: 1px 5px;
  border-radius: 4px;
  color: var(--cea-blue);
}
</style>
