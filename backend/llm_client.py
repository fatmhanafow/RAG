
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()   

class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("APTAR_API_KEY")
        self.base_url = os.getenv("APTAR_BASE_URL", "https://core.aptar.ir/v1/chat/completions")
        self.model = os.getenv("APTAR_MODEL", "qwen3-32b")

        if not self.api_key:
            raise ValueError(
                "APTAR_API_KEY پیدا نشد! "
                "لطفاً آن را در فایل .env تعریف کنید یا به صورت متغیر محیطی ست کنید."
            )

    def stream_generate(self, prompt: str):
        """
        استریم پاسخ (کلمه به کلمه)
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "top_p": 1,
            "max_tokens": 2000,
            "stream": True  # استریم فعال
        }

        try:
            with requests.post(self.base_url, json=payload, headers=headers, stream=True, timeout=120) as response:
                response.raise_for_status()
                for line in response.iter_lines():
                    if line:
                        decoded_line = line.decode("utf-8").strip()
                        if decoded_line.startswith("data: "):
                            if decoded_line == "data: [DONE]":
                                break
                            data_str = decoded_line[6:]  # حذف "data: "
                            try:
                                data = json.loads(data_str)
                                if "choices" in data and data["choices"]:
                                    delta = data["choices"][0].get("delta", {})
                                    content = delta.get("content", "")
                                    if content:
                                        yield content
                            except json.JSONDecodeError:
                                continue  # اگر خط JSON خراب بود، رد کن
        except requests.exceptions.RequestException as e:
            yield f"\n\nخطا در استریم: {str(e)}"
        except Exception as e:
            yield f"\n\nخطای غیرمنتظره: {str(e)}"

    def generate(self, prompt: str) -> str:
        """
        نسخه غیراستریم (برای وقتی که استریم کار نکرد یا نیاز به پاسخ کامل داشتی)
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "top_p": 1,
            "max_tokens": 2000,
            "stream": False
        }

        try:
            response = requests.post(self.base_url, json=payload, headers=headers, timeout=60)
            response.raise_for_status()
            data = response.json()

            if "choices" in data and data["choices"]:
                return data["choices"][0]["message"]["content"].strip()
            elif "error" in data:
                return f"خطا از مدل: {data['error']}"
            else:
                return f"پاسخ نامعتبر: {data}"

        except requests.exceptions.HTTPError as e:
            try:
                error_detail = response.json()
            except:
                error_detail = response.text
            return f"HTTP خطا {response.status_code}: {error_detail}"
        except Exception as e:
            return f"خطای غیرمنتظره: {str(e)}"