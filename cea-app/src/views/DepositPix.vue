<template>
  <div class="container">
    <h2 class="screen-title">Depositar via PIX</h2>
    <p class="screen-subtitle">Crédito instantâneo na sua carteira CEA</p>

    <!-- Etapa 1 — Valor -->
    <section v-if="step === 'form'" class="pix-card">
      <h3>Informe o valor</h3>

      <div class="amount-input">
        <span>R$</span>
        <input
          v-model="amountStr"
          type="number"
          min="1"
          max="500000"
          step="0.01"
          placeholder="0,00"
          inputmode="decimal"
          autofocus
        />
      </div>

      <div class="presets">
        <button
          v-for="v in presets"
          :key="v"
          class="preset"
          :class="{ active: amountStr == v }"
          @click="amountStr = String(v)"
        >
          R$ {{ v.toLocaleString('pt-BR') }}
        </button>
      </div>

      <button class="cta" :disabled="!validAmount" @click="generate">
        {{ loading ? 'Gerando...' : 'Gerar QR Code PIX' }}
      </button>

      <p v-if="errorMsg" class="error">{{ errorMsg }}</p>
    </section>

    <!-- Etapa 2 — QR Code -->
    <section v-else-if="step === 'qr'" class="pix-card qr-card">
      <div class="timer" :class="{ urgent: secondsLeft < 120 }">
        Expira em {{ timerLabel }}
      </div>

      <h3>Escaneie o QR Code</h3>
      <p>Ou use o código Copia e Cola abaixo</p>

      <!-- QR Code visual via API pública de QR (sem dependência extra) -->
      <div class="qr-wrap">
        <img
          :src="`https://api.qrserver.com/v1/create-qr-code/?size=180x180&data=${encodeURIComponent(pixData.qrcode)}`"
          alt="QR Code PIX"
          width="180"
          height="180"
        />
      </div>

      <div class="copy-box" @click="copy">
        <code>{{ shortCode }}</code>
        <span class="copy-label">{{ copied ? 'Copiado!' : 'Toque para copiar' }}</span>
      </div>

      <div class="amount-badge">
        Valor: <strong>{{ formatBRL(pixData.amount) }}</strong>
      </div>

      <p class="hint">Após o pagamento o saldo será creditado automaticamente.</p>

      <button class="cta secondary" @click="reset">Gerar novo PIX</button>
    </section>

    <!-- Etapa 3 — Confirmado -->
    <section v-else class="pix-card success-card">
      <span class="check">✔</span>
      <h3>Pagamento confirmado!</h3>
      <p>{{ formatBRL(pixData.amount) }} creditados na sua carteira.</p>
      <router-link to="/portfolio" class="cta">Ver Carteira</router-link>
    </section>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, ref } from 'vue'
import { createPixCharge, connectWalletSocket } from '../services/api.js'
import { auth } from '../store/auth.js'

const step = ref('form')
const amountStr = ref('')
const loading = ref(false)
const errorMsg = ref('')
const pixData = ref({})
const copied = ref(false)
const secondsLeft = ref(0)
const presets = [100, 500, 1000, 5000]

let _timer = null
let _ws = null

const validAmount = computed(() => {
  const v = parseFloat(amountStr.value)
  return !isNaN(v) && v >= 1 && v <= 500_000
})

const timerLabel = computed(() => {
  const m = Math.floor(secondsLeft.value / 60).toString().padStart(2, '0')
  const s = (secondsLeft.value % 60).toString().padStart(2, '0')
  return `${m}:${s}`
})

const shortCode = computed(() => {
  const c = pixData.value.qrcode ?? ''
  return c.length > 60 ? c.slice(0, 30) + '...' + c.slice(-20) : c
})

function formatBRL(v) {
  return (v ?? 0).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}

async function generate() {
  loading.value = true
  errorMsg.value = ''
  try {
    const res = await createPixCharge({
      amount: parseFloat(amountStr.value),
      userId: auth.name ?? 'demo',
    })
    pixData.value = res
    step.value = 'qr'

    // countdown timer
    const expiry = new Date(res.expires_at)
    secondsLeft.value = Math.max(0, Math.round((expiry - Date.now()) / 1000))
    _timer = setInterval(() => {
      secondsLeft.value--
      if (secondsLeft.value <= 0) {
        clearInterval(_timer)
        if (step.value === 'qr') reset()
      }
    }, 1000)

    // WebSocket para receber confirmação automática
    _ws = connectWalletSocket(auth.name ?? 'demo', (data) => {
      if (data.event === 'wallet.updated' || data.event === 'wallet_updated') {
        step.value = 'confirmed'
        clearInterval(_timer)
        _ws?.close()
      }
    })
  } catch (err) {
    errorMsg.value = err.message || 'Erro ao gerar cobrança PIX.'
  } finally {
    loading.value = false
  }
}

async function copy() {
  try {
    await navigator.clipboard.writeText(pixData.value.qrcode ?? '')
    copied.value = true
    setTimeout(() => (copied.value = false), 2500)
  } catch {
    copied.value = false
  }
}

function reset() {
  step.value = 'form'
  amountStr.value = ''
  pixData.value = {}
  clearInterval(_timer)
  _ws?.close()
}

onBeforeUnmount(() => {
  clearInterval(_timer)
  _ws?.close()
})
</script>

<style scoped>
h3 {
  font-size: 1rem;
  color: var(--cea-blue);
  margin: 0;
}

.pix-card {
  background: linear-gradient(180deg, #fff 0%, #f8fbff 100%);
  border: 1px solid var(--cea-border);
  border-radius: 18px;
  padding: 22px;
  display: grid;
  gap: 16px;
  box-shadow: 0 10px 22px rgba(13, 60, 143, 0.08);
}

/* ── Valor ── */
.amount-input {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 1.5rem;
  font-family: Sora, sans-serif;
  font-weight: 800;
  color: var(--cea-blue);
}

.amount-input input {
  flex: 1;
  border: none;
  border-bottom: 2px solid var(--cea-border);
  border-radius: 0;
  background: transparent;
  font: inherit;
  color: var(--cea-text);
  padding: 4px 0;
}

.amount-input input:focus {
  outline: none;
  border-bottom-color: var(--cea-blue-2);
}

.presets {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

.preset {
  border: 1px solid var(--cea-border);
  border-radius: 10px;
  background: #f5f8ff;
  color: var(--cea-blue);
  font-weight: 700;
  padding: 10px;
  cursor: pointer;
  font-size: 0.86rem;
}

.preset.active {
  background: var(--cea-blue);
  color: #fff;
  border-color: var(--cea-blue);
}

.preset:hover:not(.active) {
  background: #e8f0ff;
}

/* ── QR ── */
.qr-card {
  justify-items: center;
  text-align: center;
}

.timer {
  font-size: 0.82rem;
  font-weight: 800;
  background: #e8f4ff;
  color: var(--cea-blue-2);
  border-radius: 999px;
  padding: 5px 12px;
}

.timer.urgent {
  background: #fff0f0;
  color: #dc2626;
}

.qr-wrap {
  border: 3px solid var(--cea-border);
  border-radius: 14px;
  padding: 12px;
  background: #fff;
}

.qr-wrap img {
  display: block;
  border-radius: 8px;
}

.copy-box {
  width: 100%;
  background: #f0f6ff;
  border: 1px solid rgba(31, 102, 220, 0.2);
  border-radius: 12px;
  padding: 12px 14px;
  cursor: pointer;
  display: grid;
  gap: 4px;
}

.copy-box code {
  font-family: monospace;
  font-size: 0.74rem;
  color: var(--cea-text);
  word-break: break-all;
}

.copy-label {
  font-size: 0.76rem;
  font-weight: 700;
  color: var(--cea-blue-2);
}

.amount-badge {
  font-size: 0.9rem;
  color: var(--cea-muted);
}

.amount-badge strong {
  color: var(--cea-text);
  font-size: 1.05rem;
}

.hint {
  font-size: 0.82rem;
  color: var(--cea-muted);
  margin: 0;
}

/* ── Sucesso ── */
.success-card {
  justify-items: center;
  text-align: center;
  gap: 14px;
}

.check {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: #dcfce7;
  color: #16a34a;
  font-size: 1.4rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* ── Botões ── */
.cta {
  border: none;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--cea-blue), var(--cea-blue-2));
  color: #fff;
  padding: 13px;
  font-weight: 800;
  cursor: pointer;
  text-decoration: none;
  text-align: center;
  box-shadow: 0 8px 18px rgba(13, 60, 143, 0.22);
}

.cta:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.cta:hover:not(:disabled) {
  transform: translateY(-1px);
}

.cta.secondary {
  background: transparent;
  border: 1px solid var(--cea-border);
  color: var(--cea-muted);
  box-shadow: none;
}

.error {
  color: #b91c1c;
  font-size: 0.86rem;
  font-weight: 700;
  margin: 0;
}
</style>
