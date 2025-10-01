<template>
  <div class="result-card">
    <h2>分析结果</h2>
    <div v-if="!selectedJobId" class="no-selection">
      请从左侧列表选择一个任务查看结果
    </div>
    <div v-else-if="loading" class="loading">
      加载中...
    </div>
    <div v-else-if="error" class="error">
      错误：{{ error }}
    </div>
    <div v-else class="result-content">
      <div class="job-info">
        <h3>{{ jobInfo?.original_filename || '(未命名)' }}</h3>
        <div class="job-meta">
          <span class="job-id">任务ID: {{ jobInfo?.job_id }}</span>
          <span class="status" :class="getStatusClass(jobInfo?.status)">
            {{ jobInfo?.status }}
          </span>
        </div>
        <div v-if="jobInfo?.model_name" class="model-info">
          模型: {{ jobInfo.model_name }}
        </div>
        <div v-if="jobInfo?.completed_at" class="completed-at">
          完成时间: {{ formatDate(jobInfo.completed_at) }}
        </div>
      </div>
      
      <div v-if="jobInfo?.result" class="result-data">
        <h4>分析结果:</h4>
        <pre class="result-json">{{ JSON.stringify(jobInfo.result, null, 2) }}</pre>
      </div>
      
      <div v-if="jobInfo?.message" class="message">
        <h4>消息:</h4>
        <div class="message-content">{{ jobInfo.message }}</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useVideoStore } from '@/stores/video'

const videoStore = useVideoStore()

const props = defineProps<{
  selectedJobId: string
}>()

const loading = ref(false)
const error = ref('')
const jobInfo = ref<any>(null)

const jobInfoComputed = computed(() => {
  if (!props.selectedJobId) return null
  return videoStore.jobs.find(job => job.job_id === props.selectedJobId)
})

const getStatusClass = (status: string) => {
  switch (status) {
    case 'SUCCEEDED':
      return 'status-success'
    case 'FAILED':
      return 'status-failed'
    case 'RUNNING':
      return 'status-running'
    default:
      return 'status-pending'
  }
}

const formatDate = (dateString: string) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleString('zh-CN')
}

const loadJobResult = async (jobId: string) => {
  if (!jobId) return
  
  loading.value = true
  error.value = ''
  
  try {
    const result = await videoStore.getJobResult(jobId)
    jobInfo.value = result
  } catch (err) {
    error.value = err as string
  } finally {
    loading.value = false
  }
}

watch(() => props.selectedJobId, (newJobId) => {
  if (newJobId) {
    loadJobResult(newJobId)
  } else {
    jobInfo.value = null
    error.value = ''
  }
}, { immediate: true })
</script>

<style scoped>
.result-card {
  padding: 24px;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  max-width: 720px;
}

.no-selection {
  text-align: center;
  color: #6b7280;
  padding: 40px 20px;
  font-style: italic;
}

.loading {
  text-align: center;
  color: #6b7280;
  padding: 40px 20px;
}

.error {
  color: #dc2626;
  padding: 20px;
  background: #fef2f2;
  border-radius: 8px;
  margin: 16px 0;
}

.job-info {
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e5e7eb;
}

.job-info h3 {
  margin: 0 0 12px 0;
  color: #111827;
}

.job-meta {
  display: flex;
  gap: 16px;
  align-items: center;
  margin-bottom: 8px;
}

.job-id {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', monospace;
  font-size: 12px;
  color: #6b7280;
}

.status {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.status-success {
  background: #ecfdf5;
  color: #047857;
}

.status-failed {
  background: #fef2f2;
  color: #b91c1c;
}

.status-running {
  background: #eff6ff;
  color: #1d4ed8;
}

.status-pending {
  background: #f3f4f6;
  color: #6b7280;
}

.model-info, .completed-at {
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 4px;
}

.result-data {
  margin-bottom: 24px;
}

.result-data h4 {
  margin: 0 0 12px 0;
  color: #374151;
}

.result-json {
  background: #f8fafc;
  padding: 16px;
  border-radius: 8px;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', monospace;
  font-size: 14px;
  line-height: 1.5;
  overflow-x: auto;
  white-space: pre-wrap;
  word-break: break-word;
}

.message {
  margin-bottom: 24px;
}

.message h4 {
  margin: 0 0 12px 0;
  color: #374151;
}

.message-content {
  background: #f8fafc;
  padding: 16px;
  border-radius: 8px;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', monospace;
  font-size: 14px;
  line-height: 1.5;
}
</style>


