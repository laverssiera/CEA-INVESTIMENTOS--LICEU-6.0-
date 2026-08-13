<template>
  <div class="container">
    <h2 class="screen-title">Assinatura Digital</h2>
    <p class="screen-subtitle">Gestão e assinatura de contratos com trilha completa</p>

    <section class="card">
      <h3>Novo contrato</h3>
      <label class="field">
        <span>Título</span>
        <input v-model="form.title" placeholder="Contrato de investimento Série A" />
      </label>
      <label class="field">
        <span>Hash do documento</span>
        <input v-model="form.content_hash" placeholder="sha256:..." />
      </label>
      <label class="field">
        <span>Partes (separadas por vírgula)</span>
        <input v-model="form.counterparties" placeholder="investidor,admin,tesouraria" />
      </label>
      <button class="cta" :disabled="loading" @click="createNewContract">
        {{ loading ? 'Criando...' : 'Criar contrato' }}
      </button>
      <p v-if="errorMsg" class="error">{{ errorMsg }}</p>
      <p v-if="successMsg" class="ok">{{ successMsg }}</p>
    </section>

    <section class="card">
      <h3>Meus contratos</h3>
      <div v-if="!contracts.length" class="empty">Nenhum contrato disponível.</div>
      <div v-for="c in contracts" :key="c.contract_id" class="row">
        <div>
          <strong>{{ c.title }}</strong>
          <small>{{ c.contract_id }} · {{ c.status }}</small>
        </div>
        <button class="secondary" @click="openSign(c.contract_id)">Assinar</button>
      </div>
    </section>

    <section v-if="selectedContract" class="card sign-box">
      <h3>Assinar contrato {{ selectedContract }}</h3>
      <label class="field">
        <span>Token de assinatura</span>
        <input v-model="signatureToken" placeholder="Assinatura OTP/Token" />
      </label>
      <button class="cta" :disabled="loading || !signatureToken" @click="signSelected">
        {{ loading ? 'Assinando...' : 'Confirmar assinatura' }}
      </button>
    </section>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { createContract, fetchContracts, signContract } from '../services/api.js'

const form = ref({ title: '', content_hash: '', counterparties: '' })
const contracts = ref([])
const loading = ref(false)
const errorMsg = ref('')
const successMsg = ref('')
const selectedContract = ref('')
const signatureToken = ref('')

async function loadContracts() {
  try {
    const data = await fetchContracts()
    contracts.value = data.items ?? []
  } catch {
    contracts.value = []
  }
}

function openSign(contractId) {
  selectedContract.value = contractId
  signatureToken.value = ''
}

async function createNewContract() {
  loading.value = true
  errorMsg.value = ''
  successMsg.value = ''
  try {
    const counterparties = form.value.counterparties
      .split(',')
      .map((s) => s.trim())
      .filter(Boolean)
    await createContract({
      title: form.value.title,
      content_hash: form.value.content_hash,
      counterparties,
    })
    successMsg.value = 'Contrato criado com sucesso.'
    form.value = { title: '', content_hash: '', counterparties: '' }
    await loadContracts()
  } catch (err) {
    errorMsg.value = err.message
  } finally {
    loading.value = false
  }
}

async function signSelected() {
  loading.value = true
  errorMsg.value = ''
  successMsg.value = ''
  try {
    await signContract(selectedContract.value, signatureToken.value)
    successMsg.value = `Contrato ${selectedContract.value} assinado.`
    selectedContract.value = ''
    signatureToken.value = ''
    await loadContracts()
  } catch (err) {
    errorMsg.value = err.message
  } finally {
    loading.value = false
  }
}

onMounted(loadContracts)
</script>

<style scoped>
.card { background: #fff; border: 1px solid var(--cea-border); border-radius: 16px; padding: 18px; margin-bottom: 12px; display: grid; gap: 10px; }
h3 { margin: 0; color: var(--cea-blue); font-size: 0.95rem; }
.field { display: grid; gap: 5px; font-size: 0.82rem; color: var(--cea-muted); }
.field input { border: 1px solid var(--cea-border); border-radius: 10px; padding: 10px; background: #f8fbff; }
.row { display: flex; justify-content: space-between; gap: 10px; align-items: center; padding: 8px 0; border-bottom: 1px solid #eef3fb; }
.row:last-child { border-bottom: none; }
.row strong { display: block; font-size: 0.9rem; color: var(--cea-text); }
.row small { font-size: 0.75rem; color: var(--cea-muted); }
.cta { border: none; border-radius: 12px; background: linear-gradient(135deg, var(--cea-blue), var(--cea-blue-2)); color: #fff; padding: 12px; font-weight: 800; cursor: pointer; }
.secondary { border: 1px solid var(--cea-border); border-radius: 10px; background: #f5f8ff; color: var(--cea-blue); padding: 8px 10px; font-weight: 700; cursor: pointer; }
.error { color: #b91c1c; margin: 0; font-size: 0.82rem; }
.ok { color: #166534; margin: 0; font-size: 0.82rem; }
.empty { color: var(--cea-muted); font-size: 0.86rem; }
</style>
