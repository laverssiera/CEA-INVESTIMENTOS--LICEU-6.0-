<template>
  <section class="app-download">
    <div class="app-download__content">
      <p class="eyebrow">Disponivel para iOS e Android</p>
      <h2>Baixe o app CEA Investimentos</h2>
      <p>
        Acompanhe investimentos, financiamento e projetos em tempo real.
        Gerencie seus investimentos em qualquer lugar com experiencia completa no celular.
      </p>

      <div class="app-download__badges">
        <span>5.0 de avaliacao</span>
        <span>Seguranca institucional</span>
        <span>+10.000 investidores</span>
      </div>

      <div class="app-download__buttons">
        <a href="#" class="app-btn app-btn--apple" aria-label="Baixar na App Store">
          <strong>App Store</strong>
        </a>
        <a href="#" class="app-btn app-btn--play" aria-label="Baixar no Google Play">
          <strong>Google Play</strong>
        </a>
        <RouterLink to="/app-preview" class="app-btn app-btn--preview" aria-label="Ver preview do app">
          <strong>Ver preview</strong>
        </RouterLink>
      </div>

      <div class="app-download__qr" aria-label="QR code para download do app">
        <div class="app-download__qr-grid"></div>
        <small>Escaneie e baixe o app</small>
      </div>
    </div>

    <div class="app-download__phone">
      <img src="/mockup-app.svg" alt="Mockup do app CEA Investimentos" />
    </div>
  </section>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>

<style scoped>
.app-download {
  border-radius: 24px;
  border: 1px solid var(--border);
  background: linear-gradient(145deg, #ffffff 0%, #f1f5fb 55%, #eaf1fa 100%);
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
  gap: 28px;
  padding: 30px;
  box-shadow: 0 18px 38px rgba(13, 43, 82, 0.12);
}

.app-download__content h2 {
  margin: 10px 0 10px;
  color: var(--deep);
  font-size: clamp(1.6rem, 2.8vw, 2.2rem);
}

.app-download__content p {
  margin: 0;
  color: var(--muted);
  max-width: 56ch;
}

.app-download__badges {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-top: 16px;
}

.app-download__badges span {
  font-size: 0.78rem;
  font-weight: 700;
  padding: 7px 10px;
  border-radius: 999px;
  border: 1px solid rgba(31, 59, 99, 0.15);
  background: #ffffff;
  color: var(--primary);
}

.app-download__buttons {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-top: 18px;
}

.app-btn {
  text-decoration: none;
  border-radius: 12px;
  padding: 12px 16px;
  min-width: 160px;
  text-align: center;
  border: 1px solid transparent;
}

.app-btn strong {
  font-size: 0.95rem;
}

.app-btn--apple {
  background: #0f1724;
  color: #ffffff;
}

.app-btn--play {
  background: #ffffff;
  color: #1452a7;
  border-color: rgba(20, 82, 167, 0.25);
}

.app-btn--preview {
  background: rgba(200, 169, 106, 0.18);
  color: #7f601e;
  border-color: rgba(200, 169, 106, 0.35);
}

.app-download__qr {
  margin-top: 14px;
  display: grid;
  gap: 8px;
  width: fit-content;
}

.app-download__qr-grid {
  width: 76px;
  height: 76px;
  border-radius: 6px;
  border: 1px solid var(--border);
  background-image:
    linear-gradient(90deg, #0d2b52 20%, transparent 20%),
    linear-gradient(#0d2b52 20%, transparent 20%);
  background-size: 12px 12px;
  background-position: 0 0;
}

.app-download__qr small {
  color: var(--muted);
  font-size: 0.75rem;
}

.app-download__phone {
  display: flex;
  align-items: center;
  justify-content: center;
}

.app-download__phone img {
  width: min(290px, 100%);
  height: auto;
  filter: drop-shadow(0 14px 24px rgba(13, 43, 82, 0.25));
}

@media (max-width: 920px) {
  .app-download {
    grid-template-columns: 1fr;
  }

  .app-download__phone {
    order: -1;
  }
}
</style>
