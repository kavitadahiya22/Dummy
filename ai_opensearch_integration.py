#!/usr/bin/env python3
"""
Enhanced OpenSearch Integration for AI-Powered Penetration Testing
Specialized for AI analysis results and real-time dashboard updates
"""

import json
import datetime
import requests
import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class AIOpenSearchIntegration:
    def __init__(self, opensearch_url="http://opensearch:9200", 
                 dashboard_url="http://opensearch-dashboards:5601"):
        self.opensearch_url = opensearch_url
        self.dashboard_url = dashboard_url
        self.pentest_index = f"ai-pentest-results-{datetime.datetime.now().strftime('%Y-%m')}"
        self.insights_index = f"ai-insights-{datetime.datetime.now().strftime('%Y-%m')}"
        
    def create_ai_index_templates(self):
        """Create specialized index templates for AI-enhanced pentest results"""
        
        # Pentest results template
        pentest_template = {
            "index_patterns": ["ai-pentest-results-*"],
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
                        "ai_recommended": {"type": "boolean"},
                        "ai_priority": {"type": "integer"},
                        "vulnerability_type": {"type": "keyword"},
                        "severity": {"type": "keyword"},
                        "confidence_score": {"type": "float"},
                        "ai_analysis": {"type": "text"},
                        "findings_count": {"type": "integer"},
                        "status": {"type": "keyword"},
                        "execution_time": {"type": "float"},
                        "risk_score": {"type": "integer"},
                        "cvss_score": {"type": "float"},
                        "cwe_id": {"type": "keyword"},
                        "owasp_category": {"type": "keyword"},
                        "ai_model_used": {"type": "keyword"},
                        "remediation_priority": {"type": "keyword"}
                    }
                }
            }
        }
        
        # AI insights template
        insights_template = {
            "index_patterns": ["ai-insights-*"],
            "template": {
                "settings": {
                    "number_of_shards": 1,
                    "number_of_replicas": 0
                },
                "mappings": {
                    "properties": {
                        "timestamp": {"type": "date"},
                        "target_url": {"type": "keyword"},
                        "ai_model": {"type": "keyword"},
                        "insight_type": {"type": "keyword"},
                        "risk_assessment": {"type": "keyword"},
                        "confidence_level": {"type": "float"},
                        "vulnerability_predictions": {"type": "text"},
                        "remediation_suggestions": {"type": "text"},
                        "compliance_impact": {"type": "text"},
                        "business_risk": {"type": "keyword"},
                        "attack_complexity": {"type": "keyword"},
                        "exploitability": {"type": "keyword"}
                    }
                }
            }
        }
        
        # Create templates
        templates = [
            ("ai-pentest-template", pentest_template),
            ("ai-insights-template", insights_template)
        ]
        
        for template_name, template_data in templates:
            try:
                response = requests.put(
                    f"{self.opensearch_url}/_index_template/{template_name}",
                    json=template_data,
                    headers={"Content-Type": "application/json"}
                )
                if response.status_code in [200, 201]:
                    print(f"✅ {template_name} created successfully")
                else:
                    print(f"❌ Failed to create {template_name}: {response.text}")
            except Exception as e:
                print(f"❌ Error creating {template_name}: {e}")
    
    def index_ai_pentest_results(self, results_data):
        """Index AI-enhanced penetration testing results"""
        if not isinstance(results_data, dict):
            print("❌ Invalid results data format")
            return False
        
        metadata = results_data.get('metadata', {})
        test_results = results_data.get('test_results', {})
        ai_strategy = metadata.get('ai_strategy', {})
        ai_insights = metadata.get('ai_insights', {})
        
        # Index individual tool results
        self._index_tool_results(test_results, ai_strategy, metadata)
        
        # Index AI insights separately
        self._index_ai_insights(ai_insights, metadata)
        
        print(f"✅ AI pentest results indexed to OpenSearch")
        return True
    
    def _index_tool_results(self, test_results, ai_strategy, metadata):
        """Index individual tool results with AI context"""
        recommended_tools = ai_strategy.get('recommended_tools', [])
        
        documents = []
        for tool_name, result in test_results.items():
            doc = {
                "timestamp": datetime.datetime.now().isoformat(),
                "target_url": metadata.get('target_url'),
                "tool_name": tool_name,
                "ai_recommended": tool_name in recommended_tools,
                "ai_priority": recommended_tools.index(tool_name) + 1 if tool_name in recommended_tools else 999,
                "status": result.get('status', 'unknown'),
                "findings_count": result.get('findings_count', 0),
                "ai_model_used": self._get_ai_model_used(metadata),
                "execution_time": self._calculate_execution_time(result),
                "risk_score": self._calculate_risk_score(result, tool_name),
                "remediation_priority": self._get_remediation_priority(result, tool_name)
            }
            
            # Add vulnerability-specific fields
            vulnerabilities = self._extract_vulnerabilities_from_result(tool_name, result)
            for vuln in vulnerabilities:
                vuln_doc = doc.copy()
                vuln_doc.update(vuln)
                documents.append(vuln_doc)
            
            # If no specific vulnerabilities, add the general result
            if not vulnerabilities:
                documents.append(doc)
        
        # Bulk index
        self._bulk_index(self.pentest_index, documents)
    
    def _index_ai_insights(self, ai_insights, metadata):
        """Index AI analysis insights"""
        if not ai_insights:
            return
        
        insight_doc = {
            "timestamp": datetime.datetime.now().isoformat(),
            "target_url": metadata.get('target_url'),
            "ai_model": self._get_ai_model_used(metadata),
            "insight_type": "vulnerability_analysis",
            "risk_assessment": ai_insights.get('risk_assessment', 'unknown'),
            "confidence_level": 0.8,  # Default confidence
            "vulnerability_predictions": json.dumps(ai_insights.get('vulnerability_focus', [])),
            "remediation_suggestions": json.dumps(ai_insights.get('remediation_suggestions', [])),
            "business_risk": ai_insights.get('business_risk', 'medium'),
            "attack_complexity": ai_insights.get('attack_complexity', 'medium'),
            "exploitability": ai_insights.get('exploitability', 'medium')
        }
        
        # Index single insight document
        try:
            response = requests.post(
                f"{self.opensearch_url}/{self.insights_index}/_doc",
                json=insight_doc,
                headers={"Content-Type": "application/json"}
            )
            if response.status_code in [200, 201]:
                print(f"✅ AI insights indexed successfully")
        except Exception as e:
            print(f"❌ Error indexing AI insights: {e}")
    
    def _extract_vulnerabilities_from_result(self, tool_name, result):
        """Extract vulnerability details from tool results"""
        vulnerabilities = []
        
        if tool_name == "sqlmap":
            if result.get('findings_count', 0) > 0:
                vulnerabilities.append({
                    "vulnerability_type": "SQL Injection",
                    "severity": "High",
                    "confidence_score": 0.9,
                    "cvss_score": 7.5,
                    "cwe_id": "CWE-89",
                    "owasp_category": "A03:2021 – Injection"
                })
        
        elif tool_name == "nuclei":
            findings = result.get('findings_count', 0)
            if findings > 0:
                vulnerabilities.append({
                    "vulnerability_type": "Multiple Vulnerabilities",
                    "severity": self._assess_severity_by_findings(findings),
                    "confidence_score": 0.7,
                    "owasp_category": "A06:2021 – Vulnerable Components"
                })
        
        elif tool_name == "nikto":
            findings = result.get('findings_count', 0)
            if findings > 0:
                vulnerabilities.append({
                    "vulnerability_type": "Web Server Vulnerabilities",
                    "severity": "Medium",
                    "confidence_score": 0.6,
                    "owasp_category": "A05:2021 – Security Misconfiguration"
                })
        
        elif tool_name == "hydra":
            if result.get('findings_count', 0) > 0:
                vulnerabilities.append({
                    "vulnerability_type": "Weak Authentication",
                    "severity": "High",
                    "confidence_score": 0.8,
                    "cvss_score": 6.5,
                    "cwe_id": "CWE-287",
                    "owasp_category": "A07:2021 – Identification and Authentication Failures"
                })
        
        elif tool_name == "nmap":
            findings = result.get('findings_count', 0)
            if findings > 0:
                vulnerabilities.append({
                    "vulnerability_type": "Network Exposure",
                    "severity": "Low",
                    "confidence_score": 0.5,
                    "owasp_category": "A05:2021 – Security Misconfiguration"
                })
        
        return vulnerabilities
    
    def _assess_severity_by_findings(self, findings_count):
        """Assess severity based on number of findings"""
        if findings_count >= 10:
            return "Critical"
        elif findings_count >= 5:
            return "High"
        elif findings_count >= 2:
            return "Medium"
        else:
            return "Low"
    
    def _calculate_execution_time(self, result):
        """Calculate tool execution time"""
        # This would be enhanced with actual timing data
        status = result.get('status', 'unknown')
        if status == 'timeout':
            return 300.0  # 5 minutes timeout
        elif status == 'success':
            return 60.0   # Average successful execution
        else:
            return 0.0
    
    def _calculate_risk_score(self, result, tool_name):
        """Calculate risk score based on tool and findings"""
        findings = result.get('findings_count', 0)
        base_scores = {
            'sqlmap': 8,
            'hydra': 7,
            'nuclei': 6,
            'nikto': 5,
            'nmap': 3,
            'zap': 6
        }
        
        base_score = base_scores.get(tool_name, 4)
        return min(10, base_score + min(findings, 2))
    
    def _get_remediation_priority(self, result, tool_name):
        """Get remediation priority based on tool and results"""
        if result.get('findings_count', 0) == 0:
            return "low"
        
        high_priority_tools = ['sqlmap', 'hydra', 'metasploit']
        if tool_name in high_priority_tools:
            return "high"
        elif result.get('findings_count', 0) >= 5:
            return "medium"
        else:
            return "low"
    
    def _get_ai_model_used(self, metadata):
        """Extract which AI model was used"""
        ai_insights = metadata.get('ai_insights', {})
        if 'openai' in str(ai_insights).lower():
            return "OpenAI"
        elif 'deepseek' in str(ai_insights).lower():
            return "DeepSeek"
        else:
            return "Fallback"
    
    def _bulk_index(self, index_name, documents):
        """Bulk index documents to OpenSearch"""
        if not documents:
            return
        
        bulk_data = ""
        for doc in documents:
            action = {"index": {"_index": index_name}}
            bulk_data += json.dumps(action) + "\n"
            bulk_data += json.dumps(doc) + "\n"
        
        try:
            response = requests.post(
                f"{self.opensearch_url}/_bulk",
                data=bulk_data,
                headers={"Content-Type": "application/x-ndjson"}
            )
            
            if response.status_code == 200:
                print(f"✅ Bulk indexed {len(documents)} documents to {index_name}")
            else:
                print(f"❌ Bulk indexing failed: {response.text}")
        except Exception as e:
            print(f"❌ Error in bulk indexing: {e}")
    
    def create_ai_dashboards(self):
        """Create specialized dashboards for AI-enhanced results"""
        dashboard_configs = [
            {
                "id": "ai-pentest-overview",
                "title": "AI-Powered Penetration Testing Overview",
                "description": "Real-time dashboard for AI-enhanced penetration testing results"
            },
            {
                "id": "ai-insights-dashboard", 
                "title": "AI Security Insights",
                "description": "AI analysis and recommendations dashboard"
            },
            {
                "id": "vulnerability-risk-matrix",
                "title": "AI Risk Assessment Matrix",
                "description": "AI-driven vulnerability risk prioritization"
            }
        ]
        
        for config in dashboard_configs:
            self._create_dashboard(config)
    
    def _create_dashboard(self, config):
        """Create individual dashboard"""
        dashboard_data = {
            "version": "2.0.0",
            "objects": [
                {
                    "id": config["id"],
                    "type": "dashboard",
                    "attributes": {
                        "title": config["title"],
                        "description": config["description"],
                        "panelsJSON": json.dumps([])  # Empty panels for now
                    }
                }
            ]
        }
        
        try:
            response = requests.post(
                f"{self.dashboard_url}/api/saved_objects/_import",
                json=dashboard_data,
                headers={"Content-Type": "application/json", "osd-xsrf": "true"}
            )
            
            if response.status_code == 200:
                print(f"✅ Dashboard '{config['title']}' created")
            else:
                print(f"❌ Failed to create dashboard: {response.text}")
        except Exception as e:
            print(f"❌ Error creating dashboard: {e}")
    
    def get_dashboard_urls(self):
        """Get URLs for accessing the AI dashboards"""
        return {
            "main_dashboard": f"{self.dashboard_url}/app/dashboards#/view/ai-pentest-overview",
            "insights_dashboard": f"{self.dashboard_url}/app/dashboards#/view/ai-insights-dashboard",
            "risk_matrix": f"{self.dashboard_url}/app/dashboards#/view/vulnerability-risk-matrix"
        }

def main():
    """Main function for AI OpenSearch integration"""
    print("🤖 AI-Enhanced OpenSearch Integration")
    print("=" * 50)
    
    # Initialize AI OpenSearch integration
    ai_opensearch = AIOpenSearchIntegration()
    
    # Create AI-specific index templates
    ai_opensearch.create_ai_index_templates()
    
    # Check for AI results files
    results_files = []
    for results_dir in ["./results", "./crew_results", "."]:
        if Path(results_dir).exists():
            results_files.extend(Path(results_dir).glob("ai_pentest_results_*.json"))
    
    if not results_files:
        # Look for any recent results files
        for results_dir in ["./results", "./crew_results", "."]:
            if Path(results_dir).exists():
                results_files.extend(Path(results_dir).glob("*results*.json"))
    
    # Process the most recent results
    if results_files:
        latest_file = max(results_files, key=lambda f: f.stat().st_mtime)
        print(f"📊 Processing AI results from: {latest_file}")
        
        try:
            with open(latest_file, 'r') as f:
                results_data = json.load(f)
            
            ai_opensearch.index_ai_pentest_results(results_data)
        except Exception as e:
            print(f"❌ Error processing results file: {e}")
    else:
        print("⚠️ No AI pentest results files found")
    
    # Create AI-specific dashboards
    ai_opensearch.create_ai_dashboards()
    
    # Print dashboard URLs
    dashboard_urls = ai_opensearch.get_dashboard_urls()
    print(f"\n🎯 AI Dashboard URLs:")
    for name, url in dashboard_urls.items():
        print(f"  • {name}: {url}")

if __name__ == "__main__":
    main()
