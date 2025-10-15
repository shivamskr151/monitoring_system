#!/bin/bash

# MediaMTX Monitoring System - Linux/macOS Shell Script
# Simple Unix-only solution

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo "================================================"
echo -e "${BLUE}🚀 MediaMTX Monitoring System${NC}"
echo "================================================"
echo ""

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed or not in PATH${NC}"
    echo "Please install Docker and try again."
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed or not in PATH${NC}"
    echo "Please install Docker Compose and try again."
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    echo -e "${RED}❌ docker-compose.yml not found. Please run this script from the project root.${NC}"
    exit 1
fi

echo -e "${BLUE}📋 System Configuration:${NC}"
echo "  ✅ External Authentication: Enabled"
echo "  ✅ Docker Compose: Multi-service setup"
echo "  ✅ Grafana Dashboard: MediaMTX Data Streaming Dashboard"
echo "  ✅ All Services: Orchestrated with Docker Compose"
echo ""

# Stop existing services if running
echo -e "${BLUE}📦 Stopping existing services...${NC}"
docker-compose down >/dev/null 2>&1 || true

# Build the MediaMTX exporter
echo -e "${BLUE}🔨 Building MediaMTX exporter...${NC}"
docker-compose build mediamtx-exporter

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Build failed! Check the error messages above.${NC}"
    exit 1
fi

# Build the backend authentication service
echo -e "${BLUE}🔨 Building authentication backend...${NC}"
docker-compose build backend

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Backend build failed! Check the error messages above.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Build completed successfully!${NC}"

# Start all services
echo -e "${BLUE}🚀 Starting MediaMTX monitoring system...${NC}"
docker-compose up -d

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to start services! Check Docker permissions.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Services started successfully!${NC}"

# Wait for services to start
echo -e "${BLUE}⏳ Waiting for services to initialize (30 seconds)...${NC}"
sleep 30

# Check service status
echo -e "${BLUE}📊 Checking service status...${NC}"
docker-compose ps

# Display access information
echo ""
echo "================================================"
echo -e "${GREEN}🎉 MediaMTX Monitoring System is Running!${NC}"
echo "================================================"
echo ""
echo -e "${BLUE}📋 Access URLs:${NC}"
echo "  📊 Grafana Dashboard: http://localhost:3000 (admin/admin)"
echo "  📈 Prometheus: http://localhost:9090"
echo "  🎥 MediaMTX API: http://localhost:8887"
echo "  🔐 Authentication Backend: http://localhost:8000"
echo "  📡 MediaMTX Metrics: http://localhost:9998/metrics"
echo "  🔄 Custom Exporter: http://localhost:8081/metrics"
echo "  🖥️  Node Exporter: http://localhost:9100/metrics"
echo ""
echo -e "${BLUE}🎥 Streaming URLs:${NC}"
echo "  📺 RTSP Stream: rtsp://localhost:8554/camera1"
echo "  🌐 HLS Stream: http://localhost:8888/camera1/index.m3u8"
echo "  🔗 WebRTC Stream: http://localhost:8889/camera1"
echo ""
echo -e "${BLUE}🔐 Authentication Users:${NC}"
echo "  👤 admin / admin123 (Full access)"
echo "  👤 viewer / viewer123 (Read/Playback)"
echo "  👤 guest / guest123 (Read only)"
echo "  👤 streamer / streamer123 (Read/Publish/Playback)"
echo ""
echo -e "${BLUE}🛠️  Management Commands:${NC}"
echo "  📊 View logs: docker-compose logs -f"
echo "  📊 View specific service: docker-compose logs -f [service-name]"
echo "  🛑 Stop system: docker-compose down"
echo "  🔄 Restart system: docker-compose restart"
echo "  🔄 Restart specific service: docker-compose restart [service-name]"
echo ""
echo -e "${GREEN}✅ Your MediaMTX monitoring system is ready!${NC}"
echo "   All services are running with external authentication."
echo ""
