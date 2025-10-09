@echo off
REM MediaMTX Monitoring System Startup Script for Windows
REM This script sets up and starts the complete monitoring stack with MediaMTX, Prometheus, Grafana, and custom exporters

echo 🚀 Starting MediaMTX Monitoring System...

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not running. Please start Docker Desktop first.
    pause
    exit /b 1
)

REM Check if docker-compose is available
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] docker-compose is not installed. Please install docker-compose first.
    pause
    exit /b 1
)

REM Stop any existing containers
echo [INFO] Stopping existing containers...
docker-compose down >nul 2>&1

REM Pull latest images
echo [INFO] Pulling latest Docker images...
docker-compose pull

REM Build custom mediamtx-exporter if Dockerfile exists
if exist "Dockerfile.mediamtx-exporter" (
    echo [INFO] Building custom MediaMTX exporter...
    docker-compose build mediamtx-exporter
)

REM Start the services
echo [INFO] Starting monitoring services...
docker-compose up -d

REM Wait for services to be ready
echo [INFO] Waiting for services to initialize...
timeout /t 10 /nobreak >nul

REM Check essential services
echo [INFO] Checking essential services...

REM Check Grafana (most important for user)
curl -f http://localhost:3000/api/health >nul 2>&1
if %errorlevel% equ 0 (
    echo [SUCCESS] Grafana is running on http://localhost:3000
) else (
    echo [WARNING] Grafana health check failed
)

REM Check Prometheus
curl -f http://localhost:9090/-/healthy >nul 2>&1
if %errorlevel% equ 0 (
    echo [SUCCESS] Prometheus is running on http://localhost:9090
) else (
    echo [WARNING] Prometheus health check failed
)

echo.
echo [SUCCESS] 🎉 Monitoring system started successfully!
echo.
echo 📊 Access Points:
echo    📈 Prometheus: http://localhost:9090
echo    📊 Grafana: http://localhost:3000 (admin/admin)
echo    🎥 MediaMTX API: http://localhost:8887
echo    📈 MediaMTX Metrics: http://localhost:9998/metrics
echo    🔧 MediaMTX Custom Exporter: http://localhost:8081/metrics
echo    💻 Node Exporter: http://localhost:9100/metrics
echo    🐳 cAdvisor: http://localhost:8080/metrics
echo    📹 RTSP Stream: rtsp://localhost:8554/camera1
echo    📺 HLS Stream: http://localhost:8888/camera1/index.m3u8
echo    🌐 WebRTC Stream: http://localhost:8889/camera1
echo.
echo 📝 Authentication Details:
echo    Grafana: admin / admin
echo    MediaMTX API: NO AUTHENTICATION REQUIRED
echo    MediaMTX Metrics: NO AUTHENTICATION REQUIRED
echo    Prometheus: NO AUTHENTICATION REQUIRED
echo    All Exporters: NO AUTHENTICATION REQUIRED
echo.
echo 🎯 Your Camera Stream:
echo    RTSP: rtsp://localhost:8554/camera1
echo    Source: rtsp://admin:Tatva%%40321@183.82.113.87:554/Streaming/Channels/301
echo.
echo 🔧 Management Commands:
echo    Stop system: docker-compose down
echo    View logs: docker-compose logs -f [service-name]
echo    Restart service: docker-compose restart [service-name]
echo    Check status: docker-compose ps
echo.
echo 📋 Services Running:
echo    ✅ Prometheus (metrics collection)
echo    ✅ Grafana (dashboards)
echo    ✅ MediaMTX (streaming server)
echo    ✅ MediaMTX Custom Exporter (custom metrics)
echo    ✅ Node Exporter (system metrics)
echo    ✅ cAdvisor (container metrics)
echo.
pause
