
# app.py
import streamlit as st
import requests

st.set_page_config(page_title="چت‌بات RAG Aptar", page_icon="🤖", layout="wide")

st.markdown(
    """
    <style>
    /* فقط پیام‌های چت راست‌به‌چپ بشن */
    .stChatMessage {
        direction: rtl !important;
        text-align: right !important;
    }

    /* ورودی چت هم RTL باشه (کاربر راحت تایپ کنه) */
    .stChatInput > div > div > input,
    .stChatInput textarea {
        direction: rtl !important;
        text-align: right !important;
    }

    /* عنوان‌ها و توضیحات هم RTL (اختیاری اما قشنگ‌تر) */
    h1, h2, h3, .stMarkdown p {
        direction: rtl;
        text-align: right;
    }

    /* فونت فارسی */
    body, textarea, input {
        font-family: "Vazirmatn", "Tahoma", sans-serif;
    }

    /* جلوگیری از به‌هم‌ریختگی اعداد و انگلیسی داخل فارسی */
    .stMarkdown {
        unicode-bidi: plaintext;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🤖 RAG ChatBot")
st.markdown("ابتدا فایل txt یا pdf آپلود کنید، سپس سوال بپرسید. پاسخ‌ها بر اساس محتوای فایل خواهد بود.")

BACKEND = "http://localhost:8000"

# --- سایدبار آپلود ---
with st.sidebar:
    st.header("آپلود دانش پایه")
    uploaded_file = st.file_uploader(
            "فایل txt یا pdf انتخاب کنید",
            type=["txt", "pdf"], 
            accept_multiple_files=True)
    
    if st.button("آپلود و ایندکس همه فایل‌ها"):
        if uploaded_file:
            with st.spinner(f"در حال آپلود و ایندکس {len(uploaded_file)} فایل..."):
                all_chunks = 0
                for uploaded_file in uploaded_file:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    try:
                        response = requests.post(f"{BACKEND}/upload", files=files, timeout=300)
                        response.raise_for_status()
                        result = response.json()
                        all_chunks += result.get('chunks_indexed', 0)
                        st.success(f"✅ {uploaded_file.name}: {result.get('chunks_indexed', 0)} چانک ایندکس شد.")
                    except Exception as e:
                        st.error(f"❌ خطا در {uploaded_file.name}: {str(e)}")
                st.success(f"🎉 همه فایل‌ها آپلود شدند! مجموع {all_chunks} چانک ایندکس شد.")
        else:
            st.warning("⚠️ لطفاً حداقل یک فایل انتخاب کنید.")

# --- چت اصلی ---
st.header("چت با بات")

if "messages" not in st.session_state:
    st.session_state.messages = []

# نمایش تاریخچه - فقط اینجا dir="rtl" می‌ذاریم
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(f"<div style='direction: rtl; text-align: right;'>{message['content']}</div>", unsafe_allow_html=True)

# ورودی کاربر
if prompt := st.chat_input("سوال خود را اینجا بنویسید..."):
    # متن خام و تمیز رو به بک‌اند می‌فرستیم (بدون هیچ dir یا کاراکتر RTL مخفی)
    clean_prompt = prompt.strip()

    # ذخیره و نمایش پیام کاربر با RTL
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f"<div style='direction: rtl; text-align: right;'>{prompt}</div>", unsafe_allow_html=True)

    # دریافت و نمایش پاسخ بات
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            response = requests.post(
                f"{BACKEND}/query",
                data={"q": clean_prompt, "k": 5},
                stream=True,
                timeout=120
            )
            response.raise_for_status()

            for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                if chunk:
                    full_response += chunk
                    message_placeholder.markdown(
                        f"<div style='direction: rtl; text-align: right;'>{full_response}▌</div>",
                        unsafe_allow_html=True
                    )

            # نهایی
            message_placeholder.markdown(
                f"<div style='direction: rtl; text-align: right;'>{full_response}</div>",
                unsafe_allow_html=True
            )

        except Exception as e:
            error_msg = "خطایی در دریافت پاسخ رخ داد. لطفاً دوباره امتحان کنید."
            message_placeholder.markdown(
                f"<div style='direction: rtl; text-align: right;'>{error_msg}</div>",
                unsafe_allow_html=True
            )
            full_response = error_msg

        st.session_state.messages.append({"role": "assistant", "content": full_response})

