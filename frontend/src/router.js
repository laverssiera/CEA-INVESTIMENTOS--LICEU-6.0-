import { createRouter, createWebHistory } from 'vue-router'
import AboutView from './views/AboutView.vue'
import AdminDashboardView from './views/AdminDashboardView.vue'
import AdminLoginView from './views/AdminLoginView.vue'
import CareersExperienceView from './views/CareersExperienceView.vue'
import ClientDashboardView from './views/ClientDashboardView.vue'
import CollaboratorCommsView from './views/collaborator/CollaboratorCommsView.vue'
import CollaboratorDashboardView from './views/collaborator/CollaboratorDashboardView.vue'
import CollaboratorDocsView from './views/collaborator/CollaboratorDocsView.vue'
import CollaboratorTasksView from './views/collaborator/CollaboratorTasksView.vue'
import CollaboratorTrainingView from './views/collaborator/CollaboratorTrainingView.vue'
import ESGView from './views/ESGView.vue'
import AppPreviewView from './views/AppPreviewView.vue'
import HomeView from './views/HomeView.vue'
import CreditCommitteeView from './views/backoffice/CreditCommitteeView.vue'
import GovernanceDashboardView from './views/backoffice/GovernanceDashboardView.vue'
import OperationsAutomationView from './views/backoffice/OperationsAutomationView.vue'
import RbacMatrixView from './views/backoffice/RbacMatrixView.vue'
import HomeCEAView from './views/cea/HomeCEAView.vue'
import ServicesCEAView from './views/cea/ServicesCEAView.vue'
import CustomerExperienceView from './views/cea/CustomerExperienceView.vue'
import InvestorHomeView from './views/InvestorHomeView.vue'
import InvestorPortfolioView from './views/InvestorPortfolioView.vue'
import InvestorProjectsView from './views/InvestorProjectsView.vue'
import LoginView from './views/LoginView.vue'
import MarketIntelligenceView from './views/MarketIntelligenceView.vue'
import DashboardView from './views/DashboardView.vue'
import FinancingView from './views/FinancingView.vue'
import InstitutionalView from './views/InstitutionalView.vue'
import InstitutionalPolicyView from './views/InstitutionalPolicyView.vue'
import InterplanetaryEcosystemView from './views/InterplanetaryEcosystemView.vue'

const INVESTOR_ROLES = ['investor_pf', 'investor_pj']
const ADMIN_ROLES = ['admin', 'risk_manager', 'governance', 'diretoria']
const COLLABORATOR_ROLES = ['analista_credito', 'compliance', 'tesouraria', 'colaborador']
const INTERNAL_ROLES = [...new Set([...ADMIN_ROLES, ...COLLABORATOR_ROLES])]

const resolveAuthenticatedHome = (role) => {
  if (COLLABORATOR_ROLES.includes(role)) return '/colaborador'
  if (ADMIN_ROLES.includes(role)) return '/admin'
  if (INVESTOR_ROLES.includes(role)) return '/investidor/dashboard'
  if (role === 'cliente_financiamento') return '/cliente/dashboard'
  return '/'
}

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'home', component: HomeCEAView },
    { path: '/visao-geral', name: 'overview', component: HomeView },
    { path: '/sobre', name: 'about', component: AboutView },
    { path: '/institucional', name: 'institutional', component: InstitutionalView },
    { path: '/interplanetary/ecossistema', name: 'interplanetary-ecosystem', component: InterplanetaryEcosystemView },
    { path: '/institucional/:slug', name: 'institutional-policy', component: InstitutionalPolicyView },
    { path: '/servicos', name: 'services', component: ServicesCEAView },
    { path: '/experiencia-cliente', name: 'customer-experience', component: CustomerExperienceView },
    {
      path: '/investir',
      name: 'invest',
      component: MarketIntelligenceView,
      alias: ['/market-intelligence', '/cea/market-intelligence'],
    },
    {
      path: '/financiamento',
      name: 'financing',
      component: FinancingView,
    },
    {
      path: '/trabalhe-conosco',
      name: 'careers',
      component: CareersExperienceView,
    },
    {
      path: '/esg',
      name: 'esg',
      component: ESGView,
    },
    {
      path: '/app-preview',
      name: 'app-preview',
      component: AppPreviewView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/investidor',
      name: 'investor-home',
      component: InvestorHomeView,
      meta: { requiresAuth: true, roles: INVESTOR_ROLES },
    },
    {
      path: '/investidor/dashboard',
      name: 'investor-dashboard',
      component: DashboardView,
      alias: ['/cea/dashboard'],
      meta: { requiresAuth: true, roles: INVESTOR_ROLES },
    },
    {
      path: '/investidor/carteira',
      name: 'investor-portfolio',
      component: InvestorPortfolioView,
      meta: { requiresAuth: true, roles: INVESTOR_ROLES },
    },
    {
      path: '/investidor/projetos',
      name: 'investor-projects',
      component: InvestorProjectsView,
      meta: { requiresAuth: true, roles: INVESTOR_ROLES },
    },
    {
      path: '/investidor/home-broker',
      name: 'home-broker',
      component: () => import('./modules/home-broker/HomeBroker.vue'),
      meta: { requiresAuth: true, roles: INVESTOR_ROLES },
    },
    {
      path: '/cliente/dashboard',
      name: 'client-dashboard',
      component: ClientDashboardView,
      meta: { requiresAuth: true },
    },
    {
      path: '/colaborador',
      name: 'collaborator-dashboard',
      component: CollaboratorDashboardView,
      meta: { requiresAuth: true, roles: INTERNAL_ROLES },
    },
    {
      path: '/colaborador/dashboard',
      name: 'collaborator-dashboard-alias',
      component: CollaboratorDashboardView,
      meta: { requiresAuth: true, roles: INTERNAL_ROLES },
    },
    {
      path: '/colaborador/tarefas',
      name: 'collaborator-tasks',
      component: CollaboratorTasksView,
      meta: { requiresAuth: true, roles: INTERNAL_ROLES },
    },
    {
      path: '/colaborador/documentos',
      name: 'collaborator-docs',
      component: CollaboratorDocsView,
      meta: { requiresAuth: true, roles: INTERNAL_ROLES },
    },
    {
      path: '/colaborador/comunicados',
      name: 'collaborator-comms',
      component: CollaboratorCommsView,
      meta: { requiresAuth: true, roles: INTERNAL_ROLES },
    },
    {
      path: '/colaborador/treinamentos',
      name: 'collaborator-training',
      component: CollaboratorTrainingView,
      meta: { requiresAuth: true, roles: INTERNAL_ROLES },
    },
    {
      path: '/admin/login',
      name: 'admin-login',
      component: AdminLoginView,
      meta: { guestOnly: true, redirectIfAuth: '/admin' },
    },
    {
      path: '/admin',
      name: 'admin-dashboard',
      component: AdminDashboardView,
      meta: { requiresAuth: true, roles: ADMIN_ROLES },
    },
    {
      path: '/admin/governanca',
      name: 'governance-dashboard',
      component: GovernanceDashboardView,
      meta: { requiresAuth: true, roles: ADMIN_ROLES },
    },
    {
      path: '/admin/comite-credito',
      name: 'credit-committee',
      component: CreditCommitteeView,
      meta: { requiresAuth: true, roles: ADMIN_ROLES },
    },
    {
      path: '/admin/rbac',
      name: 'rbac-matrix',
      component: RbacMatrixView,
      meta: { requiresAuth: true, roles: ADMIN_ROLES },
    },
    {
      path: '/admin/rotinas',
      name: 'operations-automation',
      component: OperationsAutomationView,
      meta: { requiresAuth: true, roles: ADMIN_ROLES },
    },
  ],
})

router.beforeEach((to) => {
  const token = localStorage.getItem('cea.accessToken')
  const role = localStorage.getItem('cea.userRole') || 'guest'
  const isAuthenticated = Boolean(token)

  // Redireciona usuário autenticado saindo das telas de login
  if (to.meta.guestOnly && isAuthenticated) {
    return resolveAuthenticatedHome(role)
  }

  if (!to.meta.requiresAuth) return true

  if (!isAuthenticated) {
    const requiresInstitutionalLogin = to.path.startsWith('/admin') || to.path.startsWith('/colaborador')
    const loginRoute = requiresInstitutionalLogin ? '/admin/login' : '/login'
    return { path: loginRoute, query: { redirect: to.fullPath } }
  }

  // Verifica se o perfil tem acesso à rota
  const allowedRoles = to.meta.roles
  if (allowedRoles && !allowedRoles.includes(role)) {
    return '/'
  }

  return true
})

export default router
