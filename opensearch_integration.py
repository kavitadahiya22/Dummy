#!/usr/bin/env python3
"""
OpenSearch Dashboard Integration for Penetration Testing Results
Real-time dashboard for monitoring and visualizing security test results
"""

import json
import datetime
import requests
import os
from pathlib import Path

class OpenSearchIntegration:
    def __init__(self, opensearch_url="http://opensearch:9200", 
                 dashboard_url="http://opensearch-dashboards:5601"):
        self.opensearch_url = opensearch_url
        self.dashboard_url = dashboard_url
        self.index_name = f"pentest-results-{datetime.datetime.now().strftime('%Y-%m')}"
        
    def create_index_template(self):
        """Create OpenSearch index template for pentest results"""
        template = {
            "index_patterns": ["pentest-results-*"],
            "template": {
                "settings": {
                    "number_of_shards": 1,
                    "number_of_replicas": 0
                },
                "mappings": {
                    "properties": {
                        "timestamp": {"type": "date"},
                        "target_url": {"type": "keyword"},
                        "tool_name": {"type": "keyword"},
                        "test_phase": {"type": "keyword"},
                        "vulnerability_type": {"type": "keyword"},
                        "severity": {"type": "keyword"},
                        "status": {"type": "keyword"},
                        "description": {"type": "text"},
                        "location": {"type": "keyword"},
                        "risk_score": {"type": "integer"},
                        "evidence": {"type": "text"},
                        "recommendation": {"type": "text"},
                        "cvss_score": {"type": "float"},
                        "cwe_id": {"type": "keyword"},
                        "owasp_category": {"type": "keyword"}
                    }
                }
            }
        }
        
        try:
            response = requests.put(
                f"{self.opensearch_url}/_index_template/pentest-template",
                json=template,
                headers={"Content-Type": "application/json"}
            )
            if response.status_code in [200, 201]:
                print("✅ OpenSearch index template created successfully")
                return True
            else:
                print(f"❌ Failed to create index template: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Error creating index template: {e}")
            return False
    
    def index_vulnerability(self, vuln_data):
        """Index a vulnerability finding to OpenSearch"""
        document = {
            "timestamp": datetime.datetime.now().isoformat(),
            **vuln_data
        }
        
        try:
            response = requests.post(
                f"{self.opensearch_url}/{self.index_name}/_doc",
                json=document,
                headers={"Content-Type": "application/json"}
            )
            if response.status_code in [200, 201]:
                return True
            else:
                print(f"❌ Failed to index vulnerability: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Error indexing vulnerability: {e}")
            return False
    
    def bulk_index_results(self, results_file):
        """Bulk index results from JSON file"""
        try:
            with open(results_file, 'r') as f:
                results = json.load(f)
            
            # Convert results to OpenSearch documents
            documents = []
            for tool_name, tool_results in results.items():
                if isinstance(tool_results, dict):
                    self._process_tool_results(tool_name, tool_results, documents)
            
            # Bulk index documents
            if documents:
                bulk_data = ""
                for doc in documents:
                    action = {"index": {"_index": self.index_name}}
                    bulk_data += json.dumps(action) + "\n"
                    bulk_data += json.dumps(doc) + "\n"
                
                response = requests.post(
                    f"{self.opensearch_url}/_bulk",
                    data=bulk_data,
                    headers={"Content-Type": "application/x-ndjson"}
                )
                
                if response.status_code == 200:
                    print(f"✅ Successfully indexed {len(documents)} documents")
                    return True
                else:
                    print(f"❌ Bulk indexing failed: {response.text}")
                    return False
            
        except Exception as e:
            print(f"❌ Error in bulk indexing: {e}")
            return False
    
    def _process_tool_results(self, tool_name, tool_results, documents):
        """Process individual tool results and extract vulnerabilities"""
        # Map tool results to standardized vulnerability format
        vulnerabilities = self._extract_vulnerabilities(tool_name, tool_results)
        
        for vuln in vulnerabilities:
            doc = {
                "timestamp": datetime.datetime.now().isoformat(),
                "tool_name": tool_name,
                "test_phase": self._get_test_phase(tool_name),
                **vuln
            }
            documents.append(doc)
    
    def _extract_vulnerabilities(self, tool_name, results):
        """Extract vulnerabilities from tool-specific results"""
        vulnerabilities = []
        
        if tool_name == "sqlmap":
            # Extract SQL injection findings
            if "sql_injection_points" in results:
                for point in results.get("sql_injection_points", []):
                    vulnerabilities.append({
                        "vulnerability_type": "SQL Injection",
                        "severity": "High",
                        "location": point,
                        "risk_score": 8,
                        "cvss_score": 7.5,
                        "cwe_id": "CWE-89",
                        "owasp_category": "A03:2021 – Injection",
                        "description": f"SQL injection vulnerability found at {point}",
                        "recommendation": "Use parameterized queries and input validation"
                    })
        
        elif tool_name == "nuclei" or tool_name == "vulnerability":
            # Extract nuclei/general vulnerability findings
            if "vulnerabilities" in results:
                for vuln in results.get("vulnerabilities", []):
                    vulnerabilities.append({
                        "vulnerability_type": vuln.get("type", "Unknown"),
                        "severity": vuln.get("severity", "Medium"),
                        "location": vuln.get("location", "Unknown"),
                        "risk_score": self._severity_to_score(vuln.get("severity", "Medium")),
                        "description": vuln.get("description", "Vulnerability detected"),
                        "recommendation": "Review and remediate the identified vulnerability"
                    })
        
        elif tool_name == "hydra" or tool_name == "exploitation":
            # Extract authentication vulnerabilities
            if "valid_credentials" in results:
                for cred in results.get("valid_credentials", []):
                    vulnerabilities.append({
                        "vulnerability_type": "Weak Authentication",
                        "severity": "High",
                        "location": "/login",
                        "risk_score": 7,
                        "cvss_score": 6.5,
                        "cwe_id": "CWE-287",
                        "owasp_category": "A07:2021 – Identification and Authentication Failures",
                        "description": f"Weak credentials found: {cred}",
                        "evidence": cred,
                        "recommendation": "Implement strong password policies and multi-factor authentication"
                    })
        
        return vulnerabilities
    
    def _get_test_phase(self, tool_name):
        """Map tool name to test phase"""
        phase_mapping = {
            "nmap": "Reconnaissance",
            "amass": "Reconnaissance", 
            "nikto": "Vulnerability Assessment",
            "nuclei": "Vulnerability Assessment",
            "zap": "Vulnerability Assessment",
            "sqlmap": "Exploitation",
            "hydra": "Exploitation",
            "metasploit": "Exploitation",
            "bloodhound": "Post-Exploitation",
            "crackmapexec": "Post-Exploitation"
        }
        return phase_mapping.get(tool_name, "Unknown")
    
    def _severity_to_score(self, severity):
        """Convert severity to numeric risk score"""
        severity_scores = {
            "Critical": 10,
            "High": 8,
            "Medium": 5,
            "Low": 2,
            "Info": 1
        }
        return severity_scores.get(severity, 5)
    
    def create_dashboard(self):
        """Create OpenSearch Dashboard for pentest results"""
        dashboard_config = {
            "version": "2.0.0",
            "objects": [
                {
                    "id": "pentest-overview",
                    "type": "dashboard",
                    "attributes": {
                        "title": "Penetration Testing Overview",
                        "description": "Real-time dashboard for penetration testing results",
                        "panelsJSON": json.dumps([
                            {
                                "gridData": {"x": 0, "y": 0, "w": 24, "h": 15},
                                "panelIndex": "1",
                                "embeddableConfig": {},
                                "panelRefName": "panel_1"
                            }
                        ])
                    }
                }
            ]
        }
        
        try:
            response = requests.post(
                f"{self.dashboard_url}/api/saved_objects/_import",
                json=dashboard_config,
                headers={"Content-Type": "application/json", "osd-xsrf": "true"}
            )
            
            if response.status_code == 200:
                print("✅ Dashboard created successfully")
                return True
            else:
                print(f"❌ Failed to create dashboard: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error creating dashboard: {e}")
            return False
    
    def get_dashboard_url(self):
        """Get the URL to access the dashboard"""
        return f"{self.dashboard_url}/app/dashboards#/view/pentest-overview"

def main():
    """Main function for OpenSearch integration"""
    print("🔍 OpenSearch Dashboard Integration")
    print("=" * 40)
    
    # Initialize OpenSearch integration
    opensearch = OpenSearchIntegration()
    
    # Create index template
    opensearch.create_index_template()
    
    # Check for results files to index
    results_dir = Path("./results") if Path("./results").exists() else Path("./crew_results")
    
    if results_dir.exists():
        for result_file in results_dir.glob("*.json"):
            print(f"📊 Indexing results from {result_file}")
            opensearch.bulk_index_results(result_file)
    
    # Create dashboard
    opensearch.create_dashboard()
    
    print(f"\n🎯 Dashboard URL: {opensearch.get_dashboard_url()}")
    print("🔍 Access your real-time penetration testing dashboard!")

if __name__ == "__main__":
    main()
