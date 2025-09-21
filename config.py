"""
配置模块 - Railway System Video Analysis Service
"""
import os
from pathlib import Path
from typing import Optional


class Config:
    """应用配置类"""
    
    # 服务器配置
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    
    # 文件存储配置
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "uploads")
    MAX_FILE_SIZE: str = os.getenv("MAX_FILE_SIZE", "100MB")
    
    # 模型配置
    MAX_WORKERS: int = int(os.getenv("MAX_WORKERS", "4"))
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "dummy")
    
    # 日志配置
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: Optional[str] = os.getenv("LOG_FILE")
    
    @classmethod
    def ensure_directories(cls):
        """确保必要的目录存在"""
        Path(cls.UPLOAD_DIR).mkdir(exist_ok=True)
        
        if cls.LOG_FILE:
            log_dir = Path(cls.LOG_FILE).parent
            log_dir.mkdir(parents=True, exist_ok=True)


# 全局配置实例
config = Config()
config.ensure_directories()
