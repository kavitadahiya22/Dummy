# OWASP Juice Shop Penetration Testing Suite

A comprehensive automated penetration testing suite specifically designed for testing OWASP Juice Shop and similar web applications. This suite includes multiple security tools and methodologies to perform thorough security assessments.

## 🎯 Features

- **Automated Full Penetration Testing**: Complete automation from reconnaissance to reporting
- **Multiple Tool Integration**: Integrates with popular security tools (nmap, nikto, sqlmap, hydra, etc.)
- **Fallback Methods**: Python-based implementations when external tools are not available
- **Multi-Agent Coordination**: CrewAI-based approach for coordinated testing
- **Comprehensive Reporting**: Detailed HTML and JSON reports
- **Juice Shop Specific**: Tailored for OWASP Juice Shop vulnerabilities and challenges

## 📋 Tools Included

### Core Automation
- `pentest_automation.py` - Master automation script that orchestrates all tools
- `demo.py` - Demo script to test the suite and check prerequisites

### Reconnaissance & Enumeration
- `amass.py` - Subdomain enumeration and information gathering
- `nmap.py` - Port scanning and service detection
- `nikto.py` - Web server vulnerability scanning

### Vulnerability Assessment
- `nuclei.py` - Automated vulnerability scanning with templates
- `zap.py` - OWASP ZAP web application security scanning

### Exploitation
- `sqlmap.py` - SQL injection testing and exploitation
- `hydra.py` - Brute force attacks on login forms
- `metasploit.py` - Metasploit framework integration

### Post-Exploitation
- `bloodhound.py` - Web application user and privilege enumeration
- `crackmapexec.py` - Credential validation and lateral movement testing

### Utilities
- `utils.py` - Common utility functions and wordlist generation
- `crewai_utils.py` - Multi-agent coordination framework

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Using setup scripts
./docker-setup.sh up          # Start Juice Shop + Pentest Suite
./docker-setup.sh test        # Run automated penetration test
./docker-setup.sh interactive # Interactive testing mode

# Or using Docker Compose directly
docker-compose up -d
docker-compose exec pentest-suite python docker_runner.py --interactive
```

### Option 2: Local Installation

```bash
# Clone or download the suite
cd penetration-testing-suite

# Install Python dependencies
pip install -r requirements.txt

# Run demo to check setup
python demo.py
```

### 2. Setup Target (OWASP Juice Shop)

```bash
# Using Docker (recommended)
docker run --rm -p 3000:3000 bkimminich/juice-shop

# Or download from GitHub
git clone https://github.com/juice-shop/juice-shop.git
cd juice-shop
npm install
npm start
```

### 3. Run Penetration Test

```bash
# Docker environment
./docker-setup.sh test

# Local environment
python pentest_automation.py http://localhost:3000

# Individual tools
python nmap.py http://localhost:3000
python sqlmap.py http://localhost:3000
python hydra.py http://localhost:3000

# Multi-agent approach
python crewai_utils.py http://localhost:3000
```

## 🔧 Installation & Prerequisites

### Docker Installation (Recommended)

**Prerequisites:**
- Docker Desktop or Docker Engine
- Docker Compose

**Setup:**
```bash
# Clone the repository
git clone <repository-url>
cd owasp-juice-shop-pentest-suite

# Start everything with one command
./docker-setup.sh up

# Or on Windows
docker-setup.bat up
```

**Advantages:**
- ✅ Pre-configured environment with all tools
- ✅ Isolated testing environment
- ✅ Consistent results across platforms
- ✅ Easy setup and cleanup
- ✅ Includes OWASP ZAP integration

### Local Installation

**Required Python Packages:**
```bash
pip install requests urllib3 beautifulsoup4 lxml
```

**Optional External Tools (for enhanced capabilities):**
- **nmap** - Network scanning
- **nikto** - Web vulnerability scanning  
- **sqlmap** - SQL injection testing
- **hydra** - Brute force attacks
- **nuclei** - Vulnerability templates
- **OWASP ZAP** - Web application scanning
- **Metasploit** - Exploitation framework
- **amass** - Subdomain enumeration
- **crackmapexec** - Network testing

*Note: The scripts include Python-based fallback methods when external tools are not available.*

## 📖 Usage Examples

### Docker Environment (Recommended)

```bash
# Complete automated test with Docker
./docker-setup.sh up && ./docker-setup.sh test

# Interactive Docker testing
./docker-setup.sh interactive

# Check results
docker-compose exec pentest-suite ls -la /app/results/

# View live logs
docker-compose logs -f pentest-suite
```

### Local Environment

```bash
# Full automated test
python pentest_automation.py http://localhost:3000

# With custom output directory
python pentest_automation.py http://localhost:3000 -o my_results

# With credentials for brute force
python pentest_automation.py http://localhost:3000 -u admin -p passwords.txt
```

### Individual Tool Testing
```bash
# Docker environment
docker-compose exec pentest-suite python nmap.py http://juice-shop:3000
docker-compose exec pentest-suite python sqlmap.py http://juice-shop:3000

# Local environment
python nmap.py http://localhost:3000
python nikto.py http://localhost:3000
python sqlmap.py http://localhost:3000
python hydra.py http://localhost:3000 admin passwords.txt
python bloodhound.py http://localhost:3000
```

### Multi-Agent Coordination
```bash
# Docker environment
docker-compose exec pentest-suite python crewai_utils.py http://juice-shop:3000

# Local environment
python crewai_utils.py http://localhost:3000
```

## 🎯 Juice Shop Specific Features

The suite includes specific targeting for OWASP Juice Shop:

### Pre-configured User Accounts
- `admin@juice-sh.op:admin123`
- `jim@juice-sh.op:ncc-1701`
- `bender@juice-sh.op:OhG0dPlease1nsertLiquor!`
- `amy@juice-sh.op:K1f`

### Common Vulnerable Endpoints
- `/rest/products/search` - SQL injection
- `/rest/user/login` - Authentication bypass
- `/api/Feedbacks` - XSS and injection
- `/ftp/` - Directory traversal
- `/administration` - Admin panel access

### Challenge-Specific Tests
- JWT token manipulation
- Insecure direct object references
- Business logic flaws
- Client-side security issues

## 📊 Report Generation

The suite generates comprehensive reports in multiple formats:

### JSON Reports
- Individual tool results
- Consolidated findings
- Technical details
- Vulnerability classifications

### HTML Reports
- Executive summary
- Risk assessment
- Detailed findings
- Remediation recommendations

### Example Report Structure
```
pentest_results_20250816_143022/
├── nmap_20250816_143022.txt
├── nikto_20250816_143022.txt
├── sqlmap_20250816_143022.txt
├── hydra_20250816_143022.txt
├── pentest_report_20250816_143022.json
└── pentest_report.html
```

## 🔒 Security Considerations

### Ethical Use Only
- Only test applications you own or have explicit permission to test
- Use this suite in controlled environments
- Follow responsible disclosure practices

### Rate Limiting
- The scripts include delays to avoid overwhelming targets
- Adjust timeout values for slower targets
- Consider using proxy for load distribution

### Legal Compliance
- Ensure compliance with local laws and regulations
- Obtain proper authorization before testing
- Document testing scope and approval

## 🛠️ Customization

### Adding New Tools
1. Create new Python script following the pattern
2. Add to `pentest_automation.py` workflow
3. Update documentation and demo

### Custom Wordlists
```python
# In utils.py
def create_custom_wordlists():
    return {
        'usernames': ['custom1', 'custom2'],
        'passwords': ['pass1', 'pass2'],
        'paths': ['/custom', '/admin']
    }
```

### Target-Specific Configuration
```python
# Custom target configuration
target_config = {
    'timeout': 30,
    'user_agents': ['Custom-Agent/1.0'],
    'rate_limit': 1.0
}
```

## 🧪 Testing Methodology

### Phase 1: Reconnaissance
- Information gathering
- Subdomain enumeration
- Port scanning
- Service detection

### Phase 2: Vulnerability Assessment
- Automated scanning
- Manual testing
- Vulnerability classification
- Risk assessment

### Phase 3: Exploitation
- Proof of concept development
- Privilege escalation
- Data extraction
- Impact demonstration

### Phase 4: Post-Exploitation
- Persistence testing
- Lateral movement
- Data exfiltration
- Clean up

### Phase 5: Reporting
- Finding documentation
- Risk assessment
- Remediation recommendations
- Executive summary

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Implement changes with tests
4. Update documentation
5. Submit pull request

## 📄 License

This project is for educational and authorized testing purposes only. Use responsibly.

## ⚠️ Disclaimer

This penetration testing suite is intended for educational purposes and authorized security testing only. Users are responsible for ensuring they have proper authorization before testing any systems. The authors are not responsible for any misuse of this tool.

## 📞 Support

For issues, questions, or contributions:
- Create GitHub issues for bugs
- Submit pull requests for improvements
- Follow responsible disclosure for security issues

---

**Happy Ethical Hacking! 🔒**
