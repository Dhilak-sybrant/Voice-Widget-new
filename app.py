from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/convai-widget.js')
def serve_widget():
    agent_id = request.args.get('agent', 'YOUR_DEFAULT_AGENT_ID')
    js = f"""
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
        const branding = shadowRoot.querySelector('[class*="poweredBy"], div[part="branding"]');
        if (branding) {{
            branding.textContent = "Powered by Sybrant";
            clearInterval(check);
        }}
    }}, 500);
    """
    return Response(js, mimetype='application/javascript')

@app.route('/')
def home():
    return 'Voice Widget Masking Server Running!'
