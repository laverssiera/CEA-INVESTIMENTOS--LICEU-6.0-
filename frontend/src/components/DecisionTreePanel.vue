<template>
  <section class="panel">
    <small>Árvore de decisão ML</small>
    <h3>Fluxo inteligente para caixa de obras</h3>

    <div class="tree">
      <div class="tree-node">
        <strong>Saldo de caixa disponível?</strong>
      </div>
      <div class="tree-node">
        Curto prazo (&lt; 30 dias) → <strong>Tesouro Selic</strong>
      </div>
      <div class="tree-node">
        Médio prazo (30–90 dias) → <strong>CDB liquidez diária</strong>
      </div>
      <div class="tree-node">
        Longo prazo (&gt; 90 dias) → <strong>Fundo DI / IPCA+</strong>
      </div>
    </div>

    <ul class="list" v-if="recommendation?.allocation?.length">
      <li v-for="item in recommendation.allocation" :key="item.asset">
        {{ item.percentage }}% em {{ item.asset }}
      </li>
    </ul>
  </section>
</template>

<script setup>
defineProps({
  recommendation: {
    type: Object,
    default: () => ({}),
  },
})
</script>
