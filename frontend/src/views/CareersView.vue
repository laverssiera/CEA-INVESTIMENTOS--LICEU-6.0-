<template>
  <div class="page">
    <section class="hero">
      <div>
        <p class="eyebrow">Trabalhe Conosco</p>
        <h2>Times financeiros, operacionais e de tecnologia para escalar a plataforma.</h2>
        <p>
          A frente institucional demanda perfis de crédito, risco, relacionamento, compliance,
          produto e engenharia de software com foco em ativos reais.
        </p>
      </div>

      <div class="hero-grid">
        <div class="card">
          <small>Formato</small>
          <div class="stat-value">Banco + tech</div>
          <span class="tag info">Operação híbrida</span>
        </div>
        <div class="card">
          <small>Foco</small>
          <div class="stat-value">RWA</div>
          <span class="tag warning">Escala operacional</span>
        </div>
      </div>
    </section>

    <section class="grid-2">
      <article class="panel">
        <small>Candidatura</small>
        <h3>Envio de perfil profissional</h3>
        <form v-if="!submitted" class="form-grid" @submit.prevent="handleSubmit">
          <label>
            Nome
            <input v-model="form.name" type="text" placeholder="Seu nome" required />
          </label>
          <label>
            Email
            <input v-model="form.email" type="email" placeholder="voce@email.com" required />
          </label>
          <label>
            Área de interesse
            <input v-model="form.area" type="text" placeholder="Crédito, risco, produto, engenharia" required />
          </label>
          <label>
            LinkedIn
            <input v-model="form.linkedin" type="url" placeholder="https://linkedin.com/in/..." />
          </label>
          <label>
            Upload CV
            <input type="file" />
          </label>
          <label>
            Mensagem
            <input v-model="form.message" type="text" placeholder="Resumo do seu perfil" />
          </label>
          <p v-if="error" class="form-error">{{ error }}</p>
          <button class="primary-btn" type="submit" :disabled="loading">
            {{ loading ? 'Enviando...' : 'Enviar candidatura' }}
          </button>
        </form>

        <div v-if="submitted" class="card" style="margin-top:16px">
          <p><strong>Protocolo:</strong> {{ result.id }}</p>
          <p>{{ result.message }}</p>
        </div>
      </article>

      <article class="panel">
        <small>Áreas</small>
        <h3>Frentes prioritárias</h3>
        <ul class="list">
          <li>originação e análise de crédito;</li>
          <li>compliance, auditoria e jurídico;</li>
          <li>tesouraria e relacionamento institucional;</li>
          <li>produto digital e engenharia da plataforma.</li>
        </ul>
      </article>
    </section>
  </div>
</template>