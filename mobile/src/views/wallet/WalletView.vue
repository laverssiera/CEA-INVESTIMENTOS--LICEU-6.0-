<template>
  <div class="p-5 bg-black min-h-screen text-white font-sans">
    <!-- Header Mobile -->
    <div class="flex justify-between items-center mb-8 pt-4">
      <div>
        <h1 class="text-2xl font-bold">CEA Banking</h1>
        <p class="text-zinc-500 text-sm">Status: Institutional Premium</p>
      </div>
      <div class="w-12 h-12 bg-zinc-800 rounded-full flex items-center justify-center">
        👤
      </div>
    </div>

    <!-- Black Card -->
    <div class="bg-gradient-to-br from-zinc-800 to-zinc-950 border border-zinc-700 rounded-[2.5rem] p-8 mb-8 shadow-2xl">
      <p class="text-zinc-400 text-sm font-medium">Saldo em Carteira</p>
      <div class="flex items-baseline gap-2 mt-2">
        <span class="text-2xl font-medium text-zinc-500">R$</span>
        <h2 class="text-5xl font-bold tracking-tighter">125.000,00</h2>
      </div>
      <div class="mt-8 flex justify-between items-center">
        <div class="bg-white/5 px-4 py-2 rounded-2xl border border-white/10 backdrop-blur-sm">
          <p class="text-[10px] uppercase tracking-widest text-zinc-500 font-bold">RWA Yield</p>
          <p class="text-emerald-400 font-bold">+R$ 1.240,42</p>
        </div>
        <div class="w-8 h-8 rounded-full border border-zinc-700 flex items-center justify-center text-xs">
          QR
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="grid grid-cols-4 gap-4 mb-10">
      <div v-for="action in actions" :key="action.label" class="flex flex-col items-center gap-2">
        <div class="w-14 h-14 bg-zinc-900 border border-zinc-800 rounded-2xl flex items-center justify-center text-xl">
          {{ action.icon }}
        </div>
        <span class="text-[10px] font-bold uppercase tracking-wider text-zinc-500">{{ action.label }}</span>
      </div>
    </div>

    <!-- Assets / RWA Row -->
    <div class="mb-6 flex justify-between items-center">
      <h3 class="text-lg font-bold">Ativos Reais (RWA)</h3>
      <span class="text-blue-500 text-xs font-bold uppercase">Ver Todos</span>
    </div>

    <div class="space-y-4">
      <div v-for="asset in assets" :key="asset.name" class="bg-zinc-900/50 p-4 rounded-3xl border border-zinc-800 flex items-center gap-4">
        <div class="w-12 h-12 bg-blue-500/20 rounded-2xl flex items-center justify-center font-bold text-blue-400 text-xs">
          RWA
        </div>
        <div class="flex-1">
          <h4 class="font-bold text-sm">{{ asset.name }}</h4>
          <p class="text-xs text-zinc-500">{{ asset.type }}</p>
        </div>
        <div class="text-right">
          <p class="font-bold text-sm">{{ asset.val }}</p>
          <p class="text-xs text-emerald-500">{{ asset.roi }}</p>
        </div>
      </div>
    </div>

    <!-- Tab Bar -->
    <div class="fixed bottom-0 left-0 right-0 p-6 bg-black/80 backdrop-blur-xl border-t border-zinc-900 flex justify-around items-center">
      <span class="text-white text-xl">🏠</span>
      <span class="text-zinc-600 text-xl">💹</span>
      <span class="text-zinc-600 text-xl">💳</span>
      <span class="text-zinc-600 text-xl">⚙️</span>
    </div>
  </div>
</template>

<script setup>
const actions = [
  { label: 'Pix', icon: '⚡' },
  { label: 'Pagar', icon: '📄' },
  { label: 'RWA', icon: '💎' },
  { label: 'John', icon: '🤖' }
]

const assets = [
  { name: 'Condomínio Archimedes I', type: 'Fundo Imobiliário', val: 'R$ 45.000', roi: '+18%' },
  { name: 'Geração Solar CEA-04', type: 'Energia Limpa', val: 'R$ 12.000', roi: '+22.5%' }
]
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
body { font-family: 'Inter', sans-serif; }
</style>
