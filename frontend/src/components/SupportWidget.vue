<template>
  <div>
    <!-- Botão flutuante -->
    <button
      class="support-widget__btn"
      :class="{ 'support-widget__btn--open': open }"
      @click="open = !open"
      aria-label="Suporte CEA"
    >
      <span v-if="!open">💬</span>
      <span v-else>✕</span>
    </button>

    <!-- Painel de contato -->
    <transition name="support-slide">
      <div v-if="open" class="support-widget__panel">
        <div class="support-widget__header">
          <strong>Fale com a CEA</strong>
          <span class="support-widget__online">● Online agora</span>
        </div>
        <p class="support-widget__subtitle">
          Nossa equipe responde em menos de 2 minutos pelo WhatsApp.
        </p>
        <div class="support-widget__actions">
          <a
            :href="whatsappLink"
            target="_blank"
            rel="noopener"
            class="support-widget__wa-btn"
            @click="open = false"
          >
            💬 Abrir WhatsApp
          </a>
          <a
            :href="`tel:${phone}`"
            class="support-widget__phone-btn"
          >
            📞 {{ phoneDisplay }}
          </a>
        </div>
        <p class="support-widget__hours">Seg–Sex · 09:00 às 18:00</p>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const open = ref(false)
const phone = '+551140000000'
const phoneDisplay = '(11) 4000-0000'
const whatsapp = '+5511900000000'
const whatsappLink = `https://wa.me/${whatsapp}?text=Ol%C3%A1%2C%20preciso%20de%20ajuda%20com%20a%20plataforma%20CEA%20INVESTIMENTOS.`
</script>

<style scoped>
.support-widget__btn {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 1000;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: #25d366;
  border: none;
  cursor: pointer;
  font-size: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 24px rgba(37,211,102,0.4);
  transition: background 0.2s, transform 0.2s;
  color: var(--white);
}

.support-widget__btn:hover {
  background: #1ebe5a;
  transform: scale(1.07);
}

.support-widget__btn--open {
  background: var(--deep);
  box-shadow: 0 8px 24px rgba(13,43,82,0.3);
}

.support-widget__panel {
  position: fixed;
  bottom: 92px;
  right: 24px;
  z-index: 999;
  width: 300px;
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 20px;
  box-shadow: 0 20px 48px rgba(13,43,82,0.18);
}

.support-widget__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}

.support-widget__header strong {
  color: var(--deep);
  font-size: 1rem;
}

.support-widget__online {
  font-size: 0.72rem;
  color: #25d366;
  font-weight: 600;
}

.support-widget__subtitle {
  margin: 0 0 16px;
  font-size: 0.88rem;
  color: var(--muted);
  line-height: 1.5;
}

.support-widget__actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.support-widget__wa-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px;
  border-radius: 10px;
  background: #25d366;
  color: var(--white);
  font-weight: 700;
  text-decoration: none;
  font-size: 0.95rem;
  transition: background 0.2s;
}

.support-widget__wa-btn:hover {
  background: #1ebe5a;
}

.support-widget__phone-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px;
  border-radius: 10px;
  background: rgba(31,59,99,0.08);
  color: var(--primary);
  font-weight: 600;
  text-decoration: none;
  font-size: 0.9rem;
  transition: background 0.2s;
}

.support-widget__phone-btn:hover {
  background: rgba(31,59,99,0.15);
}

.support-widget__hours {
  margin: 10px 0 0;
  font-size: 0.78rem;
  color: var(--muted);
  text-align: center;
}

/* Animação */
.support-slide-enter-active,
.support-slide-leave-active {
  transition: opacity 0.18s ease, transform 0.18s ease;
}

.support-slide-enter-from,
.support-slide-leave-to {
  opacity: 0;
  transform: translateY(12px) scale(0.97);
}

@media (max-width: 480px) {
  .support-widget__panel {
    right: 12px;
    left: 12px;
    width: auto;
    bottom: 84px;
  }
}
</style>
