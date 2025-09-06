#!/usr/bin/env python3
"""
Startup Revenue Insights Tracker
Monitors and analyzes startup revenue data from multiple sources
"""

import requests
import pandas as pd
import json
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Optional
import asyncio
import aiohttp
from dataclasses import dataclass
import sqlite3
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class StartupData:
    """Data structure for startup information"""
    name: str
    industry: str
    founded_date: str
    revenue_estimate: Optional[float]
    growth_rate: Optional[float]
    funding_raised: Optional[float]
    employee_count: Optional[int]
    revenue_model: str
    last_updated: str
    source: str
    stage: str
    location: str

class StartupTracker:
    """Main class for tracking and analyzing startup data"""
    
    def __init__(self, db_path: str = "startup_data.db"):
        self.db_path = db_path
        self.setup_database()
        
        # API endpoints and configurations
        self.crunchbase_api = "https://api.crunchbase.com/api/v4"
        self.github_api = "https://api.github.com"
        
        # Data sources configuration
        self.data_sources = {
            'crunchbase': {
                'enabled': True,
                'rate_limit': 200,  # requests per hour
                'priority': 1
            },
            'github_trending': {
                'enabled': True,
                'rate_limit': 5000,  # requests per hour
                'priority': 2
            },
            'product_hunt': {
                'enabled': True,
                'rate_limit': 1000,
                'priority': 3
            }
        }
        
        # Industry categories for classification
        self.industries = [
            'SaaS', 'AI/ML', 'FinTech', 'HealthTech', 'EdTech', 'PropTech',
            'E-commerce', 'Developer Tools', 'Marketing Tech', 'HR Tech',
            'ClimaTech', 'FoodTech', 'Transportation', 'Cybersecurity',
            'Content/Media', 'Gaming', 'Social', 'Hardware', 'Biotech',
            'Energy', 'Manufacturing', 'Agriculture', 'Real Estate',
            'Legal Tech', 'Insurance Tech', 'Construction Tech'
        ]
    
    def setup_database(self):
        """Initialize SQLite database for storing startup data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS startups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            industry TEXT,
            founded_date TEXT,
            revenue_estimate REAL,
            growth_rate REAL,
            funding_raised REAL,
            employee_count INTEGER,
            revenue_model TEXT,
            last_updated TEXT,
            source TEXT,
            stage TEXT,
            location TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS revenue_tracking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            startup_id INTEGER,
            revenue_period TEXT,
            revenue_amount REAL,
            metric_type TEXT,
            data_date TEXT,
            confidence_score REAL,
            FOREIGN KEY (startup_id) REFERENCES startups (id)
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS market_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            industry TEXT,
            market_size REAL,
            growth_rate REAL,
            avg_first_year_revenue REAL,
            success_rate REAL,
            analysis_date TEXT
        )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    
    async def fetch_github_trending(self, session: aiohttp.ClientSession) -> List[Dict]:
        """Fetch trending repositories that could be potential startups"""
        try:
            # Get trending repositories
            url = f"{self.github_api}/search/repositories"
            params = {
                'q': 'stars:>100 created:>2023-01-01',
                'sort': 'stars',
                'order': 'desc',
                'per_page': 50
            }
            
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    startups = []
                    for repo in data.get('items', []):
                        # Look for commercial potential indicators
                        if self._is_potential_startup(repo):
                            startup_data = self._extract_github_startup_data(repo)
                            startups.append(startup_data)
                    
                    logger.info(f"Found {len(startups)} potential startups on GitHub")
                    return startups
                else:
                    logger.error(f"GitHub API error: {response.status}")
                    return []
                    
        except Exception as e:
            logger.error(f"Error fetching GitHub data: {e}")
            return []
    
    def _is_potential_startup(self, repo: Dict) -> bool:
        """Determine if a GitHub repo represents a potential startup"""
        indicators = [
            'saas' in repo['description'].lower() if repo.get('description') else False,
            'startup' in repo['description'].lower() if repo.get('description') else False,
            'business' in repo['description'].lower() if repo.get('description') else False,
            'platform' in repo['description'].lower() if repo.get('description') else False,
            repo.get('stargazers_count', 0) > 500,
            repo.get('forks_count', 0) > 50,
            repo.get('has_wiki', False),
            bool(repo.get('homepage')),
        ]
        
        return sum(indicators) >= 3
    
    def _extract_github_startup_data(self, repo: Dict) -> StartupData:
        """Extract startup data from GitHub repository"""
        return StartupData(
            name=repo['name'],
            industry=self._classify_industry(repo.get('description', '') + ' ' + repo.get('topics', [])),
            founded_date=repo['created_at'][:10],
            revenue_estimate=None,  # Not available from GitHub
            growth_rate=None,
            funding_raised=None,
            employee_count=None,
            revenue_model='Unknown',
            last_updated=datetime.now().isoformat()[:10],
            source='GitHub',
            stage='Early',
            location='Unknown'
        )
    
    def _classify_industry(self, text: str) -> str:
        """Classify startup industry based on description and keywords"""
        text_lower = text.lower()
        
        # Industry keyword mapping
        industry_keywords = {
            'SaaS': ['saas', 'software as a service', 'cloud software'],
            'AI/ML': ['ai', 'artificial intelligence', 'machine learning', 'ml', 'deep learning', 'neural network'],
            'FinTech': ['fintech', 'financial', 'banking', 'payment', 'crypto', 'blockchain'],
            'HealthTech': ['health', 'medical', 'healthcare', 'telemedicine', 'wellness'],
            'EdTech': ['education', 'learning', 'teaching', 'school', 'university'],
            'Developer Tools': ['developer', 'programming', 'coding', 'api', 'devops', 'ci/cd'],
            'E-commerce': ['ecommerce', 'e-commerce', 'retail', 'shopping', 'marketplace'],
            'Marketing Tech': ['marketing', 'advertising', 'social media', 'analytics', 'seo'],
            'Cybersecurity': ['security', 'cybersecurity', 'encryption', 'privacy', 'firewall'],
            'ClimaTech': ['climate', 'sustainability', 'green', 'environment', 'carbon'],
        }
        
        for industry, keywords in industry_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return industry
        
        return 'Other'
    
    async def collect_startup_data(self) -> List[StartupData]:
        """Collect startup data from all configured sources"""
        all_startups = []
        
        async with aiohttp.ClientSession() as session:
            # GitHub trending repositories
            github_startups = await self.fetch_github_trending(session)
            all_startups.extend(github_startups)
            
            # Add more data sources here as needed
            # crunchbase_startups = await self.fetch_crunchbase_data(session)
            # product_hunt_startups = await self.fetch_product_hunt_data(session)
        
        logger.info(f"Collected data for {len(all_startups)} startups")
        return all_startups
    
    def save_startup_data(self, startups: List[StartupData]):
        """Save startup data to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for startup in startups:
            try:
                cursor.execute('''
                INSERT OR REPLACE INTO startups 
                (name, industry, founded_date, revenue_estimate, growth_rate, 
                 funding_raised, employee_count, revenue_model, last_updated, 
                 source, stage, location)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    startup.name,
                    startup.industry,
                    startup.founded_date,
                    startup.revenue_estimate,
                    startup.growth_rate,
                    startup.funding_raised,
                    startup.employee_count,
                    startup.revenue_model,
                    startup.last_updated,
                    startup.source,
                    startup.stage,
                    startup.location
                ))
            except Exception as e:
                logger.error(f"Error saving startup {startup.name}: {e}")
        
        conn.commit()
        conn.close()
        logger.info(f"Saved {len(startups)} startups to database")
    
    def analyze_industry_trends(self) -> Dict:
        """Analyze trends across industries"""
        conn = sqlite3.connect(self.db_path)
        
        # Get industry distribution
        industry_query = '''
        SELECT industry, COUNT(*) as count, 
               AVG(revenue_estimate) as avg_revenue,
               AVG(growth_rate) as avg_growth
        FROM startups 
        WHERE industry IS NOT NULL
        GROUP BY industry
        ORDER BY count DESC
        '''
        
        industry_data = pd.read_sql_query(industry_query, conn)
        
        # Get funding trends
        funding_query = '''
        SELECT industry, 
               AVG(funding_raised) as avg_funding,
               COUNT(*) as startup_count
        FROM startups 
        WHERE funding_raised IS NOT NULL
        GROUP BY industry
        ORDER BY avg_funding DESC
        '''
        
        funding_data = pd.read_sql_query(funding_query, conn)
        
        conn.close()
        
        return {
            'industry_distribution': industry_data.to_dict('records'),
            'funding_trends': funding_data.to_dict('records'),
            'total_startups': len(industry_data),
            'analysis_date': datetime.now().isoformat()[:10]
        }
    
    def generate_revenue_insights(self) -> Dict:
        """Generate insights about revenue patterns"""
        conn = sqlite3.connect(self.db_path)
        
        # Revenue by stage analysis
        stage_revenue_query = '''
        SELECT stage, 
               COUNT(*) as count,
               AVG(revenue_estimate) as avg_revenue,
               MIN(revenue_estimate) as min_revenue,
               MAX(revenue_estimate) as max_revenue
        FROM startups 
        WHERE revenue_estimate IS NOT NULL
        GROUP BY stage
        '''
        
        stage_data = pd.read_sql_query(stage_revenue_query, conn)
        
        # Growth rate analysis
        growth_query = '''
        SELECT industry,
               AVG(growth_rate) as avg_growth_rate,
               COUNT(*) as sample_size
        FROM startups
        WHERE growth_rate IS NOT NULL
        GROUP BY industry
        ORDER BY avg_growth_rate DESC
        '''
        
        growth_data = pd.read_sql_query(growth_query, conn)
        
        conn.close()
        
        return {
            'revenue_by_stage': stage_data.to_dict('records'),
            'growth_by_industry': growth_data.to_dict('records'),
            'insights_generated': datetime.now().isoformat()[:10]
        }
    
    def export_data(self, format: str = 'json') -> str:
        """Export collected data in specified format"""
        conn = sqlite3.connect(self.db_path)
        
        # Get all startup data
        query = '''
        SELECT * FROM startups
        ORDER BY created_at DESC
        '''
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format.lower() == 'json':
            filename = f"startup_data_{timestamp}.json"
            df.to_json(filename, orient='records', indent=2)
        elif format.lower() == 'csv':
            filename = f"startup_data_{timestamp}.csv"
            df.to_csv(filename, index=False)
        else:
            raise ValueError("Supported formats: json, csv")
        
        logger.info(f"Data exported to {filename}")
        return filename
    
    async def run_analysis(self):
        """Run complete startup analysis pipeline"""
        logger.info("Starting startup analysis pipeline...")
        
        # Collect data from all sources
        startups = await self.collect_startup_data()
        
        # Save to database
        if startups:
            self.save_startup_data(startups)
        
        # Generate analysis
        industry_trends = self.analyze_industry_trends()
        revenue_insights = self.generate_revenue_insights()
        
        # Save analysis results
        analysis_results = {
            'collection_date': datetime.now().isoformat(),
            'startups_collected': len(startups),
            'industry_trends': industry_trends,
            'revenue_insights': revenue_insights
        }
        
        # Export results
        results_filename = f"analysis_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_filename, 'w') as f:
            json.dump(analysis_results, f, indent=2)
        
        logger.info(f"Analysis complete. Results saved to {results_filename}")
        return analysis_results

def main():
    """Main function to run the startup tracker"""
    tracker = StartupTracker()
    
    # Run async analysis
    results = asyncio.run(tracker.run_analysis())
    
    print("=" * 50)
    print("STARTUP REVENUE INSIGHTS TRACKER")
    print("=" * 50)
    print(f"Analysis Date: {results['collection_date']}")
    print(f"Startups Analyzed: {results['startups_collected']}")
    print("\nTop Industries by Startup Count:")
    
    for industry in results['industry_trends']['industry_distribution'][:5]:
        print(f"  {industry['industry']}: {industry['count']} startups")
    
    print("\nRevenue Insights by Stage:")
    for stage in results['revenue_insights']['revenue_by_stage']:
        if stage['avg_revenue']:
            print(f"  {stage['stage']}: ${stage['avg_revenue']:,.0f} average revenue")
    
    print("\nData exported and analysis complete!")

if __name__ == "__main__":
    main()