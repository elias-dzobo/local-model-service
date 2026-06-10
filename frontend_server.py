from flask import Flask, render_template_string, jsonify
import requests

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 20px;
            gap: 24px;
        }
        .container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 16px;
            padding: 40px;
            max-width: 600px;
            width: 100%;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }
        .container.coach {
            background: rgba(255, 255, 255, 0.95);
            border-left: 4px solid #10b981;
        }
        h1 {
            color: #1a1a2e;
            margin-bottom: 24px;
            font-size: 1.8rem;
        }
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 14px 28px;
            font-size: 1rem;
            border-radius: 8px;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            font-weight: 600;
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
        }
        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        .btn.green {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        }
        .btn.green:hover {
            box-shadow: 0 8px 20px rgba(16, 185, 129, 0.4);
        }
        .results {
            margin-top: 24px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
            display: none;
        }
        .results.show {
            display: block;
        }
        .results pre {
            white-space: pre-wrap;
            word-wrap: break-word;
            font-size: 0.9rem;
            color: #333;
        }
        .loading {
            display: none;
            margin-top: 20px;
            color: #667eea;
            font-weight: 500;
        }
        .loading.show {
            display: block;
        }
        .error {
            color: #dc3545;
            margin-top: 16px;
            display: none;
        }
        .error.show {
            display: block;
        }
        .info {
            margin-top: 16px;
            padding: 12px;
            background: #e7f1ff;
            border-radius: 6px;
            color: #0056b3;
            font-size: 0.9rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Value at Risk Request</h1>
        <div class="info">
            <strong>Endpoint:</strong> https://cripsdmagent.azurewebsites.net/v1/results<br>
            <strong>Request Body:</strong> {"type": "Value at Risk"}
        </div>
        <br>
        <button class="btn" id="fetchBtn" onclick="fetchResults()">
            Fetch Results
        </button>
        <div class="loading" id="loading">Loading...</div>
        <div class="error" id="error"></div>
        <div class="results" id="results">
            <h3 style="margin-bottom: 12px; color: #1a1a2e;">Response:</h3>
            <pre id="responseData"></pre>
        </div>
    </div>

    <div class="container coach">
        <h1>Retail Coach</h1>
        <div class="info">
            <strong>Endpoint:</strong> https://cripsdmagent.azurewebsites.net/v1/retail_coach/response<br>
            <strong>Request Body:</strong> {"session_id": "10", "message": "explain the impact assessment data"}
        </div>
        <br>
        <button class="btn green" id="coachBtn" onclick="fetchCoachResponse()">
            Get Coach Response
        </button>
        <div class="loading" id="coachLoading">Loading...</div>
        <div class="error" id="coachError"></div>
        <div class="results" id="coachResults">
            <h3 style="margin-bottom: 12px; color: #1a1a2e;">Response:</h3>
            <pre id="coachResponseData"></pre>
        </div>
    </div>

    <script>
        async function fetchResults() {
            const btn = document.getElementById('fetchBtn');
            const loading = document.getElementById('loading');
            const results = document.getElementById('results');
            const error = document.getElementById('error');
            const responseData = document.getElementById('responseData');

            btn.disabled = true;
            loading.classList.add('show');
            results.classList.remove('show');
            error.classList.remove('show');

            try {
                const response = await fetch('/api/results');
                const data = await response.json();
                
                if (response.ok) {
                    responseData.textContent = JSON.stringify(data, null, 2);
                    results.classList.add('show');
                } else {
                    error.textContent = 'Error: ' + (data.error || 'Unknown error');
                    error.classList.add('show');
                }
            } catch (err) {
                error.textContent = 'Error: ' + err.message;
                error.classList.add('show');
            } finally {
                btn.disabled = false;
                loading.classList.remove('show');
            }
        }

        async function fetchCoachResponse() {
            const btn = document.getElementById('coachBtn');
            const loading = document.getElementById('coachLoading');
            const results = document.getElementById('coachResults');
            const error = document.getElementById('coachError');
            const responseData = document.getElementById('coachResponseData');

            btn.disabled = true;
            loading.classList.add('show');
            results.classList.remove('show');
            error.classList.remove('show');

            try {
                const response = await fetch('/api/retail_coach');
                const data = await response.json();
                
                if (response.ok) {
                    responseData.textContent = JSON.stringify(data, null, 2);
                    results.classList.add('show');
                } else {
                    error.textContent = 'Error: ' + (data.error || 'Unknown error');
                    error.classList.add('show');
                }
            } catch (err) {
                error.textContent = 'Error: ' + err.message;
                error.classList.add('show');
            } finally {
                btn.disabled = false;
                loading.classList.remove('show');
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/results')
def get_results():
    try:
        response = requests.post(
            'https://cripsdmagent.azurewebsites.net/v1/results',
            json={'type': 'Value at Risk'},
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/retail_coach')
def get_retail_coach():
    try:
        response = requests.post(
            'https://cripsdmagent.azurewebsites.net/v1/retail_coach/respond',
            json={
                'session_id': '10',
                'message': 'explain the impact assessment data'
            },
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting frontend server on http://localhost:3000")
    app.run(host='0.0.0.0', port=3000, debug=True)

 