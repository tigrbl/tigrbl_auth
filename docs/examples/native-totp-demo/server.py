"""Loopback-only demo of enrollment, a fresh challenge, and replay rejection."""

from base64 import b64encode
from http.cookies import CookieError, SimpleCookie
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from io import BytesIO
import json
from pathlib import Path
import re
import secrets
import sqlite3
import time

from qrcode import make
from qrcode.image.svg import SvgPathImage
from tba_provider_authenticator_totp_local import TotpLocalAuthenticator, new_secret, provisioning_uri

ROOT = Path(__file__).resolve().parent
ADDRESS = ("127.0.0.1", 8769)
ORIGIN = f"http://{ADDRESS[0]}:{ADDRESS[1]}"
PROVIDER = TotpLocalAuthenticator()


class Demo(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT / "dist"), **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        self.send_header("Referrer-Policy", "no-referrer")
        super().end_headers()

    def do_POST(self):
        if self.headers.get("Origin") != ORIGIN or self.headers.get("Host") != ORIGIN.removeprefix("http://"):
            return self.respond(403, {"message": "Open the demo on its loopback address."})
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 512:
                raise ValueError
            payload = json.loads(self.rfile.read(length))
            cookie = SimpleCookie(self.headers.get("Cookie", "")).get("totp_demo")
            handle = cookie.value if cookie else ""
            if not isinstance(payload, dict):
                raise ValueError
        except (ValueError, CookieError):
            return self.respond(400, {"message": "Invalid request."})

        with sqlite3.connect(ROOT / ".local" / "totp.sqlite3") as db:
            db.execute("BEGIN IMMEDIATE")
            if self.path == "/api/start":
                if re.fullmatch(r"[A-Za-z0-9_-]{43}", handle):
                    db.execute("DELETE FROM enrollments WHERE handle = ?", (handle,))
                handle, secret = secrets.token_urlsafe(32), new_secret()
                db.execute("DELETE FROM enrollments WHERE expires < ?", (int(time.time()),))
                db.execute("INSERT INTO enrollments VALUES (?, ?, ?, 0, -1, 0)",
                           (handle, secret, int(time.time()) + 300))
                uri = provisioning_uri(secret, "demo@example.test", "Tigrbl Auth demo")
                image = BytesIO()
                make(uri, image_factory=SvgPathImage).save(image)
                qr = "data:image/svg+xml;base64," + b64encode(image.getvalue()).decode("ascii")
                return self.respond(200, {"secret": secret, "qr": qr}, handle)
            if self.path not in ("/api/confirm", "/api/challenge"):
                return self.respond(404, {"message": "Unknown action."})
            row = db.execute("SELECT secret, expires, active, last_step, attempts FROM enrollments WHERE handle = ?",
                             (handle,)).fetchone()
            challenge = self.path == "/api/challenge"
            if row is None or row[1] < int(time.time()) or bool(row[2]) != challenge or row[4] >= 6:
                return self.respond(409, {"message": "Start enrollment again."})
            step = PROVIDER.verify_step(payload.get("code"), row[0], window=1, after_step=row[3])
            if step is None:
                db.execute("UPDATE enrollments SET attempts = attempts + 1 WHERE handle = ?", (handle,))
                return self.respond(400, {"message": "The code is invalid or has already been used."})
            db.execute("UPDATE enrollments SET active = 1, last_step = ?, attempts = 0, expires = ? WHERE handle = ?",
                       (step, int(time.time()) + 900, handle))
            message = "Sign-in code accepted." if challenge else "Authenticator enrolled. Wait for a fresh code."
            return self.respond(200, {"message": message})

    def respond(self, status, body, handle=None):
        value = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(value)))
        if handle:
            self.send_header("Set-Cookie", f"totp_demo={handle}; Path=/; HttpOnly; SameSite=Strict")
        self.end_headers()
        self.wfile.write(value)


if __name__ == "__main__":
    if not (ROOT / "dist" / "index.html").is_file():
        raise SystemExit("Build the demo frontend first.")
    (ROOT / ".local").mkdir(mode=0o700, exist_ok=True)
    with sqlite3.connect(ROOT / ".local" / "totp.sqlite3") as db:
        db.execute("""CREATE TABLE IF NOT EXISTS enrollments (
            handle TEXT PRIMARY KEY, secret TEXT, expires INTEGER, active INTEGER,
            last_step INTEGER, attempts INTEGER
        )""")
    print(f"Open {ORIGIN}", flush=True)
    ThreadingHTTPServer(ADDRESS, Demo).serve_forever()
