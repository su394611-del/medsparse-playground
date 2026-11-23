import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import webbrowser


def main():
    parser = argparse.ArgumentParser(description="Serve the MedSparse playground on localhost.")
    parser.add_argument("--no-browser", action="store_true", help="Print the URL without opening a browser.")
    args = parser.parse_args()
    web_root = Path(__file__).resolve().parent / "web"
    handler = partial(SimpleHTTPRequestHandler, directory=str(web_root))
    with ThreadingHTTPServer(("127.0.0.1", 0), handler) as server:
        url = f"http://127.0.0.1:{server.server_port}/"
        print(url, flush=True)
        if not args.no_browser:
            webbrowser.open(url)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
