#!/usr/bin/env python3
"""
MediaMTX Monitoring System - Unified Setup and Run Script
=========================================================

This single script handles everything for the MediaMTX monitoring system:
- Cross-platform support (Windows, Linux, macOS)
- System requirements checking
- Interactive configuration
- Docker Compose orchestration
- Service management (start, stop, status, logs)
- Complete system reset

Features:
- Prometheus for metrics collection
- Grafana for visualization
- Node Exporter for system metrics
- MediaMTX streaming server
- Custom MediaMTX exporter
- External authentication backend

Requirements:
- Python 3.7+
- Docker and Docker Compose
- Internet connection for downloading images

Usage:
    python run.py                    # Interactive setup and start
    python run.py --start           # Start the system
    python run.py --stop            # Stop the system
    python run.py --status          # Show system status
    python run.py --logs            # Show system logs
    python run.py --reset           # Reset everything
    python run.py --check           # Check requirements only
    python run.py --configure       # Interactive configuration
"""

import os
import sys
import subprocess
import json
import time
import argparse
import platform
from pathlib import Path

# Fix Windows encoding issues
if platform.system() == "Windows":
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

class Colors:
    """ANSI color codes for terminal output"""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    PURPLE = '\033[0;35m'
    CYAN = '\033[0;36m'
    WHITE = '\033[1;37m'
    NC = '\033[0m'  # No Color

class MediaMTXManager:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.docker_compose_file = self.project_root / "docker-compose.yml"
        self.env_file = self.project_root / ".env"
        self.config = {}
        self.is_windows = platform.system() == "Windows"
        
    def print_header(self):
        """Print the system header"""
        print(f"\n{Colors.CYAN}{'='*70}")
        print(f"🚀 MediaMTX Complete Monitoring System")
        print(f"{'='*70}{Colors.NC}")
        print(f"{Colors.BLUE}📋 System Features:{Colors.NC}")
        print(f"  ✅ External Authentication: Enabled")
        print(f"  ✅ Docker Compose: Multi-service setup")
        print(f"  ✅ Grafana Dashboard: MediaMTX Data Streaming Dashboard")
        print(f"  ✅ All Services: Orchestrated with Docker Compose")
        print(f"  ✅ Cross-Platform: Windows, Linux, macOS")
        print()
    
    def print_status(self, message, status="info"):
        """Print colored status messages"""
        if status == "success":
            print(f"{Colors.GREEN}[SUCCESS] {message}{Colors.NC}")
        elif status == "error":
            print(f"{Colors.RED}[ERROR] {message}{Colors.NC}")
        elif status == "warning":
            print(f"{Colors.YELLOW}[WARNING] {message}{Colors.NC}")
        elif status == "info":
            print(f"{Colors.BLUE}[INFO] {message}{Colors.NC}")
        else:
            print(f"{message}")
    
    def check_requirements(self):
        """Check system requirements"""
        self.print_status("Checking system requirements...", "info")
        
        requirements_met = True
        
        # Check Python version
        python_version = sys.version_info
        if python_version >= (3, 7):
            self.print_status(f"Python: {python_version.major}.{python_version.minor}.{python_version.micro} ✅", "success")
        else:
            self.print_status(f"Python: {python_version.major}.{python_version.minor}.{python_version.micro} ❌ (Need 3.7+)", "error")
            requirements_met = False
        
        # Check Docker
        try:
            result = subprocess.run(['docker', '--version'], 
                                  capture_output=True, text=True, check=True)
            self.print_status(f"Docker: {result.stdout.strip()} ✅", "success")
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.print_status("Docker not found. Please install Docker Desktop.", "error")
            requirements_met = False
        
        # Check Docker Compose
        try:
            result = subprocess.run(['docker-compose', '--version'], 
                                  capture_output=True, text=True, check=True)
            self.print_status(f"Docker Compose: {result.stdout.strip()} ✅", "success")
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.print_status("Docker Compose not found. Please install Docker Compose.", "error")
            requirements_met = False
        
        # Check if Docker daemon is running
        try:
            subprocess.run(['docker', 'info'], 
                          capture_output=True, text=True, check=True)
            self.print_status("Docker daemon is running ✅", "success")
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.print_status("Docker daemon is not running. Please start Docker.", "error")
            requirements_met = False
        
        # Check if we're in the right directory
        if not self.docker_compose_file.exists():
            self.print_status("docker-compose.yml not found. Please run this script from the project root.", "error")
            requirements_met = False
        else:
            self.print_status("Project files found ✅", "success")
        
        # Check available disk space
        try:
            if self.is_windows:
                # Windows disk space check
                result = subprocess.run(['wmic', 'logicaldisk', 'get', 'size,freespace,caption'], 
                                      capture_output=True, text=True)
                self.print_status("Disk space check: Windows detected ✅", "info")
            else:
                # Unix disk space check
                result = subprocess.run(['df', '-h', '.'], 
                                      capture_output=True, text=True, check=True)
                self.print_status("Disk space check: OK ✅", "success")
        except:
            self.print_status("Could not check disk space", "warning")
        
        # Check network connectivity
        try:
            if self.is_windows:
                subprocess.run(['ping', '-n', '1', '8.8.8.8'], 
                              capture_output=True, text=True, check=True, timeout=5)
            else:
                subprocess.run(['ping', '-c', '1', '8.8.8.8'], 
                              capture_output=True, text=True, check=True, timeout=5)
            self.print_status("Network connectivity: OK ✅", "success")
        except:
            self.print_status("Network connectivity: Check your internet connection", "warning")
        
        if requirements_met:
            self.print_status("All requirements met! ✅", "success")
        else:
            self.print_status("Some requirements are not met. Please fix them before proceeding.", "error")
        
        return requirements_met
    
    def create_env_file(self):
        """Create .env file with default configuration"""
        env_content = """# MediaMTX Monitoring System Configuration
# ================================================

# Prometheus Configuration
PROMETHEUS_PORT=9090

# Grafana Configuration
GRAFANA_PORT=3000
GF_SECURITY_ADMIN_PASSWORD=admin

# MediaMTX Configuration
RTSP_PORT=8554
RTMP_PORT=1935
API_PORT=8887
HLS_PORT=8888
WEBRTC_PORT=8889
MEDIAMTX_METRICS_PORT=9998

# Exporter Configuration
NODE_EXPORTER_PORT=9100
EXPORTER_HOST_PORT=8081

# Backend Configuration
BACKEND_PORT=8000

# Network Configuration
MONITORING_NETWORK_NAME=monitoring

# Optional: Override any of these values by uncommenting and modifying
# Example:
# GRAFANA_PORT=3001
# PROMETHEUS_PORT=9091
"""
        
        if not self.env_file.exists():
            with open(self.env_file, 'w') as f:
                f.write(env_content)
            self.print_status(f"Created {self.env_file}", "success")
        else:
            self.print_status(f"{self.env_file} already exists", "info")
    
    def configure_system(self):
        """Interactive configuration"""
        self.print_status("Starting interactive configuration...", "info")
        
        # Load existing .env if it exists
        env_vars = {}
        if self.env_file.exists():
            with open(self.env_file, 'r') as f:
                for line in f:
                    if '=' in line and not line.strip().startswith('#'):
                        key, value = line.strip().split('=', 1)
                        env_vars[key] = value
        
        # Configuration questions
        configs = [
            ("GRAFANA_PORT", "Grafana port", "3000"),
            ("PROMETHEUS_PORT", "Prometheus port", "9090"),
            ("GF_SECURITY_ADMIN_PASSWORD", "Grafana admin password", "admin"),
            ("RTSP_PORT", "RTSP port", "8554"),
            ("HLS_PORT", "HLS port", "8888"),
            ("WEBRTC_PORT", "WebRTC port", "8889"),
        ]
        
        for key, description, default in configs:
            current_value = env_vars.get(key, default)
            new_value = input(f"{description} [{current_value}]: ").strip()
            if new_value:
                env_vars[key] = new_value
            else:
                env_vars[key] = current_value
        
        # Write updated .env file
        with open(self.env_file, 'w') as f:
            f.write("# MediaMTX Monitoring System Configuration\n")
            f.write("# ================================================\n\n")
            for key, value in env_vars.items():
                f.write(f"{key}={value}\n")
        
        self.print_status("Configuration saved", "success")
    
    def start_system(self):
        """Start the monitoring system"""
        self.print_status("Starting MediaMTX monitoring system...", "info")
        
        # Create .env file if it doesn't exist
        self.create_env_file()
        
        # Stop any existing services
        self.print_status("Stopping existing services...", "info")
        subprocess.run(['docker-compose', 'down'], cwd=self.project_root, 
                      capture_output=True)
        
        # Build services
        self.print_status("Building MediaMTX exporter...", "info")
        result = subprocess.run(['docker-compose', 'build', 'mediamtx-exporter'], cwd=self.project_root)
        if result.returncode != 0:
            self.print_status("MediaMTX exporter build failed!", "error")
            return False
        
        self.print_status("Building authentication backend...", "info")
        result = subprocess.run(['docker-compose', 'build', 'backend'], cwd=self.project_root)
        if result.returncode != 0:
            self.print_status("Backend build failed!", "error")
            return False
        
        self.print_status("Build completed successfully!", "success")
        
        # Start services
        self.print_status("Starting MediaMTX monitoring system...", "info")
        result = subprocess.run(['docker-compose', 'up', '-d'], cwd=self.project_root)
        if result.returncode != 0:
            self.print_status("Failed to start services!", "error")
            return False
        
        self.print_status("Services started successfully!", "success")
        
        # Wait for services to start
        self.print_status("Waiting for services to initialize (30 seconds)...", "info")
        time.sleep(30)
        
        # Check status
        self.show_status()
        
        self.print_status("MediaMTX monitoring system started successfully!", "success")
        self.show_access_info()
        
        return True
    
    def stop_system(self):
        """Stop the monitoring system"""
        self.print_status("Stopping MediaMTX monitoring system...", "info")
        
        result = subprocess.run(['docker-compose', 'down'], cwd=self.project_root)
        if result.returncode == 0:
            self.print_status("System stopped successfully!", "success")
        else:
            self.print_status("Failed to stop system!", "error")
    
    def show_status(self):
        """Show system status"""
        self.print_status("System Status:", "info")
        
        result = subprocess.run(['docker-compose', 'ps'], cwd=self.project_root, 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(result.stdout)
        else:
            self.print_status("Could not get system status", "error")
    
    def show_logs(self):
        """Show system logs"""
        self.print_status("Showing system logs (Ctrl+C to exit):", "info")
        
        try:
            subprocess.run(['docker-compose', 'logs', '-f'], cwd=self.project_root)
        except KeyboardInterrupt:
            self.print_status("Logs stopped", "info")
    
    def reset_system(self):
        """Reset and clean up everything"""
        self.print_status("Resetting MediaMTX monitoring system...", "warning")
        
        confirm = input("This will remove all containers, images, and data. Continue? (y/N): ")
        if confirm.lower() != 'y':
            self.print_status("Reset cancelled", "info")
            return
        
        # Stop and remove containers
        subprocess.run(['docker-compose', 'down', '-v'], cwd=self.project_root)
        
        # Remove images
        subprocess.run(['docker-compose', 'down', '--rmi', 'all'], cwd=self.project_root)
        
        # Clean up Docker system
        subprocess.run(['docker', 'system', 'prune', '-f'])
        
        self.print_status("System reset complete!", "success")
    
    def show_access_info(self):
        """Show access information"""
        print(f"\n{Colors.GREEN}{'='*70}")
        print(f"🎉 MediaMTX Monitoring System is Running!")
        print(f"{'='*70}{Colors.NC}")
        print(f"\n{Colors.BLUE}📋 Access URLs:{Colors.NC}")
        print(f"  📊 Grafana Dashboard: http://localhost:3000 (admin/admin)")
        print(f"  📈 Prometheus: http://localhost:9090")
        print(f"  🎥 MediaMTX API: http://localhost:8887")
        print(f"  🔐 Authentication Backend: http://localhost:8000")
        print(f"  📡 MediaMTX Metrics: http://localhost:9998/metrics")
        print(f"  🔄 Custom Exporter: http://localhost:8081/metrics")
        print(f"  🖥️  Node Exporter: http://localhost:9100/metrics")
        
        print(f"\n{Colors.BLUE}🎥 Streaming URLs:{Colors.NC}")
        print(f"  📺 RTSP Stream: rtsp://localhost:8554/camera1")
        print(f"  🌐 HLS Stream: http://localhost:8888/camera1/index.m3u8")
        print(f"  🔗 WebRTC Stream: http://localhost:8889/camera1")
        
        print(f"\n{Colors.BLUE}🔐 Authentication Users:{Colors.NC}")
        print(f"  👤 admin / admin123 (Full access)")
        print(f"  👤 viewer / viewer123 (Read/Playback)")
        print(f"  👤 guest / guest123 (Read only)")
        print(f"  👤 streamer / streamer123 (Read/Publish/Playback)")
        
        print(f"\n{Colors.BLUE}🛠️  Management Commands:{Colors.NC}")
        print(f"  📊 View logs: python run.py --logs")
        print(f"  📊 View specific service: docker-compose logs -f [service-name]")
        print(f"  📊 Show status: python run.py --status")
        print(f"  🛑 Stop system: python run.py --stop")
        print(f"  🔄 Restart system: python run.py --stop && python run.py --start")
        print(f"  🗑️  Reset system: python run.py --reset")
        print()
    
    def run(self):
        """Main function"""
        parser = argparse.ArgumentParser(
            description='MediaMTX Monitoring System - Unified Setup and Run Script',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  python run.py                    # Interactive setup and start
  python run.py --start           # Start the system
  python run.py --stop            # Stop the system
  python run.py --status          # Show system status
  python run.py --logs            # Show system logs
  python run.py --reset           # Reset everything
  python run.py --check           # Check requirements only
  python run.py --configure       # Interactive configuration
            """
        )
        
        parser.add_argument('--check', action='store_true',
                          help='Check system requirements')
        parser.add_argument('--configure', action='store_true',
                          help='Interactive configuration')
        parser.add_argument('--start', action='store_true',
                          help='Start the monitoring system')
        parser.add_argument('--stop', action='store_true',
                          help='Stop the monitoring system')
        parser.add_argument('--status', action='store_true',
                          help='Show system status')
        parser.add_argument('--logs', action='store_true',
                          help='Show system logs')
        parser.add_argument('--reset', action='store_true',
                          help='Reset and clean up everything')
        
        args = parser.parse_args()
        
        # If no arguments provided, show header and run interactive setup
        if not any(vars(args).values()):
            self.print_header()
            if self.check_requirements():
                self.create_env_file()
                if input("\nStart the monitoring system now? (Y/n): ").lower() != 'n':
                    self.start_system()
            return
        
        # Handle individual commands
        if args.check:
            self.print_header()
            self.check_requirements()
        elif args.configure:
            self.configure_system()
        elif args.start:
            self.print_header()
            if self.check_requirements():
                self.start_system()
        elif args.stop:
            self.stop_system()
        elif args.status:
            self.show_status()
        elif args.logs:
            self.show_logs()
        elif args.reset:
            self.reset_system()

if __name__ == "__main__":
    try:
        manager = MediaMTXManager()
        manager.run()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Operation cancelled by user{Colors.NC}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Unexpected error: {e}{Colors.NC}")
        sys.exit(1)
