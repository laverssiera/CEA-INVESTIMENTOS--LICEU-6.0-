<template>
  <div class="page">
    <h1 class="section-title">Home Broker CEA</h1>

    <QuotesPanel />

    <div class="grid-3 mt-4">
      <Watchlist @select="selectAsset" />
      <AssetChart :asset="selectedAsset" />
      <OrderPanel :asset="selectedAsset" />
    </div>

    <PortfolioTable class="mt-6" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import AssetChart from './components/AssetChart.vue'
import OrderPanel from './components/OrderPanel.vue'
import PortfolioTable from './components/PortfolioTable.vue'
import QuotesPanel from './components/QuotesPanel.vue'
import Watchlist from './components/Watchlist.vue'

const selectedAsset = ref(null)

function selectAsset(asset) {
  selectedAsset.value = asset
}
</script>

<style scoped>
.mt-4 {
  margin-top: 16px;
}

.mt-6 {
  margin-top: 24px;
}
</style>
