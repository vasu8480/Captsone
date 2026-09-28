#!/usr/bin/env python3
"""Generate HTML documentation files for GitHub Pages."""

import os

os.makedirs('docs', exist_ok=True)

# Landing page
landing = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Starter App</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            padding: 50px;
            max-width: 600px;
            text-align: center;
        }
        h1 { color: #2c3e50; margin-bottom: 20px; font-size: 2.5em; }
        .subtitle { color: #7f8c8d; font-size: 1.2em; margin-bottom: 40px; }
        .links { display: flex; flex-direction: column; gap: 15px; }
        a {
            display: inline-block;
            padding: 15px 30px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
            transition: background 0.3s;
        }
        a:hover { background: #764ba2; }
        .description { color: #555; margin-top: 30px; line-height: 1.6; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧮 Starter App</h1>
        <p class="subtitle">Calculator API with CI/CD Pipelines</p>
        <div class="links">
            <a href="api.html">📚 API Documentation & Tester</a>
            <a href="README.html">📖 Read the README</a>
        </div>
        <div class="description">
            <p>A demonstration capstone project featuring:</p>
            <ul style="text-align: left; display: inline-block; margin-top: 20px;">
                <li>✅ Automated CI/CD pipelines</li>
                <li>✅ Docker containerization</li>
                <li>✅ Linting & testing</li>
                <li>✅ Staged deployment</li>
                <li>✅ Interactive API tester</li>
            </ul>
        </div>
    </div>
</body>
</html>"""

# README page
readme = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Starter App - README</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1, h2 { color: #2c3e50; margin: 30px 0 15px 0; }
        h1 { font-size: 2em; border-bottom: 3px solid #667eea; padding-bottom: 10px; }
        code { background: #f5f5f5; padding: 2px 6px; border-radius: 3px; color: #d73814; }
        pre { background: #f5f5f5; padding: 15px; border-radius: 5px; overflow-x: auto; margin: 15px 0; }
        a { color: #667eea; text-decoration: none; }
        a:hover { text-decoration: underline; }
        .back {
            display: inline-block;
            margin-bottom: 20px;
            padding: 10px 20px;
            background: #667eea;
            color: white;
            border-radius: 5px;
            text-decoration: none;
        }
        .back:hover { background: #764ba2; }
    </style>
</head>
<body>
    <div class="container">
        <a href="/" class="back">← Back to Home</a>
        <h1>Capstone Starter App</h1>
        <p>A practical CI/CD capstone: a tiny calculator API with enough runtime surface to test linting, testing, container builds, release tagging, staged deployment, smoke checks, and rollback.</p>
        <h2>API Endpoints</h2>
        <ul>
            <li><code>/</code> returns service metadata and available endpoints.</li>
            <li><code>/health</code> returns liveness information.</li>
            <li><code>/ready</code> returns readiness information.</li>
            <li><code>/operations</code> returns the supported calculator operations.</li>
            <li><code>/calculate?op=add&a=2&b=3</code> performs a calculation.</li>
        </ul>
        <h2>Local Development</h2>
        <pre><code>cd starter-app
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m src.app
curl http://127.0.0.1:8000/</code></pre>
        <h2>Docker</h2>
        <pre><code>docker build -t starter-app:local .
docker run --rm -p 8000:8000 starter-app:local
curl http://127.0.0.1:8000/health</code></pre>
    </div>
</body>
</html>"""

# API page (simplified - just listing endpoints)
api = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Starter App API</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }
        h1, h2 { color: #2c3e50; margin: 30px 0 15px 0; }
        h1 { font-size: 2em; border-bottom: 3px solid #667eea; padding-bottom: 10px; }
        .subtitle { color: #7f8c8d; font-size: 1.1em; margin-bottom: 30px; }
        .endpoint {
            background: #f9f9f9;
            padding: 15px;
            margin: 15px 0;
            border-left: 4px solid #667eea;
            border-radius: 5px;
        }
        .method {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 3px;
            font-weight: bold;
            color: white;
            margin-right: 10px;
            font-family: monospace;
        }
        .get { background: #61affe; }
        code { background: #f5f5f5; padding: 2px 6px; border-radius: 3px; font-family: monospace; color: #d73814; }
        a { color: #667eea; text-decoration: none; }
        a:hover { text-decoration: underline; }
        .back {
            display: inline-block;
            margin-bottom: 20px;
            padding: 10px 20px;
            background: #667eea;
            color: white;
            border-radius: 5px;
            text-decoration: none;
        }
        .back:hover { background: #764ba2; }
    </style>
</head>
<body>
    <div class="container">
        <a href="/" class="back">← Back to Home</a>
        <h1>🧮 API Documentation</h1>
        <p class="subtitle">Starter App Calculator API</p>
        <h2>Endpoints</h2>
        <div class="endpoint">
            <span class="method get">GET</span> <code>/</code>
            <p>Returns service metadata and available endpoints.</p>
        </div>
        <div class="endpoint">
            <span class="method get">GET</span> <code>/health</code>
            <p>Returns liveness information.</p>
        </div>
        <div class="endpoint">
            <span class="method get">GET</span> <code>/ready</code>
            <p>Returns readiness information.</p>
        </div>
        <div class="endpoint">
            <span class="method get">GET</span> <code>/operations</code>
            <p>Returns the supported calculator operations.</p>
        </div>
        <div class="endpoint">
            <span class="method get">GET</span> <code>/calculate?op=add&a=2&b=3</code>
            <p>Performs a calculation. Operations: add, subtract, multiply, divide.</p>
        </div>
    </div>
</body>
</html>"""

with open('docs/index.html', 'w') as f:
    f.write(landing)
with open('docs/README.html', 'w') as f:
    f.write(readme)
with open('docs/api.html', 'w') as f:
    f.write(api)

print("✅ Generated all documentation pages")
