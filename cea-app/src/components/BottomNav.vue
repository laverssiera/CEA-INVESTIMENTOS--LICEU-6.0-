<template>
  <nav class="bottom-nav">
    <router-link to="/"><span>⌂</span><small>Home</small></router-link>
    <router-link to="/account"><span>⊞</span><small>Conta</small></router-link>
    <router-link to="/portfolio"><span>◍</span><small>Carteira</small></router-link>
    <router-link to="/yields"><span>◈</span><small>Rendimentos</small></router-link>
    <router-link to="/profile"><span>◎</span><small>Perfil</small></router-link>
    <router-link to="/support"><span>☏</span><small>Suporte</small></router-link>
  </nav>
</template>

<style scoped>
.bottom-nav {
  position: fixed;
  bottom: 10px;
  left: 50%;
  transform: translateX(-50%);
  width: min(420px, calc(100% - 20px));
  display: flex;
  justify-content: space-between;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(8px);
  padding: 8px;
  border: 1px solid var(--cea-border);
  border-radius: 16px;
  box-shadow: 0 8px 22px rgba(13, 60, 143, 0.14);
}

.bottom-nav a {
  color: var(--cea-muted);
  text-decoration: none;
  font-weight: 600;
  font-size: 0.68rem;
  display: grid;
  justify-items: center;
  gap: 3px;
  padding: 5px 6px;
  border-radius: 10px;
  border: 1px solid transparent;
  min-width: 56px;
}

.bottom-nav a span {
  font-size: 0.9rem;
}

.bottom-nav a.router-link-active {
  color: var(--cea-blue);
  background: rgba(31, 102, 220, 0.11);
  border-color: rgba(31, 102, 220, 0.2);
}

.bottom-nav a:hover {
  transform: translateY(-1px);
  color: var(--cea-blue);
}

.bottom-nav a:active {
  transform: translateY(0);
}
</style>
