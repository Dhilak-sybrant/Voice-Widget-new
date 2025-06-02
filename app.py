from flask import Flask, render_template

app = Flask(__name__)

@app.route("/convai-widget.js")
def serve_widget():
    return render_template("convai-widget.js")

@app.route("/")
def index():
    return "Custom ElevenLabs Widget Running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
