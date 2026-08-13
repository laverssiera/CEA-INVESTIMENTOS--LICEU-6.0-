<template>
  <section class="panel">
    <small>Plano de Cybersegurança</small>
    <h3>Postura enterprise e bancária</h3>

    <div class="grid-2">
      <article v-for="(items, key) in securityData" :key="key" class="security-card">
        <strong>{{ labels[key] ?? key }}</strong>
        <ul class="list">
          <li v-for="item in items" :key="item">{{ item }}</li>
        </ul>
      </article>
    </div>
  </section>
</template>

<script setup>
defineProps({
  securityData: {
    type: Object,
    default: () => ({}),
  },
})

const labels = {
  network: 'Segurança de rede',
  identity: 'Autenticação e identidade',
  data: 'Proteção de dados',
  governance: 'Governança e auditoria',
}
</script>
