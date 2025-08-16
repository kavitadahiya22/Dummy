#!/usr/bin/env python3
"""
Setup script for Enhanced Penetration Testing Suite
Installs required packages for OpenSearch integration and PDF reporting
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a Python package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ Successfully installed {package}")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install {package}")
        return False

def main():
    print("🔧 Setting up Enhanced Penetration Testing Suite")
    print("=" * 50)
    
    # Required packages for enhanced features
    packages = [
        "reportlab",           # PDF generation
        "matplotlib",          # Charts and graphs
        "requests",           # HTTP requests
        "beautifulsoup4",     # HTML parsing
        "lxml",               # XML parsing
        "urllib3",            # HTTP library
        "python-nmap",        # Nmap Python wrapper
        "plotly",             # Interactive charts
        "jinja2",             # Template engine
        "weasyprint",         # Alternative PDF generator
        "opensearch-py"       # OpenSearch Python client
    ]
    
    print("📦 Installing required packages...")
    
    success_count = 0
    for package in packages:
        print(f"Installing {package}...")
        if install_package(package):
            success_count += 1
    
    print(f"\n📊 Installation Summary: {success_count}/{len(packages)} packages installed")
    
    if success_count == len(packages):
        print("✅ All packages installed successfully!")
        print("\n🚀 Enhanced Penetration Testing Suite is ready!")
        print("\nFeatures enabled:")
        print("  • OpenSearch Dashboard Integration")
        print("  • PDF Report Generation with Charts")
        print("  • Advanced Vulnerability Analysis")
        print("  • Real-time Results Visualization")
    else:
        print("⚠️ Some packages failed to install. The suite may have limited functionality.")
        print("You can manually install missing packages using: pip install <package_name>")
    
    print("\n🎯 Next steps:")
    print("  1. Start OpenSearch and Dashboard: docker-compose up opensearch opensearch-dashboards")
    print("  2. Run the enhanced pentest: python enhanced_pentest_automation.py <target_url>")
    print("  3. Access dashboard at: http://localhost:5601")

if __name__ == "__main__":
    main()
