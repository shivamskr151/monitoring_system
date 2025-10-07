# MediaMTX Monitoring System

A comprehensive video streaming monitoring solution using MediaMTX, Prometheus, and Grafana with custom metrics exporters and real-time monitoring capabilities.

## 🏗️ Architecture

- **MediaMTX**: RTSP/RTMP/HLS/WebRTC streaming server with metrics endpoint
- **Prometheus**: Metrics collection and storage
- **Grafana**: Visualization and dashboards with **optimized provisioning** (automatic setup)
- **Node Exporter**: System metrics (CPU, memory, disk, network)
- **cAdvisor**: Container metrics and resource usage
- **Custom MediaMTX Exporter**: Python-based custom metrics collector

## ⚡ Grafana Provisioning Optimization

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

With the new Grafana provisioning setup:

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

The system is configured for camera integration:

```yaml
# Camera RTSP URL (configured in mediamtx.yml)
Camera 1: rtsp://admin:Tatva%40321@183.82.113.87:554/Streaming/Channels/301
```

### Adding New Cameras

1. Edit `mediamtx.yml` under the `paths` section:
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
- `mediamtx_paths_total`: Number of configured paths (demo data)
- `mediamtx_readers_total`: Number of active readers/viewers (simulated)
- `mediamtx_bytes_received_total`: Total bytes received from sources (simulated)
- `mediamtx_bytes_sent_total`: Total bytes sent to readers (simulated)
- `mediamtx_connections_total`: Total active connections (simulated)

### 📊 Dashboard Panels (Optimized)
The Grafana dashboard includes the following monitoring panels:
- **Active Paths**: Real-time count of MediaMTX streaming paths
- **Bytes Received from Sources**: Data throughput from camera sources
- **Bytes Sent to Viewers**: Data throughput to connected viewers
- **Active Readers/Viewers**: Current number of connected viewers
- **Total Server Connections**: Overall connection count
- **Server CPU Usage**: System resource utilization

### 📈 Data Sources
- **✅ Real Data**: CPU usage, System metrics (Node Exporter)
- **📊 Simulated Data**: MediaMTX custom metrics (realistic demo data)
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
├── 📄 mediamtx-exporter.py            # Python metrics exporter with demo data
├── 📄 mediamtx.yml                    # MediaMTX server configuration
├── 📄 prometheus.yml                  # Prometheus collection rules and targets
├── 📄 README.md                       # This documentation file
├── 📄 start-monitoring.sh             # Optimized startup script
└── 📁 grafana-provisioning/           # Grafana automatic configuration
    ├── 📁 datasources/
    │   └── 📄 prometheus.yml          # Auto-configured Prometheus datasource
    └── 📁 dashboards/
        ├── 📄 dashboard.yml           # Dashboard provisioning settings
        └── 📄 mediamtx-dashboard.json # Monitoring dashboard
```

### 🆕 Recent Optimizations

**Grafana Provisioning Structure** (Latest Update):
- ✅ **Eliminated manual setup**: No more manual datasource configuration
- ✅ **Centralized configuration**: All Grafana settings in `grafana-provisioning/`
- ✅ **Automatic dashboard loading**: Dashboards appear immediately on startup
- ✅ **Version control ready**: All configuration files tracked in files
- ✅ **Cleaner structure**: Removed redundant files and duplicate configurations
- ✅ **Fixed compatibility issues**: Removed deprecated Angular-based plugins
- ✅ **Optimized datasource config**: Updated to latest Grafana provisioning format
- ✅ **Fixed MediaMTX configuration**: Removed invalid `apiAuthentication` fields
- ✅ **Resolved container restart issues**: MediaMTX now runs stable without errors
- ✅ **Streamlined system**: Clean, focused monitoring setup

## 🔧 Configuration Files

### Core Configuration
- **`docker-compose.yml`**: Service orchestration, networking, and volume mounts
- **`mediamtx.yml`**: MediaMTX server configuration with camera source
- **`prometheus.yml`**: Prometheus collection rules and scrape targets
- **`start-monitoring.sh`**: Optimized startup script with health checks

### Custom Exporter
- **`mediamtx-exporter.py`**: Python-based custom metrics collector with demo data
- **`Dockerfile.mediamtx-exporter`**: Container build configuration for custom exporter

### Grafana Provisioning (Optimized)
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
```

## 🚨 Troubleshooting

### Common Issues

1. **Camera connection failed**
   - Check camera IP and credentials in `mediamtx.yml`
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
   - **Solution**: Remove these fields from `mediamtx.yml`:
     ```bash
     # Remove invalid authentication fields
     sed -i '/apiAuthentication:/,/^$/d' mediamtx.yml
     sed -i '/metricsAuthentication:/,/^$/d' mediamtx.yml
     
     # Restart MediaMTX
     docker-compose restart mediamtx
     ```

### Logs Location

```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs mediamtx
docker-compose logs prometheus
docker-compose logs grafana
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
1. Enable authentication in `mediamtx.yml` if needed
2. Change Grafana admin password in `docker-compose.yml`
3. Enable TLS for WebRTC in `mediamtx.yml`
4. Implement network segmentation
5. Regular security updates

## 📞 Support

For issues and questions:
1. Check logs for error messages
2. Verify configuration syntax
3. Test network connectivity
4. Review MediaMTX documentation: https://github.com/bluenviron/mediamtx
