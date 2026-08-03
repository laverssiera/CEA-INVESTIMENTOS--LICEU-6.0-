<template>
  <div class="container">
    <h2 class="screen-title">Central de Suporte</h2>
    <p class="screen-subtitle">Atendimento institucional para investidores e clientes</p>

    <section class="support-card">
      <div class="title-row">
        <h3>Fale com um especialista</h3>
        <span class="status" :class="{ offline: !isOnline }">
          <i></i>{{ isOnline ? 'Online agora' : 'Fora do horario' }}
        </span>
      </div>
      <p>Horario: Segunda a sexta, 08:00 as 18:00</p>
      <ul>
        <li>Chat prioritario para carteira ativa</li>
        <li>Suporte de onboarding documental</li>
        <li>Acompanhamento de solicitacoes em tempo real</li>
      </ul>
      <a class="cta" href="https://wa.me/5511999990000" target="_blank" rel="noopener noreferrer">Abrir Atendimento</a>
    </section>

    <section class="support-card light">
      <h3>Canais</h3>
      <p>
        WhatsApp:
        <a class="channel-link" href="https://wa.me/5511999990000" target="_blank" rel="noopener noreferrer">+55 11 99999-0000</a>
      </p>
      <p>
        E-mail:
        <a class="channel-link" href="mailto:suporte@cea.com.br">suporte@cea.com.br</a>
      </p>
    </section>

    <section class="support-card light form-card">
      <h3>Abrir Ticket Interno</h3>
      <p>Registre sua solicitacao para acompanhamento institucional.</p>

      <form @submit.prevent="submitTicket">
        <label>
          Assunto
          <input v-model="subject" type="text" required placeholder="Ex.: Atualizacao de cadastro" />
        </label>

        <label>
          E-mail (opcional)
          <input v-model="email" type="email" placeholder="para recebermos retorno" />
        </label>

        <label>
          Mensagem
          <textarea v-model="message" rows="4" required placeholder="Descreva o que voce precisa."></textarea>
        </label>

        <button class="send-btn" type="submit" :disabled="loading">
          {{ loading ? 'Enviando...' : 'Enviar Ticket' }}
        </button>
      </form>

      <div v-if="protocol" class="sent-message">
        <strong>Ticket registrado!</strong>
        <span>Protocolo: <code>{{ protocol }}</code></span>
        <small>Nosso time retornara em ate 1 dia util.</small>
      </div>

      <p v-if="errorMsg" class="error-message">{{ errorMsg }}</p>
    </section>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { submitSupportTicket } from '../services/api.js'

const subject = ref('')
const message = ref('')
const email = ref('')
const loading = ref(false)
const protocol = ref('')
const errorMsg = ref('')

const isOnline = computed(() => {
  const now = new Date()
  const day = now.getDay()
  const hour = now.getHours()
  return day >= 1 && day <= 5 && hour >= 8 && hour < 18
})

async function submitTicket() {
  loading.value = true
  errorMsg.value = ''
  protocol.value = ''
  try {
    const res = await submitSupportTicket({
      subject: subject.value,
      message: message.value,
      email: email.value,
    })
    protocol.value = res.protocol
    subject.value = ''
    message.value = ''
    email.value = ''
  } catch (err) {
    errorMsg.value = err.message || 'Erro ao enviar o ticket. Tente novamente.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.support-card {
  background: linear-gradient(135deg, var(--cea-blue), var(--cea-blue-2));
  color: #fff;
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.16);
  padding: 18px;
  display: grid;
  gap: 10px;
  margin-bottom: 12px;
  box-shadow: 0 12px 24px rgba(13, 60, 143, 0.22);
}

.support-card h3 {
  font-size: 1rem;
}

.title-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
}

.status {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 0.74rem;
  font-weight: 700;
  color: #d7ffe3;
  background: rgba(255, 255, 255, 0.16);
  border: 1px solid rgba(255, 255, 255, 0.24);
  border-radius: 999px;
  padding: 5px 8px;
}

.status i {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #88f6a6;
  box-shadow: 0 0 0 0 rgba(136, 246, 166, 0.5);
  animation: pulse 1.8s ease infinite;
}

.status.offline {
  color: #ffe0d5;
}

.status.offline i {
  background: #ffc5b4;
  box-shadow: none;
  animation: none;
}

.support-card p,
.support-card li {
  color: #dce7ff;
  font-size: 0.92rem;
}

.support-card ul {
  margin: 0;
  padding-left: 18px;
  display: grid;
  gap: 6px;
}

.cta {
  margin-top: 4px;
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: 10px;
  background: #fff;
  color: var(--cea-blue);
  padding: 10px 12px;
  font-weight: 800;
  cursor: pointer;
  text-decoration: none;
  text-align: center;
}

.cta:hover {
  transform: translateY(-1px);
}

.support-card.light {
  background: linear-gradient(180deg, #fff 0%, #f7faff 100%);
  border-color: var(--cea-border);
  box-shadow: 0 8px 18px rgba(13, 60, 143, 0.08);
}

.support-card.light p {
  color: var(--cea-text);
}

.form-card form {
  display: grid;
  gap: 10px;
}

.form-card label {
  display: grid;
  gap: 6px;
  color: var(--cea-text);
  font-weight: 700;
  font-size: 0.9rem;
}

.form-card input,
.form-card textarea {
  border: 1px solid var(--cea-border);
  border-radius: 10px;
  background: #fff;
  padding: 10px 12px;
  color: var(--cea-text);
  font: inherit;
}

.form-card input:focus,
.form-card textarea:focus {
  outline: 2px solid rgba(31, 102, 220, 0.2);
  border-color: rgba(31, 102, 220, 0.45);
}

.send-btn {
  border: none;
  border-radius: 10px;
  background: var(--cea-blue);
  color: #fff;
  padding: 10px 12px;
  font-weight: 800;
  cursor: pointer;
}

.send-btn:hover {
  transform: translateY(-1px);
}

.sent-message {
  margin-top: 8px;
  display: grid;
  gap: 4px;
  background: #f0fdf4;
  border: 1px solid #a7f3c4;
  border-radius: 10px;
  padding: 12px 14px;
  color: #1f7a46;
}

.sent-message strong {
  font-size: 0.95rem;
}

.sent-message code {
  font-family: monospace;
  font-weight: 800;
  color: var(--cea-blue);
  background: #e8f0ff;
  padding: 2px 6px;
  border-radius: 6px;
}

.sent-message small {
  color: #4a8a63;
  font-size: 0.82rem;
}

.error-message {
  margin-top: 8px;
  color: #b91c1c;
  font-weight: 700;
  font-size: 0.88rem;
}

.channel-link {
  color: var(--cea-blue);
  font-weight: 700;
  text-decoration: none;
}

.channel-link:hover {
  text-decoration: underline;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(136, 246, 166, 0.5);
  }
  70% {
    box-shadow: 0 0 0 8px rgba(136, 246, 166, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(136, 246, 166, 0);
  }
}
</style>