# Railway System - Video Analysis Service

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
RailwaySystemCode/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI应用主文件
│   ├── api/
│   │   ├── __init__.py
│   │   ├── health.py          # 健康检查API
│   │   └── video.py           # 视频分析API
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py         # Pydantic数据模型
│   └── services/
│       ├── file_storage.py    # 文件存储服务
│       ├── model_runner.py    # 模型运行器
│       └── video_analysis.py  # 视频分析服务
├── static/
│   └── index.html            # Web上传界面
├── requirements.txt          # Python依赖
├── config.py                # 配置管理
├── run_server.py           # 启动脚本
└── README.md               # 项目说明
```

## 安装和运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动服务

```bash
python run_server.py
```

或者直接使用uvicorn：

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. 访问服务

- Web界面: http://localhost:8000
- API文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/api/health

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
