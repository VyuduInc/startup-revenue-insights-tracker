#!/usr/bin/env python3
"""
Deploy Startup Revenue Insights Tracker Live
Using Streamlit Cloud or local tunnel
"""

import subprocess
import webbrowser
import time
import os
from pathlib import Path

def deploy_to_streamlit_cloud():
    """Instructions for Streamlit Cloud deployment"""
    print("🚀 DEPLOYING TO STREAMLIT CLOUD")
    print("=" * 50)
    
    print("1. Create GitHub repository:")
    print("   git init")
    print("   git add .")
    print("   git commit -m 'Initial commit - Startup Revenue Insights Tracker'")
    print("   git branch -M main")
    print("   git remote add origin https://github.com/YOUR_USERNAME/startup-revenue-insights-tracker")
    print("   git push -u origin main")
    
    print("\n2. Deploy to Streamlit Cloud:")
    print("   - Go to https://share.streamlit.io")
    print("   - Connect GitHub account")
    print("   - Click 'New app'")
    print("   - Select repository: startup-revenue-insights-tracker")
    print("   - Main file: dashboard.py")
    print("   - Requirements file: requirements.txt")
    print("   - Click 'Deploy!'")
    
    print("\n✅ Your app will be live at:")
    print("   https://YOUR_USERNAME-startup-revenue-insights-tracker-dashboard-xxxxx.streamlit.app/")
    
    # Open Streamlit Cloud
    webbrowser.open("https://share.streamlit.io")

def run_local_with_tunnel():
    """Run locally with public tunnel"""
    try:
        # Try to install pyngrok
        subprocess.run(["pip", "install", "pyngrok"], check=True)
        
        print("🌐 STARTING LOCAL SERVER WITH PUBLIC TUNNEL")
        print("=" * 50)
        
        # Create tunnel script
        tunnel_script = '''
import streamlit as st
from pyngrok import ngrok
import subprocess
import threading
import time

def run_streamlit():
    subprocess.run(["streamlit", "run", "dashboard.py", "--server.port", "8504"])

# Start Streamlit in background
thread = threading.Thread(target=run_streamlit, daemon=True)
thread.start()

# Wait for Streamlit to start
time.sleep(5)

# Create tunnel
public_tunnel = ngrok.connect(8504)
print(f"🌍 PUBLIC URL: {public_tunnel.public_url}")
print("📱 Share this URL with anyone!")
print("Press Ctrl+C to stop")

# Keep running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    ngrok.disconnect(public_tunnel.public_url)
    print("\\n🛑 Tunnel closed")
'''
        
        with open("tunnel_deploy.py", "w") as f:
            f.write(tunnel_script)
        
        # Run the tunnel
        subprocess.run(["python", "tunnel_deploy.py"])
        
    except subprocess.CalledProcessError:
        print("❌ Could not install pyngrok. Using local deployment instead.")
        run_local_only()

def run_local_only():
    """Run local server only"""
    print("💻 STARTING LOCAL SERVER")
    print("=" * 40)
    print("Dashboard will be available at: http://localhost:8504")
    print("Press Ctrl+C to stop")
    
    try:
        subprocess.run([
            "streamlit", "run", "dashboard.py", 
            "--server.port", "8504",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")

def main():
    """Main deployment function"""
    print("🎯 STARTUP REVENUE INSIGHTS TRACKER - LIVE DEPLOYMENT")
    print("=" * 60)
    
    print("Choose deployment option:")
    print("1. 🌍 Streamlit Cloud (Free, Public, Recommended)")
    print("2. 🔗 Local + Public Tunnel (Temporary)")
    print("3. 💻 Local Only")
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        deploy_to_streamlit_cloud()
    elif choice == "2":
        run_local_with_tunnel()
    elif choice == "3":
        run_local_only()
    else:
        print("Invalid choice. Running local server.")
        run_local_only()

if __name__ == "__main__":
    # Ensure we're in the right directory
    os.chdir(Path(__file__).parent)
    main()