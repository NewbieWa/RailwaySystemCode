from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any
import asyncio
import random
import cv2
import numpy as np
from datetime import datetime


class ModelRunner(ABC):
    @abstractmethod
    def get_model_name(self) -> str:
        pass
    
    @abstractmethod
    async def run(self, video_path: Path) -> Dict[str, Any]:
        pass


class DummyModelRunner(ModelRunner):
    def get_model_name(self) -> str:
        return "dummy"
    
    async def run(self, video_path: Path) -> Dict[str, Any]:
        # Simulate video processing time
        await asyncio.sleep(random.uniform(1.5, 3.0))
        
        return {
            "video_path": str(video_path),
            "objects_detected": random.randint(1, 5),
            "processing_time": f"{random.uniform(1.5, 3.0):.2f}s",
            "processed_at": datetime.now().isoformat(),
            "model_name": self.get_model_name()
        }


class OpenCVModelRunner(ModelRunner):
    def get_model_name(self) -> str:
        return "opencv_basic"
    
    async def run(self, video_path: Path) -> Dict[str, Any]:
        """Basic video analysis using OpenCV"""
        start_time = datetime.now()
        
        try:
            # Open video file
            cap = cv2.VideoCapture(str(video_path))
            
            if not cap.isOpened():
                raise ValueError(f"Could not open video file: {video_path}")
            
            # Get video properties
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            duration = frame_count / fps if fps > 0 else 0
            
            # Analyze frames
            frame_analysis = []
            motion_detected = False
            frame_skip = max(1, frame_count // 20)  # Analyze ~20 frames
            
            frame_idx = 0
            prev_frame = None
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                if frame_idx % frame_skip == 0:
                    # Convert to grayscale for analysis
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    
                    # Basic motion detection
                    if prev_frame is not None:
                        diff = cv2.absdiff(prev_frame, gray)
                        motion_amount = np.mean(diff)
                        if motion_amount > 30:  # Threshold for motion detection
                            motion_detected = True
                    
                    # Edge detection
                    edges = cv2.Canny(gray, 50, 150)
                    edge_density = np.sum(edges > 0) / (width * height)
                    
                    frame_analysis.append({
                        "frame_number": frame_idx,
                        "motion_detected": motion_amount > 30 if prev_frame is not None else False,
                        "edge_density": float(edge_density)
                    })
                    
                    prev_frame = gray
                
                frame_idx += 1
            
            cap.release()
            
            # Calculate processing time
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return {
                "video_path": str(video_path),
                "video_properties": {
                    "width": width,
                    "height": height,
                    "fps": fps,
                    "frame_count": frame_count,
                    "duration_seconds": duration
                },
                "analysis_results": {
                    "motion_detected": motion_detected,
                    "frames_analyzed": len(frame_analysis),
                    "average_edge_density": float(np.mean([f["edge_density"] for f in frame_analysis])) if frame_analysis else 0
                },
                "processing_time": f"{processing_time:.2f}s",
                "processed_at": datetime.now().isoformat(),
                "model_name": self.get_model_name(),
                "frame_analysis": frame_analysis[:10]  # Return first 10 frames for details
            }
            
        except Exception as e:
            raise Exception(f"Video analysis failed: {str(e)}")


class RailwayDetectionModelRunner(ModelRunner):
    def get_model_name(self) -> str:
        return "railway_detection"
    
    async def run(self, video_path: Path) -> Dict[str, Any]:
        """Railway-specific video analysis"""
        start_time = datetime.now()
        
        try:
            # Open video file
            cap = cv2.VideoCapture(str(video_path))
            
            if not cap.isOpened():
                raise ValueError(f"Could not open video file: {video_path}")
            
            # Get video properties
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            # Railway-specific analysis
            track_detections = []
            train_detections = []
            obstacle_detections = []
            
            frame_skip = max(1, frame_count // 30)  # Analyze ~30 frames
            frame_idx = 0
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                if frame_idx % frame_skip == 0:
                    # Convert to grayscale
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    
                    # Detect horizontal lines (potential railway tracks)
                    edges = cv2.Canny(gray, 50, 150)
                    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50, minLineLength=100, maxLineGap=10)
                    
                    horizontal_lines = 0
                    if lines is not None:
                        for line in lines:
                            x1, y1, x2, y2 = line[0]
                            angle = abs(np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi)
                            if angle < 15 or angle > 165:  # Horizontal lines
                                horizontal_lines += 1
                    
                    # Detect bright objects (potential trains)
                    bright_objects = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)[1]
                    bright_regions = cv2.findContours(bright_objects, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
                    large_bright_objects = len([c for c in bright_regions if cv2.contourArea(c) > 1000])
                    
                    # Detect dark objects (potential obstacles)
                    dark_objects = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)[1]
                    dark_regions = cv2.findContours(dark_objects, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
                    large_dark_objects = len([c for c in dark_regions if cv2.contourArea(c) > 500])
                    
                    track_detections.append(horizontal_lines)
                    train_detections.append(large_bright_objects)
                    obstacle_detections.append(large_dark_objects)
                
                frame_idx += 1
            
            cap.release()
            
            # Calculate processing time
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return {
                "video_path": str(video_path),
                "video_properties": {
                    "width": width,
                    "height": height,
                    "fps": fps,
                    "frame_count": frame_count
                },
                "railway_analysis": {
                    "avg_track_lines_per_frame": float(np.mean(track_detections)) if track_detections else 0,
                    "max_track_lines_detected": max(track_detections) if track_detections else 0,
                    "avg_bright_objects_per_frame": float(np.mean(train_detections)) if train_detections else 0,
                    "max_bright_objects_detected": max(train_detections) if train_detections else 0,
                    "avg_dark_objects_per_frame": float(np.mean(obstacle_detections)) if obstacle_detections else 0,
                    "max_dark_objects_detected": max(obstacle_detections) if obstacle_detections else 0
                },
                "safety_assessment": {
                    "track_visibility": "good" if np.mean(track_detections) > 2 else "poor",
                    "potential_trains_detected": max(train_detections) > 0,
                    "potential_obstacles": max(obstacle_detections) > 0
                },
                "processing_time": f"{processing_time:.2f}s",
                "processed_at": datetime.now().isoformat(),
                "model_name": self.get_model_name()
            }
            
        except Exception as e:
            raise Exception(f"Railway video analysis failed: {str(e)}")


class ModelRegistry:
    def __init__(self):
        self._runners: Dict[str, ModelRunner] = {}
    
    def register(self, runner: ModelRunner):
        self._runners[runner.get_model_name()] = runner
    
    def get_runner(self, model_name: str) -> ModelRunner:
        if model_name not in self._runners:
            raise ValueError(f"Unknown model: {model_name}")
        return self._runners[model_name]
    
    def list_models(self) -> list[str]:
        return list(self._runners.keys())

