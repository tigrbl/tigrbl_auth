# Local TOTP enrollment demo

Run these commands from this directory with Python, uv, and Node.js installed.

```sh
npm ci
npm run build
uv run --project ../../.. --locked --with qrcode==8.2 python server.py
```

Open `http://127.0.0.1:8769`. Scan the QR code with an authenticator, submit its current code, then wait for a fresh code to verify sign-in. Submitting either accepted code again is rejected. Enrollment expires after five minutes.

The loopback service uses an expiring synthetic enrollment in `.local/totp.sqlite3`. Use only demo secrets. Restart enrollment to replace the current browser's demo credential.
