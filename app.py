# from flask import Flask, request, Response

# app = Flask(__name__)

# @app.route('/convai-widget.js')
# def serve_widget():
#     agent_id = request.args.get('agent', 'YOUR_DEFAULT_AGENT_ID')
#     js = f"""
#     const tag = document.createElement("elevenlabs-convai");
#     tag.setAttribute("agent-id", "{agent_id}");
#     document.body.appendChild(tag);

#     const script = document.createElement("script");
#     script.src = "https://elevenlabs.io/convai-widget/index.js";
#     script.async = true;
#     script.type = "text/javascript";
#     document.body.appendChild(script);

#     const check = setInterval(() => {{
#         const widget = document.querySelector('elevenlabs-convai');
#         if (!widget) return;
#         const shadowRoot = widget.shadowRoot || widget.attachShadow?.();
#         if (!shadowRoot) return;
#         const branding = shadowRoot.querySelector('[class*="poweredBy"], div[part="branding"]');
#         if (branding) {{
#             branding.textContent = "Powered by Sybrant";
#             clearInterval(check);
#         }}
#     }}, 500);
#     """
#     return Response(js, mimetype='application/javascript')

# @app.route('/')
# def home():
#     return 'Voice Widget Masking Server Running!'


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)


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

# def generate_widget_js(agent_id, branding):
#     return f"""
#     const tag = document.createElement("elevenlabs-convai");
#     tag.setAttribute("agent-id", "{agent_id}");
#     document.body.appendChild(tag);

#     const script = document.createElement("script");
#     script.src = "https://elevenlabs.io/convai-widget/index.js";
#     script.async = true;
#     script.type = "text/javascript";
#     document.body.appendChild(script);

#     const check = setInterval(() => {{
#         const widget = document.querySelector('elevenlabs-convai');
#         if (!widget) return;
#         const shadowRoot = widget.shadowRoot || widget.attachShadow?.();
#         if (!shadowRoot) return;
#         const brandingElem = shadowRoot.querySelector('[class*="poweredBy"], div[part="branding"]');
#         if (brandingElem) {{
#             brandingElem.textContent = "{branding}";
#             clearInterval(check);
#         }}
#     }}, 500);
#     """

def generate_widget_js(agent_id, branding):
    return f"""
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

        // Inject custom CSS
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
            /* Example: Hide feedback or logo */
            div[part='feedback-button'], 
            img[alt*='logo'] {{
                display: none !important;
            }}
        `;
        shadowRoot.appendChild(style);

        clearInterval(check);
    }}, 500);
    """


@app.route('/')
def home():
    return 'Voice Widget Masking Server Running!'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

