#!/usr/bin/env python3
"""
Deploy Startup Revenue Insights Tracker to Modal
"""

import shlex
import subprocess
from pathlib import Path
import modal

# Define container dependencies
image = modal.Image.debian_slim(python_version="3.11").pip_install(
    "streamlit>=1.49.0",
    "pandas>=2.0.0", 
    "numpy>=1.24.0",
    "plotly>=5.10.0",
    "requests>=2.28.0",
    "aiohttp>=3.8.0"
)

app = modal.App(name="startup-revenue-insights-tracker", image=image)

# Mount all necessary files
files_to_mount = [
    "dashboard.py",
    "startup_tracker.py", 
    "startup_opportunity_analysis_2025.md",
    "top_50_business_opportunities_2025.md",
    "revenue_tracking_framework.md"
]

mounts = []
for file_name in files_to_mount:
    local_path = Path(__file__).parent / file_name
    if local_path.exists():
        remote_path = Path("/root") / file_name
        mounts.append(modal.Mount.from_local_file(local_path, remote_path))

# Mount .streamlit config
streamlit_config_path = Path(__file__).parent / ".streamlit" / "config.toml"
if streamlit_config_path.exists():
    config_mount = modal.Mount.from_local_file(
        streamlit_config_path,
        Path("/root/.streamlit/config.toml")
    )
    mounts.append(config_mount)

@app.function(
    allow_concurrent_inputs=100,
    mounts=mounts,
    cpu=1.0,
    memory=1024
)
@modal.web_server(8000)
def run():
    """Run the Streamlit dashboard"""
    cmd = "streamlit run dashboard.py --server.port 8000 --server.enableCORS=false --server.enableXsrfProtection=false --server.headless=true"
    subprocess.Popen(cmd, shell=True, cwd="/root")

if __name__ == "__main__":
    print("🚀 Deploying Startup Revenue Insights Tracker to Modal...")
    print("📊 Dashboard will be available at the provided URL after deployment")
    app.serve()