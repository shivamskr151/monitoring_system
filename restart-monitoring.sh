#!/bin/bash

echo "🔄 Restarting monitoring system with timeout fixes..."

# Stop existing containers
echo "📦 Stopping existing containers..."
docker-compose down

# Rebuild the mediamtx-exporter with fixes
echo "🔨 Rebuilding mediamtx-exporter..."
docker-compose build mediamtx-exporter

# Start the monitoring stack
echo "🚀 Starting monitoring stack..."
docker-compose up -d

# Wait a moment for services to start
echo "⏳ Waiting for services to start..."
sleep 10

# Check health of mediamtx-exporter
echo "🏥 Checking mediamtx-exporter health..."
docker-compose exec mediamtx-exporter curl -f http://localhost:8080/health || echo "⚠️  Health check failed, but service may still be starting..."

# Show status
echo "📊 Container status:"
docker-compose ps

echo ""
echo "✅ Monitoring system restarted with fixes:"
echo "   - Added scrape_timeout: 10s to Prometheus config"
echo "   - Reduced MediaMTX request timeout to 3s"
echo "   - Added health check endpoint"
echo "   - Improved error handling and logging"
echo ""
echo "🔍 Check Prometheus targets at: http://localhost:9090/targets"
echo "📈 View Grafana dashboards at: http://localhost:3000"
echo "🏥 Test exporter health at: http://localhost:8081/health"
