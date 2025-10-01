<script setup lang="ts">
import { ref } from 'vue'
import VideoUpload from './components/VideoUpload.vue'
import JobList from './components/JobList.vue'
import JobResult from './components/JobResult.vue'

const selectedJobId = ref('')

const handleJobSelected = (jobId: string) => {
  selectedJobId.value = jobId
}
</script>

<template>
  <div class="app">
    <div class="container">
      <aside class="sidebar">
        <JobList @job-selected="handleJobSelected" />
      </aside>

      <main class="main-content">
        <VideoUpload />
        <JobResult :selected-job-id="selectedJobId" />
      </main>
    </div>
  </div>
</template>

<style scoped>
.app {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
  margin: 0;
  padding: 24px;
  background: #f8fafc;
  min-height: 100vh;
}

.container {
  display: grid;
  grid-template-columns: 380px 1fr;
  gap: 24px;
  align-items: start;
  max-width: 1000px;
  margin: 0 auto;
  min-height: calc(100vh - 48px);
}

.sidebar {
  position: sticky;
  top: 24px;
}

.main-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

@media (max-width: 1024px) {
  .container {
    grid-template-columns: 320px 1fr;
    gap: 20px;
  }
}

@media (max-width: 768px) {
  .app {
    padding: 16px;
  }

  .container {
    grid-template-columns: 1fr;
    gap: 16px;
    max-width: 100%;
  }

  .sidebar {
    position: static;
  }
}

@media (max-width: 480px) {
  .app {
    padding: 12px;
  }

  .container {
    gap: 12px;
  }
}
</style>
