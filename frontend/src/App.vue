<template>
  <div class="shell">
    <header class="topbar cea-topbar">
      <!-- Logo + Tagline -->
      <RouterLink to="/" class="cea-logo">
        <img src="/image.png" alt="CEA Investimentos" class="cea-logo-image" />
      </RouterLink>

      <!-- Navegação principal -->
      <nav class="nav" :class="{ 'nav--open': menuOpen }">
        <RouterLink to="/" @click="menuOpen = false">Home</RouterLink>
        <RouterLink to="/institucional" @click="menuOpen = false">Institucional</RouterLink>
        <RouterLink to="/interplanetary/ecossistema" @click="menuOpen = false">Interplanetary</RouterLink>
        <RouterLink to="/investir" @click="menuOpen = false">Investir</RouterLink>
        <RouterLink to="/financiamento" @click="menuOpen = false">Financiamento</RouterLink>
        <RouterLink to="/servicos" @click="menuOpen = false">Serviços</RouterLink>
        <RouterLink to="/esg" @click="menuOpen = false">ESG</RouterLink>
        <RouterLink to="/cliente/dashboard" @click="menuOpen = false">Área cliente</RouterLink>
        <RouterLink v-if="isCollaboratorRole || isBackofficeRole" to="/colaborador" @click="menuOpen = false">Colaborador</RouterLink>
        <RouterLink v-if="isBackofficeRole" to="/admin" @click="menuOpen = false">Backoffice</RouterLink>
        <RouterLink to="/experiencia-cliente" @click="menuOpen = false">Contato</RouterLink>
        <RouterLink to="/login" class="cea-nav-login" @click="menuOpen = false">Login</RouterLink>
      </nav>

      <!-- Botão hamburguer (mobile) -->
      <button class="cea-hamburger" @click="menuOpen = !menuOpen" aria-label="Menu">
        <span></span><span></span><span></span>
      </button>
    </header>

    <main>
      <RouterView />
    </main>

    <footer class="footer cea-footer">
      <div class="cea-footer-main">
        <div>
          <p class="eyebrow" style="margin:0">CEA INVESTIMENTOS</p>
          <p style="margin:4px 0 0;font-size:0.85rem;color:var(--muted)">
            Financial Intelligence Engine para Ativos Reais (RWA) integrada à LICEU 6.0.
          </p>
        </div>
        <div class="cea-footer-contacts">
          <a href="tel:+551140000000">📞 (11) 4000-0000</a>
          <a href="https://wa.me/5511900000000" target="_blank" rel="noopener">💬 WhatsApp</a>
          <a href="mailto:atendimento@ceainvestimentos.com">✉️ atendimento@ceainvestimentos.com</a>
        </div>
        <div class="cea-footer-links-row">
          <RouterLink to="/institucional">Institucional</RouterLink>
          <RouterLink to="/interplanetary/ecossistema">Interplanetary</RouterLink>
          <RouterLink to="/servicos">Serviços</RouterLink>
          <RouterLink to="/investir">Investir</RouterLink>
          <RouterLink to="/financiamento">Financiamento</RouterLink>
          <RouterLink to="/experiencia-cliente">Atendimento</RouterLink>
          <RouterLink to="/trabalhe-conosco">Carreiras</RouterLink>
        </div>
        <div class="cea-footer-links-row cea-footer-links-row--policies">
          <p class="eyebrow" style="margin:0">Governança e Compliance</p>
          <RouterLink to="/institucional/politica-investimentos">Política de investimentos</RouterLink>
          <RouterLink to="/institucional/termos-de-uso">Termos de uso</RouterLink>
          <RouterLink to="/institucional/politica-de-risco">Política de risco</RouterLink>
          <RouterLink to="/institucional/lgpd">LGPD</RouterLink>
          <RouterLink to="/institucional/auditoria">Auditoria</RouterLink>
          <RouterLink to="/institucional/estrutura-decisoria">Estrutura decisória</RouterLink>
        </div>
      </div>
      <div class="cea-footer-bottom-bar">
        <span>© 2026 CEA INVESTIMENTOS · Av. Paulista, 1000 — São Paulo/SP</span>
        <span>Segurança bancária · Zero Trust · MFA · Compliance CVM</span>
      </div>
    </footer>

    <!-- Widget flutuante de suporte -->
    <SupportWidget />
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { RouterLink, RouterView } from 'vue-router'
import SupportWidget from './components/SupportWidget.vue'
import { useAuthStore } from './store/auth'

const menuOpen = ref(false)
const auth = useAuthStore()
const collaboratorRoles = new Set(['analista_credito', 'compliance', 'tesouraria', 'colaborador'])
const backofficeRoles = new Set(['admin', 'risk_manager', 'governance', 'diretoria'])
const isCollaboratorRole = computed(() => collaboratorRoles.has(auth.state.userRole))
const isBackofficeRole = computed(() => backofficeRoles.has(auth.state.userRole))
</script>

<style scoped>
.cea-topbar {
  border-bottom: 1px solid var(--border);
  padding: 16px 0;
  gap: 16px;
}

.cea-logo {
  text-decoration: none;
  color: inherit;
  flex-shrink: 0;
}

.cea-logo-image {
  display: block;
  height: 81px;
  width: 152px;
  max-width: none;
}

.cea-nav-login {
  background: var(--gold) !important;
  color: #2b230d !important;
}

.cea-nav-login:hover {
  background: #b8943a !important;
}

.cea-hamburger {
  display: none;
  flex-direction: column;
  gap: 5px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
}

.cea-hamburger span {
  display: block;
  width: 22px;
  height: 2px;
  background: var(--deep);
  border-radius: 2px;
  transition: transform 0.2s;
}

/* Footer */
.cea-footer {
  background: var(--white);
  border-top: 1px solid var(--border);
  padding: 32px 0 0;
  width: 100%;
  max-width: 100%;
}

.cea-footer-main {
  width: min(1180px, calc(100% - 32px));
  margin: 0 auto;
  display: flex;
  gap: 32px;
  flex-wrap: wrap;
  align-items: flex-start;
  padding-bottom: 24px;
}

.cea-footer-contacts {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.cea-footer-contacts a {
  font-size: 0.88rem;
  color: var(--muted);
  text-decoration: none;
  transition: color 0.15s;
}

.cea-footer-contacts a:hover {
  color: var(--primary);
}

.cea-footer-links-row {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.cea-footer-links-row--policies {
  min-width: 230px;
}

.cea-footer-links-row a {
  font-size: 0.88rem;
  color: var(--muted);
  text-decoration: none;
  transition: color 0.15s;
}

.cea-footer-links-row a:hover {
  color: var(--primary);
}

.cea-footer-bottom-bar {
  border-top: 1px solid var(--border);
  padding: 14px 16px;
  width: min(1180px, calc(100% - 32px));
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  font-size: 0.78rem;
  color: var(--muted);
  flex-wrap: wrap;
  gap: 6px;
}

/* Mobile */
@media (max-width: 800px) {
  .cea-hamburger {
    display: flex;
  }

  .nav {
    display: none;
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: var(--white);
    border-bottom: 1px solid var(--border);
    flex-direction: column;
    align-items: stretch;
    padding: 12px 16px;
    gap: 4px;
    box-shadow: 0 8px 24px rgba(13,43,82,0.12);
    z-index: 100;
  }

  .nav--open {
    display: flex;
  }

  .nav a {
    border-radius: 10px;
    padding: 10px 14px;
  }
}
</style>
