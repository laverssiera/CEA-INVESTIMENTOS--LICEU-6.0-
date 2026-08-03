<template>
  <div class="container">
    <h2 class="screen-title">Meus Projetos</h2>
    <p class="screen-subtitle">Acompanhamento de obras com progresso LICEU</p>

    <ProjectCard />
    <ProjectCard />
  </div>
</template>

<script setup>
import ProjectCard from '../components/ProjectCard.vue'
</script>

<style scoped>
h2 { margin-bottom: 0; }
</style>
