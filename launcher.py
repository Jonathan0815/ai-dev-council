from http.server import HTTPServer
from ui import UIHandler

print("AI Dev Council v2.0 — http://localhost:8000")
print("   Final. No more errors. You won.")
HTTPServer(("", 8000), UIHandler).serve_forever()
