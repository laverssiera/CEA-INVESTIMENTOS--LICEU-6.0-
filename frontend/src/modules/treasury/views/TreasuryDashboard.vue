<template>
  <div class="min-h-screen bg-zinc-950 text-white p-6">
    <header class="mb-8 flex justify-between items-center">
      <div>
        <h1 class="text-3xl font-bold tracking-tight text-white">Treasury Control Center</h1>
        <p class="text-zinc-400">Monitoramento Enterprise da Holding LICEU 6.0</p>
      </div>
      <div class="flex items-center gap-4">
        <div class="px-4 py-2 bg-emerald-500/10 border border-emerald-500/20 rounded-full text-emerald-400 text-sm font-medium">
          John AI Online
        </div>
      </div>
    </header>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <!-- Liquidez Total -->
      <div class="bg-zinc-900 border border-zinc-800 rounded-2xl p-6 hover:border-zinc-700 transition-all">
        <h2 class="text-zinc-400 text-sm font-medium mb-2">Liquidez do Ecossistema</h2>
        <p class="text-4xl font-bold text-white">R$ 150.2M</p>
        <div class="mt-4 flex items-center gap-2 text-emerald-400 text-sm">
          <span class="p-1 bg-emerald-400/10 rounded">▲ 4.2%</span>
          <span>vs último ciclo</span>
        </div>
      </div>

      <!-- ROI -->
      <div class="bg-zinc-900 border border-zinc-800 rounded-2xl p-6">
        <h2 class="text-zinc-400 text-sm font-medium mb-2">Yield Médio (RWA)</h2>
        <p class="text-4xl font-bold text-white">18.7%</p>
        <div class="mt-4 text-zinc-500 text-sm italic">
          Otimizado por IA
        </div>
      </div>

      <!-- Health Index -->
      <div class="bg-zinc-900 border border-zinc-800 rounded-2xl p-6">
        <h2 class="text-zinc-400 text-sm font-medium mb-2">Health Index (Mesh)</h2>
        <p class="text-4xl font-bold text-white">0.94</p>
        <div class="mt-4 w-full bg-zinc-800 h-2 rounded-full overflow-hidden">
          <div class="bg-blue-500 h-full w-[94%]"></div>
        </div>
      </div>

      <!-- John Finance Recommendation -->
      <div class="bg-blue-600 rounded-2xl p-6 flex flex-col justify-between">
        <div>
          <h2 class="text-blue-100 text-sm font-medium mb-2">John AI Advisory</h2>
          <p class="text-lg font-semibold leading-tight text-white">
            "Expandir liquidez para fornecedores Tier-1 via Liquidity Mesh."
          </p>
        </div>
        <button class="mt-4 bg-white text-blue-600 font-bold py-2 rounded-xl text-sm hover:bg-blue-50 transition-colors">
          Executar Ordem
        </button>
      </div>
    </div>

    <!-- Seção de Ativos e Fluxo -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div class="lg:col-span-2 bg-zinc-900 border border-zinc-800 rounded-2xl p-6">
        <h3 class="text-xl font-bold mb-6">Fluxo de Caixa dos Monólitos</h3>
        <!-- Placeholder para Gráfico ECharts -->
        <div class="h-64 flex items-end justify-between gap-4">
          <div v-for="h in [40, 70, 45, 90, 65, 80, 55]" :key="h" 
               class="bg-blue-500/50 hover:bg-blue-400 transition-all rounded-t-lg w-full"
               :style="{ height: h + '%' }"></div>
        </div>
        <div class="mt-4 flex justify-between text-zinc-500 text-xs font-mono">
          <span>OPERA</span>
          <span>ARCHI.</span>
          <span>ACAD.</span>
          <span>CEA</span>
          <span>CEF.</span>
          <span>GAME</span>
          <span>JURID.</span>
        </div>
      </div>

      <!-- Alertas de Risco -->
      <div class="bg-zinc-900 border border-zinc-800 rounded-2xl p-6">
        <div class="flex justify-between items-center mb-6">
          <h3 class="text-xl font-bold">Risk Engine Signals</h3>
          <span class="text-xs bg-zinc-800 px-2 py-1 rounded">Real-time</span>
        </div>
        <div class="space-y-4">
          <div v-for="n in 3" :key="n" class="p-4 bg-zinc-950 border-l-4 border-amber-500 rounded-r-lg">
            <p class="text-sm font-medium">Alerta de Liquidez Local</p>
            <p class="text-xs text-zinc-500 mt-1">Obra #422 reportou atraso de 15% em fornecedores.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
// Mock data para a interface
const liquidity = ref("12.500.000")
</script>
