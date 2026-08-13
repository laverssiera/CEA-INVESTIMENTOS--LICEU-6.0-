<template>
  <section class="institutional" :class="{ 'institutional--dark': darkMode }">
    <div class="container">
      <div class="institutional__header">
        <p class="eyebrow">Institucional</p>
        <h2 class="title">Missao, visao e fundamentos de governanca da CEA Investimentos</h2>
        <p class="institutional__lead">
          Estruturamos capital, risco e governanca para conectar investidores a ativos reais com disciplina
          operacional, transparencia e padrao institucional de mercado.
        </p>
      </div>

      <div class="grid">
        <article class="card card--featured">
          <div class="card__icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none">
              <path d="M12 3 4 7v5c0 5 3.4 9.4 8 10 4.6-.6 8-5 8-10V7l-8-4Z" />
              <path d="m9.5 12 1.8 1.8 3.2-3.6" />
            </svg>
          </div>
          <h3>Missao</h3>
          <p>
            Conectar capital a oportunidades reais, promovendo investimentos inteligentes que impulsionam o
            crescimento sustentavel da construcao civil e geram valor para investidores, clientes e sociedade.
          </p>
        </article>

        <article class="card card--featured">
          <div class="card__icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none">
              <path d="M2.5 12s3.5-6 9.5-6 9.5 6 9.5 6-3.5 6-9.5 6-9.5-6-9.5-6Z" />
              <circle cx="12" cy="12" r="3" />
            </svg>
          </div>
          <h3>Visao</h3>
          <p>
            Ser referencia em investimentos estruturados para o setor da construcao, integrando tecnologia,
            transparencia e inteligencia financeira para democratizar o acesso ao crescimento economico.
          </p>
        </article>
      </div>

      <article class="values">
        <div class="section-heading">
          <div class="card__icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none">
              <path d="M12 2v20" />
              <path d="M5 7h8a3 3 0 1 1 0 6H9a3 3 0 1 0 0 6h10" />
            </svg>
          </div>
          <div>
            <h3>Valores</h3>
            <p>Princípios que orientam a operação institucional, a alocação de capital e a relação com o mercado.</p>
          </div>
        </div>

        <ul>
          <li>Transparencia</li>
          <li>Seguranca</li>
          <li>Inovacao</li>
          <li>Crescimento Compartilhado</li>
          <li>Sustentabilidade</li>
          <li>Meritocracia Financeira</li>
          <li>Etica e Compliance</li>
        </ul>
      </article>

      <div class="governance-grid">
        <article class="card card--support">
          <div class="section-heading">
            <div class="card__icon" aria-hidden="true">
              <svg viewBox="0 0 24 24" fill="none">
                <path d="M4 6h16" />
                <path d="M7 3v6" />
                <path d="M17 3v6" />
                <rect x="4" y="6" width="16" height="14" rx="2" />
                <path d="M8 11h8" />
                <path d="M8 15h5" />
              </svg>
            </div>
            <div>
              <h3>Governanca</h3>
              <p>Segregacao de funcoes, decisao colegiada e visibilidade executiva em toda a cadeia operacional.</p>
            </div>
          </div>
          <ul class="detail-list">
            <li>Backoffice com RBAC por perfis institucionais.</li>
            <li>Trilha de auditoria para eventos sensiveis.</li>
            <li>Fluxos com aprovacao dupla e monitoramento continuo.</li>
          </ul>
        </article>

        <article class="card card--support">
          <div class="section-heading">
            <div class="card__icon" aria-hidden="true">
              <svg viewBox="0 0 24 24" fill="none">
                <path d="M12 3 5 6v6c0 4.2 2.7 8 7 9 4.3-1 7-4.8 7-9V6l-7-3Z" />
                <path d="m9.5 12 1.5 1.5 3.5-4" />
              </svg>
            </div>
            <div>
              <h3>Compliance</h3>
              <p>Controles aderentes a boas praticas de KYC, AML, suitability e seguranca operacional.</p>
            </div>
          </div>
          <ul class="detail-list">
            <li>Autenticacao com MFA e renovacao segura de sessao.</li>
            <li>Validação de perfis e acessos por regra de negocio.</li>
            <li>Controles de risco, auditoria e conformidade operacional.</li>
          </ul>
        </article>

        <article class="card card--support">
          <div class="section-heading">
            <div class="card__icon" aria-hidden="true">
              <svg viewBox="0 0 24 24" fill="none">
                <path d="M6 4h9l3 3v13H6z" />
                <path d="M15 4v4h4" />
                <path d="M9 12h6" />
                <path d="M9 16h6" />
              </svg>
            </div>
            <div>
              <h3>Regulatorio</h3>
              <p>Arquitetura preparada para relatorios, evidencias de controle e evolucao institucional regulada.</p>
            </div>
          </div>
          <ul class="detail-list">
            <li>Documentacao institucional organizada por dominio.</li>
            <li>Base para relatorios executivos e regulatórios.</li>
            <li>Padrao operacional aderente a instituicoes financeiras digitais.</li>
          </ul>
        </article>
      </div>
    </div>
  </section>
</template>

<script setup>
defineProps({
  darkMode: {
    type: Boolean,
    default: false,
  },
})
</script>

<style scoped>
.institutional {
  padding: 80px 20px;
  background:
    radial-gradient(circle at top left, rgba(200, 169, 106, 0.12), transparent 26%),
    linear-gradient(180deg, #f8fafc 0%, #eef3f8 100%);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.institutional__header {
  margin-bottom: 40px;
}

.title {
  margin: 10px 0 14px;
  font-size: clamp(2rem, 3vw, 2.7rem);
  font-weight: 700;
  line-height: 1.15;
  color: #0a2540;
  max-width: 14ch;
}

.institutional__lead {
  margin: 0;
  max-width: 72ch;
  color: #5f6f83;
  font-size: 1.02rem;
}

.grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.card,
.values {
  position: relative;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.94);
  padding: 28px;
  border-radius: 18px;
  border: 1px solid rgba(13, 43, 82, 0.08);
  box-shadow: 0 18px 40px rgba(10, 37, 64, 0.08);
  backdrop-filter: blur(8px);
  animation: fade-up 0.7s ease both;
}

.card::before,
.values::before {
  content: "";
  position: absolute;
  inset: 0 auto auto 0;
  width: 100%;
  height: 3px;
  background: linear-gradient(90deg, #c8a96a 0%, #0d2b52 100%);
  opacity: 0.85;
}

.card:hover,
.values:hover {
  transform: translateY(-4px);
  box-shadow: 0 24px 44px rgba(10, 37, 64, 0.12);
  transition: transform 0.28s ease, box-shadow 0.28s ease;
}

.card--featured:nth-child(2) {
  animation-delay: 0.08s;
}

.card--support:nth-child(1) {
  animation-delay: 0.12s;
}

.card--support:nth-child(2) {
  animation-delay: 0.2s;
}

.card--support:nth-child(3) {
  animation-delay: 0.28s;
}

.card__icon {
  width: 52px;
  height: 52px;
  border-radius: 14px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 18px;
  background: linear-gradient(135deg, rgba(13, 43, 82, 0.08), rgba(200, 169, 106, 0.18));
  color: #0d2b52;
}

.card__icon svg {
  width: 24px;
  height: 24px;
  stroke: currentColor;
  stroke-width: 1.8;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.card h3,
.values h3 {
  margin: 0 0 12px;
  color: #0a2540;
  font-size: 1.35rem;
}

.card p,
.values p,
.detail-list li {
  color: #5f6f83;
  line-height: 1.7;
}

.section-heading {
  display: flex;
  gap: 16px;
  align-items: flex-start;
  margin-bottom: 18px;
}

.section-heading .card__icon {
  margin-bottom: 0;
  flex-shrink: 0;
}

.values ul {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
  list-style: none;
  padding: 0;
  margin: 0;
}

.values li {
  padding: 14px 16px;
  border-radius: 12px;
  text-align: center;
  font-weight: 600;
  color: #17365d;
  background: linear-gradient(180deg, #eef2f7 0%, #e6edf5 100%);
  border: 1px solid rgba(13, 43, 82, 0.06);
}

.governance-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 24px;
}

.detail-list {
  margin: 0;
  padding-left: 18px;
}

.detail-list li + li {
  margin-top: 10px;
}

.institutional--dark {
  background:
    radial-gradient(circle at top left, rgba(200, 169, 106, 0.2), transparent 28%),
    linear-gradient(180deg, #081c37 0%, #0c2446 100%);
}

.institutional--dark .title,
.institutional--dark .card h3,
.institutional--dark .values h3,
.institutional--dark .values li,
.institutional--dark .section-heading p {
  color: #e8eef7;
}

.institutional--dark .institutional__lead,
.institutional--dark .card p,
.institutional--dark .values p,
.institutional--dark .detail-list li {
  color: #b4c5d8;
}

.institutional--dark .card,
.institutional--dark .values {
  background: rgba(11, 30, 56, 0.92);
  border-color: rgba(113, 144, 187, 0.28);
  box-shadow: 0 16px 32px rgba(0, 0, 0, 0.35);
}

.institutional--dark .card__icon {
  background: linear-gradient(135deg, rgba(30, 65, 112, 0.5), rgba(200, 169, 106, 0.3));
  color: #f3f7fc;
}

.institutional--dark .values li {
  background: linear-gradient(180deg, #16345d 0%, #122b4e 100%);
  border-color: rgba(113, 144, 187, 0.3);
}

@keyframes fade-up {
  from {
    opacity: 0;
    transform: translateY(18px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 980px) {
  .grid,
  .governance-grid,
  .values ul {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .institutional {
    padding: 64px 16px;
  }

  .card,
  .values {
    padding: 22px;
    border-radius: 16px;
  }

  .section-heading {
    flex-direction: column;
  }
}
</style>
