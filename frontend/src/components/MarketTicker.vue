<template>
  <article class="panel">
    <small>Market realtime</small>
    <h3>Indicadores ao vivo</h3>

    <div class="grid-4">
      <div class="card">
        <small>CDI</small>
        <div class="stat-value">{{ indicators.cdi }}%</div>
      </div>
      <div class="card">
        <small>SELIC</small>
        <div class="stat-value">{{ indicators.selic }}%</div>
      </div>
      <div class="card">
        <small>Dólar</small>
        <div class="stat-value">R$ {{ indicators.dolar }}</div>
      </div>
      <div class="card">
        <small>Liquidez</small>
        <div class="stat-value">{{ indicators.liquidez }}</div>
      </div>
    </div>
  </article>
</template>

<script setup>
defineProps({
  indicators: {
    type: Object,
    default: () => ({ cdi: 0, selic: 0, dolar: 0, liquidez: 'N/D' }),
  },
})
</script>
