from flask import Flask, request, Response, render_template_string

app = Flask(__name__)

# In-memory storage for demonstration (use a database in production)
user_sessions = {}

@app.route('/convai-widget.js')
def serve_sybrant_widget():
    agent_id = request.args.get('agent', 'YOUR_DEFAULT_AGENT_ID')
    session_id = request.args.get('session_id')
    user_data = user_sessions.get(session_id, {})
    
    branding = "Powered by Sybrant"
    if user_data.get('company'):
        branding = f"Powered by {user_data.get('company')}"
    
    js = generate_widget_js(agent_id, branding)
    return Response(js, mimetype='application/javascript')

@app.route('/leaserush-widget.js')
def serve_leaserush_widget():
    agent_id = request.args.get('agent', 'YOUR_DEFAULT_AGENT_ID')
    session_id = request.args.get('session_id')
    user_data = user_sessions.get(session_id, {})
    
    branding = "Powered by Leaserush"
    if user_data.get('company'):
        branding = f"Powered by {user_data.get('company')}"
    
    js = generate_widget_js(agent_id, branding)
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

@app.route('/start-call', methods=['GET', 'POST'])
def start_call():
    if request.method == 'POST':
        # Generate a unique session ID (in production, use a better method)
        import uuid
        session_id = str(uuid.uuid4())
        
        # Store user data
        user_data = {
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'company': request.form.get('company'),
            'purpose': request.form.get('purpose')
        }
        user_sessions[session_id] = user_data
        
        # Render the page with the widget
        return render_template_string('''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Voice Assistant</title>
                <style>
                    body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
                    .user-info { background: #f5f5f5; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
                </style>
            </head>
            <body>
                <h1>Welcome to our Voice Assistant</h1>
                <div class="user-info">
                    <h3>Your Information:</h3>
                    <p><strong>Name:</strong> {{ user_data.name }}</p>
                    <p><strong>Email:</strong> {{ user_data.email }}</p>
                    <p><strong>Phone:</strong> {{ user_data.phone }}</p>
                    <p><strong>Company:</strong> {{ user_data.company }}</p>
                    <p><strong>Purpose:</strong> {{ user_data.purpose }}</p>
                </div>
                
                <h2>Start your conversation below:</h2>
                <script src="/convai-widget.js?agent=YOUR_AGENT_ID&session_id={{ session_id }}"></script>
            </body>
            </html>
        ''', user_data=user_data, session_id=session_id)
    
    # Show the form for GET requests
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Start a Call</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; }
                form { background: #f5f5f5; padding: 20px; border-radius: 5px; }
                label { display: block; margin-top: 10px; }
                input, textarea, select { width: 100%; padding: 8px; margin-top: 5px; box-sizing: border-box; }
                button { background: #4CAF50; color: white; padding: 10px 15px; border: none; border-radius: 4px; margin-top: 15px; cursor: pointer; }
                button:hover { background: #45a049; }
            </style>
        </head>
        <body>
            <h1>Start a Voice Call</h1>
            <p>Please provide your details before starting the conversation.</p>
            
            <form method="POST" action="/start-call">
                <label for="name">Full Name:</label>
                <input type="text" id="name" name="name" required>
                
                <label for="email">Email:</label>
                <input type="email" id="email" name="email" required>
                
                <label for="phone">Phone Number:</label>
                <input type="tel" id="phone" name="phone">
                
                <label for="company">Company (optional):</label>
                <input type="text" id="company" name="company">
                
                <label for="purpose">Purpose of Call:</label>
                <select id="purpose" name="purpose" required>
                    <option value="">-- Select a purpose --</option>
                    <option value="Sales Inquiry">Sales Inquiry</option>
                    <option value="Support">Support</option>
                    <option value="Feedback">Feedback</option>
                    <option value="Other">Other</option>
                </select>
                
                <button type="submit">Start Voice Call</button>
            </form>
        </body>
        </html>
    ''')

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Voice Widget Masking Server</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; text-align: center; }
            .button { display: inline-block; background: #4CAF50; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; margin: 10px; }
            .button:hover { background: #45a049; }
        </style>
    </head>
    <body>
        <h1>Voice Widget Masking Server</h1>
        <p>This server provides customized voice widget integration.</p>
        
        <a href="/start-call" class="button">Start a New Call</a>
        <p>or</p>
        <p>Use the widget directly by including this script:</p>
        <code>&lt;script src="/convai-widget.js?agent=YOUR_AGENT_ID"&gt;&lt;/script&gt;</code>
    </body>
    </html>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
