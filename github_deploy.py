#!/usr/bin/env python3
"""
GitHub Deployment Script using stored token
"""
import keyring
import subprocess
import os
import sys
import requests
import json

def get_github_token():
    """Retrieve GitHub token from keyring"""
    try:
        token = keyring.get_password('memex', 'Memex Deployments for Github')
        if token:
            print("✅ GitHub token retrieved from secrets")
            return token.strip()
        else:
            print("❌ Token not found with that exact name")
            # Try variations
            variations = [
                'Memex Deployments for Github',
                'memex deployments for github', 
                'GitHub Token',
                'github-token'
            ]
            for var in variations:
                token = keyring.get_password('memex', var)
                if token:
                    print(f"✅ Found token with name: {var}")
                    return token.strip()
            return None
    except Exception as e:
        print(f"❌ Error retrieving token: {e}")
        return None

def create_github_repo(token, repo_name, description):
    """Create GitHub repository using API"""
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    data = {
        'name': repo_name,
        'description': description,
        'private': False,
        'auto_init': False
    }
    
    response = requests.post('https://api.github.com/user/repos', 
                           headers=headers, json=data)
    
    if response.status_code == 201:
        repo_info = response.json()
        print(f"✅ Repository created: {repo_info['html_url']}")
        return repo_info['clone_url'], repo_info['html_url']
    elif response.status_code == 422:
        print("⚠️ Repository already exists, using existing repo")
        # Get user info to construct URL
        user_response = requests.get('https://api.github.com/user', headers=headers)
        if user_response.status_code == 200:
            username = user_response.json()['login']
            clone_url = f"https://github.com/{username}/{repo_name}.git"
            html_url = f"https://github.com/{username}/{repo_name}"
            return clone_url, html_url
    else:
        print(f"❌ Failed to create repository: {response.json()}")
        return None, None

def push_to_github(token, clone_url):
    """Push code to GitHub repository"""
    try:
        # Add authentication to URL
        auth_url = clone_url.replace('https://', f'https://{token}@')
        
        # Check if remote already exists
        result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                              capture_output=True, text=True)
        
        if result.returncode != 0:
            # Add remote
            subprocess.run(['git', 'remote', 'add', 'origin', auth_url], check=True)
            print("✅ Remote origin added")
        else:
            # Update remote URL
            subprocess.run(['git', 'remote', 'set-url', 'origin', auth_url], check=True)
            print("✅ Remote origin updated")
        
        # Push to GitHub
        result = subprocess.run(['git', 'push', '-u', 'origin', 'main'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("🚀 Code successfully pushed to GitHub!")
            return True
        else:
            print(f"❌ Push failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error pushing to GitHub: {e}")
        return False

def main():
    print("🚀 DEPLOYING STARTUP REVENUE INSIGHTS TRACKER TO GITHUB")
    print("=" * 60)
    
    # Get GitHub token
    token = get_github_token()
    if not token:
        print("❌ Cannot proceed without GitHub token")
        return False
    
    # Repository details
    repo_name = "startup-revenue-insights-tracker"
    description = "Professional Business Intelligence Platform - Top 20 Startup Opportunities with Complete Tech Stacks"
    
    # Create repository
    print("📦 Creating GitHub repository...")
    clone_url, html_url = create_github_repo(token, repo_name, description)
    
    if not clone_url:
        print("❌ Failed to create/access repository")
        return False
    
    # Push code
    print("📤 Pushing code to GitHub...")
    success = push_to_github(token, clone_url)
    
    if success:
        print("\n🎉 SUCCESS!")
        print(f"📍 Repository URL: {html_url}")
        print(f"🌐 Ready for Streamlit Cloud deployment")
        print(f"📋 Next step: Deploy on https://share.streamlit.io")
        print(f"    - Repository: {repo_name}")
        print(f"    - Main file: dashboard.py")
        return True
    else:
        print("❌ Deployment failed")
        return False

if __name__ == "__main__":
    main()