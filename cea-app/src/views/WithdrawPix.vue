<template>
  <div class="container">
    <h2 class="screen-title">Saque PIX</h2>
    <p class="screen-subtitle">Transferência instantânea para qualquer chave PIX</p>

    <!-- Saldo disponível -->
    <div class="balance-banner">
      <span>Saldo disponível</span>
      <strong>{{ formatBRL(walletBalance) }}</strong>
    </div>

    <!-- Etapa 1 — Chave + Valor -->
    <section v-if="step === 'form'" class="card">
      <h3>Dados do saque</h3>

      <label class="field">
        <span>Tipo de chave</span>
        <select v-model="keyType">
          <option value="cpf">CPF</option>
          <option value="cnpj">CNPJ</option>
          <option value="email">E-mail</option>
          <option value="phone">Telefone</option>
          <option value="random">Chave aleatória</option>
        </select>
      </label>

      <label class="field">
        <span>Chave PIX</span>
        <input
          v-model="pixKey"
          :placeholder="keyPlaceholder"
          autocomplete="off"
        />
      </label>

      <label class="field">
        <span>Valor (R$)</span>
        <input
          v-model="amountStr"
          type="number"
          min="1"
          :max="walletBalance"
          step="0.01"
          placeholder="0,00"
          inputmode="decimal"
        />
      </label>

      <p v-if="amountExceeds" class="warn">Valor maior que o saldo disponível.</p>

      <button class="cta" :disabled="!canProceed" @click="step = 'confirm'">
        Continuar
      </button>

      <p v-if="errorMsg" class="error">{{ errorMsg }}</p>
    </section>

    <!-- Etapa 2 — Confirmação -->
    <section v-else-if="step === 'confirm'" class="card confirm-card">
      <h3>Confirmar saque</h3>

      <div class="row"><span>Valor</span><strong>{{ formatBRL(amount) }}</strong></div>
      <div class="row"><span>Chave {{ keyType.toUpperCase() }}</span><strong>{{ pixKey }}</strong></div>
      <div class="row warn-row">
        <span>Saldo após saque</span>
        <strong>{{ formatBRL(walletBalance - amount) }}</strong>
      </div>

      <label class="field">
        <span>Código MFA</span>
        <input v-model="mfaCode" type="password" placeholder="Digite seu código MFA" />
      </label>

      <p class="notice">Transferências PIX são irreversíveis. Confirme os dados antes de prosseguir.</p>

      <div class="btn-pair">
        <button class="cta secondary" @click="step = 'form'">Voltar</button>
        <button class="cta" :disabled="loading" @click="doWithdraw">
          {{ loading ? 'Processando...' : 'Confirmar saque' }}
        </button>
      </div>

      <p v-if="errorMsg" class="error">{{ errorMsg }}</p>
    </section>

    <!-- Etapa 3 — Sucesso -->
    <section v-else class="card success-card">
      <span class="check">✔</span>
      <h3>Solicitação enviada!</h3>
      <p>{{ formatBRL(result.amount) }} aguardando aprovação institucional para envio PIX.</p>
      <p class="protocol">Protocolo: <code>{{ result.wid }}</code></p>
      <div class="btn-pair">
        <router-link to="/account" class="cta secondary">Ver extrato</router-link>
        <button class="cta" @click="reset">Novo saque</button>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { fetchWalletBalance, pixWithdraw } from '../services/api.js'
import { auth } from '../store/auth.js'

const step = ref('form')
const keyType = ref('cpf')
const pixKey = ref('')
const amountStr = ref('')
const loading = ref(false)
const errorMsg = ref('')
const result = ref({})
const walletBalance = ref(0)
const mfaCode = ref('')

const KEY_PLACEHOLDERS = {
  cpf: '000.000.000-00',
  cnpj: '00.000.000/0001-00',
  email: 'email@exemplo.com',
  phone: '+55 11 90000-0000',
  random: '0000aaaa-0000-0000-0000-000000000000',
}
const keyPlaceholder = computed(() => KEY_PLACEHOLDERS[keyType.value] ?? '')

const amount = computed(() => parseFloat(amountStr.value) || 0)
const amountExceeds = computed(() => amount.value > walletBalance.value)
const canProceed = computed(
  () => pixKey.value.trim().length >= 3 && amount.value >= 1 && !amountExceeds.value
)

function formatBRL(v) {
  return (v ?? 0).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}

onMounted(async () => {
  try {
    const data = await fetchWalletBalance()
    walletBalance.value = data.balance ?? 0
  } catch { /* usa zero */ }
})

async function doWithdraw() {
  loading.value = true
  errorMsg.value = ''
  try {
    if (!mfaCode.value.trim()) {
      throw new Error('Informe o código MFA para prosseguir.')
    }
    const data = await pixWithdraw({
      amount: amount.value,
      userId: auth.name ?? 'demo',
      pixKey: pixKey.value.trim(),
      keyType: keyType.value,
      mfaCode: mfaCode.value.trim(),
    })
    result.value = data
    step.value = 'success'
  } catch (err) {
    errorMsg.value = err.message
  } finally {
    loading.value = false
  }
}

function reset() {
  step.value = 'form'
  pixKey.value = ''
  amountStr.value = ''
  mfaCode.value = ''
  result.value = {}
  errorMsg.value = ''
}
</script>

<style scoped>
h3 { font-size: 1rem; color: var(--cea-blue); margin: 0; }

.balance-banner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(135deg, #0d2f6e, #101e3a);
  color: #fff;
  border-radius: 14px;
  padding: 14px 18px;
  margin-bottom: 16px;
}

.balance-banner span { font-size: 0.82rem; color: #8faed4; }
.balance-banner strong { font-size: 1.2rem; font-family: Sora, sans-serif; }

.card {
  background: #fff;
  border: 1px solid var(--cea-border);
  border-radius: 18px;
  padding: 20px;
  display: grid;
  gap: 14px;
  box-shadow: 0 8px 20px rgba(13, 60, 143, 0.08);
}

.field { display: grid; gap: 5px; font-size: 0.85rem; color: var(--cea-muted); }

.field select,
.field input {
  border: 1px solid var(--cea-border);
  border-radius: 10px;
  padding: 10px 12px;
  font-size: 0.94rem;
  color: var(--cea-text);
  background: #f8fbff;
}

.field select:focus, .field input:focus {
  outline: none;
  border-color: var(--cea-blue-2);
}

.row {
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem;
  padding: 8px 0;
  border-bottom: 1px solid #f0f4fa;
}

.row:last-of-type { border-bottom: none; }
.row span { color: var(--cea-muted); }
.row strong { color: var(--cea-text); }
.warn-row strong { color: var(--cea-blue-2); }

.notice {
  font-size: 0.8rem;
  color: #b45309;
  background: #fffbeb;
  border: 1px solid #fde68a;
  border-radius: 10px;
  padding: 10px 12px;
  margin: 0;
}

.btn-pair { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }

.cta {
  border: none;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--cea-blue), var(--cea-blue-2));
  color: #fff;
  padding: 13px;
  font-weight: 800;
  cursor: pointer;
  text-align: center;
  text-decoration: none;
  box-shadow: 0 8px 18px rgba(13, 60, 143, 0.22);
}

.cta:disabled { opacity: 0.5; cursor: not-allowed; }
.cta:hover:not(:disabled) { transform: translateY(-1px); }

.cta.secondary {
  background: transparent;
  border: 1px solid var(--cea-border);
  color: var(--cea-muted);
  box-shadow: none;
}

.success-card { justify-items: center; text-align: center; }

.check {
  width: 56px; height: 56px;
  border-radius: 50%;
  background: #dcfce7;
  color: #16a34a;
  font-size: 1.4rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.protocol { font-size: 0.82rem; color: var(--cea-muted); margin: 0; }
.protocol code { color: var(--cea-blue); font-size: 0.78rem; word-break: break-all; }

.warn { color: #b91c1c; font-size: 0.83rem; margin: 0; font-weight: 700; }
.error { color: #b91c1c; font-size: 0.86rem; font-weight: 700; margin: 0; }
</style>
