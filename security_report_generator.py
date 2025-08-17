#!/usr/bin/env python3
"""
Professional Security Report Generator
Creates comprehensive PDF reports from penetration test results
"""

import json
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import datetime
from collections import Counter
import os

class SecurityReportGenerator:
    def __init__(self, opensearch_url="http://localhost:9200"):
        self.opensearch_url = opensearch_url
        self.index_name = "pentest-results-2025-08"
        
    def fetch_data(self):
        """Fetch all data from OpenSearch"""
        try:
            query = {
                "query": {"match_all": {}},
                "size": 1000
            }
            
            response = requests.post(
                f"{self.opensearch_url}/{self.index_name}/_search",
                json=query,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                vulnerabilities = [hit["_source"] for hit in data["hits"]["hits"]]
                print(f"✅ Fetched {len(vulnerabilities)} vulnerability records")
                return vulnerabilities
            else:
                print(f"❌ Failed to fetch data: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Error fetching data: {e}")
            return []
    
    def create_visualizations(self, data):
        """Create professional security visualizations"""
        if not data:
            print("❌ No data available for visualizations")
            return
        
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        # Set up the plotting style
        plt.style.use('seaborn-v0_8')
        sns.set_palette("viridis")
        
        # Create a comprehensive report with multiple subplots
        fig = plt.figure(figsize=(20, 24))
        
        # 1. Severity Distribution (Pie Chart)
        plt.subplot(4, 2, 1)
        severity_counts = df['severity'].value_counts()
        colors = ['#FF6B6B', '#FF8E53', '#FF6B9D', '#4ECDC4', '#45B7D1']
        plt.pie(severity_counts.values, labels=severity_counts.index, autopct='%1.1f%%', 
                colors=colors, startangle=90)
        plt.title('🔥 Vulnerability Severity Distribution', fontsize=14, fontweight='bold')
        
        # 2. Tools Performance (Bar Chart)
        plt.subplot(4, 2, 2)
        tool_counts = df['tool_name'].value_counts()
        bars = plt.bar(tool_counts.index, tool_counts.values, color='skyblue', alpha=0.8)
        plt.title('🛠️ Security Tools Performance', fontsize=14, fontweight='bold')
        plt.xlabel('Security Tools')
        plt.ylabel('Vulnerabilities Found')
        plt.xticks(rotation=45)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{int(height)}', ha='center', va='bottom')
        
        # 3. Risk Score Distribution (Histogram)
        plt.subplot(4, 2, 3)
        plt.hist(df['risk_score'], bins=10, color='coral', alpha=0.7, edgecolor='black')
        plt.title('📊 Risk Score Distribution', fontsize=14, fontweight='bold')
        plt.xlabel('Risk Score')
        plt.ylabel('Number of Vulnerabilities')
        plt.grid(True, alpha=0.3)
        
        # 4. CVSS Score Distribution (Histogram)
        plt.subplot(4, 2, 4)
        plt.hist(df['cvss_score'], bins=10, color='lightgreen', alpha=0.7, edgecolor='black')
        plt.title('🎯 CVSS Score Distribution', fontsize=14, fontweight='bold')
        plt.xlabel('CVSS Score')
        plt.ylabel('Number of Vulnerabilities')
        plt.grid(True, alpha=0.3)
        
        # 5. Vulnerability Types (Horizontal Bar Chart)
        plt.subplot(4, 2, 5)
        vuln_types = df['vulnerability_type'].value_counts().head(10)
        plt.barh(range(len(vuln_types)), vuln_types.values, color='lightpink')
        plt.yticks(range(len(vuln_types)), vuln_types.index)
        plt.title('🔍 Top 10 Vulnerability Types', fontsize=14, fontweight='bold')
        plt.xlabel('Count')
        
        # 6. OWASP Categories (Pie Chart)
        plt.subplot(4, 2, 6)
        owasp_counts = df['owasp_category'].value_counts()
        plt.pie(owasp_counts.values, labels=owasp_counts.index, autopct='%1.1f%%', 
                startangle=90)
        plt.title('🎯 OWASP Top 10 Distribution', fontsize=14, fontweight='bold')
        
        # 7. Risk vs CVSS Correlation (Scatter Plot)
        plt.subplot(4, 2, 7)
        scatter = plt.scatter(df['cvss_score'], df['risk_score'], 
                            c=df['severity'].astype('category').cat.codes, 
                            alpha=0.6, s=50, cmap='viridis')
        plt.xlabel('CVSS Score')
        plt.ylabel('Risk Score')
        plt.title('📈 Risk Score vs CVSS Score Correlation', fontsize=14, fontweight='bold')
        plt.colorbar(scatter, label='Severity')
        plt.grid(True, alpha=0.3)
        
        # 8. Status Overview (Pie Chart)
        plt.subplot(4, 2, 8)
        status_counts = df['status'].value_counts()
        plt.pie(status_counts.values, labels=status_counts.index, autopct='%1.1f%%', 
                startangle=90, colors=['lightblue', 'orange', 'lightcoral'])
        plt.title('📋 Testing Status Overview', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        
        # Save the comprehensive report
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'security_report_{timestamp}.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"✅ Comprehensive security report saved: {filename}")
        
        # Create executive summary
        self.create_executive_summary(df, timestamp)
        
        plt.show()
        
    def create_executive_summary(self, df, timestamp):
        """Create executive summary report"""
        summary = f"""
🔒 PENETRATION TESTING EXECUTIVE SUMMARY
Generated: {datetime.datetime.now().strftime('%B %d, %Y at %H:%M')}
========================================================

📊 OVERALL SECURITY POSTURE
• Total Vulnerabilities Found: {len(df)}
• Critical/High Risk Issues: {len(df[df['severity'].isin(['Critical', 'High'])])}
• Average CVSS Score: {df['cvss_score'].mean():.1f}/10.0
• Average Risk Score: {df['risk_score'].mean():.1f}/10.0

🎯 SEVERITY BREAKDOWN
{df['severity'].value_counts().to_string()}

🛠️ MOST EFFECTIVE SECURITY TOOLS
{df['tool_name'].value_counts().head(5).to_string()}

🔥 TOP VULNERABILITY TYPES
{df['vulnerability_type'].value_counts().head(5).to_string()}

📈 OWASP TOP 10 COVERAGE
{df['owasp_category'].value_counts().to_string()}

⚠️ IMMEDIATE ACTION REQUIRED
• Critical Issues: {len(df[df['severity'] == 'Critical'])}
• High Risk Issues: {len(df[df['severity'] == 'High'])}
• Items Needing Immediate Attention: {len(df[df['risk_score'] >= 8])}

🎯 RECOMMENDATIONS
1. Prioritize fixing Critical and High severity vulnerabilities
2. Focus on OWASP Top 10 categories with highest counts
3. Implement security controls for most common vulnerability types
4. Regular penetration testing to track improvement
5. Security awareness training for development teams

📊 DASHBOARD ACCESS
• OpenSearch Dashboard: http://localhost:5601
• Index Pattern: pentest-results-*
• Real-time monitoring available

Generated by: Automated Security Analysis System
Report ID: SEC_REPORT_{timestamp}
"""
        
        summary_filename = f'executive_summary_{timestamp}.txt'
        with open(summary_filename, 'w') as f:
            f.write(summary)
        
        print(f"✅ Executive summary saved: {summary_filename}")
        print(summary)

def main():
    """Main function to generate comprehensive security report"""
    print("🚀 Professional Security Report Generator")
    print("=" * 50)
    
    generator = SecurityReportGenerator()
    
    print("📥 Fetching penetration test data from OpenSearch...")
    data = generator.fetch_data()
    
    if data:
        print("📊 Generating professional visualizations...")
        generator.create_visualizations(data)
        print("\n🎉 Professional security report generation completed!")
        print("📈 Files generated:")
        print("   • security_report_[timestamp].png - Visual report")
        print("   • executive_summary_[timestamp].txt - Executive summary")
    else:
        print("❌ No data found. Please ensure OpenSearch contains vulnerability data.")

if __name__ == "__main__":
    main()
