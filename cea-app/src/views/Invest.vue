<template>
  <div class="container">
    <h2 class="screen-title">Opcoes de Investimento</h2>
    <p class="screen-subtitle">Disponivel para iOS e Android</p>

    <InvestmentCard title="Fundo Imobiliario" yield="9.5% a.a." />

    <InvestmentCard title="Infraestrutura" yield="11.2% a.a." />
  </div>
</template>

<script setup>
import InvestmentCard from '../components/InvestmentCard.vue'
</script>

<style scoped>
h2 { margin-bottom: 0; }
</style>
