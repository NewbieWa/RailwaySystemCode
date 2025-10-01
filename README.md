# 视频分析校验系统

一个基于FastAPI的Python服务框架，提供Web服务和视频分析功能。

## 功能特性

### 1. Web服务
- 基于FastAPI的现代Web API
- 自动API文档生成 (Swagger UI)
- 健康检查端点
- 静态文件服务
- 异步处理支持

### 2. 视频分析服务
- 支持多种视频格式上传
- 异步视频处理
- 多种分析模型：
  - `dummy`: 模拟分析模型
  - `opencv_basic`: 基于OpenCV的基础分析
  - `railway_detection`: 铁路专用检测模型
- 实时任务状态查询
- 结果存储和检索

## 项目结构

```
视频分析校验系统/
├── app/                     # 后端FastAPI应用
│   ├── __init__.py
│   ├── main.py             # FastAPI应用主文件
│   ├── api/
│   │   ├── __init__.py
│   │   ├── health.py       # 健康检查API
│   │   └── video.py        # 视频分析API
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py      # Pydantic数据模型
│   └── services/
│       ├── file_storage.py # 文件存储服务
│       ├── model_runner.py # 模型运行器
│       └── video_analysis.py # 视频分析服务
├── frontend/               # 前端Vue应用
│   ├── src/
│   │   ├── components/     # Vue组件
│   │   ├── views/          # 页面视图
│   │   ├── services/       # API服务
│   │   ├── stores/         # Pinia状态管理
│   │   └── router/         # 路由配置
│   ├── package.json        # 前端依赖配置
│   ├── vite.config.ts      # Vite构建配置
│   └── tsconfig.json       # TypeScript配置
├── static/
│   └── index.html          # 静态Web上传界面
├── uploads/                # 视频文件存储目录
├── requirements.txt        # Python依赖
├── config.py              # 配置管理
├── run_server.py          # 后端启动脚本
├── start_dev.py           # 开发环境一键启动脚本
└── README.md              # 项目说明
```

## 安装和运行

### 1. 安装依赖

#### 后端依赖
```bash
pip install -r requirements.txt
```

#### 前端依赖
```bash
cd frontend
npm install
```

### 2. 启动服务

#### 🚀 一键启动（推荐）
使用新的开发启动脚本，同时启动后端和前端：

```bash
python start_dev.py
```

这个脚本会：
- 自动启动后端FastAPI服务 (端口8000)
- 自动启动前端Vue开发服务器 (端口5173)
- 自动安装前端依赖（如果未安装）
- 提供统一的进程管理

#### 手动启动
如果需要单独启动服务：

**仅启动后端：**
```bash
python run_server.py
```

**仅启动前端：**
```bash
cd frontend
npm run dev
```

### 3. 访问服务

- 🌐 **前端Vue应用**: http://localhost:5173 （主要界面）
- 🌐 **后端API**: http://localhost:8000
- 📚 **API文档**: http://localhost:8000/docs
- ❤️ **健康检查**: http://localhost:8000/api/health

## API使用说明

### 视频上传和分析

#### 1. 上传视频
```bash
curl -X POST "http://localhost:8000/api/video/upload" \
  -F "file=@your_video.mp4" \
  -F "model_name=railway_detection"
```

#### 2. 查询任务状态
```bash
curl "http://localhost:8000/api/video/{job_id}/status"
```

#### 3. 获取分析结果
```bash
curl "http://localhost:8000/api/video/{job_id}/result"
```

#### 4. 查看可用模型
```bash
curl "http://localhost:8000/api/video/models"
```

### 响应示例

#### 上传响应
```json
{
  "job_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

#### 状态响应
```json
{
  "job_id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "RUNNING",
  "message": null
}
```

#### 分析结果响应
```json
{
  "job_id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "SUCCEEDED",
  "result": {
    "video_path": "/path/to/video.mp4",
    "railway_analysis": {
      "avg_track_lines_per_frame": 3.2,
      "max_track_lines_detected": 5,
      "avg_bright_objects_per_frame": 1.1,
      "max_bright_objects_detected": 2,
      "avg_dark_objects_per_frame": 0.3,
      "max_dark_objects_detected": 1
    },
    "safety_assessment": {
      "track_visibility": "good",
      "potential_trains_detected": true,
      "potential_obstacles": false
    },
    "processing_time": "2.45s",
    "processed_at": "2024-01-01T12:00:00",
    "model_name": "railway_detection"
  },
  "message": null,
  "completed_at": "2024-01-01T12:00:00"
}
```

## 模型说明

### 1. Dummy Model (`dummy`)
- 模拟分析模型，用于测试
- 随机生成分析结果
- 处理时间：1.5-3秒

### 2. OpenCV Basic Model (`opencv_basic`)
- 基于OpenCV的基础视频分析
- 功能：
  - 视频属性提取
  - 运动检测
  - 边缘检测
  - 帧分析

### 3. Railway Detection Model (`railway_detection`)
- 铁路专用检测模型
- 功能：
  - 轨道线检测
  - 列车检测（亮物体）
  - 障碍物检测（暗物体）
  - 安全评估

## 扩展开发

### 添加新的分析模型

1. 继承`ModelRunner`基类：

```python
class YourModelRunner(ModelRunner):
    def get_model_name(self) -> str:
        return "your_model"
    
    async def run(self, video_path: Path) -> Dict[str, Any]:
        # 实现您的分析逻辑
        return {
            "model_name": self.get_model_name(),
            "results": "your_analysis_results"
        }
```

2. 在`main.py`中注册模型：

```python
model_registry.register(YourModelRunner())
```

### 自定义配置

修改`config.py`文件或设置环境变量来自定义配置：

```bash
export HOST=127.0.0.1
export PORT=9000
export MAX_WORKERS=8
export DEFAULT_MODEL=railway_detection
```

## 技术栈

- **FastAPI**: 现代、快速的Web框架
- **OpenCV**: 计算机视觉库
- **NumPy**: 数值计算库
- **Pydantic**: 数据验证和序列化
- **Uvicorn**: ASGI服务器
- **aiofiles**: 异步文件操作

## 注意事项

1. 确保安装了OpenCV和相关依赖
2. 上传的视频文件会存储在`uploads/`目录下
3. 长时间运行的任务建议使用消息队列（如Redis、RabbitMQ）
4. 生产环境建议使用反向代理（如Nginx）
5. 大文件上传可能需要调整服务器配置

## 故障排除

### 常见问题

1. **OpenCV导入错误**
   ```bash
   pip install opencv-python
   ```

2. **端口被占用**
   ```bash
   # 修改config.py中的PORT配置
   # 或使用不同端口启动
   uvicorn app.main:app --port 8001
   ```

3. **文件上传失败**
   - 检查uploads目录权限
   - 确认文件大小限制
   - 验证文件格式支持

## 许可证

MIT License
