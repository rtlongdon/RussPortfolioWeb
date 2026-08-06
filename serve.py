#!/usr/bin/env python3
"""Double-click to serve this site locally and open it in your browser."""
import http.server
import os
import webbrowser
from urllib.parse import unquote

PORT = 8793

app_root = os.path.dirname(os.path.abspath(__file__))
greatefb_docs = os.path.join(os.path.dirname(app_root), "GreatEFB", "docs")
approachtrainer_docs = os.path.join(os.path.dirname(app_root), "ApproachTrainer", "Docs")
adahrs_docs = os.path.join(os.path.dirname(app_root), "ADAHRS_Project", "docs")

os.chdir(app_root)


class MultiPathHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        path = unquote(path)
        if path.startswith("/greatefb-docs/"):
            # Strip /greatefb-docs/ and serve from GreatEFB/docs
            path = path[15:]  # Remove "/greatefb-docs/"
            return os.path.join(greatefb_docs, path.lstrip("/"))
        elif path.startswith("/approachtrainer-docs/"):
            # Strip /approachtrainer-docs/ and serve from ApproachTrainer/Docs
            path = path[21:]  # Remove "/approachtrainer-docs/"
            return os.path.join(approachtrainer_docs, path.lstrip("/"))
        elif path.startswith("/adahrs-docs/"):
            # Strip /adahrs-docs/ and serve from ADAHRS_Project/docs
            path = path[13:]  # Remove "/adahrs-docs/"
            return os.path.join(adahrs_docs, path.lstrip("/"))
        else:
            # Default: serve from AppShowcase root
            return super().translate_path(path)


class SingleUseServer(http.server.HTTPServer):
    # Windows lets SO_REUSEADDR silently hijack a port that's still actively
    # listening (not just one stuck in TIME_WAIT), so keep it off here.
    allow_reuse_address = False


try:
    with SingleUseServer(("", PORT), MultiPathHandler) as httpd:
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
