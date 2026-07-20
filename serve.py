#!/usr/bin/env python3
"""Double-click to serve this site locally and open it in your browser."""
import http.server
import os
import webbrowser

PORT = 8793

os.chdir(os.path.dirname(os.path.abspath(__file__)))

Handler = http.server.SimpleHTTPRequestHandler


class SingleUseServer(http.server.HTTPServer):
    # Windows lets SO_REUSEADDR silently hijack a port that's still actively
    # listening (not just one stuck in TIME_WAIT), so keep it off here.
    allow_reuse_address = False


try:
    with SingleUseServer(("", PORT), Handler) as httpd:
        url = f"http://localhost:{PORT}/index.html"
        print(f"Serving {os.getcwd()}")
        print(f"Open {url}")
        print("Closing the browser tab does NOT stop this server.")
        print("Press Ctrl+C (or close this window) to stop it and free the port.")
        webbrowser.open(url)
        httpd.serve_forever()
except OSError as e:
    print(f"Could not start server on port {PORT}: {e}")
    try:
        input("Press Enter to close...")
    except EOFError:
        pass
except KeyboardInterrupt:
    print("\nStopped.")
