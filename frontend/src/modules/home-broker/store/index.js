import { defineStore } from 'pinia'
import api from '../../../services/api'

export const useBrokerStore = defineStore('broker', {
  state: () => ({
    assets: [],
    portfolio: [],
    marketUpdate: null,
  }),

  actions: {
    async loadAssets() {
      const { data } = await api.get('/investments/assets')
      this.assets = data
    },

    async placeOrder(order) {
      await api.post('/investments/order', order)
      await this.loadPortfolio()
    },

    async loadPortfolio() {
      const { data } = await api.get('/investments/portfolio')
      this.portfolio = data
    },
  },
})
