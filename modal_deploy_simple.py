#!/usr/bin/env python3
"""
Simple Modal deployment for Startup Revenue Insights Tracker
"""
import modal

# Create Modal app
app = modal.App("startup-revenue-tracker")

# Define image with dependencies
image = modal.Image.debian_slim(python_version="3.11").pip_install(
    "streamlit==1.49.1",
    "pandas==2.3.2", 
    "numpy==2.3.2",
    "plotly==6.3.0"
)

# Mount the main dashboard file
dashboard_mount = modal.Mount.from_local_file(
    "dashboard.py",
    remote_path="/dashboard.py"
)

@app.function(
    image=image,
    mounts=[dashboard_mount]
)
@modal.web_server(8000, startup_timeout=60)
def serve():
    import subprocess
    import os
    
    # Change to the directory with our files
    os.chdir("/")
    
    # Start Streamlit
    subprocess.Popen([
        "streamlit", "run", "dashboard.py",
        "--server.port", "8000",
        "--server.address", "0.0.0.0",
        "--server.headless", "true",
        "--server.enableCORS", "false",
        "--server.enableXsrfProtection", "false"
    ])

@app.local_entrypoint()
def main():
    print("🚀 Deploying Startup Revenue Insights Tracker to Modal...")
    print("📊 Dashboard will be available at the URL shown below")

if __name__ == "__main__":
    app.serve()