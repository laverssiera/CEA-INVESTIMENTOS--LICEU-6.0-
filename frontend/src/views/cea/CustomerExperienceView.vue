<template>
  <div class="page">
    <section class="hero cea-cx-hero">
      <div>
        <p class="eyebrow">Atendimento e suporte</p>
        <h2>Experiência do cliente CEA</h2>
        <p>
          Atendimento humanizado com tecnologia financeira de ponta. Nossa equipe está disponível
          para acompanhar você em cada etapa da sua jornada.
        </p>
      </div>
    </section>

    <!-- Canais de contato -->
    <section>
      <h3 class="section-title">Canais de atendimento</h3>
      <div class="grid-3">
        <a :href="`tel:${contact.phone}`" class="card cea-channel-card">
          <span class="cea-channel-icon">📞</span>
          <strong>Telefone</strong>
          <span class="cea-channel-value">{{ contact.phoneDisplay }}</span>
          <span class="tag info">Ligue agora</span>
        </a>
        <a :href="whatsappLink" target="_blank" rel="noopener" class="card cea-channel-card cea-channel-card--wa">
          <span class="cea-channel-icon">💬</span>
          <strong>WhatsApp</strong>
          <span class="cea-channel-value">{{ contact.whatsappDisplay }}</span>
          <span class="tag" style="background:rgba(37,211,102,0.12);color:#1a7a3a">Resposta rápida</span>
        </a>
        <a :href="`mailto:${contact.email}`" class="card cea-channel-card">
          <span class="cea-channel-icon">✉️</span>
          <strong>E-mail</strong>
          <span class="cea-channel-value cea-channel-value--sm">{{ contact.email }}</span>
          <span class="tag info">Suporte técnico</span>
        </a>
      </div>
      <div class="cea-hours-banner">
        <span>🕘</span>
        <span>Horário de atendimento: <strong>{{ contact.hours }}</strong></span>
      </div>
    </section>

    <!-- Jornada visual -->
    <section>
      <h3 class="section-title">Jornada do cliente</h3>
      <div class="cea-journey-timeline">
        <div
          v-for="(step, i) in journey"
          :key="i"
          class="cea-timeline-step"
          :class="{ 'cea-timeline-step--last': i === journey.length - 1 }"
        >
          <div class="cea-timeline-dot">
            <span>{{ step.icon }}</span>
          </div>
          <div class="card cea-timeline-card">
            <strong>{{ step.title }}</strong>
            <p>{{ step.desc }}</p>
            <span v-if="step.sla" class="tag info">SLA: {{ step.sla }}</span>
          </div>
        </div>
      </div>
    </section>

    <!-- SLA de atendimento -->
    <section>
      <h3 class="section-title">SLA de atendimento</h3>
      <div class="grid-4">
        <div v-for="item in sla" :key="item.label" class="card cea-sla-card">
          <span class="cea-sla-icon">{{ item.icon }}</span>
          <div class="stat-value">{{ item.time }}</div>
          <small>{{ item.label }}</small>
        </div>
      </div>
    </section>

    <!-- FAQ -->
    <section>
      <h3 class="section-title">Perguntas frequentes</h3>
      <div class="cea-faq">
        <div
          v-for="(item, i) in faq"
          :key="i"
          class="card cea-faq-item"
          :class="{ 'cea-faq-item--open': openFaq === i }"
          @click="openFaq = openFaq === i ? null : i"
        >
          <div class="cea-faq-question">
            <span>{{ item.q }}</span>
            <span class="cea-faq-arrow">{{ openFaq === i ? '▲' : '▼' }}</span>
          </div>
          <p v-show="openFaq === i" class="cea-faq-answer">{{ item.a }}</p>
        </div>
      </div>
    </section>

    <!-- CTA Final -->
    <div class="card cea-cx-cta">
      <h3>Ainda tem dúvidas?</h3>
      <p>Nossa equipe está pronta para atender você agora mesmo.</p>
      <div class="actions" style="justify-content:center">
        <a :href="whatsappLink" target="_blank" rel="noopener" class="primary-btn">💬 Abrir WhatsApp</a>
        <a :href="`tel:${contact.phone}`" class="secondary-btn secondary-btn-dark">📞 Ligar agora</a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const openFaq = ref(null)

const contact = {
  phone: '+551140000000',
  phoneDisplay: '(11) 4000-0000',
  whatsapp: '+5511900000000',
  whatsappDisplay: '(11) 90000-0000',
  email: 'atendimento@ceainvestimentos.com',
  hours: '09:00 às 18:00 · Segunda a sexta',
}

const whatsappLink = `https://wa.me/${contact.whatsapp}?text=Ol%C3%A1%2C%20preciso%20de%20ajuda%20com%20minha%20conta%20CEA%20INVESTIMENTOS.`

const journey = [
  { icon: '🏠', title: 'Acesso à plataforma', desc: 'Você acessa o portal CEA e conhece os serviços disponíveis.', sla: 'Imediato' },
  { icon: '📝', title: 'Cadastro e KYC', desc: 'Preenchimento do formulário de onboarding e envio de documentos.', sla: '24h análise' },
  { icon: '✅', title: 'Aprovação do perfil', desc: 'Equipe de compliance analisa e aprova seu cadastro.', sla: '48h úteis' },
  { icon: '📊', title: 'Suitability', desc: 'Você responde o questionário de perfil de investidor.', sla: '5 minutos' },
  { icon: '💰', title: 'Primeiro investimento', desc: 'Você acessa o Home Broker e realiza sua primeira aplicação.', sla: 'Disponível após aprovação' },
  { icon: '📈', title: 'Acompanhamento', desc: 'Dashboard com posição, rendimentos e progresso dos projetos em tempo real.', sla: 'Sempre disponível' },
  { icon: '🏦', title: 'Suporte contínuo', desc: 'Atendimento especializado via WhatsApp, telefone ou e-mail.', sla: 'SLA 4h úteis' },
]

const sla = [
  { icon: '💬', time: '< 2min', label: 'Resposta WhatsApp' },
  { icon: '📞', time: '< 3min', label: 'Tempo de espera telefone' },
  { icon: '✉️', time: '4h úteis', label: 'Retorno de e-mail' },
  { icon: '✅', time: '48h', label: 'Aprovação de cadastro' },
]

const faq = [
  {
    q: 'Como faço para começar a investir?',
    a: 'Acesse a plataforma em /investir, faça seu cadastro, complete o KYC e o questionário de suitability. Após aprovação, você já pode acessar o Home Broker e realizar investimentos.',
  },
  {
    q: 'Qual o valor mínimo para investir?',
    a: 'O valor mínimo é R$ 5.000 para pessoa física. Para pessoa jurídica, consulte nossa equipe para estruturação personalizada.',
  },
  {
    q: 'Como solicitar um financiamento?',
    a: 'Acesse a seção "Financiamento" no menu principal, preencha o formulário com os dados do seu projeto e aguarde a análise da nossa equipe de crédito. O prazo é de até 72 horas.',
  },
  {
    q: 'Meus dados estão seguros?',
    a: 'Sim. Utilizamos criptografia JWT, MFA obrigatório, RBAC por perfil e auditoria de todas as ações sensíveis. Seguimos as normas da LGPD e compliance regulatório CVM.',
  },
  {
    q: 'Como acompanho meus investimentos?',
    a: 'Após login no portal do investidor, você tem acesso ao Dashboard com posição consolidada, rendimentos, histórico de ordens e progresso das obras em tempo real via integração LICEU 6.0.',
  },
  {
    q: 'Qual o horário de atendimento?',
    a: 'De segunda a sexta, das 09:00 às 18:00. Para urgências, nosso chatbot está disponível 24h pelo WhatsApp.',
  },
]
</script>

<style scoped>
.cea-cx-hero {
  display: block;
  padding: 40px;
}

.cea-channel-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  text-align: center;
  padding: 28px 20px;
  text-decoration: none;
  color: inherit;
  cursor: pointer;
  transition: transform 0.2s, border-color 0.2s;
}

.cea-channel-card:hover {
  transform: translateY(-3px);
  border-color: var(--primary);
}

.cea-channel-card--wa:hover {
  border-color: #25d366;
}

.cea-channel-icon {
  font-size: 2.4rem;
}

.cea-channel-card strong {
  font-size: 1.05rem;
  color: var(--deep);
}

.cea-channel-value {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--primary);
}

.cea-channel-value--sm {
  font-size: 0.88rem;
}

.cea-hours-banner {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 16px;
  padding: 12px 20px;
  border-radius: 12px;
  background: rgba(31,59,99,0.06);
  border: 1px solid var(--border);
  font-size: 0.92rem;
  color: var(--muted);
}

/* Timeline */
.cea-journey-timeline {
  display: flex;
  flex-direction: column;
  gap: 0;
  margin-top: 20px;
  position: relative;
}

.cea-journey-timeline::before {
  content: '';
  position: absolute;
  left: 19px;
  top: 24px;
  bottom: 24px;
  width: 2px;
  background: var(--border);
}

.cea-timeline-step {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding-bottom: 16px;
}

.cea-timeline-dot {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--deep);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  flex-shrink: 0;
  z-index: 1;
  position: relative;
}

.cea-timeline-card {
  flex: 1;
  padding: 14px 18px;
}

.cea-timeline-card strong {
  display: block;
  color: var(--deep);
  margin-bottom: 4px;
}

.cea-timeline-card p {
  margin: 0 0 8px;
  color: var(--muted);
  font-size: 0.92rem;
}

/* SLA */
.cea-sla-card {
  text-align: center;
  padding: 24px 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
}

.cea-sla-icon {
  font-size: 1.8rem;
}

.cea-sla-card .stat-value {
  font-size: 1.4rem;
}

.cea-sla-card small {
  text-align: center;
}

/* FAQ */
.cea-faq {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 20px;
}

.cea-faq-item {
  cursor: pointer;
  padding: 16px 20px;
  transition: border-color 0.2s;
}

.cea-faq-item--open {
  border-color: var(--primary);
}

.cea-faq-question {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  font-weight: 600;
  color: var(--deep);
}

.cea-faq-arrow {
  font-size: 0.75rem;
  color: var(--muted);
  flex-shrink: 0;
}

.cea-faq-answer {
  margin: 12px 0 0;
  color: var(--muted);
  font-size: 0.92rem;
  line-height: 1.6;
}

/* CTA */
.cea-cx-cta {
  text-align: center;
  padding: 40px 32px;
  background: linear-gradient(135deg, rgba(13,43,82,0.04), rgba(31,59,99,0.08));
}

.cea-cx-cta h3 {
  margin: 0 0 10px;
  color: var(--deep);
}

.cea-cx-cta > p {
  color: var(--muted);
  margin: 0 0 24px;
}
</style>
