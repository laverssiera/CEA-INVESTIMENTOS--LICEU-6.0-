import { createRouter, createWebHistory } from 'vue-router'
import { auth } from '../store/auth.js'

import Home from '../views/Home.vue'
import Invest from '../views/Invest.vue'
import Projects from '../views/Projects.vue'
import Portfolio from '../views/Portfolio.vue'
import Profile from '../views/Profile.vue'
import Support from '../views/Support.vue'
import Login from '../views/Login.vue'
import Kyc from '../views/Kyc.vue'
import DepositPix from '../views/DepositPix.vue'
import WithdrawPix from '../views/WithdrawPix.vue'
import DigitalAccount from '../views/DigitalAccount.vue'
import ProjectSplit from '../views/ProjectSplit.vue'
import YieldPayments from '../views/YieldPayments.vue'
import ContractSignatures from '../views/ContractSignatures.vue'
import InvestmentTokenization from '../views/InvestmentTokenization.vue'
import InternalWallet from '../views/InternalWallet.vue'
import MarketplaceProjects from '../views/MarketplaceProjects.vue'
import PixApprovals from '../views/PixApprovals.vue'
import PixComplianceDashboard from '../views/PixComplianceDashboard.vue'

const routes = [
  // Públicas
  { path: '/login', component: Login, meta: { guestOnly: true } },

  // Autenticadas
  { path: '/', component: Home, meta: { requiresAuth: true } },
  { path: '/invest', component: Invest, meta: { requiresAuth: true } },
  { path: '/projects', component: Projects, meta: { requiresAuth: true } },
  { path: '/portfolio', component: Portfolio, meta: { requiresAuth: true } },
  { path: '/profile', component: Profile, meta: { requiresAuth: true } },
  { path: '/support', component: Support, meta: { requiresAuth: true } },
  { path: '/kyc', component: Kyc, meta: { requiresAuth: true } },
  { path: '/deposit', component: DepositPix, meta: { requiresAuth: true } },
  { path: '/withdraw', component: WithdrawPix, meta: { requiresAuth: true } },
  { path: '/account', component: DigitalAccount, meta: { requiresAuth: true } },
  { path: '/split', component: ProjectSplit, meta: { requiresAuth: true } },
  { path: '/yields', component: YieldPayments, meta: { requiresAuth: true } },
  { path: '/contracts', component: ContractSignatures, meta: { requiresAuth: true } },
  { path: '/tokenization', component: InvestmentTokenization, meta: { requiresAuth: true } },
  { path: '/wallet', component: InternalWallet, meta: { requiresAuth: true } },
  { path: '/marketplace', component: MarketplaceProjects, meta: { requiresAuth: true } },
  { path: '/pix-approvals', component: PixApprovals, meta: { requiresAuth: true } },
  { path: '/pix-compliance', component: PixComplianceDashboard, meta: { requiresAuth: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, _from, next) => {
  if (to.meta.guestOnly && auth.isAuthenticated) {
    return next('/')
  }
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return next('/login')
  }
  next()
})

export default router

