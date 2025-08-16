# 🐳 Docker Setup for OWASP Juice Shop Penetration Testing Suite

This directory contains everything needed to run the penetration testing suite in Docker containers, providing a clean, isolated, and reproducible testing environment.

## 📋 Docker Components

### Core Files
- `Dockerfile` - Main penetration testing suite container
- `docker-compose.yml` - Multi-container orchestration 
- `docker_runner.py` - Container-optimized test runner
- `docker-setup.sh` - Linux/Mac setup script
- `docker-setup.bat` - Windows setup script
- `.dockerignore` - Files to exclude from Docker build

### Container Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Juice Shop    │    │  Pentest Suite  │    │   OWASP ZAP     │
│   Target App    │    │   (Main Tools)  │    │ (Web Scanner)   │
│   Port: 3000    │    │                 │    │   Port: 8080    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                        │                        │
         └────────────────────────┼────────────────────────┘
                                  │
                           ┌─────────────┐
                           │   Network   │
                           │ pentest-net │
                           └─────────────┘
```

## 🚀 Quick Start

### Option 1: Using Setup Scripts (Recommended)

**Linux/Mac:**
```bash
chmod +x docker-setup.sh
./docker-setup.sh up          # Start all containers
./docker-setup.sh test        # Run automated test
./docker-setup.sh interactive # Interactive mode
```

**Windows:**
```cmd
docker-setup.bat up          # Start all containers  
docker-setup.bat test        # Run automated test
docker-setup.bat interactive # Interactive mode
```

### Option 2: Using Docker Compose Directly

```bash
# Start all services
docker-compose up -d

# Run automated penetration test
docker-compose exec -e RUN_AUTOMATED_TEST=true pentest-suite python docker_runner.py

# Interactive testing mode
docker-compose exec pentest-suite python docker_runner.py --interactive

# View logs
docker-compose logs -f pentest-suite

# Stop all services
docker-compose down
```

### Option 3: Manual Docker Commands

```bash
# Build the image
docker build -t pentest-suite .

# Start Juice Shop
docker run -d --name juice-shop -p 3000:3000 bkimminich/juice-shop

# Run penetration test
docker run --rm --link juice-shop \
  -v $(pwd)/results:/app/results \
  pentest-suite python pentest_automation.py http://juice-shop:3000
```

## 🔧 Configuration Options

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `TARGET_URL` | Target application URL | `http://juice-shop:3000` |
| `PENTEST_OUTPUT_DIR` | Results output directory | `/app/results` |
| `RUN_AUTOMATED_TEST` | Run automated test on start | `false` |

### Volume Mounts

| Container Path | Host Path | Purpose |
|----------------|-----------|---------|
| `/app/results` | `./results` | Test results and reports |
| `/app/logs` | `./logs` | Application logs |
| `/zap/reports` | `./zap-reports` | ZAP scan reports |

## 📊 Available Services

### 1. Juice Shop (Target Application)
- **URL:** http://localhost:3000
- **Container:** `juice-shop-target`
- **Purpose:** Target application for penetration testing

### 2. Penetration Testing Suite
- **Container:** `pentest-automation`
- **Purpose:** Main testing tools and automation
- **Tools Included:**
  - nmap, nikto, hydra, sqlmap
  - Custom Python testing scripts
  - Multi-agent coordination framework

### 3. OWASP ZAP (Optional)
- **URL:** http://localhost:8080
- **Container:** `zap-scanner`
- **Purpose:** Advanced web application security testing

## 🎮 Usage Examples

### Automated Full Penetration Test
```bash
# Start everything and run automated test
./docker-setup.sh up
./docker-setup.sh test

# Check results
docker-compose exec pentest-suite ls -la /app/results/
```

### Interactive Testing Session
```bash
# Start interactive mode
./docker-setup.sh interactive

# Inside container, you can run:
# 1. Quick Reconnaissance
# 2. Web Vulnerability Scan  
# 3. SQL Injection Test
# 4. Brute Force Attack
# 5. Multi-Agent Test
# 6. Full Automated Test
```

### Individual Tool Testing
```bash
# Connect to container
docker-compose exec pentest-suite bash

# Run individual tools
python nmap.py http://juice-shop:3000
python sqlmap.py http://juice-shop:3000
python hydra.py http://juice-shop:3000
```

### Custom Target Testing
```bash
# Test against external target
docker run --rm -v $(pwd)/results:/app/results \
  pentest-suite python pentest_automation.py https://demo.testfire.net
```

## 📁 Directory Structure

```
/app/                           # Container working directory
├── *.py                        # All penetration testing scripts
├── requirements.txt            # Python dependencies
├── README.md                   # Documentation
├── results/                    # Test results (mounted volume)
│   ├── pentest_report_*.json   # Main test reports
│   ├── nmap_*.txt             # Port scan results  
│   ├── sqlmap_*.txt           # SQL injection results
│   └── ...                    # Other tool outputs
└── logs/                      # Application logs (mounted volume)
```

## 🔍 Monitoring and Debugging

### View Container Logs
```bash
# All containers
docker-compose logs -f

# Specific container
docker-compose logs -f pentest-suite
docker-compose logs -f juice-shop
```

### Container Status
```bash
# Check running containers
docker-compose ps

# Container resource usage
docker stats

# Network information
docker network ls
docker network inspect dummy_pentest-network
```

### Debug Mode
```bash
# Start container with bash shell
docker-compose exec pentest-suite bash

# Run tests with debug output
python pentest_automation.py http://juice-shop:3000 --debug
```

## 🛠️ Customization

### Adding New Tools
1. Install in `Dockerfile`:
```dockerfile
RUN apt-get update && apt-get install -y your-tool
```

2. Add to Python scripts or create new ones
3. Rebuild image: `docker-compose build`

### Custom Configurations
```bash
# Create custom docker-compose override
cat > docker-compose.override.yml << EOF
version: '3.8'
services:
  pentest-suite:
    environment:
      - CUSTOM_SETTING=value
    volumes:
      - ./custom-config:/app/config
EOF
```

### Environment-Specific Settings
```bash
# Development environment
export TARGET_URL=http://localhost:3000
export PENTEST_OUTPUT_DIR=./dev-results

# Production-like testing
export TARGET_URL=https://your-staging-env.com
export PENTEST_OUTPUT_DIR=./prod-results
```

## 🔒 Security Considerations

### Container Security
- Runs as non-root user (`pentester`)
- Isolated network environment
- Read-only filesystem where possible
- Limited resource allocation

### Testing Safety
- Isolated from host network by default
- Rate limiting built into tools
- Comprehensive logging for audit trails
- Easy cleanup with `docker-compose down`

### Data Protection
- Results stored in mounted volumes
- Sensitive data automatically filtered
- Configurable output sanitization

## 🧹 Cleanup Commands

```bash
# Stop and remove containers
docker-compose down

# Remove with volumes
docker-compose down -v

# Complete cleanup (images, volumes, networks)
./docker-setup.sh clean

# Manual cleanup
docker system prune -a
docker volume prune
```

## 🔧 Troubleshooting

### Common Issues

**Port Conflicts:**
```bash
# Check what's using port 3000
netstat -tulpn | grep 3000
# Or on Windows: netstat -an | findstr 3000

# Use different ports
docker-compose -f docker-compose.yml -f docker-compose.override.yml up
```

**Permission Issues:**
```bash
# Fix volume permissions
sudo chown -R $USER:$USER ./results ./logs
```

**Network Issues:**
```bash
# Recreate network
docker network rm dummy_pentest-network
docker-compose up --force-recreate
```

**Container Won't Start:**
```bash
# Check logs for errors
docker-compose logs pentest-suite

# Start in debug mode
docker-compose run --rm pentest-suite bash
```

### Performance Tuning

```bash
# Allocate more resources
docker-compose -f docker-compose.yml \
  -f docker-compose.performance.yml up

# Limit resources
docker run --memory=1g --cpus=1.0 pentest-suite
```

## 📞 Support

For Docker-specific issues:
1. Check container logs: `docker-compose logs -f`
2. Verify network connectivity: `docker-compose exec pentest-suite ping juice-shop`
3. Test individual components: `docker-compose run --rm pentest-suite python demo.py`
4. Review Docker configuration files for typos

---

**Happy Containerized Penetration Testing! 🐳🔒**
