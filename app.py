from flask import Flask
from routes.agent import agent_bp


app = Flask(__name__)

# Register your agent blueprint
app.register_blueprint(agent_bp)

@app.route("/")
def home():
    return "Travel AI Agent is running!"

if __name__ == "__main__":
    app.run(debug=True)

