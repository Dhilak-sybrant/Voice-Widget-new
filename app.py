
from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/convai-widget.js')
def serve_sybrant_widget():
    agent_id = request.args.get('agent', 'YOUR_DEFAULT_AGENT_ID')
    js = generate_widget_js(agent_id, branding="Powered by Sybrant")
    return Response(js, mimetype='application/javascript')

@app.route('/leaserush-widget.js')
def serve_leaserush_widget():
    agent_id = request.args.get('agent', 'YOUR_DEFAULT_AGENT_ID')
    js = generate_widget_js(agent_id, branding="Powered by Leaserush")
    return Response(js, mimetype='application/javascript')


def generate_widget_js(agent_id, branding):
    return f"""
    // Create and inject the form modal
    const formModal = document.createElement("div");
    formModal.style.position = "fixed";
    formModal.style.top = "0";
    formModal.style.left = "0";
    formModal.style.width = "100%";
    formModal.style.height = "100%";
    formModal.style.backgroundColor = "rgba(0,0,0,0.6)";
    formModal.style.display = "flex";
    formModal.style.justifyContent = "center";
    formModal.style.alignItems = "center";
    formModal.style.zIndex = "9999";
    formModal.innerHTML = `
        <div style="background: white; padding: 30px; border-radius: 10px; text-align: center; width: 300px;">
            <h3>Start Assistant</h3>
            <input type="text" id="userName" placeholder="Your Name" style="width: 100%; margin-bottom: 10px; padding: 8px;" />
            <input type="email" id="userEmail" placeholder="Your Email" style="width: 100%; margin-bottom: 10px; padding: 8px;" />
            <button id="startAssistant" style="padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 5px;">Start</button>
        </div>
    `;
    document.body.appendChild(formModal);

    document.getElementById("startAssistant").onclick = () => {{
        const name = document.getElementById("userName").value.trim();
        const email = document.getElementById("userEmail").value.trim();
        if (!name || !email) {{
            alert("Please fill in all fields.");
            return;
        }}

        formModal.remove();

        // Create assistant tag
        const tag = document.createElement("elevenlabs-convai");
        tag.setAttribute("agent-id", "{agent_id}");
        document.body.appendChild(tag);

        const script = document.createElement("script");
        script.src = "https://elevenlabs.io/convai-widget/index.js";
        script.async = true;
        script.type = "text/javascript";
        document.body.appendChild(script);

        const check = setInterval(() => {{
            const widget = document.querySelector('elevenlabs-convai');
            if (!widget) return;
            const shadowRoot = widget.shadowRoot || widget.attachShadow?.();
            if (!shadowRoot) return;

            const brandingElem = shadowRoot.querySelector('[class*="poweredBy"], div[part="branding"]');
            if (brandingElem) {{
                brandingElem.textContent = "{branding}";
            }}

            const style = document.createElement("style");
            style.textContent = `
                div[part='branding'] {{
                    font-size: 12px !important;
                    font-family: Arial, sans-serif !important;
                    color: #888 !important;
                    text-align: right;
                    margin-top: 10px;
                    margin-bottom: 40px;
                    margin-right: 30px;
                }}
                div[part='feedback-button'], 
                img[alt*='logo'] {{
                    display: none !important;
                }}
            `;
            shadowRoot.appendChild(style);

            clearInterval(check);
        }}, 500);
    }};
    """
@app.route('/')
def home():
    return 'Voice Widget Masking Server Running!'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
