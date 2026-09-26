import json
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

import psycopg

BIND_HOST = os.environ.get("BIND_HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", "8000"))
DB_HOST = os.environ.get("DB_HOST", "db")
DB_NAME = os.environ.get("DB_NAME", "events")
DB_USER = os.environ.get("DB_USER", "events")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "whosthegoat?mielle")

MAX_NOTE_LENGTH = 200

try:
    conn = psycopg.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        autocommit=True,
    )
except Exception as exc:
    print(f"Could not connect to {DB_HOST}: {exc}")
    sys.exit(1)

print(f"Successfully connected to {DB_HOST}, now accepting requests.")

# Sql query to create the table required
conn.execute(
    """
    CREATE TABLE IF NOT EXISTS events (
        id SERIAL PRIMARY KEY,
        note TEXT NOT NULL
    )
    """
)


class Handler(BaseHTTPRequestHandler):
    def send_json(self, status: int, response):
        body = json.dumps(response).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def parse_note(self, raw: bytes):
        try:
            data = json.loads(raw)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return None

        if not isinstance(data, dict):
            return None
        if "note" not in data:
            return None

        note = data["note"]
        if not isinstance(note, str):
            return None
        if note == "":
            return None
        if len(note) > MAX_NOTE_LENGTH:
            return None

        return note

    def do_POST(self):
        if self.path == "/events":
            length = int(self.headers.get("Content-Length", "0"))
            body_bytes = self.rfile.read(length)

            note = self.parse_note(body_bytes)

            if note is None:
                body = b"Bad Request\n"
                self.send_response(400)
                self.send_header("Content-Type", "text/plain")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return

            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO events (note)
                    VALUES (%s)
                    RETURNING id
                    """,
                    (note,),
                )

                generated_id = cur.fetchone()[0]

            response = {"id": generated_id, "note": note}
            self.send_json(201, response)
        else:
            body = b"Not Found\n"
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    def do_GET(self):
        if self.path == "/events":
            rows = conn.execute(
                "SELECT id, note FROM events ORDER BY id"
            ).fetchall()

            response = [{"id": row[0], "note": row[1]} for row in rows]
            self.send_json(200, response)
        else:
            body = b"Not Found\n"
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)


if __name__ == "__main__":
    print(f"Listening on {BIND_HOST}:{PORT}")
    server = HTTPServer((BIND_HOST, PORT), Handler)
    server.serve_forever()
