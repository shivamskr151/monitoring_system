# MediaMTX Monitoring System

A comprehensive video streaming monitoring solution using MediaMTX, Prometheus, and Grafana with custom metrics exporters and real-time monitoring capabilities.

## 🏗️ Architecture

- **MediaMTX**: RTSP/RTMP/HLS/WebRTC streaming server with metrics endpoint
- **Prometheus**: Metrics collection and storage
- **Grafana**: Visualization and dashboards with **automatic provisioning**
- **Node Exporter**: System metrics (CPU, memory, disk, network)
- **cAdvisor**: Container metrics and resource usage
- **Custom MediaMTX Exporter**: Python-based custom metrics collector

## ⚡ Grafana Provisioning

This system uses **Grafana Provisioning** for automatic configuration:

### ✅ Benefits
- **Zero manual setup**: Datasources and dashboards configured automatically
- **Version control friendly**: All configuration stored in files
- **Consistent deployments**: Same configuration across environments
- **Faster startup**: No manual configuration steps required

### 🔧 How it Works
1. **Datasource Provisioning**: `grafana-provisioning/datasources/prometheus.yml` automatically configures Prometheus
2. **Dashboard Provisioning**: `grafana-provisioning/dashboards/dashboard.yml` enables automatic dashboard loading
3. **Volume Mounts**: Docker Compose mounts provisioning folders to Grafana container
4. **Automatic Discovery**: Grafana scans and applies configurations on startup

## 🔐 Authentication & Security

### Current Configuration
- **Grafana**: `admin` / `admin` (Dashboard access)
- **MediaMTX API**: No authentication required (simplified setup)
- **MediaMTX Metrics**: No authentication required
- **Prometheus**: No authentication required
- **All Exporters**: No authentication required

### Security Features
- Grafana admin interface protected
- MediaMTX configured for simplified access (no auth barriers)
- All metrics endpoints accessible for monitoring
- Docker container isolation
- Network port exposure limited to necessary services

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Ports 3000, 9090, 8887, 8888, 8889, 8554, 1935, 9998, 8080, 8081, 9100 available

### Start the System

```bash
# Make the startup script executable (if not already)
chmod +x start-monitoring.sh

# Start the monitoring system
./start-monitoring.sh
```

### Manual Start

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f mediamtx
docker-compose logs -f prometheus
docker-compose logs -f grafana
```

### 🆕 Optimized Deployment Workflow

With the Grafana provisioning setup:

1. **Clone/Download** the project
2. **Start services**: `./start-monitoring.sh` or `docker-compose up -d`
3. **Access Grafana**: http://localhost:3000 (admin/admin)
4. **✅ Ready to monitor**: Datasources and dashboards automatically configured!

**No manual configuration required** - everything is provisioned automatically! 🎉

## 📊 Access Points

| Service | URL | Credentials | Purpose |
|---------|-----|-------------|---------|
| Grafana | http://localhost:3000 | admin / admin | Visualization dashboard |
| Prometheus | http://localhost:9090 | - | Metrics query interface |
| MediaMTX API | http://localhost:8887 | - | Stream management API |
| MediaMTX Metrics | http://localhost:9998/metrics | - | Prometheus metrics |
| MediaMTX Custom Exporter | http://localhost:8081/metrics | - | Custom metrics |
| Node Exporter | http://localhost:9100/metrics | - | System metrics |
| cAdvisor | http://localhost:8080/metrics | - | Container metrics |
| RTSP Stream | rtsp://localhost:8554/camera1 | - | Video stream access |
| HLS Stream | http://localhost:8888/camera1/index.m3u8 | - | HLS video stream |
| WebRTC Stream | http://localhost:8889/camera1 | - | WebRTC video stream |

## 📹 Camera Configuration

The system is configured for camera integration with two cameras:

```yaml
# Camera configurations (in mediamtx-clean.yml)
Camera 1: rtsp://admin:Tatva%40321@183.82.113.87:554/Streaming/Channels/301
Camera 2: rtsp://admin:admin@192.168.1.4:1935
```

### Adding New Cameras

1. Edit `mediamtx-clean.yml` under the `paths` section:
```yaml
paths:
  ~^new_camera$:
    source: rtsp://user:pass@camera_ip:port/path
    sourceOnDemand: yes
```

2. Restart MediaMTX:
```bash
docker-compose restart mediamtx
```

## 📈 Metrics Available

### MediaMTX Custom Metrics (via mediamtx-exporter)
- `mediamtx_exporter_up`: Exporter status (1=up, 0=down)
- `mediamtx_exporter_scrape_duration_seconds`: Time spent scraping MediaMTX
- All MediaMTX native metrics (when available)

### 📊 Dashboard Panels
The Grafana dashboard includes monitoring panels for:
- **Active Paths**: Real-time count of MediaMTX streaming paths
- **Bytes Received from Sources**: Data throughput from camera sources
- **Bytes Sent to Viewers**: Data throughput to connected viewers
- **Active Readers/Viewers**: Current number of connected viewers
- **Total Server Connections**: Overall connection count
- **Server CPU Usage**: System resource utilization

### 📈 Data Sources
- **✅ Real Data**: CPU usage, System metrics (Node Exporter)
- **📊 MediaMTX Data**: Real MediaMTX metrics (when available)
- **📈 Container Metrics**: Docker container resource usage (cAdvisor)

### System Metrics (Node Exporter)
- CPU usage, memory usage, disk I/O
- Network statistics and interface metrics
- File system usage and mount points
- System load and process information

### Container Metrics (cAdvisor)
- Container resource usage (CPU, memory, network)
- Container filesystem and device metrics
- Container network interface statistics
- Container process and thread counts

## 📁 Project Structure

```
monitoring-system/
├── 📄 docker-compose.yml              # Service orchestration and networking
├── 📄 Dockerfile.mediamtx-exporter    # Custom exporter container build
├── 📄 mediamtx-exporter.py            # Python metrics exporter
├── 📄 mediamtx-clean.yml              # MediaMTX server configuration (active)
├── 📄 mediamtx.yml                    # MediaMTX server configuration (backup)
├── 📄 prometheus.yml                  # Prometheus collection rules and targets
├── 📄 README.md                       # This documentation file
├── 📄 start-monitoring.sh             # Optimized startup script
├── 📄 restart-monitoring.sh           # Restart script with fixes
└── 📁 grafana-provisioning/           # Grafana automatic configuration
    ├── 📁 datasources/
    │   └── 📄 prometheus.yml          # Auto-configured Prometheus datasource
    └── 📁 dashboards/
        ├── 📄 dashboard.yml           # Dashboard provisioning settings
        └── 📄 mediamtx-dashboard.json # Monitoring dashboard
```

## 🔧 Configuration Files

### Core Configuration
- **`docker-compose.yml`**: Service orchestration, networking, and volume mounts
- **`mediamtx-clean.yml`**: MediaMTX server configuration with camera sources (active)
- **`mediamtx.yml`**: MediaMTX server configuration (backup)
- **`prometheus.yml`**: Prometheus collection rules and scrape targets
- **`start-monitoring.sh`**: Optimized startup script with health checks
- **`restart-monitoring.sh`**: Restart script with timeout fixes

### Custom Exporter
- **`mediamtx-exporter.py`**: Python-based custom metrics collector
- **`Dockerfile.mediamtx-exporter`**: Container build configuration for custom exporter

### Grafana Provisioning
- **`grafana-provisioning/datasources/prometheus.yml`**: Automatic Prometheus datasource configuration
- **`grafana-provisioning/dashboards/dashboard.yml`**: Dashboard provisioning settings
- **`grafana-provisioning/dashboards/mediamtx-dashboard.json`**: Pre-configured monitoring dashboard

## 🛠️ Management Commands

```bash
# Stop all services
docker-compose down

# Restart specific service
docker-compose restart mediamtx

# View real-time logs
docker-compose logs -f [service-name]

# Update and restart
docker-compose pull && docker-compose up -d

# Check service health
docker-compose ps

# Restart with fixes (if needed)
./restart-monitoring.sh
```

## 🚨 Troubleshooting

### Common Issues

1. **Camera connection failed**
   - Check camera IP and credentials in `mediamtx-clean.yml`
   - Verify network connectivity to camera
   - Check RTSP URL format

2. **Prometheus metrics not updating**
   - Check MediaMTX metrics endpoint: `http://localhost:9998/metrics`
   - Check custom exporter: `http://localhost:8081/metrics`
   - Review Prometheus targets: http://localhost:9090/targets
   - Verify all exporters are running: `docker-compose ps`

3. **Grafana dashboard not loading**
   - Check Prometheus datasource configuration
   - Verify dashboard JSON compatibility
   - Review Grafana logs: `docker-compose logs grafana`
   - **Provisioning Issues**: Check if provisioning files are properly mounted
     ```bash
     # Verify provisioning files exist
     ls -la grafana-provisioning/datasources/
     ls -la grafana-provisioning/dashboards/
     
     # Check Grafana provisioning logs
     docker-compose logs grafana | grep -i provision
     ```

4. **MediaMTX container restarting/not working**
   - Check for invalid configuration fields: `docker-compose logs mediamtx`
   - **Common Issue**: `apiAuthentication` and `metricsAuthentication` are not valid MediaMTX fields
   - **Solution**: Use `mediamtx-clean.yml` which has the correct configuration

5. **Custom exporter issues**
   - Check exporter health: `http://localhost:8081/health`
   - Review exporter logs: `docker-compose logs mediamtx-exporter`
   - Restart with fixes: `./restart-monitoring.sh`

### Logs Location

```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs mediamtx
docker-compose logs prometheus
docker-compose logs grafana
docker-compose logs mediamtx-exporter
```

## 🔄 Updates & Maintenance

### Regular Maintenance
1. Monitor system performance and logs
2. Update Docker images monthly
3. Backup configuration files
4. Review authentication credentials

### Scaling Considerations
- Add more MediaMTX instances for high availability
- Implement load balancing for multiple cameras
- Use external storage for Prometheus data retention
- Consider Redis caching for Grafana

## 📝 Customization

### Adding Custom Metrics
1. Modify `mediamtx-exporter.py` for additional metrics collection
2. Update `prometheus.yml` scrape configuration if needed
3. Add new dashboard panels in Grafana
4. Rebuild custom exporter: `docker-compose build mediamtx-exporter`

### Security Hardening
1. Enable authentication in `mediamtx-clean.yml` if needed
2. Change Grafana admin password in `docker-compose.yml`
3. Enable TLS for WebRTC in `mediamtx-clean.yml`
4. Implement network segmentation
5. Regular security updates

## 📞 Support

For issues and questions:
1. Check logs for error messages
2. Verify configuration syntax
3. Test network connectivity
4. Review MediaMTX documentation: https://github.com/bluenviron/mediamtx

## 🎯 Key Features

- **Real-time Monitoring**: Live metrics from MediaMTX streaming server
- **Automatic Configuration**: Grafana provisioning eliminates manual setup
- **Multi-Camera Support**: Configured for multiple RTSP camera sources
- **Container-Based**: Easy deployment with Docker Compose
- **Custom Metrics**: Python-based exporter for enhanced monitoring
- **Health Checks**: Built-in health monitoring for all services
- **Comprehensive Logging**: Detailed logs for troubleshooting

## 🚀 Getting Started

1. **Clone the repository**:
   ```bash
   git clone https://github.com/shivamskr151/monitoring_system.git
   cd monitoring_system
   ```

2. **Start the system**:
   ```bash
   chmod +x start-monitoring.sh
   ./start-monitoring.sh
   ```

3. **Access Grafana**: http://localhost:3000 (admin/admin)

4. **Monitor your streams**: All dashboards and datasources are automatically configured!

Your MediaMTX monitoring system is now ready to monitor your video streaming infrastructure! 🎉