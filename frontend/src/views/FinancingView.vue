<template>
  <div class="page">
    <section class="hero">
      <div>
        <p class="eyebrow">Financiamento</p>
        <h2>Solicitação inicial de crédito para construção e ativos reais.</h2>
        <p>
          Este fluxo consolida a triagem de dados essenciais da obra para originação, análise de
          risco e encaminhamento ao time interno.
        </p>
      </div>

      <div class="hero-grid">
        <div class="card">
          <small>Etapa</small>
          <div class="stat-value">Pré-análise</div>
          <span class="tag info">Entrada simplificada</span>
        </div>
        <div class="card">
          <small>Destino</small>
          <div class="stat-value">Pipeline crédito</div>
          <span class="tag warning">Backoffice</span>
        </div>
      </div>
    </section>

    <section class="grid-2">
      <article class="panel">
        <small>Formulário</small>
        <h3>Dados iniciais do financiamento</h3>

        <div v-if="submitted" class="card">
          <p><strong>Protocolo:</strong> {{ result.id }}</p>
          <p>{{ result.message }}</p>
        </div>

        <form v-else class="form-grid" @submit.prevent="handleSubmit">
          <label>
            Nome
            <input v-model="form.name" placeholder="Nome do responsável" type="text" required />
          </label>
          <label>
            CPF/CNPJ
            <input v-model="form.cpf_cnpj" placeholder="000.000.000-00" type="text" required />
          </label>
          <label>
            Email
            <input v-model="form.email" placeholder="contato@empresa.com" type="email" required />
          </label>
          <label>
            Possui terreno
            <select v-model="form.has_land">
              <option :value="true">Sim</option>
              <option :value="false">Não</option>
            </select>
          </label>
          <label>
            Localização
            <input v-model="form.location" placeholder="Cidade / UF" type="text" required />
          </label>
          <label>
            Tipo de obra
            <input v-model="form.project_type" placeholder="Residencial, industrial, comercial" type="text" required />
          </label>
          <label>
            Valor solicitado (R$)
            <input v-model.number="form.requested_value" placeholder="0" type="number" min="1" required />
          </label>
          <label>
            Prazo (meses)
            <input v-model.number="form.term_months" placeholder="24" type="number" min="1" max="360" required />
          </label>
          <p v-if="error" class="form-error">{{ error }}</p>
          <button class="primary-btn" type="submit" :disabled="loading">
            {{ loading ? 'Enviando...' : 'Enviar para análise' }}
          </button>
        </form>
      </article>

      <article class="panel">
        <small>Fluxo interno</small>
        <h3>O que acontece após o envio</h3>
        <ul class="list">
          <li>registro no pipeline de crédito;</li>
          <li>validação documental e cadastral;</li>
          <li>análise de risco, garantias e prazo;</li>
          <li>retorno ao cliente com status e próximos passos.</li>
        </ul>
      </article>
    </section>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { submitFinancingRequest } from '../services/liceuApi'

const loading = ref(false)
const submitted = ref(false)
const error = ref('')
const result = ref({})

const form = reactive({
  name: '',
  cpf_cnpj: '',
  email: '',
  has_land: false,
  location: '',
  project_type: '',
  requested_value: null,
  term_months: null,
})

const handleSubmit = async () => {
  loading.value = true
  error.value = ''
  try {
    result.value = await submitFinancingRequest(form)
    submitted.value = true
  } catch (e) {
    error.value = e?.response?.data?.detail || 'Erro ao enviar. Tente novamente.'
  } finally {
    loading.value = false
  }
}
</script>