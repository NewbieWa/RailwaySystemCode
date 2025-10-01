<template>
  <div class="job-list">
    <div class="logo-section">
      <div class="logo-text">
        <div class="title">铁路视频分析</div>
        <div class="subtitle">Railway Analysis</div>
      </div>
    </div>
    
    <div class="jobs-header">
      <h3>任务列表</h3>
    </div>
    
    <ul class="jobs">
      <li 
        v-for="job in jobs" 
        :key="job.job_id"
        :class="{ active: selectedJobId === job.job_id }"
        @click="selectJob(job.job_id)"
      >
        <div class="job-info">
          <div class="job-name">{{ job.original_filename || '(未命名)' }}</div>
          <div class="job-id">{{ job.job_id }}</div>
        </div>
        <span :class="getBadgeClass(job.status)">{{ job.status }}</span>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useVideoStore } from '@/stores/video'

const videoStore = useVideoStore()
const selectedJobId = ref<string>('')

const jobs = computed(() => videoStore.jobs)

const getBadgeClass = (status: string) => {
  switch (status) {
    case 'SUCCEEDED':
      return 'badge success'
    case 'FAILED':
      return 'badge failed'
    default:
      return 'badge running'
  }
}

const selectJob = async (jobId: string) => {
  selectedJobId.value = jobId
  // Emit event to parent to show job result
  emit('job-selected', jobId)
}

const emit = defineEmits<{
  'job-selected': [jobId: string]
}>()

let refreshInterval: number

onMounted(async () => {
  await videoStore.refreshJobs()
  
  // Auto-refresh jobs every 5 seconds
  refreshInterval = setInterval(async () => {
    await videoStore.refreshJobs()
  }, 5000)
})

onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
})
</script>

<style scoped>
.job-list {
  position: sticky;
  top: 24px;
  height: calc(100vh - 120px);
  min-height: 600px;
  overflow: auto;
  padding: 24px;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  background: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e5e7eb;
}

.logo-text .title {
  font-weight: 700;
  font-size: 16px;
}

.logo-text .subtitle {
  color: #6b7280;
  font-size: 12px;
}

.jobs-header h3 {
  margin: 0 0 16px 0;
  font-weight: 600;
  color: #374151;
}

.jobs {
  list-style: none;
  padding: 0;
  margin: 0;
}

.jobs li {
  padding: 12px;
  border-bottom: 1px solid #eef2f7;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: background-color 0.2s;
}

.jobs li:hover {
  background: #f8fafc;
}

.jobs li.active {
  background: #eef2ff;
}

.job-info {
  flex: 1;
}

.job-name {
  font-weight: 600;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', monospace;
  margin-bottom: 4px;
}

.job-id {
  color: #6b7280;
  font-size: 12px;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', monospace;
}

.badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 500;
}

.badge.success {
  background: #ecfdf5;
  color: #047857;
}

.badge.failed {
  background: #fef2f2;
  color: #b91c1c;
}

.badge.running {
  background: #eff6ff;
  color: #1d4ed8;
}

/* 响应式样式 */
@media (max-width: 1024px) {
  .job-list {
    padding: 20px;
  }
}

@media (max-width: 768px) {
  .job-list {
    position: static;
    height: auto;
    min-height: 400px;
    max-height: 500px;
    padding: 16px;
  }
  
  .logo-text .title {
    font-size: 14px;
  }
  
  .logo-text .subtitle {
    font-size: 11px;
  }
}

@media (max-width: 480px) {
  .job-list {
    padding: 12px;
    min-height: 300px;
    max-height: 400px;
  }
  
  .jobs li {
    padding: 10px;
  }
  
  .job-name {
    font-size: 14px;
  }
  
  .job-id {
    font-size: 11px;
  }
}
</style>


