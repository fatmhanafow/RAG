# frontend/gradio_app.py
import gradio as gr
import requests

BACKEND = "http://localhost:8000"

def upload_and_index(file):
    try:
        files = {"file": open(file.name, "rb")}
        r = requests.post(f"{BACKEND}/upload", files=files)
        j = r.json()
    except Exception as e:
        return f"Upload failed: {e}"

    if not j.get("indexed", False):
        return f"Upload OK ({j.get('chunks_indexed',0)} chunks) — WARNING: not indexed (Weaviate not connected)."
    return f"Upload & index successful: {j.get('chunks_indexed',0)} chunks indexed."


def search_query(query):
    try:
        data = {"q": query, "k": 5}
        r = requests.post(f"{BACKEND}/search", data=data)
        res = r.json()
    except Exception as e:
        return f"Search failed: {e}"

    results = res.get("results", [])
    if not results:
        return "No results found. Make sure documents are indexed and Weaviate is running."

    out = ""
    for i, h in enumerate(results, 1):
        out += f"---- RANK {i} ----\nSource: {h.get('source','')}\n{h.get('text')}\n\n"
    return out

with gr.Blocks() as demo:
    gr.Markdown("# RAG PoC — Upload & Search")
    with gr.Row():
        uploader = gr.File(label="Upload txt/pdf")
        upload_btn = gr.Button("Upload & Index")
        upload_status = gr.Textbox(label="Upload result", interactive=False)
    with gr.Row():
        query = gr.Textbox(label="Search Query")
        search_btn = gr.Button("Search")
        output = gr.Textbox(label="Results", lines=15)
    upload_btn.click(upload_and_index, inputs=[uploader], outputs=[upload_status])
    search_btn.click(search_query, inputs=[query], outputs=[output])

if __name__ == "__main__":
    demo.launch(server_port=8002)

