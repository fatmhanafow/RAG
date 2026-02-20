# frontend/gradio_app.py
import gradio as gr
import requests

BACKEND = "http://localhost:8000"

def upload_and_index(file):
    if file is None:
        return "لطفاً فایل انتخاب کنید."
    try:
        files = {"file": open(file.name, "rb")}
        r = requests.post(f"{BACKEND}/upload", files=files)
        j = r.json()
        return f"آپلود و ایندکس موفق: {j.get('chunks_indexed', 0)} چانک ذخیره شد."
    except Exception as e:
        return f"خطا در آپلود: {e}"
    

def chat(message, history):
    if not message or not message.strip():
        return "", history or []

    try:
        data = {"q": message, "k": 5}
        r = requests.post(f"{BACKEND}/query", data=data)
        r.raise_for_status()
        res = r.json()
        
        answer = res.get("answer", "خطایی رخ داد.")
        
        # مطمئن می‌شیم history لیست از تاپل باشه
        new_history = history or []
        new_history.append((message, answer))
        
        return "", new_history
        
    except requests.exceptions.HTTPError as http_err:
        error_msg = f"خطای سرور: {http_err.response.status_code}"
        new_history = history or []
        new_history.append((message, error_msg))
        return "", new_history
    except Exception as e:
        error_msg = f"خطای ارتباط: {str(e)}"
        new_history = history or []
        new_history.append((message, error_msg))
        return "", new_history

with gr.Blocks(title="چت‌بات RAG بر اساس فایل‌های آپلود شده") as demo:
    gr.Markdown("# چت‌بات هوشمند بر اساس دانش آپلود شده")
    gr.Markdown("ابتدا فایل(txt یا pdf) آپلود کنید، سپس در چت سوال بپرسید.")
    
    with gr.Row():
        with gr.Column(scale=1):
            file_input = gr.File(label="آپلود فایل (txt یا pdf)")
            upload_btn = gr.Button("آپلود و ایندکس")
            upload_status = gr.Textbox(label="وضعیت آپلود", interactive=False)
        
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(height=600)
            msg = gr.Textbox(label="سوال شما", placeholder="سوال خود را اینجا بنویسید...")
            send_btn = gr.Button("ارسال")
    
    upload_btn.click(upload_and_index, inputs=file_input, outputs=upload_status)
    send_btn.click(chat, inputs=[msg, chatbot], outputs=[msg, chatbot])
    msg.submit(chat, inputs=[msg, chatbot], outputs=[msg, chatbot])  # با Enter هم بفرسته

if __name__ == "__main__":
    demo.launch(server_port=8002)




# def search_query(query):
#     try:
#         data = {"q": query, "k": 5}
#         r = requests.post(f"{BACKEND}/search", data=data)
#         res = r.json()
#     except Exception as e:
#         return f"Search failed: {e}"

#     results = res.get("results", [])
#     if not results:
#         return "No results found. Make sure documents are indexed and Weaviate is running."

#     out = ""
#     for i, h in enumerate(results, 1):
#         out += f"---- RANK {i} ----\nSource: {h.get('source','')}\n{h.get('text')}\n\n"
#     return out

# def search_query(query):
#     try:
#         data = {"q": query, "k": 5}
#         r = requests.post(f"{BACKEND}/query", data=data)  # /query جدید
#         res = r.json()
#     except Exception as e:
#         return f"Search failed: {e}"

#     answer = res.get("answer", "No answer")
#     sources = res.get("sources", [])

#     out = f"پاسخ: {answer}\n\n"
#     out += "منابع:\n"
#     for i, s in enumerate(sources, 1):
#         out += f"---- RANK {i} ----\nSource: {s}\n\n"
#     return out

# with gr.Blocks() as demo:
#     gr.Markdown("# RAG PoC — Upload & Search")
#     with gr.Row():
#         uploader = gr.File(label="Upload txt/pdf")
#         upload_btn = gr.Button("Upload & Index")
#         upload_status = gr.Textbox(label="Upload result", interactive=False)
#     with gr.Row():
#         query = gr.Textbox(label="Search Query")
#         search_btn = gr.Button("Search")
#         output = gr.Textbox(label="Results", lines=15)
#     upload_btn.click(upload_and_index, inputs=[uploader], outputs=[upload_status])
#     search_btn.click(search_query, inputs=[query], outputs=[output])

# if __name__ == "__main__":
#     demo.launch(server_port=8002)

