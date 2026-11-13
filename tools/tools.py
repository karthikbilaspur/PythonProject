"""
Combined tools: config + email sender + html->md converter + users/posts proxy server
Usage:
    python tools.py send --to recipient@example.com --name John --subject "Test HTML Email"
    python tools.py convert -i email_template.html -o email_template.md
    python tools.py serve --port 8000
"""
import argparse
import json
import logging
import os
import smtplib
import urllib.parse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any

logging.basicConfig(level=logging.INFO)

# [STRIPPED 75 bytes]
# 1. CONFIG (old snippet #1)
# [STRIPPED 75 bytes]
class Config:
    SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
    FROM_EMAIL = os.environ.get('FROM_EMAIL', 'your-email@gmail.com')
    # Never hardcode a real password. Use env var / app password.
    # Gmail: use an App Password, not your normal password.
    PASSWORD = os.environ.get('PASSWORD', 'your-password')

    def validate(self):
        if self.PASSWORD in ('', 'your-password'):
            raise ValueError("Set PASSWORD env var (use a Gmail App Password, not your login password)")
        if self.FROM_EMAIL in ('', 'your-email@gmail.com'):
            raise ValueError("Set FROM_EMAIL env var")

# [STRIPPED 75 bytes]
# 2. EMAIL SENDER (old snippet #2) - fixed duplicate return + SMTP cleanup
# [STRIPPED 75 bytes]
class EmailSender:
    def __init__(self, config: Config):
        self.config = config

    def render_template(self, template_path: str, data: dict[str, Any]) -> str:
        with open(template_path, 'r', encoding='utf-8') as f:
            # Jinja2 Template - for untrusted templates use SandboxedEnvironment
            from jinja2 import Template
            template = Template(f.read())
        return template.render(data)  # FIX: removed duplicate unreachable return

    def send_email(self, subject: str, to_email: str, name: str,
                   template_path: str = 'email_template.html') -> bool:
        html_content = self.render_template(template_path, {'name': name})

        msg = MIMEMultipart()
        msg['From'] = self.config.FROM_EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(html_content, 'html'))

        try:
            # FIX: with-block ensures server.quit() even on error
            with smtplib.SMTP(self.config.SMTP_SERVER, self.config.SMTP_PORT, timeout=30) as server:
                server.starttls()
                server.login(self.config.FROM_EMAIL, self.config.PASSWORD)
                server.sendmail(self.config.FROM_EMAIL, to_email, msg.as_string())
            logging.info(f'Email sent to {to_email}')
            return True
        except Exception as e:
            logging.error(f'Error sending email: {e}')
            return False

# [STRIPPED 75 bytes]
# 3. HTML -> MARKDOWN (old snippet #3)
# [STRIPPED 75 bytes]
def convert_html_to_md(html_file: str, md_file: str) -> None:
    import html2text
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    h = html2text.HTML2Text()
    h.ignore_links = False
    md_content = h.handle(html_content)
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(md_content)
    print(f"Converted {html_file} -> {md_file}")

# [STRIPPED 75 bytes]
# 4. HTTP SERVER / JSONPlaceholder proxy (old snippet #4) - fixed error handling
# [STRIPPED 75 bytes]
import requests

BASE_URL = 'https://jsonplaceholder.typicode.com'

def _proxy_get(path: str):
    r = requests.get(f'{BASE_URL}{path}', timeout=10)
    r.raise_for_status()
    return r.json()

def _proxy_post(path: str, data: dict[str, Any]):
    r = requests.post(f'{BASE_URL}{path}', json=data, timeout=10)
    r.raise_for_status()
    return r.json()

class RequestHandler(BaseHTTPRequestHandler):
    # Silence default logging, use logging module instead
    def log_message(self, format: str, *args: Any) -> None:
        logging.info("%s - %s", self.address_string(), format % args)

    def _send_json(self, status: int, data: Any) -> None:
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json_body(self) -> dict[str, Any]:
        length = int(self.headers.get('Content-Length', 0))
        if length == 0:
            return {}
        body = self.rfile.read(length)
        return json.loads(body.decode())

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path
        try:
            if path in ('/users', '/posts'):
                self._send_json(200, _proxy_get(path))
            else:
                self._send_json(404, {'error': 'not found'})
        except requests.RequestException as e:
            self._send_json(502, {'error': f'upstream failed: {e}'})

    def do_POST(self):
        path = urllib.parse.urlparse(self.path).path
        try:
            if path in ('/users', '/posts'):
                data = self._read_json_body()
                # JSONPlaceholder doesn't persist, returns fake id
                result = _proxy_post(path, data)
                self._send_json(201, result)
            else:
                self._send_json(404, {'error': 'not found'})
        except json.JSONDecodeError:
            self._send_json(400, {'error': 'invalid JSON'})
        except requests.RequestException as e:
            self._send_json(502, {'error': f'upstream failed: {e}'})

def run_server(port: int = 8000):
    httpd = HTTPServer(('', port), RequestHandler)
    print(f"Server running on port {port}...  GET /users  GET /posts  POST /users  POST /posts")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        httpd.shutdown()

# [STRIPPED 75 bytes]
# CLI
# [STRIPPED 75 bytes]
def main():
    parser = argparse.ArgumentParser(description="Email + converter + proxy server")
    sub = parser.add_subparsers(dest='command', required=True)

    p_send = sub.add_parser('send', help='Send templated HTML email')
    p_send.add_argument('--to', required=True)
    p_send.add_argument('--name', default='John')
    p_send.add_argument('--subject', default='Test HTML Email')
    p_send.add_argument('--template', default='email_template.html')

    p_conv = sub.add_parser('convert', help='Convert HTML to Markdown')
    p_conv.add_argument('-i', '--input', required=True)
    p_conv.add_argument('-o', '--output', required=True)

    p_serve = sub.add_parser('serve', help='Start proxy server')
    p_serve.add_argument('--port', type=int, default=8000)

    args = parser.parse_args()

    if args.command == 'send':
        config = Config()
        config.validate()
        sender = EmailSender(config)
        ok = sender.send_email(args.subject, args.to, args.name, args.template)
        raise SystemExit(0 if ok else 1)

    elif args.command == 'convert':
        convert_html_to_md(args.input, args.output)

    elif args.command == 'serve':
        run_server(args.port)

if __name__ == '__main__':
    main()