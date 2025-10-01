import { defineStore } from 'pinia'
import { ref } from 'vue'
import { apiService, type Job } from '@/services/api'

export const useVideoStore = defineStore('video', () => {
  const jobs = ref<Job[]>([])
  const models = ref<string[]>([])
  const loading = ref(false)
  const error = ref('')

  const loadModels = async () => {
    try {
      loading.value = true
      error.value = ''
      models.value = await apiService.getModels()
    } catch (err) {
      error.value = 'Failed to load models'
      console.error('Failed to load models:', err)
    } finally {
      loading.value = false
    }
  }

  const uploadVideo = async (file: File, modelName: string): Promise<string> => {
    try {
      loading.value = true
      error.value = ''
      const result = await apiService.uploadVideo(file, modelName)
      await refreshJobs()
      return result.job_id
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Upload failed'
      throw err
    } finally {
      loading.value = false
    }
  }

  const getJobStatus = async (jobId: string) => {
    return await apiService.getJobStatus(jobId)
  }

  const getJobResult = async (jobId: string) => {
    return await apiService.getJobResult(jobId)
  }

  const refreshJobs = async () => {
    try {
      jobs.value = await apiService.getJobs()
    } catch (err) {
      console.error('Failed to refresh jobs:', err)
    }
  }

  const getHealth = async () => {
    return await apiService.getHealth()
  }

  return {
    jobs,
    models,
    loading,
    error,
    loadModels,
    uploadVideo,
    getJobStatus,
    getJobResult,
    refreshJobs,
    getHealth
  }
})


