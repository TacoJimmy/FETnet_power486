import socketserver as socketserver
from http.server import SimpleHTTPRequestHandler


class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "home.html")
        self.end_headers()

        output = """
            <html lang="zh-Hant-TW">
                <head>
                    <meta charset="UTF-8">
                </head>

                <body>
                    你好，我是 miku3920
                </body>
            </html>
        """

        self.wfile.write(output.encode('utf-8'))


print("Serving at: http://localhost:8080")
socketserver.TCPServer(('127.0.0.1', 8080), MyHandler).serve_forever()