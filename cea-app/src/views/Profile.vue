<template>
  <div class="container">
    <h2 class="screen-title">Perfil</h2>
    <p class="screen-subtitle">Configurações da sua conta institucional</p>

    <!-- Badge do investidor -->
    <div class="investor-badge">
      <div class="avatar">{{ initials }}</div>
      <div>
        <strong>{{ auth.name || 'Investidor' }}</strong>
        <span class="type-tag" :class="auth.investorType === 'PF' ? 'pf' : 'pj'">
          {{ auth.investorType === 'PF' ? 'Pessoa Física' : 'Pessoa Jurídica' }}
        </span>
      </div>
    </div>

    <!-- Menu PF/PJ condicional -->
    <ul class="menu-list">
      <li v-if="auth.investorType === 'PF'">
        <span>CPF · Dados Pessoais</span>
        <small>Atualize endereço, telefone e e-mail</small>
      </li>
      <li v-else>
        <span>CNPJ · Dados Empresariais</span>
        <small>Razão social, contatos e representantes</small>
      </li>

      <li @click="goKyc" class="clickable">
        <span>Verificação KYC</span>
        <small>Enviar ou atualizar documentos de identidade</small>
      </li>

      <li class="clickable" @click="toggleNotifications">
        <span>Notificações Push</span>
        <small>{{ notifStatus }}</small>
      </li>

      <li v-if="canApprovePix" class="clickable" @click="goPixApprovals">
        <span>Aprovações PIX</span>
        <small>Fila institucional para 1ª e 2ª aprovação de saques</small>
      </li>

      <li>
        <span>Segurança</span>
        <small>Gerencie senha e autenticação MFA</small>
      </li>

      <li class="logout" @click="doLogout">
        <span>Sair</span>
        <small>Encerrar sessão neste dispositivo</small>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { auth } from '../store/auth.js'
import { requestPermission, notify } from '../utils/notifications.js'

const router = useRouter()

const initials = computed(() => {
  const n = auth.name || 'U'
  return n.slice(0, 2).toUpperCase()
})

const canApprovePix = computed(() => ['admin', 'tesouraria', 'risk_manager'].includes(auth.role))

const notifStatus = ref(
  'Notification' in window
    ? Notification.permission === 'granted'
      ? 'Ativas — toque para desativar'
      : 'Inativas — toque para ativar'
    : 'Não suportado neste navegador'
)

async function toggleNotifications() {
  if (!('Notification' in window)) return
  if (Notification.permission !== 'granted') {
    const perm = await requestPermission()
    if (perm === 'granted') {
      notifStatus.value = 'Ativas — toque para desativar'
      notify('CEA Investimentos', 'Notificações ativadas com sucesso!')
    } else {
      notifStatus.value = 'Permissão negada pelo navegador'
    }
  }
}

function goKyc() {
  router.push('/kyc')
}

function goPixApprovals() {
  router.push('/pix-approvals')
}

function doLogout() {
  auth.logout()
  router.push('/login')
}
</script>

<style scoped>
h2 {
  margin-bottom: 0;
}

.investor-badge {
  display: flex;
  align-items: center;
  gap: 14px;
  background: linear-gradient(135deg, var(--cea-blue), var(--cea-blue-2));
  color: #fff;
  border-radius: 16px;
  padding: 16px;
  margin-bottom: 16px;
  box-shadow: 0 10px 22px rgba(13, 60, 143, 0.2);
}

.avatar {
  width: 46px;
  height: 46px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 1rem;
  flex-shrink: 0;
}

.investor-badge > div {
  display: grid;
  gap: 4px;
}

.investor-badge strong {
  font-size: 0.96rem;
}

.type-tag {
  display: inline-block;
  font-size: 0.72rem;
  font-weight: 800;
  padding: 3px 8px;
  border-radius: 999px;
  letter-spacing: 0.04em;
}

.type-tag.pf {
  background: rgba(212, 170, 58, 0.3);
  color: #ffe17a;
}

.type-tag.pj {
  background: rgba(255, 255, 255, 0.2);
  color: #d6eaff;
}

.menu-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 10px;
}

li {
  background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
  border: 1px solid var(--cea-border);
  border-radius: 16px;
  padding: 14px 16px;
  display: grid;
  gap: 4px;
}

li span {
  color: var(--cea-text);
  font-weight: 700;
}

li small {
  color: var(--cea-muted);
  font-size: 0.82rem;
}

.clickable {
  cursor: pointer;
}

.clickable:hover {
  border-color: rgba(31, 102, 220, 0.3);
}

.logout {
  cursor: pointer;
  border-color: rgba(185, 28, 28, 0.2);
}

.logout span {
  color: #b91c1c;
}

.logout:hover {
  background: #fff5f5;
}
</style>

