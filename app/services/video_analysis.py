import uuid
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor

from .file_storage import FileStorageService
from .model_runner import ModelRegistry
from ..models.schemas import JobStatus


class VideoAnalysisService:
    def __init__(self, storage_service: FileStorageService, model_registry: ModelRegistry):
        self.storage_service = storage_service
        self.model_registry = model_registry
        self.jobs: Dict[str, Dict[str, Any]] = {}
        self.executor = ThreadPoolExecutor(max_workers=4)
    
    async def submit_job(self, file, model_name: str, original_filename: str) -> str:
        """Submit a video analysis job"""
        job_id = str(uuid.uuid4())
        
        # Initialize job record
        self.jobs[job_id] = {
            "status": JobStatus.PENDING,
            "message": None,
            "result": None,
            "created_at": datetime.now(),
            "completed_at": None,
            "model_name": model_name,
            "original_filename": original_filename
        }
        
        try:
            # Store file
            file_path = await self.storage_service.store_file(file, job_id, original_filename)
            
            # Update status
            self.jobs[job_id]["status"] = JobStatus.RUNNING
            self.jobs[job_id]["file_path"] = file_path
            
            # Start processing asynchronously
            asyncio.create_task(self._process_video(job_id, file_path, model_name))
            
        except Exception as e:
            self.jobs[job_id]["status"] = JobStatus.FAILED
            self.jobs[job_id]["message"] = str(e)
            self.jobs[job_id]["completed_at"] = datetime.now()
        
        return job_id
    
    async def _process_video(self, job_id: str, video_path: Path, model_name: str):
        """Process video asynchronously"""
        try:
            runner = self.model_registry.get_runner(model_name)
            result = await runner.run(video_path)
            
            self.jobs[job_id]["status"] = JobStatus.SUCCEEDED
            self.jobs[job_id]["result"] = result
            self.jobs[job_id]["completed_at"] = datetime.now()
            
        except Exception as e:
            self.jobs[job_id]["status"] = JobStatus.FAILED
            self.jobs[job_id]["message"] = str(e)
            self.jobs[job_id]["completed_at"] = datetime.now()
    
    def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get job status and basic info"""
        if job_id not in self.jobs:
            return None
        
        job = self.jobs[job_id]
        return {
            "job_id": job_id,
            "status": job["status"],
            "message": job["message"]
        }
    
    def get_job_result(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get complete job result"""
        if job_id not in self.jobs:
            return None
        
        job = self.jobs[job_id]
        return {
            "job_id": job_id,
            "status": job["status"],
            "result": job["result"],
            "message": job["message"],
            "created_at": job.get("created_at"),
            "completed_at": job["completed_at"],
            "model_name": job.get("model_name"),
            "original_filename": job.get("original_filename")
        }
    
    def list_models(self) -> list[str]:
        """List available models"""
        return self.model_registry.list_models()

    def list_jobs(self, limit: int = 50) -> list[Dict[str, Any]]:
        """List recent jobs with basic info, newest first"""
        items = []
        for job_id, job in self.jobs.items():
            items.append({
                "job_id": job_id,
                "status": job.get("status"),
                "message": job.get("message"),
                "created_at": job.get("created_at"),
                "completed_at": job.get("completed_at"),
                "model_name": job.get("model_name"),
                "original_filename": job.get("original_filename"),
            })
        # Sort by created_at desc
        items.sort(key=lambda x: x.get("created_at") or datetime.min, reverse=True)
        return items[:limit]

