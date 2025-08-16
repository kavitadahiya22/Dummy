#!/usr/bin/env python3
"""
Advanced PDF Report Generator for Penetration Testing Results
Creates professional, attractive PDF reports with charts and visualizations
"""

import json
import datetime
import os
from pathlib import Path
from io import BytesIO
import base64

# Import required libraries with fallbacks
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.graphics.shapes import Drawing, Rect
    from reportlab.graphics.charts.piecharts import Pie
    from reportlab.graphics.charts.barcharts import VerticalBarChart
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

class PentestPDFReport:
    def __init__(self, output_file="pentest_report.pdf"):
        self.output_file = output_file
        self.story = []
        self.styles = getSampleStyleSheet() if REPORTLAB_AVAILABLE else None
        self.vulnerability_stats = {
            "Critical": 0,
            "High": 0, 
            "Medium": 0,
            "Low": 0,
            "Info": 0
        }
        self.tool_stats = {}
        self.findings = []
        
        if REPORTLAB_AVAILABLE:
            self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom styles for the report"""
        if not self.styles:
            return
            
        # Custom title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#1f4e79')
        ))
        
        # Custom heading style
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=12,
            spaceBefore=20,
            textColor=colors.HexColor('#2e5984')
        ))
        
        # Risk styles
        self.styles.add(ParagraphStyle(
            name='CriticalRisk',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.red,
            backColor=colors.HexColor('#ffebee')
        ))
        
        self.styles.add(ParagraphStyle(
            name='HighRisk',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#d84315'),
            backColor=colors.HexColor('#fff3e0')
        ))
        
        self.styles.add(ParagraphStyle(
            name='MediumRisk',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#f57c00'),
            backColor=colors.HexColor('#fffde7')
        ))
    
    def load_results(self, results_file):
        """Load penetration testing results from JSON file"""
        try:
            with open(results_file, 'r') as f:
                results = json.load(f)
            
            # Process results and extract findings
            self._process_results(results)
            print(f"✅ Loaded results from {results_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error loading results: {e}")
            return False
    
    def _process_results(self, results):
        """Process raw results and extract vulnerabilities"""
        for tool_name, tool_results in results.items():
            if isinstance(tool_results, dict):
                self.tool_stats[tool_name] = self._count_tool_findings(tool_results)
                vulnerabilities = self._extract_vulnerabilities(tool_name, tool_results)
                self.findings.extend(vulnerabilities)
                
                # Update vulnerability statistics
                for vuln in vulnerabilities:
                    severity = vuln.get('severity', 'Medium')
                    if severity in self.vulnerability_stats:
                        self.vulnerability_stats[severity] += 1
    
    def _count_tool_findings(self, tool_results):
        """Count findings for a specific tool"""
        if isinstance(tool_results, dict):
            # Count various types of findings
            count = 0
            if 'vulnerabilities' in tool_results:
                count += len(tool_results['vulnerabilities'])
            if 'sql_injection_points' in tool_results:
                count += len(tool_results['sql_injection_points'])
            if 'valid_credentials' in tool_results:
                count += len(tool_results['valid_credentials'])
            if 'open_ports' in tool_results:
                count += len(tool_results['open_ports'])
            return count
        return 0
    
    def _extract_vulnerabilities(self, tool_name, results):
        """Extract vulnerabilities from tool results"""
        vulnerabilities = []
        
        if tool_name == "sqlmap":
            for point in results.get("sql_injection_points", []):
                vulnerabilities.append({
                    "tool": tool_name,
                    "title": "SQL Injection Vulnerability",
                    "severity": "High",
                    "location": point,
                    "description": f"SQL injection vulnerability detected at {point}",
                    "impact": "An attacker could potentially read, modify, or delete database contents",
                    "recommendation": "Use parameterized queries and input validation",
                    "cvss": 7.5,
                    "cwe": "CWE-89"
                })
        
        elif tool_name == "nuclei" or tool_name == "vulnerability":
            for vuln in results.get("vulnerabilities", []):
                vulnerabilities.append({
                    "tool": tool_name,
                    "title": vuln.get("type", "Vulnerability Detected"),
                    "severity": vuln.get("severity", "Medium"),
                    "location": vuln.get("location", "Unknown"),
                    "description": vuln.get("description", "Vulnerability detected by automated scanning"),
                    "impact": "Security vulnerability that may allow unauthorized access",
                    "recommendation": "Review and remediate the identified vulnerability"
                })
        
        elif tool_name == "hydra" or tool_name == "exploitation":
            for cred in results.get("valid_credentials", []):
                vulnerabilities.append({
                    "tool": tool_name,
                    "title": "Weak Authentication",
                    "severity": "High",
                    "location": "/login",
                    "description": f"Weak credentials discovered: {cred}",
                    "impact": "Unauthorized access to user accounts",
                    "recommendation": "Implement strong password policies and MFA",
                    "cvss": 6.5,
                    "cwe": "CWE-287"
                })
        
        elif tool_name == "nmap":
            for port in results.get("open_ports", []):
                # Only report potentially risky services
                if any(service in str(port).lower() for service in ['ftp', 'telnet', 'rlogin', 'ssh', 'mysql', 'postgres']):
                    vulnerabilities.append({
                        "tool": tool_name,
                        "title": "Potentially Risky Service",
                        "severity": "Medium",
                        "location": f"Port {port}",
                        "description": f"Service running on port {port} may pose security risks",
                        "impact": "Potential attack vector for unauthorized access",
                        "recommendation": "Review service configuration and access controls"
                    })
        
        return vulnerabilities
    
    def create_chart_image(self, chart_type="severity"):
        """Create chart images using matplotlib"""
        if not MATPLOTLIB_AVAILABLE:
            return None
            
        try:
            fig, ax = plt.subplots(figsize=(8, 6))
            
            if chart_type == "severity":
                # Severity distribution pie chart
                labels = []
                sizes = []
                colors_list = []
                
                for severity, count in self.vulnerability_stats.items():
                    if count > 0:
                        labels.append(f"{severity} ({count})")
                        sizes.append(count)
                        
                        # Color mapping
                        color_map = {
                            "Critical": "#d32f2f",
                            "High": "#f57c00", 
                            "Medium": "#fbc02d",
                            "Low": "#388e3c",
                            "Info": "#1976d2"
                        }
                        colors_list.append(color_map.get(severity, "#666666"))
                
                if sizes:
                    ax.pie(sizes, labels=labels, colors=colors_list, autopct='%1.1f%%', startangle=90)
                    ax.set_title("Vulnerability Distribution by Severity", fontsize=14, fontweight='bold')
                else:
                    ax.text(0.5, 0.5, 'No vulnerabilities found', ha='center', va='center', 
                           transform=ax.transAxes, fontsize=12)
                    ax.set_title("Vulnerability Distribution by Severity", fontsize=14, fontweight='bold')
            
            elif chart_type == "tools":
                # Tool findings bar chart
                tools = list(self.tool_stats.keys())[:10]  # Top 10 tools
                counts = [self.tool_stats[tool] for tool in tools]
                
                if tools and counts:
                    bars = ax.bar(tools, counts, color='#1976d2', alpha=0.7)
                    ax.set_title("Findings by Tool", fontsize=14, fontweight='bold')
                    ax.set_xlabel("Tools")
                    ax.set_ylabel("Number of Findings")
                    plt.xticks(rotation=45, ha='right')
                    
                    # Add value labels on bars
                    for bar, count in zip(bars, counts):
                        if count > 0:
                            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                                   str(count), ha='center', va='bottom')
                else:
                    ax.text(0.5, 0.5, 'No findings to display', ha='center', va='center',
                           transform=ax.transAxes, fontsize=12)
                    ax.set_title("Findings by Tool", fontsize=14, fontweight='bold')
            
            plt.tight_layout()
            
            # Save to BytesIO
            img_buffer = BytesIO()
            plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
            img_buffer.seek(0)
            plt.close()
            
            return img_buffer
            
        except Exception as e:
            print(f"❌ Error creating chart: {e}")
            return None
    
    def generate_report(self):
        """Generate the complete PDF report"""
        if not REPORTLAB_AVAILABLE:
            print("❌ ReportLab not available. Installing required packages...")
            try:
                import subprocess
                subprocess.check_call(["pip", "install", "reportlab", "matplotlib"])
                print("✅ Packages installed. Please restart the script.")
                return False
            except:
                print("❌ Failed to install packages. Please install manually: pip install reportlab matplotlib")
                return False
        
        try:
            # Create PDF document
            doc = SimpleDocTemplate(self.output_file, pagesize=A4)
            
            # Build report content
            self._add_title_page()
            self._add_executive_summary()
            self._add_methodology()
            self._add_findings_summary()
            self._add_detailed_findings()
            self._add_recommendations()
            self._add_appendix()
            
            # Build PDF
            doc.build(self.story)
            print(f"✅ PDF report generated: {self.output_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error generating PDF report: {e}")
            return False
    
    def _add_title_page(self):
        """Add title page to the report"""
        # Title
        title = Paragraph("Penetration Testing Report", self.styles['CustomTitle'])
        self.story.append(title)
        self.story.append(Spacer(1, 0.5*inch))
        
        # Target information
        target_info = [
            ["Target:", "OWASP Juice Shop Application"],
            ["Date:", datetime.datetime.now().strftime("%B %d, %Y")],
            ["Report Type:", "Automated Penetration Testing"],
            ["Classification:", "Confidential"]
        ]
        
        table = Table(target_info, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey)
        ]))
        
        self.story.append(table)
        self.story.append(PageBreak())
    
    def _add_executive_summary(self):
        """Add executive summary section"""
        self.story.append(Paragraph("Executive Summary", self.styles['CustomHeading']))
        
        # Summary statistics
        total_vulns = sum(self.vulnerability_stats.values())
        critical_high = self.vulnerability_stats['Critical'] + self.vulnerability_stats['High']
        
        summary_text = f"""
        This penetration testing report presents the results of an automated security assessment 
        conducted against the OWASP Juice Shop application. The assessment identified 
        <strong>{total_vulns}</strong> total findings, including <strong>{critical_high}</strong> 
        critical and high-severity vulnerabilities that require immediate attention.
        
        The testing utilized multiple security tools and techniques to comprehensively evaluate 
        the application's security posture across various attack vectors including injection 
        attacks, authentication bypass, and configuration issues.
        """
        
        self.story.append(Paragraph(summary_text, self.styles['Normal']))
        self.story.append(Spacer(1, 0.3*inch))
        
        # Add severity chart if available
        chart_img = self.create_chart_image("severity")
        if chart_img:
            img = Image(chart_img, width=5*inch, height=3*inch)
            self.story.append(img)
        
        self.story.append(PageBreak())
    
    def _add_methodology(self):
        """Add methodology section"""
        self.story.append(Paragraph("Testing Methodology", self.styles['CustomHeading']))
        
        methodology_text = """
        The penetration testing was conducted using an automated framework that implements 
        industry-standard security testing tools and techniques:
        
        <strong>1. Reconnaissance Phase:</strong><br/>
        • Network discovery and port scanning (Nmap)<br/>
        • Subdomain enumeration (Amass)<br/>
        • Technology fingerprinting<br/>
        
        <strong>2. Vulnerability Assessment:</strong><br/>
        • Web application scanning (Nikto, Nuclei)<br/>
        • OWASP ZAP automated scanning<br/>
        • Custom vulnerability detection<br/>
        
        <strong>3. Exploitation Phase:</strong><br/>
        • SQL injection testing (SQLMap)<br/>
        • Authentication attacks (Hydra)<br/>
        • Directory traversal and file inclusion<br/>
        
        <strong>4. Analysis and Reporting:</strong><br/>
        • Results correlation and validation<br/>
        • Risk assessment and prioritization<br/>
        • Detailed finding documentation<br/>
        """
        
        self.story.append(Paragraph(methodology_text, self.styles['Normal']))
        self.story.append(PageBreak())
    
    def _add_findings_summary(self):
        """Add findings summary with charts"""
        self.story.append(Paragraph("Findings Summary", self.styles['CustomHeading']))
        
        # Summary table
        summary_data = [
            ["Severity", "Count", "Percentage"],
            ["Critical", str(self.vulnerability_stats['Critical']), f"{self._get_percentage('Critical'):.1f}%"],
            ["High", str(self.vulnerability_stats['High']), f"{self._get_percentage('High'):.1f}%"],
            ["Medium", str(self.vulnerability_stats['Medium']), f"{self._get_percentage('Medium'):.1f}%"],
            ["Low", str(self.vulnerability_stats['Low']), f"{self._get_percentage('Low'):.1f}%"],
            ["Info", str(self.vulnerability_stats['Info']), f"{self._get_percentage('Info'):.1f}%"]
        ]
        
        table = Table(summary_data, colWidths=[2*inch, 1*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#ffcdd2')),  # Critical - red
            ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#ffe0b2')),  # High - orange
            ('BACKGROUND', (0, 3), (-1, 3), colors.HexColor('#fff9c4')),  # Medium - yellow
            ('BACKGROUND', (0, 4), (-1, 4), colors.HexColor('#dcedc8')),  # Low - green
            ('BACKGROUND', (0, 5), (-1, 5), colors.HexColor('#e1f5fe'))   # Info - blue
        ]))
        
        self.story.append(table)
        self.story.append(Spacer(1, 0.3*inch))
        
        # Add tool findings chart
        chart_img = self.create_chart_image("tools")
        if chart_img:
            img = Image(chart_img, width=6*inch, height=4*inch)
            self.story.append(img)
        
        self.story.append(PageBreak())
    
    def _get_percentage(self, severity):
        """Calculate percentage for a severity level"""
        total = sum(self.vulnerability_stats.values())
        if total == 0:
            return 0
        return (self.vulnerability_stats[severity] / total) * 100
    
    def _add_detailed_findings(self):
        """Add detailed findings section"""
        self.story.append(Paragraph("Detailed Findings", self.styles['CustomHeading']))
        
        # Sort findings by severity
        severity_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3, "Info": 4}
        sorted_findings = sorted(self.findings, key=lambda x: severity_order.get(x.get('severity', 'Medium'), 2))
        
        for i, finding in enumerate(sorted_findings[:20], 1):  # Limit to top 20 findings
            self._add_finding_detail(i, finding)
        
        if len(self.findings) > 20:
            self.story.append(Paragraph(f"<i>Note: Showing top 20 findings. Total findings: {len(self.findings)}</i>", 
                                      self.styles['Normal']))
    
    def _add_finding_detail(self, finding_number, finding):
        """Add detail for a single finding"""
        # Finding header
        severity = finding.get('severity', 'Medium')
        title = finding.get('title', 'Unknown Vulnerability')
        
        header = f"Finding #{finding_number}: {title}"
        style_name = f"{severity}Risk" if f"{severity}Risk" in self.styles else 'Normal'
        
        self.story.append(Paragraph(header, self.styles.get(style_name, self.styles['Normal'])))
        self.story.append(Spacer(1, 0.1*inch))
        
        # Finding details table
        details = [
            ["Severity:", severity],
            ["Tool:", finding.get('tool', 'Unknown')],
            ["Location:", finding.get('location', 'Unknown')],
            ["CVSS Score:", str(finding.get('cvss', 'N/A'))],
            ["CWE ID:", finding.get('cwe', 'N/A')]
        ]
        
        table = Table(details, colWidths=[1.5*inch, 4*inch])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        
        self.story.append(table)
        self.story.append(Spacer(1, 0.1*inch))
        
        # Description
        if finding.get('description'):
            self.story.append(Paragraph(f"<strong>Description:</strong> {finding['description']}", 
                                      self.styles['Normal']))
        
        # Impact
        if finding.get('impact'):
            self.story.append(Paragraph(f"<strong>Impact:</strong> {finding['impact']}", 
                                      self.styles['Normal']))
        
        # Recommendation
        if finding.get('recommendation'):
            self.story.append(Paragraph(f"<strong>Recommendation:</strong> {finding['recommendation']}", 
                                      self.styles['Normal']))
        
        self.story.append(Spacer(1, 0.2*inch))
    
    def _add_recommendations(self):
        """Add recommendations section"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("Security Recommendations", self.styles['CustomHeading']))
        
        recommendations = [
            {
                "priority": "Critical",
                "title": "Address Critical and High Severity Vulnerabilities",
                "description": "Immediately remediate all critical and high-severity findings to prevent potential exploitation."
            },
            {
                "priority": "High", 
                "title": "Implement Input Validation",
                "description": "Establish comprehensive input validation and sanitization for all user inputs to prevent injection attacks."
            },
            {
                "priority": "High",
                "title": "Strengthen Authentication",
                "description": "Implement strong password policies, account lockout mechanisms, and multi-factor authentication."
            },
            {
                "priority": "Medium",
                "title": "Security Configuration Review",
                "description": "Review and harden security configurations for web servers, databases, and applications."
            },
            {
                "priority": "Medium",
                "title": "Regular Security Testing",
                "description": "Establish a regular penetration testing schedule to identify and address new vulnerabilities."
            }
        ]
        
        for rec in recommendations:
            self.story.append(Paragraph(f"<strong>{rec['title']}</strong> ({rec['priority']} Priority)", 
                                      self.styles['Heading2']))
            self.story.append(Paragraph(rec['description'], self.styles['Normal']))
            self.story.append(Spacer(1, 0.2*inch))
    
    def _add_appendix(self):
        """Add appendix with technical details"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("Appendix", self.styles['CustomHeading']))
        
        # Tool information
        self.story.append(Paragraph("A.1 Tools Used", self.styles['Heading2']))
        
        tools_info = """
        The following tools were utilized during the penetration testing engagement:
        
        • <strong>Nmap:</strong> Network discovery and port scanning<br/>
        • <strong>Nikto:</strong> Web server scanner<br/>
        • <strong>Nuclei:</strong> Fast vulnerability scanner<br/>
        • <strong>SQLMap:</strong> SQL injection detection and exploitation<br/>
        • <strong>Hydra:</strong> Login brute-forcer<br/>
        • <strong>OWASP ZAP:</strong> Web application security scanner<br/>
        • <strong>Custom Python Scripts:</strong> Additional security checks<br/>
        """
        
        self.story.append(Paragraph(tools_info, self.styles['Normal']))
        self.story.append(Spacer(1, 0.3*inch))
        
        # Disclaimer
        self.story.append(Paragraph("A.2 Disclaimer", self.styles['Heading2']))
        disclaimer = """
        This penetration testing report is based on automated scanning and analysis. Manual verification 
        of findings is recommended before taking remediation actions. The absence of vulnerabilities 
        in this report does not guarantee the complete security of the tested application.
        """
        
        self.story.append(Paragraph(disclaimer, self.styles['Normal']))

def main():
    """Main function for PDF report generation"""
    print("📊 PDF Report Generator")
    print("=" * 30)
    
    # Find results files
    results_files = []
    for results_dir in ["./results", "./crew_results", "."]:
        if Path(results_dir).exists():
            results_files.extend(Path(results_dir).glob("*.json"))
    
    if not results_files:
        print("❌ No results files found. Please run penetration tests first.")
        return False
    
    # Use the most recent results file
    latest_file = max(results_files, key=lambda f: f.stat().st_mtime)
    print(f"📁 Using results from: {latest_file}")
    
    # Generate PDF report
    report_name = f"pentest_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    report = PentestPDFReport(report_name)
    
    if report.load_results(latest_file):
        if report.generate_report():
            print(f"✅ PDF report generated successfully: {report_name}")
            print(f"📊 Report contains {len(report.findings)} detailed findings")
            return True
    
    return False

if __name__ == "__main__":
    main()
