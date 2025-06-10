
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
    const tag = document.createElement("elevenlabs-convai");
    tag.setAttribute("agent-id", "{agent_id}");
    document.body.appendChild(tag);

    const script = document.createElement("script");
    script.src = "https://elevenlabs.io/convai-widget/index.js";
    script.async = true;
    script.type = "text/javascript";
    document.body.appendChild(script);

    const observer = new MutationObserver(() => {{
        const widget = document.querySelector('elevenlabs-convai');
        if (!widget) return;
        const shadowRoot = widget.shadowRoot;
        if (!shadowRoot) return;

        const brandingElem = shadowRoot.querySelector('[class*="poweredBy"], div[part="branding"]');
        if (brandingElem) {{
            brandingElem.textContent = "{branding}";
        }}

        if (!shadowRoot.querySelector("#custom-style")) {{
            const style = document.createElement("style");
            style.id = "custom-style";
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
        }}

        const startCallButton = shadowRoot.querySelector('button[title="Start a call"]');
        if (startCallButton && !startCallButton._hooked) {{
            startCallButton._hooked = true;
            startCallButton.addEventListener('click', (e) => {{
                e.stopPropagation();
                e.preventDefault();

                // Show modal
                document.getElementById('visitor-form-modal').style.display = 'flex';
            }});
        }}
    }});
    observer.observe(document.body, {{ childList: true, subtree: true }});

    // Inject form modal
    const modal = document.createElement('div');
    modal.id = 'visitor-form-modal';
    modal.style = `
        display: none;
        position: fixed;
        z-index: 99999;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.6);
        align-items: center;
        justify-content: center;
    `;
    modal.innerHTML = `
        <form id="visitor-form" style="
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            width: 320px;
            font-family: sans-serif;
        ">
            <h3 style="margin-bottom: 15px;">Tell us about you</h3>
            <input type="text" placeholder="Name" name="name" required style="margin-bottom: 10px; width: 100%; padding: 8px;" />
            <input type="tel" placeholder="Mobile (+91...)" name="mobile" required style="margin-bottom: 10px; width: 100%; padding: 8px;" />
            <input type="email" placeholder="Email" name="email" required style="margin-bottom: 20px; width: 100%; padding: 8px;" />
            <button type="submit" style="width: 100%; padding: 10px; background: #1e88e5; color: white; border: none; border-radius: 4px;">Start Call</button>
        </form>
    `;
    document.body.appendChild(modal);

    document.getElementById('visitor-form').addEventListener('submit', function(e) {{
        e.preventDefault();

        const name = this.name.value.trim();
        const mobile = this.mobile.value.trim();
        const email = this.email.value.trim();

        if (!name || !mobile || !email) {{
            alert("Please fill all fields.");
            return;
        }}

        // Optional: Send user data to server
        fetch('/log-visitor', {{
            method: 'POST',
            headers: {{ 'Content-Type': 'application/json' }},
            body: JSON.stringify({{ name, mobile, email }})
        }});

        // Close modal
        document.getElementById('visitor-form-modal').style.display = 'none';

        // Trigger actual call
        const widget = document.querySelector('elevenlabs-convai');
        const shadowRoot = widget?.shadowRoot;
        const realBtn = shadowRoot?.querySelector('button[title="Start a call"]');
        realBtn?.click();
    }});
    """


@app.route('/log-visitor', methods=['POST'])
def log_visitor():
    data = request.json
    print("Visitor Info:", data)  # You can save this to DB or CSV
    return {"status": "ok"}







@app.route('/')
def home():
    return 'Voice Widget Masking Server Running!'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
