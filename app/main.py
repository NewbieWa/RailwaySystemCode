from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from .api import health, video
from .services.file_storage import FileStorageService
from .services.model_runner import (
    ModelRegistry, 
    DummyModelRunner, 
    OpenCVModelRunner, 
    RailwayDetectionModelRunner
)
from .services.video_analysis import VideoAnalysisService

# Initialize services
storage_service = FileStorageService()
model_registry = ModelRegistry()
model_registry.register(DummyModelRunner())
model_registry.register(OpenCVModelRunner())
model_registry.register(RailwayDetectionModelRunner())
analysis_service = VideoAnalysisService(storage_service, model_registry)

# Create FastAPI app
app = FastAPI(
    title="Railway System - Video Analysis Service",
    description="Web service and video analysis service",
    version="1.0.0"
)

# Include routers
app.include_router(health.router)
app.include_router(video.router)

# Mount static files
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve index.html at root
@app.get("/")
async def read_index():
    """Serve the main upload page"""
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    return {"message": "Video Analysis Service", "docs": "/docs"}


# Dependency injection for services
app.dependency_overrides = {
    VideoAnalysisService: lambda: analysis_service
}

