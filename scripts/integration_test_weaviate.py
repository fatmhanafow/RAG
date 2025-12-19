import os
import sys

# Ensure project root is on sys.path so `backend` package is importable
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

print("Posting a small text file to /upload...")
files = {"file": ("it_test.txt", "Hello world. This is a test file for RAG.\n\nAnother paragraph to make multiple chunks.")}
resp = client.post("/upload", files=files)
print("Upload response:", resp.status_code, resp.json())

print("Running /search for 'test'...")
resp2 = client.post("/search", data={"q": "test", "k": 5})
print("Search response:", resp2.status_code, resp2.json())
