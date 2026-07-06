import api from './index'
import type { PredictionRequest, SimulationRequest } from '@/types'

export const predict = (payload: PredictionRequest) => api.post('/predict', payload)
export const simulate = (payload: SimulationRequest) => api.post('/simulate', payload)
export const listPTDs = (params: { distrito?: string; concelho?: string; limit?: number }) =>
  api.get('/ptds', { params })
export const getPTD = (ptdId: string) => api.get(`/ptds/${encodeURIComponent(ptdId)}`)
export const getHealth = () => api.get('/health')
export const getReady = () => api.get('/ready')
export const getFeatureImportance = (profile: string, version?: string, task?: string) =>
  api.get('/feature-importance', { params: { profile, version, task } })
export const reloadModels = (profile: string, version?: string) =>
  api.post('/reload', null, { params: { profile, version } })