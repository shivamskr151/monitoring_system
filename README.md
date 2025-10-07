# MediaMTX Monitoring System

A production-ready monitoring stack for MediaMTX using Prometheus, Grafana (with automatic provisioning), Node Exporter, cAdvisor, and a custom MediaMTX metrics exporter.

### TL;DR

```bash
chmod +x start-monitoring.sh
./start-monitoring.sh
```

- Grafana: [http://localhost:3000](http://localhost:3000) (admin/admin)
- Prometheus: [http://localhost:9090](http://localhost:9090)
- MediaMTX API: [http://localhost:8887](http://localhost:8887)
- MediaMTX Metrics: [http://localhost:9998/metrics](http://localhost:9998/metrics)
- Exporter health: [http://localhost:8081/health](http://localhost:8081/health)

## 🏗️ Architecture

- **MediaMTX**: RTSP/RTMP/HLS/WebRTC streaming server with API and metrics
- **Prometheus**: Metrics collection and storage
- **Grafana**: Visualization and dashboards via provisioning
- **Node Exporter**: Host/system metrics
- **cAdvisor**: Container metrics and resource usage
- **Custom MediaMTX Exporter**: Python exporter that re-exposes MediaMTX metrics for Prometheus

## ⚡ Grafana Provisioning

Automatic, file-based provisioning is enabled:

- **Datasource**: `grafana-provisioning/datasources/prometheus.yml`
- **Dashboards**: `grafana-provisioning/dashboards/dashboard.yml` + `grafana-provisioning/dashboards/mediamtx-dashboard.json`

Benefits: zero manual setup, version-controlled config, consistent deployments.

## 🔐 Authentication & Security

Current settings based on `mediamtx.yml` and `docker-compose.yml`:

- **Grafana**: `admin` / `admin` (change via `GF_SECURITY_ADMIN_PASSWORD`)
- **MediaMTX auth**: `authMethod: internal`
  - Anonymous user `any` has read/playback only
  - Admin user: `admin` / `secret123` with API, metrics, publish, read, playback
- **MediaMTX API** (`:8887`): requires admin permissions
- **MediaMTX Metrics** (`:9998/metrics`): requires admin auth when scraped directly
- **Prometheus**: no auth enabled
- **Exporters (custom, node, cAdvisor)**: no auth enabled

Note: Prometheus is configured to scrape MediaMTX directly with basic auth and also via the custom exporter.

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Open ports: 3000, 9090, 8887, 8888, 8889, 8554, 1935, 9998, 8080, 8081, 9100

### Start the System

```bash
# Make the startup script executable (if not already)
chmod +x start-monitoring.sh

# Start the monitoring system
./start-monitoring.sh
```

### Manual Start

```bash
docker-compose up -d

# View logs
docker-compose logs -f mediamtx
docker-compose logs -f prometheus
docker-compose logs -f grafana
```

### Access Points

| Service | URL | Credentials | Purpose |
|---------|-----|-------------|---------|
| Grafana | [http://localhost:3000](http://localhost:3000) | admin / admin | Visualization dashboard |
| Prometheus | [http://localhost:9090](http://localhost:9090) | - | Metrics query interface |
| MediaMTX API | [http://localhost:8887](http://localhost:8887) | admin / secret123 | Stream management API |
| MediaMTX Metrics (direct) | [http://localhost:9998/metrics](http://localhost:9998/metrics) | admin / secret123 | Native metrics |
| MediaMTX Exporter | [http://localhost:8081/metrics](http://localhost:8081/metrics) | - | Re-exposed MediaMTX metrics |
| Node Exporter | [http://localhost:9100/metrics](http://localhost:9100/metrics) | - | System metrics |
| cAdvisor | [http://localhost:8080/metrics](http://localhost:8080/metrics) | - | Container metrics |
| RTSP Stream | rtsp://localhost:8554/camera1 | - | Video stream access |
| HLS Stream | [http://localhost:8888/camera1/index.m3u8](http://localhost:8888/camera1/index.m3u8) | - | HLS video stream |
| WebRTC Stream | [http://localhost:8889/camera1](http://localhost:8889/camera1) | - | WebRTC video stream |

## 📹 Camera Configuration (in `mediamtx.yml`)

Two example paths are preconfigured:

```yaml
paths:
  camera1:
    source: rtsp://<user>:<password>@<public-ip>:554/Streaming/Channels/301
    sourceOnDemand: yes

  camera2:
    source: rtsp://<user>:<password>@<lan-ip>:1935
    sourceOnDemand: yes
```

Warning: The repository's `mediamtx.yml` currently contains sample credentials and host addresses. Replace them with your own secure values before production use.

### Add a new camera
1. Edit `mediamtx.yml` and add under `paths`:
   ```yaml
   paths:
     new_camera:
       source: rtsp://user:pass@camera_ip:port/path
       sourceOnDemand: yes
   ```
2. Restart MediaMTX:
   ```bash
   docker-compose restart mediamtx
   ```

## 📈 Metrics and Dashboards

### Prometheus scrape configuration (`prometheus.yml`)
- Prometheus → itself at `localhost:9090`
- Prometheus → MediaMTX (direct) at `mediamtx:9998/metrics` using basic auth (`admin/secret123`)
- Prometheus → MediaMTX Exporter at `mediamtx-exporter:8080/metrics`
- Prometheus → Node Exporter at `node-exporter:9100`
- Prometheus → cAdvisor at `cadvisor:8080`

### Custom exporter (`mediamtx-exporter.py`)
- Serves on `:8080` inside container, mapped to host `:8081`
- Endpoints: `/metrics`, `/health`
- Attempts auth to MediaMTX metrics with `admin/secret123` first; falls back to alternatives
- Emits at least:
  - `mediamtx_exporter_up`
  - `mediamtx_exporter_scrape_duration_seconds`
  - All pass-through MediaMTX metrics when available

### Grafana dashboard
## 🔧 Configuration and Overrides

- Change Grafana admin password via `GF_SECURITY_ADMIN_PASSWORD` in `docker-compose.yml`.
- Rotate MediaMTX admin credentials in `mediamtx.yml` and update `prometheus.yml` basic_auth accordingly.
- Create a `docker-compose.override.yml` to customize ports or volumes without editing the base compose file.
- Adjust Prometheus retention by editing `--storage.tsdb.retention.time` in `docker-compose.yml`.

## 💾 Data Persistence

Named volumes are used for data durability:

- `prometheus_data`: Prometheus TSDB
- `grafana_data`: Grafana state (users, dashboards if created via UI)

Backup example:

```bash
docker run --rm -v prometheus_data:/data -v "$PWD":/backup busybox tar czf /backup/prometheus_data.tgz -C / data
docker run --rm -v grafana_data:/data -v "$PWD":/backup busybox tar czf /backup/grafana_data.tgz -C / data
```

Cleanup (dangerous – removes data):

```bash
docker volume rm monitoring_system_prometheus_data monitoring_system_grafana_data
```

## 🔌 Ports Matrix

| Service | Container | Host | Defined in |
|---------|-----------|------|------------|
| Grafana | 3000 | 3000 | `docker-compose.yml` |
| Prometheus | 9090 | 9090 | `docker-compose.yml` |
| MediaMTX RTSP | 8554 | 8554 | `docker-compose.yml` |
| MediaMTX RTMP | 1935 | 1935 | `docker-compose.yml` |
| MediaMTX API | 8887 | 8887 | `docker-compose.yml` |
| MediaMTX HLS | 8888 | 8888 | `docker-compose.yml` |
| MediaMTX WebRTC | 8889 | 8889 | `docker-compose.yml` |
| MediaMTX Metrics | 9998 | 9998 | `docker-compose.yml` |
| MediaMTX Exporter | 8080 | 8081 | `docker-compose.yml` |
| Node Exporter | 9100 | 9100 | `docker-compose.yml` |
| cAdvisor | 8080 | 8080 | `docker-compose.yml` |
- Provisioned automatically from `grafana-provisioning/dashboards/mediamtx-dashboard.json`
- Panels include: Active Paths, Bytes Received/Sent, Active Readers, Total Connections, CPU Usage, and exporter/target status

## 📁 Project Structure

```
monitoring system/
├── docker-compose.yml
├── Dockerfile.mediamtx-exporter
├── mediamtx-exporter.py
├── mediamtx.yml
├── prometheus.yml
├── README.md
├── start-monitoring.sh
├── restart-monitoring.sh
└── grafana-provisioning/
    ├── datasources/
    │   └── prometheus.yml
    └── dashboards/
        ├── dashboard.yml
        └── mediamtx-dashboard.json
```

## 🔧 Configuration Files

- `docker-compose.yml`: Orchestrates all services and networking
- `mediamtx.yml`: MediaMTX server configuration (API, metrics, paths, auth)
- `prometheus.yml`: Prometheus scrape jobs and relabeling
- `grafana-provisioning/…`: Datasource and dashboard provisioning
- `mediamtx-exporter.py`: Custom exporter re-exposing MediaMTX metrics
- `start-monitoring.sh` / `restart-monitoring.sh`: Helper scripts

## 🛠️ Common Commands

```bash
# Stop all services
docker-compose down

# Restart a service
docker-compose restart mediamtx

# View logs
docker-compose logs -f [service-name]

# Update images and restart
docker-compose pull && docker-compose up -d

# Check status
docker-compose ps
```

## 🚨 Troubleshooting

1. **MediaMTX metrics 401/403**
   - Use basic auth `admin/secret123` when scraping directly
   - Confirm `authMethod: internal` and `authInternalUsers` in `mediamtx.yml`

2. **Prometheus targets down**
   - Check http://localhost:9090/targets
   - Verify container names/ports match `prometheus.yml`

3. **Grafana dashboard missing**
   - Check provisioning mounts exist in the Grafana container
   - Logs: `docker-compose logs grafana | grep -i provision`

4. **Camera connection failed**
   - Validate RTSP URL, credentials, and network reachability from Docker host

5. **Exporter issues**
   - Health: http://localhost:8081/health
   - Logs: `docker-compose logs mediamtx-exporter`

## 🔄 Maintenance & Hardening

- Change Grafana admin password via `GF_SECURITY_ADMIN_PASSWORD`
- Rotate MediaMTX admin password in `mediamtx.yml` and `prometheus.yml`
- Keep Docker images updated; back up configuration files
- Consider enabling TLS for WebRTC and limiting exposed ports in production

## 🎯 Key Features

- Real-time monitoring for MediaMTX streams
- Automatic Grafana datasource and dashboard provisioning
- Multi-camera support via `mediamtx.yml`
- System and container metrics via Node Exporter and cAdvisor
- Custom exporter for resilient MediaMTX metrics scraping

## 📦 Getting Started

```bash
chmod +x start-monitoring.sh
./start-monitoring.sh
```

Then open Grafana at http://localhost:3000 (admin/admin).