#!/usr/bin/env python3
"""
Demo script to test the penetration testing suite
"""

import sys
import os
from pathlib import Path

def test_pentest_suite():
    """Test the penetration testing suite with demo target"""
    
    print("OWASP Juice Shop Penetration Testing Suite")
    print("=" * 50)
    
    # Default target for demo (you can change this)
    demo_target = "http://localhost:3000"
    
    print(f"Demo target: {demo_target}")
    print("Note: This will work best with a running instance of OWASP Juice Shop")
    print("You can download it from: https://github.com/juice-shop/juice-shop")
    print()
    
    # Show available tools
    tools = [
        "pentest_automation.py - Master automation script",
        "nmap.py - Port scanning and service detection", 
        "nikto.py - Web vulnerability scanning",
        "amass.py - Subdomain enumeration",
        "nuclei.py - Automated vulnerability scanning",
        "zap.py - OWASP ZAP web application scanning",
        "sqlmap.py - SQL injection testing",
        "hydra.py - Brute force attacks",
        "metasploit.py - Exploitation framework",
        "bloodhound.py - Web application enumeration",
        "crackmapexec.py - Credential validation",
        "utils.py - Utility functions",
        "crewai_utils.py - Multi-agent coordination"
    ]
    
    print("Available penetration testing tools:")
    for i, tool in enumerate(tools, 1):
        print(f"{i:2d}. {tool}")
    
    print()
    print("Usage Examples:")
    print("=" * 20)
    print(f"# Run full automated pentest:")
    print(f"python pentest_automation.py {demo_target}")
    print()
    print(f"# Run individual tools:")
    print(f"python nmap.py {demo_target}")
    print(f"python sqlmap.py {demo_target}")
    print(f"python hydra.py {demo_target}")
    print()
    print(f"# Run with credentials for brute force:")
    print(f"python hydra.py {demo_target} admin passwords.txt")
    print()
    print(f"# Run CrewAI multi-agent test:")
    print(f"python crewai_utils.py {demo_target}")
    
    print()
    print("Setting up OWASP Juice Shop:")
    print("=" * 30)
    print("1. Install Docker: https://docs.docker.com/get-docker/")
    print("2. Run: docker run --rm -p 3000:3000 bkimminich/juice-shop")
    print("3. Access at: http://localhost:3000")
    print("4. Run pentest: python pentest_automation.py http://localhost:3000")
    
    return True

def check_tool_prerequisites():
    """Check if external tools are available"""
    print("\nChecking tool prerequisites...")
    print("=" * 30)
    
    external_tools = {
        'nmap': 'Network scanning',
        'nikto': 'Web vulnerability scanning', 
        'sqlmap': 'SQL injection testing',
        'hydra': 'Brute force attacks',
        'nuclei': 'Vulnerability scanning',
        'zap-baseline.py': 'OWASP ZAP scanning',
        'msfconsole': 'Metasploit framework',
        'amass': 'Subdomain enumeration',
        'crackmapexec': 'Network credential testing'
    }
    
    import subprocess
    
    available = []
    missing = []
    
    for tool, description in external_tools.items():
        try:
            result = subprocess.run([tool, '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                available.append(f"✓ {tool} - {description}")
            else:
                missing.append(f"✗ {tool} - {description}")
        except (FileNotFoundError, subprocess.TimeoutExpired):
            missing.append(f"✗ {tool} - {description}")
    
    if available:
        print("Available tools:")
        for tool in available:
            print(f"  {tool}")
    
    if missing:
        print("\nMissing tools (scripts will use fallback methods):")
        for tool in missing:
            print(f"  {tool}")
    
    print(f"\nNote: The Python scripts include fallback methods that work without external tools.")
    print(f"For best results, install the missing tools from their official sources.")

def run_quick_test():
    """Run a quick test of the penetration testing utilities"""
    print("\nRunning quick test of utilities...")
    print("=" * 35)
    
    try:
        # Test utils module
        from utils import generate_common_passwords, create_juice_shop_wordlists, validate_url
        
        print("✓ Utils module loaded successfully")
        
        # Test password generation
        passwords = generate_common_passwords()
        print(f"✓ Generated {len(passwords)} common passwords")
        
        # Test Juice Shop wordlists
        wordlists = create_juice_shop_wordlists()
        print(f"✓ Generated Juice Shop wordlists:")
        print(f"  - {len(wordlists['emails'])} emails")
        print(f"  - {len(wordlists['passwords'])} passwords") 
        print(f"  - {len(wordlists['paths'])} paths")
        
        # Test URL validation
        test_url = validate_url("localhost:3000")
        print(f"✓ URL validation: {test_url}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error in quick test: {e}")
        return False

def main():
    """Main demo function"""
    if not test_pentest_suite():
        return 1
    
    check_tool_prerequisites()
    
    if not run_quick_test():
        return 1
    
    print("\n" + "=" * 50)
    print("Penetration testing suite is ready!")
    print("Choose your target and run the appropriate script.")
    print("For help with any script, run: python <script_name>.py --help")
    print("=" * 50)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
