import sys
from pathlib import Path

from flask import Flask

project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root / "logic"))
sys.path.insert(0, str(project_root / "routes"))

from routes.agent import agent_bp

app = Flask(__name__)
app.register_blueprint(agent_bp, url_prefix="/api")


@app.get("/")
def home():
    return "Travel AI Agent is running!"


@app.get("/health")
def health():
    return {"status": "ok"}