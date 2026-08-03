<template>
  <div class="page cea-home">

    <!-- Hero Institucional -->
    <section class="cea-hero">
      <div class="cea-hero__content">
        <p class="eyebrow">Financial Intelligence Engine · RWA · LICEU 6.0</p>
        <h2 class="cea-hero__title">
          Investimentos reais.<br>
          Retornos concretos.
        </h2>
        <p class="cea-hero__subtitle">
          A CEA INVESTIMENTOS conecta capital privado a projetos de construção civil, ativos reais
          e oportunidades de financiamento estruturado dentro do ecossistema LICEU 6.0.
        </p>
        <div class="actions cea-hero__actions">
          <RouterLink class="primary-btn" to="/investir">Quero investir</RouterLink>
          <RouterLink class="secondary-btn cea-hero__outline-btn" to="/financiamento">Solicitar financiamento</RouterLink>
        </div>
      </div>
      <div class="cea-hero__cards">
        <div class="card cea-kpi-card">
          <small>Projetos financiados</small>
          <div class="stat-value">R$ 280M+</div>
          <span class="tag info">Em obras ativas</span>
        </div>
        <div class="card cea-kpi-card">
          <small>Rentabilidade média</small>
          <div class="stat-value">CDI + 4,2%</div>
          <span class="tag warning">a.a. líquido</span>
        </div>
        <div class="card cea-kpi-card">
          <small>Investidores ativos</small>
          <div class="stat-value">1.240</div>
          <span class="tag info">PF e PJ</span>
        </div>
        <div class="card cea-kpi-card">
          <small>Rating interno</small>
          <div class="stat-value">AA+</div>
          <span class="tag info">Risco controlado</span>
        </div>
      </div>
    </section>

    <!-- Download do App -->
    <AppDownloadSection />

    <MissionVisionValues />

    <!-- Botões principais CTA -->
    <section class="cea-cta-section">
      <h3 class="section-title">O que você quer fazer hoje?</h3>
      <div class="cea-cta-grid">
        <RouterLink class="cea-cta-card" to="/investir">
          <span class="cea-cta-icon">📈</span>
          <strong>Investir</strong>
          <p>Aplique em projetos de construção com rentabilidade superior ao CDI.</p>
        </RouterLink>
        <RouterLink class="cea-cta-card" to="/financiamento">
          <span class="cea-cta-icon">🏗️</span>
          <strong>Solicitar financiamento</strong>
          <p>Financie sua obra com crédito estruturado e aprovação ágil.</p>
        </RouterLink>
        <RouterLink class="cea-cta-card" to="/servicos">
          <span class="cea-cta-icon">🏦</span>
          <strong>Acessar serviços</strong>
          <p>Explore todos os produtos e serviços financeiros da CEA.</p>
        </RouterLink>
        <RouterLink class="cea-cta-card" to="/investidor">
          <span class="cea-cta-icon">👤</span>
          <strong>Área do cliente</strong>
          <p>Acesse sua carteira, extrato e posição nos projetos.</p>
        </RouterLink>
        <RouterLink class="cea-cta-card" to="/trabalhe-conosco">
          <span class="cea-cta-icon">💼</span>
          <strong>Trabalhe conosco</strong>
          <p>Faça parte do time que está revolucionando o mercado financeiro.</p>
        </RouterLink>
        <a class="cea-cta-card" :href="`mailto:${contact.email}`">
          <span class="cea-cta-icon">✉️</span>
          <strong>Falar com especialista</strong>
          <p>Atendimento institucional por e-mail com retorno em horário comercial.</p>
        </a>
      </div>
    </section>

    <!-- Serviços CEA -->
    <section class="cea-services-section">
      <h3 class="section-title">Serviços financeiros CEA</h3>
      <div class="grid-3 cea-services-grid">
        <div class="card cea-service-card">
          <div class="cea-service-badge">Investidor PF</div>
          <h4>Investimento pessoa física</h4>
          <p>Alocação em projetos RWA com perfil conservador, moderado ou arrojado. Rendimento mensal e liquidez programada.</p>
          <RouterLink class="primary-btn cea-service-btn" to="/investir">Começar</RouterLink>
        </div>
        <div class="card cea-service-card">
          <div class="cea-service-badge">Investidor PJ</div>
          <h4>Investimento pessoa jurídica</h4>
          <p>Estruturação de fundos corporativos, reinvestimento de caixa e exposição a ativos reais com eficiência fiscal.</p>
          <RouterLink class="primary-btn cea-service-btn" to="/investir">Começar</RouterLink>
        </div>
        <div class="card cea-service-card">
          <div class="cea-service-badge">Financiamento</div>
          <h4>Crédito para construção</h4>
          <p>Pipeline de crédito integrado ao motor de análise ML da CEA. Aprovação em até 72h para projetos qualificados.</p>
          <RouterLink class="primary-btn cea-service-btn" to="/financiamento">Solicitar</RouterLink>
        </div>
        <div class="card cea-service-card">
          <div class="cea-service-badge">Estruturação</div>
          <h4>Coinvestimento</h4>
          <p>Estruturas de coinvestimento entre múltiplos investidores em projetos de grande porte da LICEU 6.0.</p>
          <RouterLink class="secondary-btn secondary-btn-dark cea-service-btn" to="/servicos">Saiba mais</RouterLink>
        </div>
        <div class="card cea-service-card">
          <div class="cea-service-badge">Projetos</div>
          <h4>Estruturação de projetos</h4>
          <p>Análise financeira, precificação de ativos e modelagem de retorno para projetos de construção e incorporação.</p>
          <RouterLink class="secondary-btn secondary-btn-dark cea-service-btn" to="/servicos">Saiba mais</RouterLink>
        </div>
        <div class="card cea-service-card">
          <div class="cea-service-badge">Parcerias</div>
          <h4>Parcerias estratégicas</h4>
          <p>Integração com construtoras, incorporadoras e fundos de investimento imobiliário dentro do ecossistema LICEU.</p>
          <a class="secondary-btn secondary-btn-dark cea-service-btn" :href="`mailto:${contact.email}`">Contato</a>
        </div>
      </div>
    </section>

    <!-- Jornada do Cliente -->
    <section class="cea-journey-section">
      <h3 class="section-title">Como funciona a jornada</h3>
      <div class="grid-2 cea-journey-grid">
        <!-- Jornada Investidor -->
        <div class="card cea-journey-card">
          <h4 class="cea-journey-title">
            <span class="cea-journey-icon">📈</span>
            Jornada do investidor
          </h4>
          <div class="cea-journey-steps">
            <div v-for="(step, i) in investorJourney" :key="i" class="cea-step">
              <div class="cea-step__num">{{ i + 1 }}</div>
              <div>
                <strong>{{ step.title }}</strong>
                <p>{{ step.desc }}</p>
              </div>
            </div>
          </div>
          <RouterLink class="primary-btn" to="/investir">Iniciar jornada</RouterLink>
        </div>
        <!-- Jornada Financiamento -->
        <div class="card cea-journey-card">
          <h4 class="cea-journey-title">
            <span class="cea-journey-icon">🏗️</span>
            Jornada de financiamento
          </h4>
          <div class="cea-journey-steps">
            <div v-for="(step, i) in financingJourney" :key="i" class="cea-step">
              <div class="cea-step__num">{{ i + 1 }}</div>
              <div>
                <strong>{{ step.title }}</strong>
                <p>{{ step.desc }}</p>
              </div>
            </div>
          </div>
          <RouterLink class="primary-btn" to="/financiamento">Solicitar agora</RouterLink>
        </div>
      </div>
    </section>

    <!-- Contato Rápido -->
    <section class="cea-contact-section">
      <div class="card cea-contact-card">
        <h3>Fale com a CEA</h3>
        <p>Nossa equipe de especialistas está disponível para atender você de segunda a sexta, das 09:00 às 18:00.</p>
        <div class="cea-contact-channels">
          <a :href="`mailto:${contact.email}`" class="cea-channel">
            <span>✉️</span>
            <div>
              <strong>E-mail</strong>
              <span>{{ contact.email }}</span>
            </div>
          </a>
        </div>
        <p class="cea-hours">Horário de atendimento: {{ contact.hours }}</p>
      </div>
    </section>

    <!-- Footer Institucional (dentro da página) -->
    <section class="cea-footer-section">
      <div class="cea-footer-grid">
        <div>
          <p class="eyebrow">CEA INVESTIMENTOS</p>
          <p>Financial Intelligence Engine para Ativos Reais integrada ao ecossistema LICEU 6.0.</p>
        </div>
        <div>
          <strong>Links rápidos</strong>
          <ul class="cea-footer-links">
            <li><RouterLink to="/investir">Investir</RouterLink></li>
            <li><RouterLink to="/financiamento">Financiamento</RouterLink></li>
            <li><RouterLink to="/servicos">Serviços</RouterLink></li>
            <li><RouterLink to="/experiencia-cliente">Atendimento</RouterLink></li>
            <li><RouterLink to="/trabalhe-conosco">Carreiras</RouterLink></li>
          </ul>
        </div>
        <div>
          <strong>Acesso rápido</strong>
          <ul class="cea-footer-links">
            <li><RouterLink to="/login">Portal do investidor</RouterLink></li>
            <li><RouterLink to="/cliente/dashboard">Área do cliente</RouterLink></li>
            <li><RouterLink to="/admin/login">Backoffice</RouterLink></li>
            <li><RouterLink to="/investidor/home-broker">Home Broker</RouterLink></li>
          </ul>
        </div>
        <div>
          <strong>Contato</strong>
          <ul class="cea-footer-links">
            <li><a :href="`mailto:${contact.email}`">{{ contact.email }}</a></li>
          </ul>
          <p class="cea-hours">{{ contact.hours }}</p>
        </div>
      </div>
      <div class="cea-footer-bottom">
        <span>© 2026 CEA INVESTIMENTOS · Todos os direitos reservados</span>
        <span>Segurança bancária · Zero Trust · MFA · Compliance CVM</span>
      </div>
    </section>

  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import AppDownloadSection from '../../components/AppDownloadSection.vue'
import MissionVisionValues from '../../components/MissionVisionValues.vue'

const contact = {
  email: 'atendimento@ceainvestimentos.com',
  hours: '09:00 às 18:00 · Segunda a sexta',
}

const investorJourney = [
  { title: 'Acesse a plataforma', desc: 'Cadastre-se gratuitamente em minutos.' },
  { title: 'Complete o KYC', desc: 'Envie documentos e passe pela análise de suitability.' },
  { title: 'Explore projetos', desc: 'Conheça os ativos disponíveis e o perfil de risco.' },
  { title: 'Invista', desc: 'Aplique diretamente no Home Broker com total segurança.' },
  { title: 'Acompanhe', desc: 'Monitore rendimentos e progresso das obras em tempo real.' },
]

const financingJourney = [
  { title: 'Solicite financiamento', desc: 'Preencha o formulário com dados do projeto.' },
  { title: 'Análise de crédito', desc: 'Motor ML avalia score e viabilidade em minutos.' },
  { title: 'Aprovação', desc: 'Pipeline interno com analista de crédito dedicado.' },
  { title: 'Execução LICEU', desc: 'Projeto integrado ao sistema de gestão LICEU 6.0.' },
  { title: 'Dashboard do cliente', desc: 'Acompanhe parcelas, obra e status em tempo real.' },
]
</script>

<style scoped>
.cea-home {
  display: flex;
  flex-direction: column;
  gap: 48px;
}

/* Hero */
.cea-hero {
  background: linear-gradient(135deg, var(--deep) 0%, #1a3f70 60%, #244c8a 100%);
  color: var(--white);
  border-radius: 24px;
  padding: 48px 40px;
  display: grid;
  grid-template-columns: 1.4fr 1fr;
  gap: 32px;
  box-shadow: 0 24px 48px rgba(13, 43, 82, 0.22);
}

.cea-hero__title {
  margin: 8px 0 16px;
  font-size: clamp(2rem, 4vw, 3.2rem);
  line-height: 1.15;
}

.cea-hero__subtitle {
  margin: 0 0 24px;
  opacity: 0.88;
  max-width: 55ch;
  font-size: 1.08rem;
}

.cea-hero__outline-btn {
  background: rgba(255,255,255,0.12);
  color: var(--white);
  border: 1.5px solid rgba(255,255,255,0.35);
}

.cea-hero__cards {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  align-content: start;
}

.cea-kpi-card {
  background: rgba(255,255,255,0.1);
  border: 1px solid rgba(255,255,255,0.18);
  padding: 16px;
}

.cea-kpi-card small {
  color: rgba(255,255,255,0.65);
}

.cea-kpi-card .stat-value {
  color: var(--white);
  font-size: 1.35rem;
}

/* CTA Grid */
.cea-cta-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-top: 20px;
}

.cea-cta-card {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 8px;
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 22px 20px;
  box-shadow: 0 8px 24px rgba(13, 43, 82, 0.06);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s;
  text-decoration: none;
  color: inherit;
}

.cea-cta-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 16px 36px rgba(13, 43, 82, 0.12);
  border-color: var(--primary);
}

.cea-cta-icon {
  font-size: 2rem;
}

.cea-cta-card strong {
  font-size: 1.05rem;
  color: var(--deep);
}

.cea-cta-card p {
  margin: 0;
  color: var(--muted);
  font-size: 0.9rem;
}

/* Services */
.cea-service-card {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.cea-service-badge {
  display: inline-flex;
  padding: 4px 10px;
  border-radius: 999px;
  background: rgba(31,59,99,0.1);
  color: var(--primary);
  font-size: 0.78rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  width: fit-content;
}

.cea-service-card h4 {
  margin: 0;
  color: var(--deep);
}

.cea-service-card p {
  margin: 0;
  color: var(--muted);
  font-size: 0.92rem;
  flex: 1;
}

.cea-service-btn {
  margin-top: auto;
  align-self: flex-start;
  font-size: 0.9rem;
  padding: 8px 14px;
}

/* Journey */
.cea-journey-card {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.cea-journey-title {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0;
  font-size: 1.1rem;
  color: var(--deep);
}

.cea-journey-icon {
  font-size: 1.4rem;
}

.cea-journey-steps {
  display: flex;
  flex-direction: column;
  gap: 12px;
  flex: 1;
}

.cea-step {
  display: flex;
  gap: 12px;
  align-items: flex-start;
}

.cea-step__num {
  min-width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--deep);
  color: var(--white);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  font-weight: 700;
  flex-shrink: 0;
}

.cea-step strong {
  display: block;
  color: var(--deep);
  font-size: 0.95rem;
}

.cea-step p {
  margin: 2px 0 0;
  color: var(--muted);
  font-size: 0.88rem;
}

/* Contact section */
.cea-contact-card {
  text-align: center;
  padding: 40px 32px;
}

.cea-contact-card h3 {
  margin: 0 0 10px;
  color: var(--deep);
  font-size: 1.5rem;
}

.cea-contact-card > p {
  color: var(--muted);
  margin: 0 0 28px;
}

.cea-contact-channels {
  display: flex;
  gap: 24px;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 16px;
}

.cea-channel {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 20px;
  border-radius: 14px;
  background: rgba(31,59,99,0.06);
  border: 1px solid var(--border);
  text-decoration: none;
  color: inherit;
  transition: background 0.2s, border-color 0.2s;
  min-width: 180px;
}

.cea-channel:hover {
  background: rgba(31,59,99,0.12);
  border-color: var(--primary);
}

.cea-channel > span {
  font-size: 1.6rem;
}

.cea-channel strong {
  display: block;
  color: var(--deep);
  font-size: 0.9rem;
}

.cea-channel span:last-child {
  display: block;
  font-size: 0.88rem;
  color: var(--muted);
}

.cea-hours {
  color: var(--muted);
  font-size: 0.88rem;
}

/* Footer section */
.cea-footer-section {
  border-top: 1px solid var(--border);
  padding-top: 40px;
}

.cea-footer-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 32px;
  margin-bottom: 32px;
}

.cea-footer-grid p {
  color: var(--muted);
  font-size: 0.92rem;
  margin: 8px 0 0;
}

.cea-footer-links {
  list-style: none;
  padding: 0;
  margin: 10px 0 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.cea-footer-links a {
  color: var(--muted);
  font-size: 0.9rem;
  transition: color 0.2s;
}

.cea-footer-links a:hover {
  color: var(--primary);
}

.cea-footer-bottom {
  border-top: 1px solid var(--border);
  padding-top: 20px;
  display: flex;
  justify-content: space-between;
  font-size: 0.82rem;
  color: var(--muted);
  flex-wrap: wrap;
  gap: 8px;
  padding-bottom: 16px;
}

@media (max-width: 900px) {
  .cea-hero {
    grid-template-columns: 1fr;
  }

  .cea-hero__cards {
    grid-template-columns: repeat(2, 1fr);
  }

  .cea-cta-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .cea-footer-grid {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 600px) {
  .cea-hero {
    padding: 28px 20px;
  }

  .cea-cta-grid {
    grid-template-columns: 1fr;
  }

  .cea-footer-grid {
    grid-template-columns: 1fr;
  }
}
</style>
