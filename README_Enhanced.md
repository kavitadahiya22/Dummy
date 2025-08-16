# Enhanced Penetration Testing Suite

## 🎯 Features

This comprehensive penetration testing suite now includes advanced reporting and visualization capabilities:

### 🆕 New Features
- **OpenSearch Dashboard Integration**: Real-time visualization of penetration testing results
- **Attractive PDF Reports**: Professional, detailed reports with charts and graphs
- **Enhanced Analytics**: Advanced vulnerability analysis and risk assessment
- **Real-time Monitoring**: Live dashboard updates during testing

### 🛡️ Core Testing Capabilities
- **Reconnaissance**: Network discovery, port scanning, subdomain enumeration
- **Vulnerability Assessment**: Web application scanning, vulnerability detection
- **Exploitation**: SQL injection, authentication attacks, XSS testing
- **Post-Exploitation**: Session analysis, privilege escalation testing

## 🚀 Quick Start

### Option 1: Docker (Recommended)

1. **Start the enhanced environment**:
```bash
docker-compose up -d
```

This will start:
- OWASP Juice Shop (target application)
- OpenSearch (search engine)
- OpenSearch Dashboards (visualization)
- Enhanced Penetration Testing Suite

2. **Access the dashboard**:
- Dashboard: http://localhost:5601
- Target App: http://localhost:3000
- OpenSearch API: http://localhost:9200

### Option 2: Local Installation

1. **Install enhanced dependencies**:
```bash
python setup_enhanced.py
```

2. **Start OpenSearch services** (requires Docker):
```bash
docker-compose up -d opensearch opensearch-dashboards
```

3. **Run enhanced penetration testing**:
```bash
python enhanced_pentest_automation.py http://localhost:3000
```

## 📊 Dashboard Features

### Real-time Visualization
- **Vulnerability Distribution**: Pie charts showing severity breakdown
- **Tool Performance**: Bar charts of findings by tool
- **Timeline Analysis**: Testing progress over time
- **Risk Assessment**: CVSS scores and risk metrics

### Interactive Analysis
- **Filter by Severity**: Focus on critical/high findings
- **Search Capabilities**: Find specific vulnerabilities
- **Export Options**: Export data for further analysis
- **Historical Comparison**: Compare results over time

## 📄 PDF Report Features

### Professional Layout
- **Executive Summary**: High-level overview for management
- **Detailed Findings**: Technical details for security teams
- **Visual Charts**: Graphs and diagrams for better understanding
- **Recommendations**: Actionable remediation advice

### Report Sections
1. **Title Page**: Professional cover with engagement details
2. **Executive Summary**: Business impact and key findings
3. **Methodology**: Testing approach and tools used
4. **Findings Summary**: Statistics and severity breakdown
5. **Detailed Findings**: Technical vulnerability details
6. **Recommendations**: Prioritized remediation steps
7. **Appendix**: Technical references and disclaimers

## 🔧 Configuration

### Environment Variables
```bash
# Target configuration
TARGET_URL=http://juice-shop:3000

# OpenSearch configuration
OPENSEARCH_URL=http://opensearch:9200
OPENSEARCH_DASHBOARD_URL=http://opensearch-dashboards:5601

# Output configuration
PENTEST_OUTPUT_DIR=/app/results
```

### Docker Compose Services

#### OpenSearch
- **Port**: 9200 (API), 9600 (Performance Analyzer)
- **Memory**: 512MB allocated
- **Security**: Disabled for development (enable for production)

#### OpenSearch Dashboards
- **Port**: 5601
- **Features**: Visualization, search, analytics
- **Dependencies**: Requires OpenSearch service

## 📈 Advanced Usage

### Custom Dashboard Creation

1. **Access Dashboards**: Navigate to http://localhost:5601
2. **Create Index Pattern**: 
   - Go to Stack Management > Index Patterns
   - Create pattern: `pentest-results-*`
3. **Build Visualizations**:
   - Pie chart for vulnerability severity
   - Bar chart for tool findings
   - Time series for testing progress
4. **Create Dashboard**: Combine visualizations

### PDF Report Customization

The PDF generator supports custom styling and branding:

```python
# Modify pdf_report_generator.py
class PentestPDFReport:
    def _setup_custom_styles(self):
        # Add your custom colors, fonts, and layouts
        pass
```

### OpenSearch Query Examples

```bash
# Get all critical vulnerabilities
curl -X GET "localhost:9200/pentest-results-*/_search" -H 'Content-Type: application/json' -d'
{
  "query": {
    "term": {
      "severity": "Critical"
    }
  }
}'

# Get findings by tool
curl -X GET "localhost:9200/pentest-results-*/_search" -H 'Content-Type: application/json' -d'
{
  "aggs": {
    "tools": {
      "terms": {
        "field": "tool_name"
      }
    }
  }
}'
```

## 🛠️ Troubleshooting

### OpenSearch Issues
- **Service not starting**: Check memory allocation and port conflicts
- **Data not indexing**: Verify index templates and permissions
- **Dashboard errors**: Ensure OpenSearch is accessible

### PDF Generation Issues
- **Missing charts**: Install matplotlib: `pip install matplotlib`
- **Font errors**: Install additional fonts for better rendering
- **Memory issues**: Reduce image resolution for large reports

### Common Problems

1. **Port Conflicts**:
   ```bash
   # Check what's using the ports
   netstat -tulpn | grep :5601
   netstat -tulpn | grep :9200
   ```

2. **Memory Issues**:
   ```bash
   # Increase Docker memory allocation
   # Or reduce OpenSearch heap size in docker-compose.yml
   ```

3. **Permission Errors**:
   ```bash
   # Fix file permissions
   chmod +x *.py
   chown -R $USER:$USER results/ reports/
   ```

## 📚 Additional Resources

### Learning Materials
- [OpenSearch Documentation](https://opensearch.org/docs/)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [Penetration Testing Methodologies](https://www.ptes.org/)

### Related Tools
- [OWASP ZAP](https://www.zaproxy.org/) - Web application scanner
- [Nuclei](https://nuclei.projectdiscovery.io/) - Fast vulnerability scanner
- [SQLMap](https://sqlmap.org/) - SQL injection tool

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This tool is for educational and authorized testing purposes only. Only use against systems you own or have explicit permission to test. Unauthorized penetration testing is illegal and unethical.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review OpenSearch and Docker logs
3. Create an issue with detailed error information

---

**🎯 Happy Pentesting with Enhanced Analytics and Reporting!**
