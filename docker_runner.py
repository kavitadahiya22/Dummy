#!/usr/bin/env python3
"""
Docker-optimized penetration testing runner
Specifically designed for containerized environments
"""

import os
import sys
import time
import subprocess
from pathlib import Path

def wait_for_target(target_url, max_attempts=30):
    """Wait for target application to be ready"""
    import requests
    
    print(f"Waiting for target {target_url} to be ready...")
    
    for attempt in range(max_attempts):
        try:
            response = requests.get(target_url, timeout=5)
            if response.status_code == 200:
                print(f"✅ Target is ready! ({response.status_code})")
                return True
        except requests.exceptions.RequestException:
            pass
        
        print(f"Attempt {attempt + 1}/{max_attempts} - Target not ready, waiting...")
        time.sleep(2)
    
    print(f"❌ Target {target_url} not ready after {max_attempts} attempts")
    return False

def run_containerized_pentest():
    """Run penetration test in Docker environment"""
    print("🐳 DOCKER CONTAINERIZED PENETRATION TESTING")
    print("=" * 50)
    
    # Get target URL from environment or use default
    target_url = os.getenv('TARGET_URL', 'http://juice-shop:3000')
    output_dir = os.getenv('PENTEST_OUTPUT_DIR', '/app/results')
    
    print(f"Target URL: {target_url}")
    print(f"Output Directory: {output_dir}")
    
    # Wait for target to be ready
    if not wait_for_target(target_url):
        print("❌ Cannot proceed without target application")
        return 1
    
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    print("\n🚀 Starting containerized penetration test...")
    
    # Run the main automation script
    try:
        cmd = [sys.executable, 'pentest_automation.py', target_url, '-o', output_dir]
        print(f"Running: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, cwd='/app')
        
        if result.returncode == 0:
            print("✅ Penetration test completed successfully!")
        else:
            print(f"❌ Penetration test failed with code {result.returncode}")
        
        return result.returncode
        
    except Exception as e:
        print(f"❌ Error running penetration test: {e}")
        return 1

def run_interactive_mode():
    """Run in interactive mode for manual testing"""
    print("🔧 INTERACTIVE PENETRATION TESTING MODE")
    print("=" * 50)
    
    target_url = os.getenv('TARGET_URL', 'http://juice-shop:3000')
    
    tools = {
        '1': ('Quick Reconnaissance', f'python nmap.py {target_url}'),
        '2': ('Web Vulnerability Scan', f'python nikto.py {target_url}'),
        '3': ('SQL Injection Test', f'python sqlmap.py {target_url}'),
        '4': ('Brute Force Attack', f'python hydra.py {target_url}'),
        '5': ('Multi-Agent Test', f'python crewai_utils.py {target_url}'),
        '6': ('Full Automated Test', f'python pentest_automation.py {target_url}'),
        '0': ('Exit', None)
    }
    
    while True:
        print(f"\nTarget: {target_url}")
        print("\nAvailable Tools:")
        for key, (name, _) in tools.items():
            print(f"  {key}. {name}")
        
        choice = input("\nSelect tool (0 to exit): ").strip()
        
        if choice == '0':
            print("Goodbye!")
            break
        elif choice in tools:
            name, command = tools[choice]
            if command:
                print(f"\n🔄 Running: {name}")
                print(f"Command: {command}")
                try:
                    subprocess.run(command, shell=True, cwd='/app')
                except KeyboardInterrupt:
                    print("\n⏹️ Interrupted by user")
                except Exception as e:
                    print(f"❌ Error: {e}")
            else:
                break
        else:
            print("❌ Invalid choice")

def main():
    """Main Docker runner function"""
    print("🐳 CONTAINERIZED PENETRATION TESTING SUITE")
    print("=" * 50)
    
    # Check if running in interactive mode
    if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
        return run_interactive_mode()
    
    # Check if we should run automated test
    if os.getenv('RUN_AUTOMATED_TEST', '').lower() in ['true', '1', 'yes']:
        return run_containerized_pentest()
    
    # Default: run demo
    print("Running demo mode...")
    print("To run automated test, set RUN_AUTOMATED_TEST=true")
    print("To run interactive mode, use: python docker_runner.py --interactive")
    
    # Import and run demo
    try:
        from demo import main as demo_main
        return demo_main()
    except ImportError:
        print("❌ Demo not available")
        return 1

if __name__ == "__main__":
    sys.exit(main())
