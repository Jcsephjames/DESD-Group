"""HTTP service for demo organic certificate checks."""

import json
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class CertificationHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/verify":
            self.send_json(404, {"error": "Unknown endpoint."})
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 4096:
                raise ValueError("Invalid request length.")
            request = json.loads(self.rfile.read(length))
            if not isinstance(request, dict):
                raise ValueError("Expected a JSON object.")
            certificate_id = request.get("certificate_id")
            query_id = request.get("query_id")
            if not isinstance(certificate_id, str):
                raise ValueError("Expected a certificate number.")
            if not isinstance(query_id, str) or not query_id.strip():
                raise ValueError("Expected a query ID.")
        except ValueError:
            self.send_json(400, {"error": "Supply certificate_id and query_id as text."})
            return

        valid = re.fullmatch(r"BIO-[0-9]+", certificate_id.strip()) is not None
        result = {"query_id": query_id, "valid": valid}
        if not valid:
            result["reason"] = "Enter a certificate number with BIO- followed by digits."
        self.send_json(200, result)

    def send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    with ThreadingHTTPServer(("0.0.0.0", 8000), CertificationHandler) as server:
        server.serve_forever()
