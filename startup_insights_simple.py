import modal
import subprocess
import shlex

app = modal.App("startup-insights-simple")

image = modal.Image.debian_slim(python_version="3.11").pip_install(
    "streamlit==1.49.1",
    "pandas==2.3.2", 
    "numpy==2.3.2",
    "plotly==6.3.0"
)

# Mount the dashboard file
dashboard_mount = modal.Mount.from_local_file(
    "dashboard.py",
    remote_path="/dashboard.py"
)

@app.function(image=image, mounts=[dashboard_mount])
@modal.web_server(8000)
def serve():
    cmd = shlex.split("streamlit run /dashboard.py --server.port 8000 --server.address 0.0.0.0 --server.headless true")
    subprocess.Popen(cmd)

if __name__ == "__main__":
    app.serve()