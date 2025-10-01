<template>
  <div class="video-upload">
    <h2>上传视频进行分析</h2>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="file">视频文件</label>
        <input 
          type="file" 
          id="file" 
          ref="fileInput"
          accept="video/*" 
          required 
          @change="handleFileChange"
        />
      </div>
      
      <div class="form-group">
        <label for="model">模型名称</label>
        <select id="model" v-model="selectedModel" required>
          <option v-for="model in availableModels" :key="model" :value="model">
            {{ model }}
          </option>
        </select>
      </div>
      
      <div class="form-group">
        <button type="submit" :disabled="isUploading">
          {{ isUploading ? '上传中...' : '提交' }}
        </button>
      </div>
    </form>
    
    <div v-if="status" class="status">
      {{ status }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useVideoStore } from '@/stores/video'

const videoStore = useVideoStore()
const fileInput = ref<HTMLInputElement>()
const selectedModel = ref('')
const isUploading = ref(false)
const status = ref('')

const availableModels = ref<string[]>([])

const handleFileChange = () => {
  // File change handled by form submission
}

const handleSubmit = async () => {
  if (!fileInput.value?.files?.[0]) return
  
  const file = fileInput.value.files[0]
  isUploading.value = true
  status.value = '上传中...'
  
  try {
    const jobId = await videoStore.uploadVideo(file, selectedModel.value)
    status.value = `任务已创建：${jobId}，开始轮询状态...`
    
    // Start polling for status
    pollStatus(jobId)
  } catch (error) {
    status.value = `错误：${error}`
    isUploading.value = false
  }
}

const pollStatus = async (jobId: string) => {
  const pollInterval = setInterval(async () => {
    try {
      const statusInfo = await videoStore.getJobStatus(jobId)
      status.value = `状态：${statusInfo.status}${statusInfo.message ? `（${statusInfo.message}）` : ''}`
      
      if (statusInfo.status === 'SUCCEEDED' || statusInfo.status === 'FAILED') {
        clearInterval(pollInterval)
        isUploading.value = false
        await videoStore.refreshJobs()
      }
    } catch (error) {
      status.value = `轮询错误：${error}`
      clearInterval(pollInterval)
      isUploading.value = false
    }
  }, 1000)
}

onMounted(async () => {
  await videoStore.loadModels()
  availableModels.value = videoStore.models
  if (availableModels.value.length > 0) {
    selectedModel.value = availableModels.value[0]
  }
})
</script>

<style scoped>
.video-upload {
  padding: 24px;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  max-width: 720px;
}

.form-group {
  margin: 12px 0;
}

label {
  display: block;
  margin: 12px 0 6px;
  font-weight: 600;
}

input, select, button {
  padding: 8px 12px;
  width: 100%;
  box-sizing: border-box;
}

button {
  cursor: pointer;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: 600;
}

button:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

.status {
  margin-top: 16px;
  color: #6b7280;
}
</style>


