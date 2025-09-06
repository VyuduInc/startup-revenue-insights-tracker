import modal

app = modal.App("startup-revenue-tracker")

image = modal.Image.debian_slim().pip_install(
    "streamlit==1.49.1",
    "pandas==2.3.2", 
    "numpy==2.3.2",
    "plotly==6.3.0"
)

@app.function(image=image)
def run():
    """Main function to run the startup revenue insights tracker"""
    import subprocess
    import os
    import time
    
    # Get the dashboard code
    dashboard_code = '''
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Professional Light Theme - Maximum Readability with Blue Primary
st.markdown("""
<style>
/* Professional Light Color Palette - High Readability */
:root {
    --primary-blue: #1e40af;
    --primary-blue-light: #3b82f6;
    --success-green: #059669;
    --success-green-light: #10b981;
    --warning-amber: #d97706;
    --danger-red: #dc2626;
    
    /* Light backgrounds */
    --bg-white: #ffffff;
    --bg-gray-50: #f9fafb;
    --bg-gray-100: #f3f4f6;
    --bg-blue-50: #eff6ff;
    --bg-green-50: #ecfdf5;
    
    /* Dark text colors */
    --text-primary: #111827;
    --text-secondary: #374151;
    --text-muted: #6b7280;
    
    /* Borders */
    --border-light: #e5e7eb;
    --border-medium: #d1d5db;
}

/* Opportunity cards - Light blue background with dark text */
.opportunity-card {
    background: linear-gradient(135deg, var(--bg-white) 0%, var(--bg-blue-50) 100%);
    color: var(--text-primary);
    padding: 24px;
    border-radius: 12px;
    border-left: 5px solid var(--primary-blue);
    margin: 20px 0;
    box-shadow: 0 2px 12px rgba(30, 64, 175, 0.1);
    transition: all 0.2s ease;
}

.opportunity-card h4 {
    color: var(--primary-blue);
    margin-bottom: 12px;
    font-weight: 700;
    font-size: 1.2em;
}

.opportunity-card p {
    color: var(--text-secondary);
    line-height: 1.6;
    margin-bottom: 8px;
}

.opportunity-card strong {
    color: var(--text-primary);
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

def main():
    st.title("🚀 Startup Revenue Insights Tracker")
    st.markdown("### Future-Proof Business Opportunities & Revenue Analysis 2025-2030")
    
    # Top 20 opportunities data
    top_opportunities = [
        {
            "name": "Legal Brief Automation Platform",
            "market_size": "45B",
            "growth_rate": 18,
            "first_year_revenue": "100-500K",
            "industry": "Legal Tech",
            "recession_proof_score": 9.2,
            "description": "AI generates legal briefs, contracts, and research summaries for small-mid law firms",
            "tech_stack": "Python/FastAPI, OpenAI GPT-4, PostgreSQL, React, AWS/GCP, Docker, LangChain"
        },
        {
            "name": "Medical Practice Workflow Optimizer",
            "market_size": "15.1B",
            "growth_rate": 22,
            "first_year_revenue": "200K-1M",
            "industry": "HealthTech",
            "recession_proof_score": 9.5,
            "description": "AI schedules patients, manages billing, automates documentation",
            "tech_stack": "Node.js/Express, Python/Django, PostgreSQL, React/TypeScript, HIPAA-compliant cloud, HL7 FHIR"
        },
        {
            "name": "Construction Project Intelligence",
            "market_size": "15.1B",
            "growth_rate": 15,
            "first_year_revenue": "150-750K",
            "industry": "PropTech",
            "recession_proof_score": 8.8,
            "description": "AI predicts delays, optimizes material ordering, tracks compliance",
            "tech_stack": "Python/Django, TensorFlow, PostgreSQL, React, AWS IoT, Docker, Redis, Celery"
        },
        {
            "name": "API Security Monitoring Platform",
            "market_size": "12B",
            "growth_rate": 25,
            "first_year_revenue": "100-500K",
            "industry": "Cybersecurity",
            "recession_proof_score": 9.7,
            "description": "Automated API vulnerability scanning and compliance monitoring",
            "tech_stack": "Go/Gin, Python, ClickHouse, React, Kubernetes, OpenAPI, OWASP ZAP, Grafana"
        },
        {
            "name": "Carbon Footprint Tracker for SMBs",
            "market_size": "270B",
            "growth_rate": 20,
            "first_year_revenue": "200K-1M",
            "industry": "ClimaTech",
            "recession_proof_score": 8.5,
            "description": "Automated carbon tracking and ESG reporting for compliance",
            "tech_stack": "Python/FastAPI, PostgreSQL, React, D3.js, AWS Lambda, Stripe API, PDF generation"
        }
    ]
    
    st.header("🎯 Top 5 Business Opportunities")
    
    for i, opp in enumerate(top_opportunities, 1):
        st.markdown(f"""
        <div class="opportunity-card">
            <h4>#{i}. {opp['name']}</h4>
            <p><strong>Industry:</strong> {opp['industry']} | 
               <strong>Market:</strong> ${opp['market_size']} | 
               <strong>Growth:</strong> {opp['growth_rate']}% | 
               <strong>First-Year Revenue:</strong> ${opp['first_year_revenue']}</p>
            <p><strong>Description:</strong> {opp['description']}</p>
            <p><strong>Tech Stack:</strong> {opp['tech_stack']}</p>
            <p><strong>Recession-Proof Score:</strong> {opp['recession_proof_score']}/10</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
'''
    
    # Write the dashboard file
    with open('/tmp/dashboard.py', 'w') as f:
        f.write(dashboard_code)
    
    os.chdir('/tmp')
    
    print("🚀 Starting Startup Revenue Insights Tracker...")
    subprocess.run([
        "streamlit", "run", "dashboard.py", 
        "--server.port", "8000",
        "--server.address", "0.0.0.0",
        "--server.headless", "true"
    ])

if __name__ == "__main__":
    app.run()