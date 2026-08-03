<template>
  <article class="stat-card">
    <small>{{ label }}</small>
    <div class="stat-value">{{ value }}</div>
    <span class="tag" :class="toneClass">{{ trend }}</span>
  </article>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  label: { type: String, required: true },
  value: { type: [String, Number], required: true },
  trend: { type: String, default: 'Ao vivo' },
  tone: { type: String, default: 'info' },
})

const toneClass = computed(() => props.tone)
</script>
