<template>
  <div class="page">
    <section class="hero">
      <div>
        <p class="eyebrow">Trabalhe Conosco</p>
        <h2>Construa o futuro financeiro com a CEA</h2>
        <p>
          Faça parte de um time que integra finanças, tecnologia e engenharia para gerar
          impacto real no mercado de ativos reais.
        </p>
        <div class="actions">
          <a href="#vagas" class="primary-btn">Ver vagas</a>
          <a href="#cultura" class="secondary-btn">Cultura CEA</a>
          <RouterLink to="/esg" class="secondary-btn">ESG</RouterLink>
          <a href="#curriculo" class="secondary-btn">Enviar curriculo</a>
        </div>
      </div>
      <div class="hero-grid">
        <div class="card">
          <small>Modelo</small>
          <div class="stat-value">Institucional + Tech</div>
          <span class="tag info">RWA e LICEU</span>
        </div>
        <div class="card">
          <small>Times</small>
          <div class="stat-value">6 Areas</div>
          <span class="tag warning">Crescimento acelerado</span>
        </div>
      </div>
    </section>

    <section id="cultura">
      <h3 class="section-title">Cultura CEA</h3>
      <div class="grid-4">
        <article class="card">
          <h4>Inovacao financeira</h4>
          <p>Produtos de investimento orientados por dados e compliance.</p>
        </article>
        <article class="card">
          <h4>Integracao com engenharia</h4>
          <p>Operacao integrada ao ecossistema LICEU 6.0.</p>
        </article>
        <article class="card">
          <h4>Tecnologia + RWA</h4>
          <p>Plataforma digital com foco em ativos reais e escala operacional.</p>
        </article>
        <article class="card">
          <h4>Impacto real no mercado</h4>
          <p>Financiamento e investimento com transformacao concreta.</p>
        </article>
      </div>
    </section>

    <section>
      <h3 class="section-title">Beneficios</h3>
      <div class="grid-2">
        <article class="panel" v-for="b in benefits" :key="b">
          <p>{{ b }}</p>
        </article>
      </div>
    </section>

    <section id="vagas">
      <h3 class="section-title">Areas</h3>
      <div class="grid-3">
        <article class="card" v-for="area in areas" :key="area">
          <h4>{{ area }}</h4>
        </article>
      </div>
    </section>

    <section id="curriculo" class="panel" style="margin-top: 24px">
      <small>Candidatura</small>
      <h3>Enviar curriculo</h3>
      <form class="form-grid" @submit.prevent="submitApplication">
        <label>
          Nome
          <input v-model="form.name" required type="text" placeholder="Seu nome" />
        </label>
        <label>
          Email
          <input v-model="form.email" required type="email" placeholder="voce@email.com" />
        </label>
        <label>
          Area de interesse
          <input v-model="form.area" required type="text" placeholder="Credito, ESG, Tecnologia..." />
        </label>
        <label>
          LinkedIn
          <input v-model="form.linkedin" type="url" placeholder="https://linkedin.com/in/..." />
        </label>
        <label>
          Mensagem
          <input v-model="form.message" type="text" placeholder="Resumo profissional" />
        </label>
        <p v-if="error" class="form-error">{{ error }}</p>
        <p v-if="success" class="tag info">Curriculo enviado com sucesso.</p>
        <button class="primary-btn" :disabled="loading" type="submit">
          {{ loading ? 'Enviando...' : 'Enviar curriculo' }}
        </button>
      </form>
    </section>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { RouterLink } from 'vue-router'

const loading = ref(false)
const success = ref(false)
const error = ref('')

const benefits = [
  'Ambiente institucional',
  'Projetos de alto impacto',
  'Crescimento profissional',
  'Participacao em inovacao financeira',
]

const areas = ['Credito', 'Investimentos', 'Compliance', 'Tecnologia', 'ESG', 'Operacoes']

const form = reactive({
  name: '',
  email: '',
  area: '',
  linkedin: '',
  message: '',
})

async function submitApplication() {
  loading.value = true
  error.value = ''
  success.value = false

  try {
    const res = await fetch('http://127.0.0.1:8000/api/careers/apply', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form),
    })

    if (!res.ok) {
      throw new Error('Falha ao enviar candidatura')
    }

    success.value = true
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Erro inesperado'
  } finally {
    loading.value = false
  }
}
</script>
