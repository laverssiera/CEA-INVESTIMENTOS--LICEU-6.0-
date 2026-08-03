<template>
  <div class="container">
    <BrandLogo />

    <h2 class="screen-title">Olá, {{ displayName }}</h2>
    <p class="screen-subtitle">Gerencie seus investimentos em qualquer lugar</p>

    <BalanceCard />

    <QuickActions />

    <h3>Projetos Ativos</h3>
    <ProjectCard />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import BrandLogo from '../components/BrandLogo.vue'
import BalanceCard from '../components/BalanceCard.vue'
import QuickActions from '../components/QuickActions.vue'
import ProjectCard from '../components/ProjectCard.vue'
import { auth } from '../store/auth.js'

const displayName = computed(() => {
  const n = auth.name
  return n ? n.split(' ')[0] : 'Investidor'
})
</script>

<style scoped>
h3 {
  margin-bottom: 12px;
  color: var(--cea-blue);
}
</style>

