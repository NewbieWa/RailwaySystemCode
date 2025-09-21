from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List

from ..models.schemas import UploadResponse, StatusResponse, ResultResponse
from ..services.video_analysis import VideoAnalysisService

router = APIRouter(prefix="/api/video", tags=["video"])


def get_analysis_service() -> VideoAnalysisService:
    """Dependency to get video analysis service"""
    from ..main import analysis_service
    return analysis_service


@router.post("/upload", response_model=UploadResponse)
async def upload_video(
    file: UploadFile = File(...),
    model_name: str = Form(...),
    analysis_service: VideoAnalysisService = None
):
    """Upload video for analysis"""
    if analysis_service is None:
        analysis_service = get_analysis_service()
    
    # Validate file type
    if not file.content_type or not file.content_type.startswith('video/'):
        raise HTTPException(status_code=400, detail="File must be a video")
    
    # Validate model
    available_models = analysis_service.list_models()
    if model_name not in available_models:
        raise HTTPException(
            status_code=400, 
            detail=f"Unknown model: {model_name}. Available models: {available_models}"
        )
    
    try:
        job_id = await analysis_service.submit_job(
            file.file, model_name, file.filename
        )
        return UploadResponse(job_id=job_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.get("/{job_id}/status", response_model=StatusResponse)
async def get_job_status(job_id: str, analysis_service: VideoAnalysisService = None):
    """Get job status"""
    if analysis_service is None:
        analysis_service = get_analysis_service()
    
    status_info = analysis_service.get_job_status(job_id)
    if status_info is None:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return StatusResponse(**status_info)


@router.get("/{job_id}/result", response_model=ResultResponse)
async def get_job_result(job_id: str, analysis_service: VideoAnalysisService = None):
    """Get job result"""
    if analysis_service is None:
        analysis_service = get_analysis_service()
    
    result_info = analysis_service.get_job_result(job_id)
    if result_info is None:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return ResultResponse(**result_info)


@router.get("/models", response_model=List[str])
async def list_models(analysis_service: VideoAnalysisService = None):
    """List available models"""
    if analysis_service is None:
        analysis_service = get_analysis_service()
    
    return analysis_service.list_models()

