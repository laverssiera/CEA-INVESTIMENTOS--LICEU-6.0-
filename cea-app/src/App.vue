<template>
  <router-view />
  <BottomNav />
</template>

<script setup>
import BottomNav from './components/BottomNav.vue'
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&family=Sora:wght@600;700;800&display=swap');

:root {
  --cea-blue: #0d3c8f;
  --cea-blue-2: #1f66dc;
  --cea-gold: #d4aa3a;
  --cea-text: #1f2f45;
  --cea-muted: #617086;
  --cea-bg: #f3f6fb;
  --cea-card: #ffffff;
  --cea-border: #e3e9f2;
}

body {
  margin: 0;
  font-family: Manrope, 'Segoe UI', sans-serif;
  background:
    radial-gradient(circle at 20% -10%, rgba(31, 102, 220, 0.14), transparent 32%),
    radial-gradient(circle at 100% 0%, rgba(212, 170, 58, 0.12), transparent 26%),
    var(--cea-bg);
  color: var(--cea-text);
}

* {
  box-sizing: border-box;
}

.container {
  width: min(420px, calc(100% - 24px));
  margin: 0 auto;
  padding: 20px 0 100px;
}

h2,
h3,
h1,
p {
  margin: 0;
}

h1,
h2,
h3 {
  font-family: Sora, Manrope, sans-serif;
}

.screen-title {
  color: var(--cea-blue);
  margin-bottom: 14px;
}

.screen-subtitle {
  color: var(--cea-muted);
  margin-top: 4px;
  margin-bottom: 16px;
  font-size: 0.92rem;
}

.container > * {
  animation: riseIn 420ms ease both;
}

.container > *:nth-child(2) { animation-delay: 40ms; }
.container > *:nth-child(3) { animation-delay: 80ms; }
.container > *:nth-child(4) { animation-delay: 120ms; }
.container > *:nth-child(5) { animation-delay: 160ms; }

a,
button {
  transition: transform 180ms ease, box-shadow 180ms ease, background-color 180ms ease, color 180ms ease, border-color 180ms ease;
}

@keyframes riseIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (prefers-reduced-motion: reduce) {
  .container > * {
    animation: none;
  }

  a,
  button {
    transition: none;
  }
}
</style>
