import { defineStore } from 'pinia'
export const useModelStore = defineStore('model', {
  state: () => ({
    profile: 'leve',
    version: null,
    featureNames: [],
  }),
  actions: {
    async loadFeatureNames(profile: string) {
      const res = await getFeatureImportance(profile)
      this.featureNames = Object.keys(res.data.feature_importances[Object.keys(res.data.feature_importances)[0]])
    },
  },
})