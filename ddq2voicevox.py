from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import requests
import wave

class VOICEVOXHTTPRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args):
        BaseHTTPRequestHandler.__init__(self, *args)

    def do_POST(self):
        content_length = int(self.headers["content-length"])
        body = self.rfile.read(content_length).decode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "audio/wave")
        self.end_headers()
        self.wfile.write(generate_wav(body))

def generate_wav(text, speaker=1):
    host = 'localhost'
    port = 50021
    params = (
        ('text', text),
        ('speaker', speaker),
    )
    response1 = requests.post(
        f'http://{host}:{port}/audio_query',
        params=params
    )
    headers = {'Content-Type': 'application/json',}
    response2 = requests.post(
        f'http://{host}:{port}/synthesis',
        headers=headers,
        params=params,
        data=json.dumps(response1.json())
    )

    return response2.content

with HTTPServer(('0.0.0.0', 8275), VOICEVOXHTTPRequestHandler) as server:
    server.serve_forever()
