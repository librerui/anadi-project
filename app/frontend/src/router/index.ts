import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '@/views/Dashboard.vue'
import Prediction from '@/views/Prediction.vue'
import Simulation from '@/views/Simulation.vue'
import Health from '@/views/Health.vue'
import RegionalAnalysis from '@/views/RegionalAnalysis.vue'

const routes = [
  { path: '/', name: 'Dashboard', component: Dashboard },
  { path: '/predict', name: 'Prediction', component: Prediction },
  { path: '/simulate', name: 'Simulation', component: Simulation },
  { path: '/health', name: 'Health', component: Health },
  { path: '/regional', name: 'Regional', component: RegionalAnalysis },
]

const router = createRouter({ history: createWebHistory(), routes })
export default router