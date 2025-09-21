from enum import Enum
from typing import Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel


class JobStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"


class UploadResponse(BaseModel):
    job_id: str


class StatusResponse(BaseModel):
    job_id: str
    status: JobStatus
    message: Optional[str] = None


class ResultResponse(BaseModel):
    job_id: str
    status: JobStatus
    result: Optional[Dict[str, Any]] = None
    message: Optional[str] = None
    completed_at: Optional[datetime] = None


class HealthResponse(BaseModel):
    status: str

