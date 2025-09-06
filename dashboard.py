#!/usr/bin/env python3
"""
Startup Revenue Insights Dashboard
Interactive visualization of startup revenue data and market opportunities
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sqlite3
import json
from datetime import datetime, timedelta
import numpy as np

# Configure Streamlit page
st.set_page_config(
    page_title="Startup Revenue Insights Tracker",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

/* Main background - Clean white */
.main .block-container {
    padding-top: 2rem;
    background-color: var(--bg-white);
}

/* Override Streamlit's default styling for light theme */
.stApp {
    background-color: var(--bg-white);
}

/* Metric cards - Clean white cards with dark text */
.metric-card {
    background-color: var(--bg-white);
    color: var(--text-primary);
    padding: 24px;
    border-radius: 12px;
    border: 2px solid var(--border-light);
    margin: 12px 0;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    transition: all 0.2s ease;
}

.metric-card:hover {
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
    border-color: var(--primary-blue-light);
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

.opportunity-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(30, 64, 175, 0.15);
    background: linear-gradient(135deg, var(--bg-blue-50) 0%, #dbeafe 100%);
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

/* Revenue projection cards - Light green theme with dark text */
.revenue-projection {
    background: linear-gradient(135deg, var(--bg-white) 0%, var(--bg-green-50) 100%);
    color: var(--text-primary);
    padding: 28px;
    border-radius: 12px;
    border: 2px solid var(--success-green);
    text-align: center;
    box-shadow: 0 2px 12px rgba(5, 150, 105, 0.1);
    transition: all 0.2s ease;
}

.revenue-projection:hover {
    box-shadow: 0 4px 20px rgba(5, 150, 105, 0.15);
    transform: translateY(-1px);
    background: linear-gradient(135deg, var(--bg-green-50) 0%, #d1fae5 100%);
}

.revenue-projection h2 {
    color: var(--success-green);
    margin: 12px 0;
    font-size: 2.4em;
    font-weight: 800;
}

.revenue-projection h4 {
    color: var(--text-muted);
    margin-bottom: 8px;
    font-weight: 600;
    text-transform: uppercase;
    font-size: 0.9em;
    letter-spacing: 1px;
}

/* Success factor cards - Light amber theme with dark text */
.success-factor {
    background-color: var(--bg-white);
    color: var(--text-primary);
    padding: 20px;
    border-radius: 10px;
    margin: 12px 0;
    border-left: 4px solid var(--warning-amber);
    border: 1px solid #fed7aa;
    box-shadow: 0 2px 8px rgba(217, 119, 6, 0.1);
    transition: all 0.2s ease;
}

.success-factor:hover {
    background-color: #fffbeb;
    box-shadow: 0 4px 12px rgba(217, 119, 6, 0.15);
}

.success-factor strong {
    color: var(--warning-amber);
    font-weight: 700;
}

/* Phase cards - Light blue theme with dark text */
.phase-card {
    background: linear-gradient(135deg, var(--bg-white) 0%, var(--bg-blue-50) 100%);
    color: var(--text-primary);
    padding: 24px;
    border-radius: 12px;
    margin: 20px 0;
    border-left: 5px solid var(--primary-blue);
    border: 1px solid #bfdbfe;
    box-shadow: 0 2px 12px rgba(30, 64, 175, 0.1);
    transition: all 0.2s ease;
}

.phase-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(30, 64, 175, 0.15);
    background: linear-gradient(135deg, var(--bg-blue-50) 0%, #dbeafe 100%);
}

.phase-card h3 {
    color: var(--primary-blue);
    margin-bottom: 12px;
    font-weight: 700;
}

.phase-card ul {
    color: var(--text-secondary);
    line-height: 1.7;
}

.phase-card li {
    margin-bottom: 6px;
}

/* Override ALL text to be dark on light backgrounds */
.stMarkdown, .stMarkdown p, .stMarkdown div, .stText, p, span, div, label {
    color: var(--text-primary) !important;
    background-color: transparent !important;
}

/* Exception: Button text should remain white on blue backgrounds */
.stButton > button, .stButton > button * {
    color: white !important;
    background-color: var(--primary-blue);
}

.stButton > button:hover, .stButton > button:hover * {
    color: white !important;
    background-color: #1e3a8a;
}

/* Enhanced metric containers - Light theme */
[data-testid="metric-container"] {
    background: var(--bg-white);
    border: 2px solid var(--border-light);
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    transition: all 0.2s ease;
}

[data-testid="metric-container"]:hover {
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    border-color: var(--primary-blue-light);
}

[data-testid="metric-container"] > div {
    color: var(--text-primary) !important;
}

[data-testid="metric-container"] [data-testid="metric-value"] {
    color: var(--primary-blue) !important;
    font-weight: 700 !important;
}

/* Sidebar - Light theme */
.css-1d391kg, .css-1lcbmhc, .css-1cypcdb {
    background-color: var(--bg-gray-50) !important;
    color: var(--text-primary) !important;
}

/* Professional tab styling - Light theme */
.stTabs [data-baseweb="tab-list"] {
    background-color: var(--bg-gray-50);
    padding: 8px;
    border-radius: 8px;
    border: 1px solid var(--border-light);
}

.stTabs [data-baseweb="tab"] {
    color: var(--text-muted) !important;
    background-color: transparent;
    padding: 12px 24px;
    border-radius: 6px;
    font-weight: 500;
    transition: all 0.2s ease;
}

.stTabs [data-baseweb="tab"]:hover {
    color: var(--text-primary) !important;
    background-color: var(--bg-white);
}

/* Exception: Selected tab has white text on blue background */
.stTabs [aria-selected="true"] {
    background-color: var(--primary-blue) !important;
    color: white !important;
    font-weight: 700;
    box-shadow: 0 2px 8px rgba(30, 64, 175, 0.3);
}

.stTabs [aria-selected="true"] * {
    color: white !important;
}

/* Form elements - Light theme */
.stSelectbox > div > div {
    background-color: var(--bg-white);
    color: var(--text-primary);
    border-color: var(--border-medium);
}

.stSlider > div > div > div {
    color: var(--text-primary);
}

/* Button styling - Blue primary with white text */
.stButton > button {
    background-color: var(--primary-blue) !important;
    color: white !important;
    border: none;
    border-radius: 8px;
    padding: 12px 24px;
    font-weight: 700;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background-color: #1e3a8a !important;
    color: white !important;
    box-shadow: 0 4px 12px rgba(30, 64, 175, 0.3);
    transform: translateY(-1px);
}

.stButton > button:focus {
    background-color: var(--primary-blue) !important;
    color: white !important;
    outline: 2px solid #3b82f6;
    outline-offset: 2px;
}

/* Header styling - Dark text on light background */
h1, h2, h3, h4, h5, h6 {
    color: var(--text-primary) !important;
    font-weight: 700;
}

h1 {
    color: var(--primary-blue) !important;
    border-bottom: 3px solid var(--primary-blue);
    padding-bottom: 12px;
    margin-bottom: 24px;
}

h2 {
    color: var(--primary-blue) !important;
    margin-top: 32px;
    margin-bottom: 16px;
}

h3 {
    color: var(--text-primary) !important;
    margin-top: 24px;
    margin-bottom: 12px;
}

/* Subheader styling */
.stSubheader {
    color: var(--text-secondary) !important;
    font-weight: 600;
}

/* Ensure all text is dark EXCEPT on blue backgrounds */
* {
    color: var(--text-primary) !important;
}

/* Exception: White text on blue backgrounds only */
.stButton > button,
.stButton > button *,
.stTabs [aria-selected="true"],
.stTabs [aria-selected="true"] * {
    color: white !important;
}

/* Force override for any remaining problematic white text */
[style*="color: white"]:not(.stButton button):not([aria-selected="true"]), 
[style*="color: #ffffff"]:not(.stButton button):not([aria-selected="true"]), 
[style*="color: #fff"]:not(.stButton button):not([aria-selected="true"]) {
    color: var(--text-primary) !important;
}

/* Ensure sidebar text is dark */
.css-1d391kg *, .css-1lcbmhc *, .css-1cypcdb * {
    color: var(--text-primary) !important;
}

/* Ensure form labels are dark */
label, .stSelectbox label, .stSlider label {
    color: var(--text-primary) !important;
}
</style>
""", unsafe_allow_html=True)

class StartupDashboard:
    def __init__(self, db_path: str = "startup_data.db"):
        self.db_path = db_path
        
        # Top 20 opportunities from our analysis with tech stacks
        self.top_opportunities = [
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
            },
            {
                "name": "Insurance Claims Processing Automation",
                "market_size": "1.3T",
                "growth_rate": 16,
                "first_year_revenue": "300K-2M",
                "industry": "InsurTech",
                "recession_proof_score": 9.0,
                "description": "AI processes claims, fraud detection, document verification",
                "tech_stack": "Python/FastAPI, OpenCV, TensorFlow, PostgreSQL, React, AWS Textract, Docker"
            },
            {
                "name": "Restaurant Operations AI",
                "market_size": "35B",
                "growth_rate": 14,
                "first_year_revenue": "100-400K",
                "industry": "FoodTech",
                "recession_proof_score": 7.8,
                "description": "Inventory prediction, staff scheduling, menu optimization",
                "tech_stack": "Python/Django, Scikit-learn, PostgreSQL, React, POS integrations, Stripe, Redis"
            },
            {
                "name": "Industry-Specific Code Generators",
                "market_size": "24B",
                "growth_rate": 28,
                "first_year_revenue": "50-300K",
                "industry": "Developer Tools",
                "recession_proof_score": 8.5,
                "description": "Code generation for specific industries (fintech, healthcare, etc.)",
                "tech_stack": "Python/FastAPI, OpenAI Codex, MongoDB, React/Monaco Editor, GitHub API, Docker"
            },
            {
                "name": "Multi-Cloud Cost Optimization",
                "market_size": "723B",
                "growth_rate": 24,
                "first_year_revenue": "200K-1M",
                "industry": "DevOps/Cloud",
                "recession_proof_score": 9.1,
                "description": "Automated cloud resource optimization across providers",
                "tech_stack": "Go, Python, InfluxDB, React, AWS/GCP/Azure APIs, Terraform, Kubernetes"
            },
            {
                "name": "Veterinary Practice Manager",
                "market_size": "2.3B",
                "growth_rate": 12,
                "first_year_revenue": "75-250K",
                "industry": "PetTech",
                "recession_proof_score": 8.2,
                "description": "Appointment scheduling, inventory, billing automation",
                "tech_stack": "Ruby on Rails, PostgreSQL, React, Stripe, Twilio, PDF generation, Docker"
            },
            {
                "name": "Mental Health Screening Automation",
                "market_size": "5.6B",
                "growth_rate": 26,
                "first_year_revenue": "200-800K",
                "industry": "MentalHealthTech",
                "recession_proof_score": 9.3,
                "description": "Automated screening tools for workplace/schools",
                "tech_stack": "Python/Django, TensorFlow, PostgreSQL, React, HIPAA compliance, WebRTC, Chart.js"
            },
            {
                "name": "Small Business Cash Flow Predictor",
                "market_size": "12B",
                "growth_rate": 19,
                "first_year_revenue": "200-900K",
                "industry": "FinTech",
                "recession_proof_score": 8.9,
                "description": "Predicts cash flow, suggests financing options",
                "tech_stack": "Python/FastAPI, Scikit-learn, PostgreSQL, React, Plaid API, Stripe, ML models"
            },
            {
                "name": "Podcast Production Automation",
                "market_size": "2B",
                "growth_rate": 23,
                "first_year_revenue": "75-400K",
                "industry": "MediaTech",
                "recession_proof_score": 7.5,
                "description": "Automated editing, transcription, social media content",
                "tech_stack": "Python/FastAPI, FFmpeg, Whisper AI, PostgreSQL, React, AWS S3, WebSockets"
            },
            {
                "name": "HVAC Service Optimization",
                "market_size": "170B",
                "growth_rate": 8,
                "first_year_revenue": "60-300K",
                "industry": "ServiceTech",
                "recession_proof_score": 8.7,
                "description": "Route optimization, inventory prediction, customer scheduling",
                "tech_stack": "Python/Django, Google Maps API, PostgreSQL, React Native, Stripe, Twilio"
            },
            {
                "name": "Corporate Skill Gap Analyzer",
                "market_size": "400B",
                "growth_rate": 15,
                "first_year_revenue": "250K-1M",
                "industry": "HRTech",
                "recession_proof_score": 8.6,
                "description": "Identifies skill gaps, suggests training programs",
                "tech_stack": "Python/Django, NLP libraries, PostgreSQL, React, D3.js, API integrations, Docker"
            },
            {
                "name": "Supply Chain Sustainability Monitor",
                "market_size": "24B",
                "growth_rate": 21,
                "first_year_revenue": "300K-1.5M",
                "industry": "SupplyTech",
                "recession_proof_score": 8.8,
                "description": "Tracks supplier sustainability metrics",
                "tech_stack": "Python/FastAPI, Apache Kafka, PostgreSQL, React, Mapbox, PDF reports, Docker"
            },
            {
                "name": "Energy Usage Optimizer for Offices",
                "market_size": "15B",
                "growth_rate": 17,
                "first_year_revenue": "150-800K",
                "industry": "EnergyTech",
                "recession_proof_score": 8.4,
                "description": "AI optimizes HVAC, lighting based on occupancy",
                "tech_stack": "Python/Django, IoT sensors, InfluxDB, React, MQTT, Machine Learning, Raspberry Pi"
            },
            {
                "name": "Crypto Tax Automation",
                "market_size": "13.6B",
                "growth_rate": 35,
                "first_year_revenue": "150-750K",
                "industry": "CryptoTech",
                "recession_proof_score": 7.2,
                "description": "Automated crypto transaction tracking and tax reporting",
                "tech_stack": "Python/FastAPI, Web3.py, PostgreSQL, React, Blockchain APIs, PDF generation"
            },
            {
                "name": "Social Media Compliance Monitor",
                "market_size": "65B",
                "growth_rate": 18,
                "first_year_revenue": "150-750K",
                "industry": "RegTech",
                "recession_proof_score": 8.3,
                "description": "Monitors posts for regulatory compliance (financial, healthcare)",
                "tech_stack": "Python/FastAPI, NLP/BERT, PostgreSQL, React, Social Media APIs, Real-time processing"
            },
            {
                "name": "Equipment Financing Optimizer",
                "market_size": "1T",
                "growth_rate": 12,
                "first_year_revenue": "300K-1.5M",
                "industry": "FinTech",
                "recession_proof_score": 8.1,
                "description": "Matches businesses with optimal equipment financing",
                "tech_stack": "Python/Django, ML models, PostgreSQL, React, Credit APIs, DocuSign, Stripe Connect"
            }
        ]
        
        # Revenue benchmarks by industry
        self.revenue_benchmarks = {
            "SaaS Vertical": {"month_1": 1000, "month_6": 8000, "month_12": 30000, "growth_rate": 18},
            "AI/Automation": {"month_1": 2000, "month_6": 15000, "month_12": 50000, "growth_rate": 22},
            "Developer Tools": {"month_1": 500, "month_6": 5000, "month_12": 20000, "growth_rate": 27},
            "Professional Services": {"month_1": 3000, "month_6": 12000, "month_12": 35000, "growth_rate": 15},
            "HealthTech": {"month_1": 2500, "month_6": 18000, "month_12": 60000, "growth_rate": 25},
        }
    
    def load_data(self) -> pd.DataFrame:
        """Load startup data from database or create sample data"""
        try:
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query("SELECT * FROM startups", conn)
            conn.close()
            
            if df.empty:
                # Create sample data for demonstration
                df = self.create_sample_data()
            
            return df
        except:
            # If no database, create sample data
            return self.create_sample_data()
    
    def create_sample_data(self) -> pd.DataFrame:
        """Create sample startup data for demonstration"""
        np.random.seed(42)
        
        industries = ["SaaS", "AI/ML", "FinTech", "HealthTech", "EdTech", "DevTools", "ClimaTech", "LegalTech"]
        stages = ["Pre-Seed", "Seed", "Series A", "Series B", "Growth"]
        
        data = []
        for i in range(100):
            industry = np.random.choice(industries)
            stage = np.random.choice(stages, p=[0.4, 0.3, 0.15, 0.1, 0.05])
            
            # Revenue estimates based on stage
            revenue_ranges = {
                "Pre-Seed": (0, 100000),
                "Seed": (50000, 1000000),
                "Series A": (500000, 5000000),
                "Series B": (2000000, 20000000),
                "Growth": (10000000, 100000000)
            }
            
            min_rev, max_rev = revenue_ranges[stage]
            revenue = np.random.randint(min_rev, max_rev) if max_rev > min_rev else min_rev
            
            data.append({
                "name": f"Startup_{i+1}",
                "industry": industry,
                "stage": stage,
                "revenue_estimate": revenue,
                "growth_rate": np.random.normal(25, 15),
                "funding_raised": revenue * np.random.uniform(2, 8),
                "employee_count": max(1, int(revenue / 150000)),
                "founded_date": f"2023-{np.random.randint(1,13):02d}-{np.random.randint(1,29):02d}",
                "location": np.random.choice(["San Francisco", "New York", "Austin", "Seattle", "Boston"])
            })
        
        return pd.DataFrame(data)
    
    def render_header(self):
        """Render dashboard header"""
        st.title("🚀 Startup Revenue Insights Tracker")
        st.markdown("### Future-Proof Business Opportunities & Revenue Analysis 2025-2030")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Market Opportunities", "50+", "📈")
        
        with col2:
            st.metric("Avg First-Year Revenue", "$300K+", "💰")
        
        with col3:
            st.metric("Success Rate", "23%", "🎯")
        
        with col4:
            st.metric("Market Size", "$1.2T+", "🌍")
    
    def render_top_opportunities(self):
        """Render top 20 business opportunities with tech stacks"""
        st.header("🎯 Top 20 Business Opportunities")
        
        # Add filter options
        col1, col2 = st.columns(2)
        with col1:
            selected_industries = st.multiselect(
                "Filter by Industry",
                options=list(set([opp['industry'] for opp in self.top_opportunities])),
                default=[]
            )
        with col2:
            min_revenue = st.selectbox(
                "Minimum First-Year Revenue",
                options=["Any", "100K+", "200K+", "300K+"],
                index=0
            )
        
        # Filter opportunities
        filtered_opps = self.top_opportunities.copy()
        
        if selected_industries:
            filtered_opps = [opp for opp in filtered_opps if opp['industry'] in selected_industries]
        
        if min_revenue != "Any":
            min_val = int(min_revenue.replace("K+", "")) * 1000
            filtered_opps = [opp for opp in filtered_opps 
                           if int(opp['first_year_revenue'].split('-')[0].replace('K', '')) * 1000 >= min_val]
        
        st.write(f"Showing {len(filtered_opps)} opportunities")
        
        for i, opp in enumerate(filtered_opps, 1):
            with st.container():
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
    
    def render_revenue_projections(self):
        """Render revenue projection models"""
        st.header("📊 Revenue Projection Models")
        
        # Industry selection
        selected_industry = st.selectbox(
            "Select Industry for Revenue Projection",
            list(self.revenue_benchmarks.keys())
        )
        
        benchmark = self.revenue_benchmarks[selected_industry]
        
        # Calculate monthly projections
        months = list(range(1, 13))
        growth_rate = benchmark["growth_rate"] / 100 / 12  # Monthly growth rate
        
        projections = []
        current_revenue = benchmark["month_1"]
        
        for month in months:
            if month == 1:
                revenue = benchmark["month_1"]
            elif month == 6:
                revenue = benchmark["month_6"]
            elif month == 12:
                revenue = benchmark["month_12"]
            else:
                # Interpolate based on growth rate
                revenue = current_revenue * (1 + growth_rate)
                current_revenue = revenue
            
            projections.append(revenue)
        
        # Create projection chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=months,
            y=projections,
            mode='lines+markers',
            name='Revenue Projection',
            line=dict(color='#1e40af', width=3),
            marker=dict(size=10, color='#059669', line=dict(color='#1e40af', width=2))
        ))
        
        fig.update_layout(
            title=f"{selected_industry} - First Year Revenue Projection",
            xaxis_title="Month",
            yaxis_title="Monthly Revenue ($)",
            template="plotly_white",
            height=400,
            paper_bgcolor='white',
            plot_bgcolor='rgba(249, 250, 251, 0.5)',
            font=dict(color='#111827', size=12),
            title_font=dict(color='#1e40af', size=16, family="Arial Black"),
            xaxis=dict(gridcolor='rgba(229, 231, 235, 0.8)', color='#374151'),
            yaxis=dict(gridcolor='rgba(229, 231, 235, 0.8)', color='#374151')
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Display key metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="revenue-projection">
                <h4>Month 1 Revenue</h4>
                <h2>${benchmark['month_1']:,}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="revenue-projection">
                <h4>Month 6 Revenue</h4>
                <h2>${benchmark['month_6']:,}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="revenue-projection">
                <h4>Year 1 Total (ARR)</h4>
                <h2>${benchmark['month_12']*12:,}</h2>
            </div>
            """, unsafe_allow_html=True)
    
    def render_market_analysis(self, df: pd.DataFrame):
        """Render market analysis charts"""
        st.header("📈 Market Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Industry distribution
            industry_counts = df['industry'].value_counts()
            
            # Professional color palette for pie chart
            professional_colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', 
                                 '#06b6d4', '#84cc16', '#f97316', '#ec4899', '#6366f1']
            
            fig_pie = px.pie(
                values=industry_counts.values,
                names=industry_counts.index,
                title="Startup Distribution by Industry",
                template="plotly_dark",
                color_discrete_sequence=professional_colors
            )
            fig_pie.update_layout(
                paper_bgcolor='white',
                plot_bgcolor='white',
                font=dict(color='#111827', size=12),
                title_font=dict(color='#1e40af', size=14, family="Arial Black")
            )
            
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Revenue by stage
            stage_revenue = df.groupby('stage')['revenue_estimate'].mean().sort_values(ascending=True)
            
            fig_bar = px.bar(
                x=stage_revenue.values,
                y=stage_revenue.index,
                orientation='h',
                title="Average Revenue by Stage",
                template="plotly_white",
                color=stage_revenue.values,
                color_continuous_scale=[[0, '#e5e7eb'], [0.5, '#3b82f6'], [1, '#059669']]
            )
            fig_bar.update_layout(
                paper_bgcolor='white',
                plot_bgcolor='rgba(249, 250, 251, 0.5)',
                font=dict(color='#111827', size=12),
                title_font=dict(color='#1e40af', size=14, family="Arial Black"),
                xaxis=dict(gridcolor='rgba(229, 231, 235, 0.8)', color='#374151'),
                yaxis=dict(gridcolor='rgba(229, 231, 235, 0.8)', color='#374151')
            )
            
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Revenue vs Growth Rate Scatter
        st.subheader("Revenue vs Growth Rate Analysis")
        
        fig_scatter = px.scatter(
            df,
            x='revenue_estimate',
            y='growth_rate',
            color='industry',
            size='funding_raised',
            hover_data=['name', 'stage'],
            title="Revenue vs Growth Rate by Industry",
            template="plotly_white",
            color_discrete_sequence=professional_colors
        )
        
        fig_scatter.update_layout(
            xaxis_title="Revenue Estimate ($)",
            yaxis_title="Growth Rate (%)",
            height=500,
            paper_bgcolor='white',
            plot_bgcolor='rgba(249, 250, 251, 0.5)',
            font=dict(color='#111827', size=12),
            title_font=dict(color='#1e40af', size=14, family="Arial Black"),
            xaxis=dict(gridcolor='rgba(229, 231, 235, 0.8)', color='#374151'),
            yaxis=dict(gridcolor='rgba(229, 231, 235, 0.8)', color='#374151')
        )
        
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    def render_success_factors(self):
        """Render success factors analysis"""
        st.header("🎯 Success Factors Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Key Success Indicators")
            success_factors = [
                {"factor": "Time to First Customer", "target": "< 30 days", "weight": 9.2},
                {"factor": "Monthly Growth Rate", "target": "> 15%", "weight": 9.5},
                {"factor": "Customer Retention", "target": "> 95%", "weight": 9.0},
                {"factor": "CAC Payback Period", "target": "< 6 months", "weight": 8.8},
                {"factor": "Product-Market Fit", "target": "40%+ very disappointed", "weight": 9.7}
            ]
            
            for factor in success_factors:
                st.markdown(f"""
                <div class="success-factor">
                    <strong>{factor['factor']}</strong><br>
                    Target: {factor['target']}<br>
                    Importance: <strong>{factor['weight']}/10</strong>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.subheader("Revenue Model Performance")
            
            models = ["Subscription", "Usage-Based", "Hybrid", "One-time", "Freemium"]
            success_rates = [78, 65, 82, 45, 58]
            avg_revenue = [450000, 320000, 680000, 180000, 290000]
            
            fig = make_subplots(
                rows=1, cols=2,
                subplot_titles=("Success Rate (%)", "Average Revenue ($)"),
                specs=[[{"secondary_y": False}, {"secondary_y": False}]]
            )
            
            fig.add_trace(
                go.Bar(x=models, y=success_rates, name="Success Rate (%)", 
                      marker_color="#10b981", marker_line=dict(color="#065f46", width=1)),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Bar(x=models, y=avg_revenue, name="Avg Revenue ($)", 
                      marker_color="#3b82f6", marker_line=dict(color="#1e40af", width=1)),
                row=1, col=2
            )
            
            fig.update_layout(
                template="plotly_white", 
                height=400,
                paper_bgcolor='white',
                plot_bgcolor='rgba(249, 250, 251, 0.5)',
                font=dict(color='#111827', size=11),
                title_font=dict(color='#1e40af'),
                showlegend=False
            )
            
            # Update grid colors for light theme
            fig.update_xaxes(gridcolor='rgba(229, 231, 235, 0.8)', color='#374151')
            fig.update_yaxes(gridcolor='rgba(229, 231, 235, 0.8)', color='#374151')
            st.plotly_chart(fig, use_container_width=True)
    
    def render_implementation_guide(self):
        """Render implementation guidance"""
        st.header("🛠️ Implementation Guide")
        
        st.subheader("Phase-by-Phase Roadmap")
        
        phases = [
            {
                "phase": "Phase 1: Market Validation",
                "timeline": "Months 1-3",
                "revenue_target": "$1K-$5K MRR",
                "key_activities": [
                    "Identify specific vertical pain point",
                    "Build MVP with core automation features",
                    "Validate with 10-15 early customers",
                    "Establish product-market fit metrics"
                ]
            },
            {
                "phase": "Phase 2: Revenue Generation",
                "timeline": "Months 4-12",
                "revenue_target": "$25K-$50K MRR",
                "key_activities": [
                    "Target $300K-$600K ARR",
                    "Implement subscription + usage pricing",
                    "Focus on customer success and retention",
                    "Build automated customer acquisition"
                ]
            },
            {
                "phase": "Phase 3: Scale & Expansion",
                "timeline": "Months 13-24",
                "revenue_target": "$100K+ MRR",
                "key_activities": [
                    "Reach $1M+ ARR",
                    "Add complementary vertical features",
                    "Implement AI/automation enhancements",
                    "Consider strategic partnerships"
                ]
            }
        ]
        
        for phase in phases:
            st.markdown(f"""
            <div class="phase-card">
                <h3>{phase['phase']} ({phase['timeline']})</h3>
                <p><strong>Revenue Target:</strong> {phase['revenue_target']}</p>
                <p><strong>Key Activities:</strong></p>
                <ul>
                    {''.join([f'<li>{activity}</li>' for activity in phase['key_activities']])}
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    def render_sidebar(self):
        """Render sidebar with filters and controls"""
        with st.sidebar:
            st.header("🎛️ Dashboard Controls")
            
            st.subheader("Quick Actions")
            if st.button("🔄 Refresh Data"):
                st.rerun()
            
            if st.button("📊 Run Analysis"):
                st.info("Analysis pipeline would run here...")
            
            if st.button("📤 Export Data"):
                st.success("Data exported successfully!")
            
            st.subheader("Market Filters")
            
            # Industry filter
            industries = ["All", "SaaS", "AI/ML", "FinTech", "HealthTech", "EdTech", "DevTools", "ClimaTech"]
            selected_industry = st.selectbox("Filter by Industry", industries)
            
            # Stage filter
            stages = ["All", "Pre-Seed", "Seed", "Series A", "Series B", "Growth"]
            selected_stage = st.selectbox("Filter by Stage", stages)
            
            # Revenue range
            revenue_range = st.slider(
                "Revenue Range ($K)",
                min_value=0,
                max_value=10000,
                value=(0, 1000),
                step=50
            )
            
            st.subheader("📚 Resources")
            st.markdown("""
            - [Startup Revenue Analysis](https://example.com)
            - [Market Research Reports](https://example.com)
            - [Industry Benchmarks](https://example.com)
            - [Success Stories](https://example.com)
            """)
    
    def run(self):
        """Main dashboard rendering function"""
        # Load data
        df = self.load_data()
        
        # Render components
        self.render_header()
        self.render_sidebar()
        
        # Main content tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🎯 Opportunities", 
            "📊 Revenue Models", 
            "📈 Market Analysis", 
            "🎯 Success Factors",
            "🛠️ Implementation"
        ])
        
        with tab1:
            self.render_top_opportunities()
        
        with tab2:
            self.render_revenue_projections()
        
        with tab3:
            self.render_market_analysis(df)
        
        with tab4:
            self.render_success_factors()
        
        with tab5:
            self.render_implementation_guide()

def main():
    """Main function to run the dashboard"""
    dashboard = StartupDashboard()
    dashboard.run()

if __name__ == "__main__":
    main()