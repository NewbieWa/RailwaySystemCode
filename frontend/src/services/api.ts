export interface Job {
  job_id: string
  status: string
  message?: string
  created_at?: string
  completed_at?: string
  model_name?: string
  original_filename?: string
  result?: any
}

export interface UploadResponse {
  job_id: string
}

export interface StatusResponse {
  job_id: string
  status: string
  message?: string
}

export interface ResultResponse {
  job_id: string
  status: string
  result?: any
  message?: string
  completed_at?: string
}

class ApiService {
  private baseUrl = '/api'

  async getModels(): Promise<string[]> {
    const response = await fetch(`${this.baseUrl}/video/models`)
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    return await response.json()
  }

  async uploadVideo(file: File, modelName: string): Promise<UploadResponse> {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('model_name', modelName)

    const response = await fetch(`${this.baseUrl}/video/upload`, {
      method: 'POST',
      body: formData
    })

    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.detail || 'Upload failed')
    }

    return await response.json()
  }

  async getJobStatus(jobId: string): Promise<StatusResponse> {
    const response = await fetch(`${this.baseUrl}/video/${jobId}/status`)
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    return await response.json()
  }

  async getJobResult(jobId: string): Promise<ResultResponse> {
    const response = await fetch(`${this.baseUrl}/video/${jobId}/result`)
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    return await response.json()
  }

  async getJobs(): Promise<Job[]> {
    const response = await fetch(`${this.baseUrl}/video/jobs`)
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    return await response.json()
  }

  async getHealth(): Promise<{ status: string }> {
    const response = await fetch(`${this.baseUrl}/health`)
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    return await response.json()
  }
}

export const apiService = new ApiService()


