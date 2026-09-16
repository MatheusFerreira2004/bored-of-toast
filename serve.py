from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial

if __name__ == "__main__":
    public = Path(__file__).resolve().parent / "dist"
    handler = partial(SimpleHTTPRequestHandler, directory=str(public))
    server = ThreadingHTTPServer(("127.0.0.1", 8000), handler)
    print("Bored of Toast: http://localhost:8000 — Ctrl+C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
