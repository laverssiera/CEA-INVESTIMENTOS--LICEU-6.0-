<template>
  <div class="page">
    <section class="hero cea-services-hero">
      <div>
        <p class="eyebrow">Portfólio de serviços</p>
        <h2>Serviços financeiros CEA INVESTIMENTOS</h2>
        <p>
          Da captação de recursos à estruturação de projetos — oferecemos soluções completas
          para investidores, tomadores de crédito e parceiros estratégicos.
        </p>
      </div>
    </section>

    <section>
      <h3 class="section-title">Para investidores</h3>
      <div class="grid-3">
        <div
          v-for="s in investorServices"
          :key="s.slug"
          class="card cea-service"
          :class="{ 'cea-service--featured': s.featured }"
        >
          <span class="cea-service-icon">{{ s.icon }}</span>
          <div class="cea-service-badge">{{ s.badge }}</div>
          <h4>{{ s.title }}</h4>
          <p>{{ s.description }}</p>
          <ul class="cea-service-features">
            <li v-for="f in s.features" :key="f">{{ f }}</li>
          </ul>
          <RouterLink :to="s.cta.path" class="primary-btn cea-service-btn">{{ s.cta.label }}</RouterLink>
        </div>
      </div>
    </section>

    <section>
      <h3 class="section-title">Para construtores e tomadores de crédito</h3>
      <div class="grid-3">
        <div
          v-for="s in creditServices"
          :key="s.slug"
          class="card cea-service"
        >
          <span class="cea-service-icon">{{ s.icon }}</span>
          <div class="cea-service-badge cea-service-badge--alt">{{ s.badge }}</div>
          <h4>{{ s.title }}</h4>
          <p>{{ s.description }}</p>
          <ul class="cea-service-features">
            <li v-for="f in s.features" :key="f">{{ f }}</li>
          </ul>
          <RouterLink :to="s.cta.path" class="primary-btn cea-service-btn">{{ s.cta.label }}</RouterLink>
        </div>
      </div>
    </section>

    <section>
      <h3 class="section-title">Parcerias e estruturação</h3>
      <div class="grid-3">
        <div
          v-for="s in partnerServices"
          :key="s.slug"
          class="card cea-service"
        >
          <span class="cea-service-icon">{{ s.icon }}</span>
          <div class="cea-service-badge cea-service-badge--partner">{{ s.badge }}</div>
          <h4>{{ s.title }}</h4>
          <p>{{ s.description }}</p>
          <ul class="cea-service-features">
            <li v-for="f in s.features" :key="f">{{ f }}</li>
          </ul>
          <a :href="whatsappLink" target="_blank" rel="noopener" class="secondary-btn secondary-btn-dark cea-service-btn">
            {{ s.cta.label }}
          </a>
        </div>
      </div>
    </section>

    <!-- CTA Final -->
    <div class="card cea-services-cta">
      <h3>Não encontrou o que precisa?</h3>
      <p>Fale diretamente com nossos especialistas e descubra a solução ideal para o seu perfil.</p>
      <div class="actions">
        <a :href="whatsappLink" target="_blank" rel="noopener" class="primary-btn">💬 Falar com especialista</a>
        <RouterLink to="/experiencia-cliente" class="secondary-btn secondary-btn-dark">Central de atendimento</RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'

const whatsappLink = `https://wa.me/5511900000000?text=Ol%C3%A1%2C%20gostaria%20de%20saber%20mais%20sobre%20os%20servi%C3%A7os%20CEA%20INVESTIMENTOS.`

const investorServices = [
  {
    slug: 'pf',
    icon: '👤',
    badge: 'Pessoa Física',
    title: 'Investimento PF',
    description: 'Invista em projetos de construção civil lastreados em ativos reais com rentabilidade superior ao CDI.',
    features: ['A partir de R$ 5.000', 'Perfil conservador a arrojado', 'Rendimento mensal', 'Liquidez programada'],
    cta: { label: 'Investir agora', path: '/investir' },
    featured: true,
  },
  {
    slug: 'pj',
    icon: '🏢',
    badge: 'Pessoa Jurídica',
    title: 'Investimento PJ',
    description: 'Alocar o caixa da empresa em RWA com eficiência fiscal e retorno previsível.',
    features: ['Estruturação corporativa', 'Relatórios contábeis', 'Gestão de risco', 'Reinvestimento automático'],
    cta: { label: 'Acessar', path: '/investir' },
    featured: false,
  },
  {
    slug: 'coinvestimento',
    icon: '🤝',
    badge: 'Coinvestimento',
    title: 'Coinvestimento coletivo',
    description: 'Participe de projetos de grande porte junto a outros investidores em estruturas de FII ou CRI.',
    features: ['Ticket menor por investidor', 'Projetos selecionados', 'Diversificação automática', 'Relatórios consolidados'],
    cta: { label: 'Saiba mais', path: '/investir' },
    featured: false,
  },
]

const creditServices = [
  {
    slug: 'credito-construcao',
    icon: '🏗️',
    badge: 'Financiamento',
    title: 'Crédito para construção',
    description: 'Financiamento ágil para projetos de construção civil com análise de crédito ML e decisão em 72h.',
    features: ['Análise automatizada', 'Aprovação em 72h', 'Integração LICEU 6.0', 'Execução monitorada'],
    cta: { label: 'Solicitar', path: '/financiamento' },
  },
  {
    slug: 'estruturacao',
    icon: '📊',
    badge: 'Estruturação',
    title: 'Estruturação financeira',
    description: 'Modelagem completa do projeto: fluxo de caixa, precificação, retorno e apresentação a investidores.',
    features: ['VGV e landbank', 'Due diligence', 'Apresentação regulatória', 'Integração com CVM'],
    cta: { label: 'Falar com equipe', path: '/experiencia-cliente' },
  },
  {
    slug: 'liceu',
    icon: '⚙️',
    badge: 'LICEU 6.0',
    title: 'Gestão integrada LICEU',
    description: 'Seu projeto financiado pela CEA passa a ser gerenciado pela LICEU 6.0 com dashboards em tempo real.',
    features: ['Avanço de obra em tempo real', 'Relatórios de produção', 'Controle de custos', 'Alertas automáticos'],
    cta: { label: 'Ver integração', path: '/investir' },
  },
]

const partnerServices = [
  {
    slug: 'incorporadoras',
    icon: '🏙️',
    badge: 'Parceria',
    title: 'Incorporadoras parceiras',
    description: 'Acesso ao capital de investidores CEA para seus projetos imobiliários com estruturação completa.',
    features: ['Capital qualificado', 'Processo simplificado', 'Compliance garantido'],
    cta: { label: 'Ser parceiro' },
  },
  {
    slug: 'fundos',
    icon: '📈',
    badge: 'Fundos',
    title: 'Fundos de investimento',
    description: 'Distribuição de cotas e integração com gestores de FII e FIP para ampliação de portfólio.',
    features: ['Distribuição qualificada', 'Relatórios regulatórios', 'Integração de sistemas'],
    cta: { label: 'Conversar' },
  },
  {
    slug: 'estrategico',
    icon: '🌐',
    badge: 'Estratégico',
    title: 'Parcerias estratégicas',
    description: 'Integrações com bancos, fintechs e plataformas do mercado imobiliário e de capitais.',
    features: ['API aberta', 'White label disponível', 'Acordos de cooperação'],
    cta: { label: 'Entrar em contato' },
  },
]
</script>

<style scoped>
.cea-services-hero {
  display: block;
  padding: 40px;
}

.cea-service {
  display: flex;
  flex-direction: column;
  gap: 10px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.cea-service:hover {
  transform: translateY(-3px);
  box-shadow: 0 20px 40px rgba(13,43,82,0.12);
}

.cea-service--featured {
  border: 2px solid var(--gold);
}

.cea-service-icon {
  font-size: 2.2rem;
}

.cea-service-badge {
  display: inline-flex;
  padding: 4px 10px;
  border-radius: 999px;
  background: rgba(31,59,99,0.1);
  color: var(--primary);
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  width: fit-content;
}

.cea-service-badge--alt {
  background: rgba(200,169,106,0.15);
  color: #7a5b1a;
}

.cea-service-badge--partner {
  background: rgba(13,43,82,0.08);
  color: var(--deep);
}

.cea-service h4 {
  margin: 0;
  color: var(--deep);
  font-size: 1.08rem;
}

.cea-service p {
  margin: 0;
  color: var(--muted);
  font-size: 0.92rem;
  flex: 1;
}

.cea-service-features {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.cea-service-features li {
  font-size: 0.88rem;
  color: var(--muted);
  padding-left: 16px;
  position: relative;
}

.cea-service-features li::before {
  content: '✓';
  position: absolute;
  left: 0;
  color: var(--primary);
  font-weight: 700;
}

.cea-service-btn {
  margin-top: auto;
  align-self: flex-start;
  font-size: 0.9rem;
  padding: 9px 16px;
}

.cea-services-cta {
  text-align: center;
  padding: 40px 32px;
  background: linear-gradient(135deg, rgba(13,43,82,0.04), rgba(31,59,99,0.08));
}

.cea-services-cta h3 {
  margin: 0 0 10px;
  color: var(--deep);
}

.cea-services-cta > p {
  color: var(--muted);
  margin: 0 0 24px;
}
</style>
