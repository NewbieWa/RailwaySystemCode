import os
import aiofiles
from pathlib import Path
from typing import BinaryIO


class FileStorageService:
    def __init__(self, upload_dir: str = "uploads"):
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(exist_ok=True)
    
    async def store_file(self, file: BinaryIO, job_id: str, original_filename: str) -> Path:
        """Store uploaded file and return the file path"""
        # Create subdirectory for the job
        job_dir = self.upload_dir / job_id
        job_dir.mkdir(exist_ok=True)
        
        # Determine file extension
        file_extension = Path(original_filename).suffix
        if not file_extension:
            file_extension = ".mp4"  # Default extension
        
        # Create file path
        file_path = job_dir / f"video{file_extension}"
        
        # Write file asynchronously
        async with aiofiles.open(file_path, 'wb') as f:
            while chunk := await file.read(8192):  # Read in chunks
                await f.write(chunk)
        
        return file_path
    
    def get_file_path(self, job_id: str) -> Path:
        """Get the file path for a job"""
        job_dir = self.upload_dir / job_id
        # Find the video file in the job directory
        for file_path in job_dir.glob("video.*"):
            return file_path
        raise FileNotFoundError(f"No video file found for job {job_id}")
    
    def cleanup_job_files(self, job_id: str):
        """Clean up files for a job"""
        job_dir = self.upload_dir / job_id
        if job_dir.exists():
            import shutil
            shutil.rmtree(job_dir)