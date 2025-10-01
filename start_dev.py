#!/usr/bin/env python3
"""
开发环境启动脚本 - 同时启动后端FastAPI和前端Vue开发服务器
Railway System Video Analysis Service
"""
import subprocess
import sys
import os
import signal
import time
from pathlib import Path
import threading

def run_backend():
    """启动后端FastAPI服务"""
    print("🚀 启动后端FastAPI服务...")
    
    # 确保uploads目录存在
    uploads_dir = Path("uploads")
    uploads_dir.mkdir(exist_ok=True)
    
    # 启动后端服务
    backend_process = subprocess.Popen([
        sys.executable, "-m", "uvicorn", 
        "app.main:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--reload",
        "--log-level", "info"
    ])
    
    return backend_process

def run_frontend():
    """启动前端Vue开发服务器"""
    print("🚀 启动前端Vue开发服务器...")
    
    # 检查前端目录是否存在
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ 前端目录不存在！")
        return None
    
    # 检查package.json是否存在
    package_json = frontend_dir / "package.json"
    if not package_json.exists():
        print("❌ frontend/package.json 不存在！")
        return None
    
    # 检查node_modules是否存在，如果不存在则安装依赖
    node_modules = frontend_dir / "node_modules"
    if not node_modules.exists():
        print("📦 安装前端依赖...")
        install_process = subprocess.run(
            ["npm", "install"],
            cwd=frontend_dir,
            capture_output=True,
            text=True
        )
        if install_process.returncode != 0:
            print(f"❌ 依赖安装失败: {install_process.stderr}")
            return None
        print("✅ 前端依赖安装完成")
    
    # 启动前端开发服务器
    frontend_process = subprocess.Popen([
        "npm", "run", "dev"
    ], cwd=frontend_dir)
    
    return frontend_process

def signal_handler(sig, frame):
    """处理中断信号"""
    print("\n🛑 正在停止服务...")
    if 'backend_process' in globals() and backend_process:
        backend_process.terminate()
    if 'frontend_process' in globals() and frontend_process:
        frontend_process.terminate()
    sys.exit(0)

def main():
    """主函数"""
    print("🎯 视频分析校验系统 - 开发环境启动器")
    print("=" * 50)
    
    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    global backend_process, frontend_process
    backend_process = None
    frontend_process = None
    
    try:
        # 启动后端
        backend_process = run_backend()
        if not backend_process:
            print("❌ 后端启动失败")
            return
        
        # 等待后端启动
        print("⏳ 等待后端服务启动...")
        time.sleep(3)
        
        # 启动前端
        frontend_process = run_frontend()
        if not frontend_process:
            print("❌ 前端启动失败")
            if backend_process:
                backend_process.terminate()
            return
        
        print("=" * 50)
        print("✅ 服务启动完成！")
        print("🌐 后端API: http://localhost:8000")
        print("🌐 前端应用: http://localhost:5173")
        print("📚 API文档: http://localhost:8000/docs")
        print("=" * 50)
        print("按 Ctrl+C 停止所有服务")
        
        # 等待进程结束
        while True:
            if backend_process.poll() is not None:
                print("❌ 后端服务意外停止")
                break
            if frontend_process.poll() is not None:
                print("❌ 前端服务意外停止")
                break
            time.sleep(1)
            
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)
    except Exception as e:
        print(f"❌ 启动失败: {e}")
    finally:
        # 清理进程
        if backend_process:
            backend_process.terminate()
            backend_process.wait()
        if frontend_process:
            frontend_process.terminate()
            frontend_process.wait()
        print("👋 所有服务已停止")

if __name__ == "__main__":
    main()
