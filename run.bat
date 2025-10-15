@echo off
REM MediaMTX Monitoring System - Windows Batch Script
REM Simple Windows-only solution

setlocal enabledelayedexpansion

echo.
echo ================================================
echo 🚀 MediaMTX Monitoring System
echo ================================================
echo.

REM Check if Docker is available
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed or not in PATH
    echo Please install Docker Desktop and try again.
    pause
    exit /b 1
)

REM Check if Docker Compose is available
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose is not installed or not in PATH
    echo Please install Docker Compose and try again.
    pause
    exit /b 1
)

REM Check if we're in the right directory
if not exist "docker-compose.yml" (
    echo ❌ docker-compose.yml not found. Please run this script from the project root.
    pause
    exit /b 1
)

echo 📋 System Configuration:
echo   ✅ External Authentication: Enabled
echo   ✅ Docker Compose: Multi-service setup
echo   ✅ Grafana Dashboard: MediaMTX Data Streaming Dashboard
echo   ✅ All Services: Orchestrated with Docker Compose
echo.

REM Stop existing services if running
echo 📦 Stopping existing services...
docker-compose down >nul 2>&1

REM Build the MediaMTX exporter
echo 🔨 Building MediaMTX exporter...
docker-compose build mediamtx-exporter

if errorlevel 1 (
    echo ❌ Build failed! Check the error messages above.
    pause
    exit /b 1
)

REM Build the backend authentication service
echo 🔨 Building authentication backend...
docker-compose build backend

if errorlevel 1 (
    echo ❌ Backend build failed! Check the error messages above.
    pause
    exit /b 1
)

echo ✅ Build completed successfully!

REM Start all services
echo 🚀 Starting MediaMTX monitoring system...
docker-compose up -d

if errorlevel 1 (
    echo ❌ Failed to start services! Check Docker permissions.
    pause
    exit /b 1
)

echo ✅ Services started successfully!

REM Wait for services to start
echo ⏳ Waiting for services to initialize (30 seconds)...
timeout /t 30 /nobreak >nul

REM Check service status
echo 📊 Checking service status...
docker-compose ps

REM Display access information
echo.
echo ================================================
echo 🎉 MediaMTX Monitoring System is Running!
echo ================================================
echo.
echo 📋 Access URLs:
echo   📊 Grafana Dashboard: http://localhost:3000 (admin/admin)
echo   📈 Prometheus: http://localhost:9090
echo   🎥 MediaMTX API: http://localhost:8887
echo   🔐 Authentication Backend: http://localhost:8000
echo   📡 MediaMTX Metrics: http://localhost:9998/metrics
echo   🔄 Custom Exporter: http://localhost:8081/metrics
echo   🖥️  Node Exporter: http://localhost:9100/metrics
echo.
echo 🎥 Streaming URLs:
echo   📺 RTSP Stream: rtsp://localhost:8554/camera1
echo   🌐 HLS Stream: http://localhost:8888/camera1/index.m3u8
echo   🔗 WebRTC Stream: http://localhost:8889/camera1
echo.
echo 🔐 Authentication Users:
echo   👤 admin / admin123 (Full access)
echo   👤 viewer / viewer123 (Read/Playback)
echo   👤 guest / guest123 (Read only)
echo   👤 streamer / streamer123 (Read/Publish/Playback)
echo.
echo 🛠️  Management Commands:
echo   📊 View logs: docker-compose logs -f
echo   📊 View specific service: docker-compose logs -f [service-name]
echo   🛑 Stop system: docker-compose down
echo   🔄 Restart system: docker-compose restart
echo   🔄 Restart specific service: docker-compose restart [service-name]
echo.
echo ✅ Your MediaMTX monitoring system is ready!
echo    All services are running with external authentication.
echo.
pause
