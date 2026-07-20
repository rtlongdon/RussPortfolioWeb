#!/usr/bin/env python3
"""Double-click to serve this site locally and open it in your browser."""
import http.server
import os
import socketserver
import webbrowser

PORT = 8793

os.chdir(os.path.dirname(os.path.abspath(__file__)))

Handler = http.server.SimpleHTTPRequestHandler

try:
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        url = f"http://localhost:{PORT}/index.html"
        print(f"Serving {os.getcwd()}")
        print(f"Open {url}")
        print("Press Ctrl+C to stop.")
        webbrowser.open(url)
        httpd.serve_forever()
except OSError as e:
    print(f"Could not start server on port {PORT}: {e}")
    input("Press Enter to close...")
except KeyboardInterrupt:
    print("\nStopped.")
