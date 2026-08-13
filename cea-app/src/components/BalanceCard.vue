<template>
  <div class="balance">
    <small>Saldo Investido</small>
    <h1>R$ 125.750,00</h1>
    <div class="kpis">
      <span>Rentabilidade Mensal</span>
      <strong>+1,42%</strong>
    </div>
  </div>
</template>

<style scoped>
.balance {
  background: linear-gradient(135deg, var(--cea-blue), var(--cea-blue-2));
  color: white;
  padding: 20px;
  border-radius: 16px;
  display: grid;
  gap: 8px;
  box-shadow: 0 14px 26px rgba(13, 60, 143, 0.28);
}

.balance small {
  color: #d9e6ff;
  font-weight: 600;
}

.balance h1 {
  font-size: 1.8rem;
}

.kpis {
  display: flex;
  justify-content: space-between;
  margin-top: 2px;
  font-size: 0.92rem;
}

.kpis span {
  color: #dce7ff;
}

.kpis strong {
  color: #8ff3ac;
}
</style>
