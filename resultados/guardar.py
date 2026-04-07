#!/usr/bin/env python3
import json, os
from http.server import HTTPServer, BaseHTTPRequestHandler

COMENTARIOS_FILE = "/data/data/com.termux/files/home/mandri_data/comentarios.json"
FOTOS_FILE = "/data/data/com.termux/files/home/mandri_data/fotos.json"

for f in [COMENTARIOS_FILE, FOTOS_FILE]:
    if not os.path.exists(f):
        with open(f, 'w') as file:
            json.dump([], file)

class Handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        if self.path == '/api/comentarios':
            with open(COMENTARIOS_FILE, 'r') as f:
                self.wfile.write(json.dumps(json.load(f)).encode())
        elif self.path == '/api/fotos':
            with open(FOTOS_FILE, 'r') as f:
                self.wfile.write(json.dumps(json.load(f)).encode())
    
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        data = json.loads(self.rfile.read(length))
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        if self.path == '/api/comentarios':
            with open(COMENTARIOS_FILE, 'r') as f:
                c = json.load(f)
            c.append(data)
            with open(COMENTARIOS_FILE, 'w') as f:
                json.dump(c, f)
        elif self.path == '/api/fotos':
            with open(FOTOS_FILE, 'r') as f:
                fts = json.load(f)
            fts.append(data)
            with open(FOTOS_FILE, 'w') as f:
                json.dump(fts, f)

print("API en puerto 8081")
HTTPServer(("", 8081), Handler).serve_forever()
