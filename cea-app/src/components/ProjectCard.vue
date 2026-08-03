<template>
  <div class="project">
    <h3>Green Residence</h3>
    <p>80% concluido</p>
    <small>Valor Investido R$ 40.000,00</small>
    <button>Ver detalhes</button>
  </div>
</template>

<style scoped>
.project {
  background: var(--cea-card);
  padding: 16px;
  border-radius: 12px;
  margin-bottom: 10px;
  border: 1px solid var(--cea-border);
  display: grid;
  gap: 8px;
  box-shadow: 0 8px 16px rgba(13, 60, 143, 0.08);
  transition: transform 180ms ease, box-shadow 180ms ease;
}

.project:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 22px rgba(13, 60, 143, 0.12);
}

.project p {
  color: #2f7b45;
  font-weight: 700;
}

.project small {
  color: var(--cea-muted);
}

.project button {
  border: none;
  border-radius: 10px;
  background: var(--cea-blue);
  color: white;
  padding: 10px;
  font-weight: 700;
  cursor: pointer;
}

.project button:hover {
  transform: translateY(-1px);
}

.project button:active {
  transform: translateY(0);
}
</style>
