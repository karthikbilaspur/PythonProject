from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import urllib.parse

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path == '/users':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            users = self.get_users()
            self.wfile.write(json.dumps(users).encode())
        elif parsed_path.path == '/posts':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            posts = self.get_posts()
            self.wfile.write(json.dumps(posts).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path == '/users':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            user_data = json.loads(body.decode())
            self.create_user(user_data)
            self.send_response(201)
            self.end_headers()
        elif parsed_path.path == '/posts':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            post_data = json.loads(body.decode())
            self.create_post(post_data)
            self.send_response(201)
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def get_users(self):
        # Call API to get users
        import requests
        response = requests.get('https://jsonplaceholder.typicode.com/users')
        return response.json()

    def get_posts(self):
        # Call API to get posts
        import requests
        response = requests.get('https://jsonplaceholder.typicode.com/posts')
        return response.json()

    def create_user(self, user_data):
        # Call API to create user
        import requests
        response = requests.post('https://jsonplaceholder.typicode.com/users', json=user_data)
        return response.json()

    def create_post(self, post_data):
        # Call API to create post
        import requests
        response = requests.post('https://jsonplaceholder.typicode.com/posts', json=post_data)
        return response.json()

def run_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, RequestHandler)
    print("Server running on port 8000...")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()