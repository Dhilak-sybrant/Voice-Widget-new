from flask import Flask, request, Response
import requests
import os
import logging
import sys

app = Flask(__name__)

# --- Logging Setup ---
log_filename = 'log.txt'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler(sys.stdout)
    ]
)

class PrintLogger:
    def write(self, message):
        if message.strip():
            logging.info(message.strip())
    def flush(self):
        pass

sys.stdout = PrintLogger()
sys.stderr = PrintLogger()

GOOGLE_SHEET_WEBHOOK_URL = 'https://script.google.com/macros/s/AKfycbysX7ZKHVAsxTmGoZeVBV65Q8imTgSEmwsrW27crcqJzDxQjCx9w-EeXMLnckmlFz38Uw/exec'

@app.route('/convai-widget.js')
def serve_sybrant_widget():
    agent_id = request.args.get('agent', 'YOUR_DEFAULT_AGENT_ID')
    branding = request.args.get('branding', 'Powered by Sybrant')
    js = generate_widget_js(agent_id, branding)
    return Response(js, mimetype='application/javascript')

@app.route('/leaserush-widget.js')
def serve_leaserush_widget():
    agent_id = request.args.get('agent', 'YOUR_DEFAULT_AGENT_ID')
    branding = request.args.get('branding', 'Powered by Leaserush')
    js = generate_widget_js(agent_id, branding)
    return Response(js, mimetype='application/javascript')

def generate_widget_js(agent_id, branding):
    return f"""(function() {{
        const tag = document.createElement("elevenlabs-convai");
        tag.setAttribute("agent-id", "{agent_id}");
        document.body.appendChild(tag);

        const script = document.createElement("script");
        script.src = "https://elevenlabs.io/convai-widget/index.js";
        script.async = true;
        document.body.appendChild(script);

        const observer = new MutationObserver(() => {{
            const widget = document.querySelector('elevenlabs-convai');
            if (!widget || !widget.shadowRoot) return;
            const shadowRoot = widget.shadowRoot;
            const brandingElem = shadowRoot.querySelector('[class*="poweredBy"], div[part="branding"]');
            if (brandingElem) brandingElem.textContent = "{branding}";

            if (!shadowRoot.querySelector("#custom-style")) {{
                const style = document.createElement("style");
                style.id = "custom-style";
                style.textContent = `
                    div[part='branding'] {{
                        font-size: 12px;
                        font-family: Arial, sans-serif;
                        color: #888;
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
                const clonedButton = startCallButton.cloneNode(true);
                startCallButton.style.display = 'none';
                const wrapper = document.createElement('div');
                wrapper.appendChild(clonedButton);
                startCallButton.parentElement.appendChild(wrapper);
                clonedButton.addEventListener('click', (e) => {{
                    e.preventDefault();
                    const expiry = localStorage.getItem("convai_form_submitted");
                    if (expiry && Date.now() < parseInt(expiry)) {{
                        startCallButton.click();
                    }} else {{
                        document.getElementById('visitor-form-modal').style.display = 'flex';
                    }}
                }});
            }}
        }});
        observer.observe(document.body, {{ childList: true, subtree: true }});

        window.addEventListener('DOMContentLoaded', () => {{
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
                const url = window.location.href;
                fetch('https://voice-widget-new-production.up.railway.app/log-visitor', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ name, mobile, email, url }})
                }});
                const expireTime = Date.now() + (5 * 60 * 1000);
                localStorage.setItem("convai_form_submitted", expireTime.toString());
                document.getElementById('visitor-form-modal').style.display = 'none';
                const widget = document.querySelector('elevenlabs-convai');
                const realBtn = widget?.shadowRoot?.querySelector('button[title="Start a call"]');
                realBtn?.click();
            }});
        }});
    }})();"""

@app.route('/log-visitor', methods=['POST'])
def log_visitor():
    data = request.json
    logging.info(f"Received visitor data: {data}")
    try:
        res = requests.post(GOOGLE_SHEET_WEBHOOK_URL, json=data)
        logging.info(f"Google Sheet Response: {res.status_code} - {res.text}")
    except Exception as e:
        logging.exception("Failed to send visitor data")
    return {"status": "ok"}

@app.route('/')
def home():
    return 'Voice Widget Masking Server Running!'

@app.route('/health')
def health():
    return {'status': 'healthy'}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
