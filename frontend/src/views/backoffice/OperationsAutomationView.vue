<template>
  <div class="page">
    <section class="hero">
      <div>
        <p class="eyebrow">Rotinas automáticas</p>
        <h2>Agenda operacional e automações institucionais</h2>
        <p>
          Monitoramento dos jobs operacionais, rotina diária das áreas e calendário ESG
          para execução institucional com rastreabilidade.
        </p>
      </div>
    </section>

    <section class="grid-2">
      <article class="panel">
        <small>Jobs automáticos</small>
        <h3>Agenda técnica</h3>
        <div class="automation-grid">
          <div class="automation-card" v-for="job in jobs" :key="job.name">
            <strong>{{ job.name }}</strong>
            <span>{{ job.schedule }}</span>
            <small>{{ job.description }}</small>
          </div>
        </div>
      </article>

      <article class="panel">
        <small>Rotinas por área</small>
        <h3>Execução operacional</h3>
        <div class="automation-grid">
          <div class="automation-card" v-for="routine in routines" :key="routine.area">
            <strong>{{ routine.area }}</strong>
            <span>{{ routine.window }}</span>
            <small>{{ routine.focus }}</small>
          </div>
        </div>
      </article>
    </section>

    <section class="panel">
      <small>Orquestração automática</small>
      <h3>Controle de execução</h3>
      <p>Disparo manual de jobs prioritários e monitoramento de resposta.</p>
      <div class="job-actions">
        <button
          v-for="job in priorityOne"
          :key="job"
          class="run-btn"
          type="button"
          @click="runJob(job)"
          :disabled="runningJob === job"
        >
          {{ runningJob === job ? `Executando ${job}...` : `Executar ${job}` }}
        </button>
      </div>
      <p class="job-feedback" v-if="lastRunMessage">{{ lastRunMessage }}</p>
    </section>

    <section class="grid-2">
      <article class="panel">
        <small>Jobs executados</small>
        <h3>Histórico recente</h3>
        <div class="automation-grid">
          <div class="automation-card" v-for="item in orchestrationLogs" :key="`${item.id}-${item.executed_at}`">
            <strong>{{ item.job }}</strong>
            <span>{{ formatDate(item.executed_at) }}</span>
            <small>{{ summarize(item.payload) }}</small>
          </div>
        </div>
      </article>

      <article class="panel">
        <small>Event bus</small>
        <h3>Eventos recentes</h3>
        <div class="automation-grid">
          <div class="automation-card" v-for="item in orchestrationEvents" :key="`${item.id}-${item.created_at}`">
            <strong>{{ item.event }}</strong>
            <span>{{ formatDate(item.created_at) }}</span>
            <small>{{ summarize(item.payload) }}</small>
          </div>
        </div>
      </article>
    </section>

    <section class="grid-2">
      <article class="panel">
        <small>Notificações</small>
        <h3>Canais disparados</h3>
        <div class="automation-grid">
          <div class="automation-card" v-for="item in notificationLogs" :key="`${item.id}-${item.sent_at}`">
            <strong>{{ item.channel }} - {{ item.trigger }}</strong>
            <span>{{ formatDate(item.sent_at) }}</span>
            <small>{{ item.message }}</small>
          </div>
        </div>
      </article>

      <article class="panel">
        <small>Documentos</small>
        <h3>Geração automática</h3>
        <div class="automation-grid">
          <div class="automation-card" v-for="item in documentLogs" :key="`${item.id}-${item.generated_at}`">
            <strong>{{ item.type }}</strong>
            <span>{{ formatDate(item.generated_at) }}</span>
            <small>{{ summarize(item.context) }}</small>
          </div>
        </div>
      </article>
    </section>

    <section>
      <h3 class="section-title">Calendário ESG e compliance</h3>
      <div class="grid-3">
        <article class="card" v-for="item in calendar" :key="item.period">
          <small>{{ item.period }}</small>
          <h3>{{ item.title }}</h3>
          <p>{{ item.description }}</p>
        </article>
      </div>
    </section>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import {
  fetchAutomationSchedules,
  fetchDocumentLogs,
  fetchNotificationLogs,
  fetchOrchestrationEvents,
  fetchOrchestrationJobs,
  fetchOrchestrationLogs,
  runOrchestrationJob,
} from '../../services/liceuApi'

const jobs = ref([])
const routines = ref([])
const calendar = ref([])
const priorityOne = ref([])
const orchestrationLogs = ref([])
const orchestrationEvents = ref([])
const notificationLogs = ref([])
const documentLogs = ref([])
const runningJob = ref('')
const lastRunMessage = ref('')

const formatDate = (value) => {
  if (!value) return '-'
  try {
    return new Date(value).toLocaleString('pt-BR')
  } catch {
    return value
  }
}

const summarize = (value) => {
  if (!value) return 'sem payload'
  const raw = typeof value === 'string' ? value : JSON.stringify(value)
  return raw.length > 120 ? `${raw.slice(0, 120)}...` : raw
}

const refreshAutomationData = async () => {
  const [orchestrationJobs, logs, events, notifications, documents] = await Promise.all([
    fetchOrchestrationJobs(),
    fetchOrchestrationLogs(),
    fetchOrchestrationEvents(),
    fetchNotificationLogs(),
    fetchDocumentLogs(),
  ])

  priorityOne.value = orchestrationJobs?.priorities?.priority_1 || []
  orchestrationLogs.value = (logs.items || []).slice(0, 8)
  orchestrationEvents.value = (events.items || []).slice(0, 8)
  notificationLogs.value = (notifications.items || []).slice(0, 8)
  documentLogs.value = (documents.items || []).slice(0, 8)
}

const runJob = async (jobName) => {
  runningJob.value = jobName
  lastRunMessage.value = ''
  try {
    const result = await runOrchestrationJob(jobName)
    lastRunMessage.value = `Job ${result.job} executado com status ${result.status}.`
    await refreshAutomationData()
  } catch (error) {
    const detail = error?.response?.data?.detail || error?.message || 'erro desconhecido'
    lastRunMessage.value = `Falha ao executar ${jobName}: ${detail}`
  } finally {
    runningJob.value = ''
  }
}

onMounted(async () => {
  const data = await fetchAutomationSchedules()
  jobs.value = data.jobs
  routines.value = data.routines
  calendar.value = data.calendar
  await refreshAutomationData()
})
</script>

<style scoped>
.job-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 10px;
}

.run-btn {
  border: 0;
  border-radius: 10px;
  padding: 10px 14px;
  background: var(--deep);
  color: white;
  cursor: pointer;
  font-weight: 600;
}

.run-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.job-feedback {
  margin-top: 10px;
  color: var(--muted);
}

.automation-grid {
  display: grid;
  gap: 10px;
  margin-top: 12px;
}

.automation-card {
  display: grid;
  gap: 4px;
  padding: 12px 14px;
  border-radius: 12px;
  background: rgba(31, 59, 99, 0.05);
}

.automation-card strong {
  color: var(--deep);
}

.automation-card span,
.automation-card small {
  color: var(--muted);
}
</style>
