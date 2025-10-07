#!/usr/bin/env python3
import requests
import time
import threading
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MediaMTXExporter:
    def __init__(self, metrics_url="http://mediamtx:9998/metrics", auth=None):
        self.metrics_url = metrics_url
        self.auth = auth
        self.metrics_data = {}
        
        # Setup session with connection pooling and retries
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=0.1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy, pool_connections=1, pool_maxsize=1)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def fetch_real_metrics(self):
        """Fetch real metrics from MediaMTX endpoint"""
        # MediaMTX metrics endpoint requires authentication
        auth_methods = [
            None,  # No auth first (since MTX_METRICS_AUTH=none)
            ("admin", "admin"),  # Default MediaMTX credentials
            ("mediamtx", "mediamtx"),
            ("root", "root"),
            ("admin", ""),
            ("", ""),
        ]
        
        for auth in auth_methods:
            try:
                response = self.session.get(self.metrics_url, auth=auth, timeout=2)
                response.raise_for_status()
                logger.info(f"Successfully fetched real MediaMTX metrics with auth: {auth}")
                return response.text
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 401:
                    logger.debug(f"Authentication failed for {auth}: {e}")
                    continue
                else:
                    logger.error(f"HTTP error for auth {auth}: {e}")
                    continue
            except requests.exceptions.Timeout:
                logger.warning(f"Timeout for auth {auth} - MediaMTX may be slow")
                continue
            except requests.exceptions.ConnectionError:
                logger.warning(f"Connection error for auth {auth} - MediaMTX may be unavailable")
                continue
            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed for auth {auth}: {e}")
                continue
            except Exception as e:
                logger.error(f"Unexpected error for auth {auth}: {e}")
                continue
        
        logger.warning("All authentication methods failed for MediaMTX metrics")
        # Return empty string - no dummy data, only real data
        return ""
    

    def update_metrics(self):
        """Update internal metrics dictionary"""
        try:
            metrics_text = self.fetch_real_metrics()
            parsed_metrics = {}
            
            if not metrics_text:
                logger.warning("No metrics data received from MediaMTX")
                self.metrics_data = {}
                return
            
            for line in metrics_text.splitlines():
                line = line.strip()
                if not line.startswith("#") and line != "":
                    parts = line.split()
                    if len(parts) == 2:
                        key, value = parts
                        try:
                            parsed_metrics[key] = float(value)
                        except ValueError:
                            parsed_metrics[key] = value
                    else:
                        logger.debug(f"Skipping malformed metric line: {line}")
            
            self.metrics_data = parsed_metrics
            logger.info(f"Successfully parsed {len(parsed_metrics)} metrics from MediaMTX")
            
        except Exception as e:
            logger.error(f"Error updating metrics: {e}")
            self.metrics_data = {}

    def get_prometheus_metrics(self):
        """Return metrics in Prometheus format"""
        if not self.metrics_data:
            # Return basic exporter status metrics when MediaMTX is unavailable
            return """# MediaMTX metrics exported by mediamtx-exporter
# HELP mediamtx_exporter_up Exporter status (1=up, 0=down)
# TYPE mediamtx_exporter_up gauge
mediamtx_exporter_up 0
# HELP mediamtx_exporter_scrape_duration_seconds Time spent scraping MediaMTX
# TYPE mediamtx_exporter_scrape_duration_seconds gauge
mediamtx_exporter_scrape_duration_seconds 0
"""
        
        metrics_text = "# MediaMTX metrics exported by mediamtx-exporter\n"
        metrics_text += "# HELP mediamtx_exporter_up Exporter status (1=up, 0=down)\n"
        metrics_text += "# TYPE mediamtx_exporter_up gauge\n"
        metrics_text += "mediamtx_exporter_up 1\n"
        
        for metric_name, value in self.metrics_data.items():
            # Clean metric name for Prometheus (replace invalid characters)
            clean_name = metric_name.replace("-", "_").replace(".", "_")
            metrics_text += f"# HELP {clean_name} MediaMTX metric: {metric_name}\n"
            metrics_text += f"# TYPE {clean_name} gauge\n"
            metrics_text += f"{clean_name} {value}\n"
        return metrics_text

class MetricsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path == '/metrics':
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                exporter.update_metrics()
                metrics_data = exporter.get_prometheus_metrics().encode()
                self.wfile.write(metrics_data)
                self.wfile.flush()
            elif self.path == '/health':
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'OK')
                self.wfile.flush()
            else:
                self.send_response(404)
                self.end_headers()
        except BrokenPipeError:
            # Client disconnected before we could send response - this is normal
            logger.debug("Client disconnected during request")
        except Exception as e:
            logger.error(f"Error serving request: {e}")
            try:
                self.send_response(500)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(f"# Error: {e}\n".encode())
                self.wfile.flush()
            except:
                pass  # Client may have disconnected

def run_exporter():
    global exporter
    # No authentication needed - MediaMTX auth is disabled
    exporter = MediaMTXExporter()
    logger.info("MediaMTX exporter started - authentication disabled")
    def update_loop():
        while True:
            try:
                exporter.update_metrics()
                time.sleep(10)
            except Exception as e:
                logger.error(f"Error updating metrics: {e}")
                time.sleep(30)
    threading.Thread(target=update_loop, daemon=True).start()
    server = HTTPServer(('0.0.0.0', 8080), MetricsHandler)
    logger.info("MediaMTX Exporter running on port 8080")
    server.serve_forever()

if __name__ == "__main__":
    run_exporter()
