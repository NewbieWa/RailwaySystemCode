#!/usr/bin/env python3
"""
启动脚本 - Railway System Video Analysis Service
"""
import uvicorn
import os
from pathlib import Path

if __name__ == "__main__":
    # 确保uploads目录存在
    uploads_dir = Path("uploads")
    uploads_dir.mkdir(exist_ok=True)
    
    # 启动服务器
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
