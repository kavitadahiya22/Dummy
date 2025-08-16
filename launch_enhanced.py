#!/usr/bin/env python3
"""
Enhanced Penetration Testing Suite Launcher
Starts the complete testing environment with OpenSearch dashboard and PDF reporting
"""

import subprocess
import sys
import time
import requests
import os
from pathlib import Path

def run_command(command, description, shell=False):
    """Run a command and handle errors"""
    print(f"🔧 {description}")
    try:
        if shell:
            result = subprocess.run(command, shell=True, check=True)
        else:
            result = subprocess.run(command, check=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        return False

def wait_for_service(url, name, timeout=300):
    """Wait for a service to become available"""
    print(f"⏳ Waiting for {name} at {url}")
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code < 500:
                print(f"✅ {name} is ready")
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(5)
    
    print(f"⚠️ {name} not ready after {timeout}s")
    return False

def setup_enhanced_environment():
    """Setup the enhanced penetration testing environment"""
    print("🚀 Enhanced Penetration Testing Suite Launcher")
    print("=" * 60)
    
    # Check if Docker is available
    if not run_command(["docker", "--version"], "Checking Docker availability"):
        print("❌ Docker is required but not available")
        return False
    
    # Check if docker-compose is available
    if not run_command(["docker-compose", "--version"], "Checking Docker Compose availability"):
        print("❌ Docker Compose is required but not available")
        return False
    
    print("\n📦 Setting up enhanced environment...")
    
    # Install Python dependencies locally
    if Path("setup_enhanced.py").exists():
        run_command([sys.executable, "setup_enhanced.py"], "Installing enhanced Python packages")
    
    # Start the enhanced Docker environment
    print("\n🐳 Starting enhanced Docker environment...")
    if not run_command(["docker-compose", "up", "-d"], "Starting enhanced containers"):
        print("❌ Failed to start Docker containers")
        return False
    
    # Wait for services to be ready
    print("\n⏳ Waiting for services to be ready...")
    services = [
        ("http://localhost:3000", "OWASP Juice Shop"),
        ("http://localhost:9200", "OpenSearch"),
        ("http://localhost:5601", "OpenSearch Dashboards")
    ]
    
    all_ready = True
    for url, name in services:
        if not wait_for_service(url, name):
            all_ready = False
    
    if all_ready:
        print("\n🎉 Enhanced Environment Ready!")
        print("=" * 60)
        print("🎯 Target Application: http://localhost:3000")
        print("📊 OpenSearch API: http://localhost:9200")
        print("📈 OpenSearch Dashboard: http://localhost:5601")
        print("=" * 60)
        
        # Run the enhanced penetration test
        print("\n🛡️ Starting Enhanced Penetration Testing...")
        target_url = "http://localhost:3000"
        
        if run_command([sys.executable, "enhanced_pentest_automation.py", target_url], 
                      "Running enhanced penetration test"):
            print("\n🎉 Enhanced Penetration Testing Complete!")
            print_results_summary()
        else:
            print("\n⚠️ Penetration testing completed with issues")
    
    return all_ready

def print_results_summary():
    """Print summary of available results and reports"""
    print("\n📊 Results Summary:")
    print("=" * 40)
    
    # Check for results files
    results_dir = Path("./results")
    if results_dir.exists():
        json_files = list(results_dir.glob("*.json"))
        if json_files:
            latest_results = max(json_files, key=lambda f: f.stat().st_mtime)
            print(f"📁 Latest Results: {latest_results}")
    
    # Check for PDF reports
    pdf_files = list(Path(".").glob("pentest_report_*.pdf"))
    if not pdf_files:
        pdf_files = list(Path("./reports").glob("*.pdf"))
    
    if pdf_files:
        latest_pdf = max(pdf_files, key=lambda f: f.stat().st_mtime)
        print(f"📄 Latest PDF Report: {latest_pdf}")
    
    print("\n🎯 Access Points:")
    print("  • Dashboard: http://localhost:5601/app/dashboards")
    print("  • OpenSearch: http://localhost:9200/_cat/indices")
    print("  • Target App: http://localhost:3000")
    
    print("\n📋 Next Steps:")
    print("  1. Review the PDF report for detailed findings")
    print("  2. Explore the OpenSearch dashboard for interactive analysis")
    print("  3. Use the APIs to export data for further processing")
    print("  4. Schedule regular testing for continuous monitoring")

def cleanup_environment():
    """Clean up the Docker environment"""
    print("\n🧹 Cleaning up environment...")
    run_command(["docker-compose", "down"], "Stopping containers")
    run_command(["docker-compose", "down", "-v"], "Removing volumes")

def main():
    """Main launcher function"""
    try:
        success = setup_enhanced_environment()
        
        if success:
            print("\n🎯 Enhanced Penetration Testing Suite is running!")
            print("Press Ctrl+C to stop the environment")
            
            # Keep running until interrupted
            try:
                while True:
                    time.sleep(10)
            except KeyboardInterrupt:
                print("\n🛑 Shutting down...")
                cleanup_environment()
        else:
            print("\n❌ Failed to setup enhanced environment")
            return 1
    
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
        cleanup_environment()
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
