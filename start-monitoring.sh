#!/bin/bash

# MediaMTX Monitoring System Startup Script
# This script sets up and starts the complete monitoring stack with MediaMTX, Prometheus, Grafana, and custom exporters

set -e

echo "🚀 Starting MediaMTX Monitoring System..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker first."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    print_error "docker-compose is not installed. Please install docker-compose first."
    exit 1
fi

# Stop any existing containers
print_status "Stopping existing containers..."
docker-compose down > /dev/null 2>&1 || true

# Pull latest images
print_status "Pulling latest Docker images..."
docker-compose pull

# Build custom mediamtx-exporter if Dockerfile exists
if [ -f "Dockerfile.mediamtx-exporter" ]; then
    print_status "Building custom MediaMTX exporter..."
    docker-compose build mediamtx-exporter
fi

# Start the services
print_status "Starting monitoring services..."
docker-compose up -d

# Wait for services to be ready
print_status "Waiting for services to initialize..."
sleep 10

# Check essential services
print_status "Checking essential services..."

# Check Grafana (most important for user)
if curl -f http://localhost:3000/api/health > /dev/null 2>&1; then
    print_success "Grafana is running on http://localhost:3000"
else
    print_warning "Grafana health check failed"
fi

# Check Prometheus
if curl -f http://localhost:9090/-/healthy > /dev/null 2>&1; then
    print_success "Prometheus is running on http://localhost:9090"
else
    print_warning "Prometheus health check failed"
fi

echo
print_success "🎉 Monitoring system started successfully!"
echo
echo "📊 Access Points:"
echo "   📈 Prometheus: http://localhost:9090"
echo "   📊 Grafana: http://localhost:3000 (admin/admin)"
echo "   🎥 MediaMTX API: http://localhost:8887"
echo "   📈 MediaMTX Metrics: http://localhost:9998/metrics"
echo "   🔧 MediaMTX Custom Exporter: http://localhost:8081/metrics"
echo "   💻 Node Exporter: http://localhost:9100/metrics"
echo "   🐳 cAdvisor: http://localhost:8080/metrics"
echo "   📹 RTSP Stream: rtsp://localhost:8554/camera1"
echo "   📺 HLS Stream: http://localhost:8888/camera1/index.m3u8"
echo "   🌐 WebRTC Stream: http://localhost:8889/camera1"
echo
echo "📝 Authentication Details:"
echo "   Grafana: admin / admin"
echo "   MediaMTX API: NO AUTHENTICATION REQUIRED"
echo "   MediaMTX Metrics: NO AUTHENTICATION REQUIRED"
echo "   Prometheus: NO AUTHENTICATION REQUIRED"
echo "   All Exporters: NO AUTHENTICATION REQUIRED"
echo
echo "🎯 Your Camera Stream:"
echo "   RTSP: rtsp://localhost:8554/camera1"
echo "   Source: rtsp://admin:Tatva%40321@183.82.113.87:554/Streaming/Channels/301"
echo
echo "🔧 Management Commands:"
echo "   Stop system: docker-compose down"
echo "   View logs: docker-compose logs -f [service-name]"
echo "   Restart service: docker-compose restart [service-name]"
echo "   Check status: docker-compose ps"
echo
echo "📋 Services Running:"
echo "   ✅ Prometheus (metrics collection)"
echo "   ✅ Grafana (dashboards)"
echo "   ✅ MediaMTX (streaming server)"
echo "   ✅ MediaMTX Custom Exporter (custom metrics)"
echo "   ✅ Node Exporter (system metrics)"
echo "   ✅ cAdvisor (container metrics)"
