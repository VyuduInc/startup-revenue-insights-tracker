# Startup Revenue Insights Tracker - Project Rules

## Project Overview
Professional Business Intelligence Platform analyzing future-proof startup opportunities for 2025-2030. This is a comprehensive market research and revenue analysis tool designed for strategic business planning, investor presentations, and development decision-making.

## Core Architecture & Technology Stack

### Application Framework
- **Primary Platform**: Streamlit for interactive web dashboard
- **Data Processing**: Pandas/NumPy for analysis and modeling
- **Visualization**: Plotly for professional interactive charts
- **Deployment**: Streamlit Community Cloud (primary), Modal (vyuduinc workspace)
- **Version Control**: Git with GitHub integration

### Design System & Styling
- **Theme**: Professional light theme with high readability
- **Primary Color**: #1e40af (professional blue)
- **Background**: White (#ffffff) with light gray accents (#f9fafb)
- **Text**: Black (#111827) for maximum readability
- **Exception**: White text ONLY on blue buttons/selected elements
- **Configuration**: `.streamlit/config.toml` with optimized settings

## Business Intelligence Patterns

### Opportunity Analysis Structure
- **Total Count**: 20 detailed business opportunities (expanded from original 5)
- **Revenue Tiers**: 
  - Tier 1: $300K+ first-year revenue potential
  - Tier 2: $150-300K revenue potential  
  - Tier 3: $50-150K revenue potential
- **Required Fields**: Name, market size, growth rate, industry, tech stack, description, recession-proof score

### Tech Stack Recommendations Format
- **Pattern**: `Primary Language/Framework + Database + Frontend + Cloud/Infrastructure + Specialized Tools`
- **Examples**: 
  - `Python/FastAPI + PostgreSQL + React + AWS/GCP + Docker + LangChain`
  - `Node.js/Express + Python/Django + PostgreSQL + React/TypeScript + HIPAA compliance`
- **Most Recommended**: Python/FastAPI + PostgreSQL + React (40% of opportunities)

### Market Analysis Standards  
- **Market Size**: Format as "45B", "15.1B", "270B" etc.
- **Growth Rates**: Annual percentage (8% to 35% range)
- **Revenue Projections**: Realistic first-year ranges (e.g., "100-500K", "200K-1M")
- **Recession-Proof Scoring**: 1-10 scale with 8.0+ considered highly resilient

## Deployment & Infrastructure

### Platform Configuration
- **Streamlit Cloud**: Primary deployment platform via GitHub integration
- **Modal Workspace**: vyuduinc workspace for serverless deployments
- **GitHub**: Source control with deployment automation
- **Requirements**: Clean `requirements.txt` with minimal, stable dependencies

### File Structure Standards
- **Main App**: `dashboard.py` (entry point)
- **Dependencies**: `requirements.txt` (cloud-optimized)  
- **Config**: `.streamlit/config.toml` (theme and server settings)
- **Documentation**: Comprehensive README.md with deployment instructions
- **Analysis Files**: Detailed markdown files for business intelligence

### Authentication & Secrets
- **GitHub Token**: Stored in Memex secrets as "Memex Deployments for Github"
- **Modal Token**: Configured for vyuduinc workspace deployment
- **Permissions**: Full DevOps access including repo management, workflow automation

## Development Workflow

### Code Quality Standards
- **Professional Grade**: Corporate-ready styling and functionality
- **Mobile Responsive**: Works across all device types
- **Performance Optimized**: Fast loading with minimal dependencies
- **Documentation**: Complete technical and business documentation

### Feature Development Pattern
- **Interactive Filtering**: By industry, revenue potential, market size
- **Professional Presentation**: Suitable for investor meetings and strategic planning
- **Implementation Guidance**: Complete roadmaps with development timelines
- **Market Intelligence**: Real data analysis with actionable insights

### Deployment Process
1. **Local Development**: Test with `streamlit run dashboard.py --server.port 8508`
2. **Git Management**: Professional commit messages with Memex attribution
3. **GitHub Push**: Automated via stored authentication tokens
4. **Streamlit Deployment**: Direct integration from GitHub repository
5. **Verification**: Test all features and professional presentation quality

## Business Context

### Target Use Cases
- **Strategic Business Planning**: Market opportunity assessment and validation
- **Investment Analysis**: Professional-grade data for investor presentations  
- **Technology Decisions**: Complete implementation guidance with tech stacks
- **Risk Assessment**: Recession-proof business model evaluation

### Success Metrics
- **Market Coverage**: $2T+ total addressable market across opportunities
- **Implementation Ready**: Complete tech stacks with 4-12 month timelines
- **Professional Quality**: Corporate presentation standards maintained
- **Global Accessibility**: Worldwide deployment with SSL and CDN

## Integration Points

### Data Sources (Future)
- **Startup Databases**: Crunchbase, CB Insights integration patterns
- **GitHub Trends**: Repository analysis for emerging technologies
- **Market Research**: Real-time data feeds for opportunity validation

### Scalability Considerations  
- **Multi-Platform**: Streamlit Cloud, Modal, Railway deployment options
- **Performance**: Optimized for concurrent users and interactive features
- **Extensibility**: Modular design for additional analysis tools and data sources