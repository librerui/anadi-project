export interface PredictionRequest {
  profile: string
  version?: string
  task: 'regression' | 'classification'
  model_name?: string
  features: Record<string, number>
}

export interface PredictionResponse {
  profile: string
  version: string
  model_name: string
  task: string
  prediction: number | string
  raw_scores?: Record<string, number>
}

export interface SimulationRequest {
  profile: string
  version?: string
  task: 'classification'
  model_name?: string
  features: Record<string, number>
  iterations: number
  noise_scale: number
  overload_class: string
  seed?: number
}

export interface SimulationResponse {
  profile: string
  version: string
  model_name: string
  task: string
  iterations: number
  overload_class: string
  overload_probability: number
  distribution: Record<string, number>
}

export interface HealthResponse {
  status: string
  detail: string
}

export interface FeatureImportanceResponse {
  profile: string
  version: string
  task: string
  feature_importances: Record<string, Record<string, number>>
}