#!/usr/bin/env python3
"""
Local OpenSearch Integration for Penetration Testing Results
Upload pentest results to local OpenSearch instance
"""

import json
import datetime
import requests
import os
import sys

class LocalOpenSearchIntegration:
    def __init__(self):
        self.opensearch_url = 'http://localhost:9200'
        self.dashboard_url = 'http://localhost:5601'
        self.index_name = f'pentest-results-{datetime.datetime.now().strftime("%Y-%m")}'
        
    def create_index_template(self):
        """Create OpenSearch index template for pentest results"""
        template = {
            'index_patterns': ['pentest-results-*'],
            'template': {
                'settings': {
                    'number_of_shards': 1,
                    'number_of_replicas': 0
                },
                'mappings': {
                    'properties': {
                        'timestamp': {'type': 'date'},
                        'target_url': {'type': 'keyword'},
                        'tool_name': {'type': 'keyword'},
                        'vulnerability_type': {'type': 'keyword'},
                        'severity': {'type': 'keyword'},
                        'description': {'type': 'text'},
                        'status': {'type': 'keyword'},
                        'risk_score': {'type': 'integer'},
                        'execution_time': {'type': 'float'},
                        'findings': {'type': 'text'}
                    }
                }
            }
        }
        
        try:
            response = requests.put(
                f'{self.opensearch_url}/_index_template/pentest-template',
                json=template,
                headers={'Content-Type': 'application/json'}
            )
            print(f'✅ Index template creation: {response.status_code}')
            return True
        except Exception as e:
            print(f'❌ Error creating template: {e}')
            return False
    
    def upload_results(self, results_file):
        """Upload penetration test results to OpenSearch"""
        try:
            with open(results_file, 'r') as f:
                results = json.load(f)
            
            documents = []
            for tool_name, tool_results in results.items():
                if isinstance(tool_results, dict):
                    # Extract meaningful data from each tool
                    severity = self._determine_severity(tool_name, tool_results)
                    risk_score = self._calculate_risk_score(severity)
                    
                    doc = {
                        'timestamp': datetime.datetime.now().isoformat(),
                        'tool_name': tool_name,
                        'target_url': 'http://localhost:3000',
                        'vulnerability_type': tool_name.replace('_', ' ').title(),
                        'severity': severity,
                        'description': f'Security assessment results from {tool_name}',
                        'status': 'completed',
                        'risk_score': risk_score,
                        'execution_time': tool_results.get('execution_time', 0),
                        'findings': json.dumps(tool_results, indent=2)[:2000]  # Truncate for indexing
                    }
                    documents.append(doc)
            
            # Bulk index documents
            if documents:
                bulk_data = ''
                for doc in documents:
                    action = {'index': {'_index': self.index_name}}
                    bulk_data += json.dumps(action) + '\n'
                    bulk_data += json.dumps(doc) + '\n'
                
                response = requests.post(
                    f'{self.opensearch_url}/_bulk',
                    data=bulk_data,
                    headers={'Content-Type': 'application/x-ndjson'}
                )
                
                print(f'📊 Bulk index response: {response.status_code}')
                if response.status_code == 200:
                    print(f'✅ Successfully indexed {len(documents)} documents')
                    print(f'📈 Index name: {self.index_name}')
                    return True
                else:
                    print(f'❌ Bulk indexing failed: {response.text}')
                    return False
        except Exception as e:
            print(f'❌ Error uploading results: {e}')
            return False
    
    def _determine_severity(self, tool_name, results):
        """Determine severity based on tool and results"""
        high_risk_tools = ['sqlmap', 'metasploit', 'hydra']
        medium_risk_tools = ['nikto', 'nuclei', 'zap']
        
        if tool_name in high_risk_tools:
            return 'High'
        elif tool_name in medium_risk_tools:
            return 'Medium'
        else:
            return 'Low'
    
    def _calculate_risk_score(self, severity):
        """Calculate risk score based on severity"""
        severity_scores = {
            'Critical': 10,
            'High': 8,
            'Medium': 5,
            'Low': 2,
            'Info': 1
        }
        return severity_scores.get(severity, 3)

def main():
    """Main function to upload pentest results"""
    results_file = 'pentest_results/pentest_report_20250816_234904.json'
    
    print("🚀 Local OpenSearch Integration for Penetration Testing")
    print("=" * 60)
    
    integration = LocalOpenSearchIntegration()
    
    print('📋 Creating index template...')
    integration.create_index_template()
    
    print('📤 Uploading penetration test results...')
    success = integration.upload_results(results_file)
    
    if success:
        print('\n🎉 Upload completed successfully!')
        print(f'🌐 OpenSearch Dashboard: {integration.dashboard_url}')
        print(f'📊 Index name: {integration.index_name}')
        print('\n📈 To view your data:')
        print(f'   1. Open: {integration.dashboard_url}')
        print('   2. Go to "Discover" tab')
        print('   3. Create index pattern: pentest-results-*')
        print('   4. Create visualizations and dashboards')
    else:
        print('❌ Upload failed. Please check OpenSearch connectivity.')

if __name__ == '__main__':
    main()
