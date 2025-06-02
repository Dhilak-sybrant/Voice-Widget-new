from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/')
def home():
    return 'Custom ElevenLabs Widget is running!'

@app.route('/convai-widget.js')
def widget():
    agent_id = request.args.get('agent') or request.args.get('data-agent') or request.args.get('agent-id') or 'agent_01jwnymxeaeg29wjmdm16pmf89'

    js_code = f'''
    // Inject ElevenLabs widget
    const script = document.createElement("script");
    script.src = "https://elevenlabs.io/convai-widget/index.js";
    script.async = true;
    document.head.appendChild(script);

    const tag = document.createElement("elevenlabs-convai");
    tag.setAttribute("agent-id", "{agent_id}");
    document.body.appendChild(tag);

    // Replace branding in shadow DOM
    const interval = setInterval(() => {{
        const widget = document.querySelector('elevenlabs-convai');
        if (!widget) return;

        const shadow = widget.shadowRoot || widget.attachShadow?.();
        if (!shadow) return;

        const branding = shadow.querySelector('[class*="poweredBy"], div[part="branding"]');
        if (branding) {{
            branding.textContent = "Powered by Sybrant";
            clearInterval(interval);
        }}
    }}, 300);
    '''

    return Response(js_code, mimetype='application/javascript')
