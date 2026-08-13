/**
 * Utilitário de notificações push para PWA / browser
 */

export async function requestPermission() {
  if (!('Notification' in window)) return 'unsupported'
  if (Notification.permission === 'granted') return 'granted'
  const result = await Notification.requestPermission()
  return result
}

export function notify(title, body, icon = '/cea-icon.png') {
  if (!('Notification' in window)) return
  if (Notification.permission !== 'granted') return

  return new Notification(title, {
    body,
    icon,
    badge: icon,
    tag: `cea-${Date.now()}`,
  })
}

// Exemplos prontos para uso em outras views
export const notifyYield = (amount) =>
  notify('CEA Investimentos', `Novo rendimento creditado: R$ ${amount}`)

export const notifyTicket = (protocol) =>
  notify('Suporte CEA', `Seu ticket ${protocol} foi registrado com sucesso.`)

export const notifyKyc = () =>
  notify('Verificação CEA', 'Sua documentação foi aprovada. Bem-vindo!')
