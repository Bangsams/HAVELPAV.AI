import openai  # type: ignore
import streamlit as st  # type: ignore
import pandas as pd  # type: ignore
import time
import base64
import re

 # Hapus jika tidak digunakan lagi

# Konfigurasi halaman
st.set_page_config(page_title="HAVELPAV - CS Lingkungan", page_icon="🌱", layout="wide")

st.markdown(
    """
    <style>
    /* Background utama dengan gradasi hijau */
    .stApp {
        background: linear-gradient(to bottom right, #d0f0c0, #f0fff0);
    }

    /* Sidebar (chat history) dengan nuansa gradasi hijau */
    section[data-testid="stSidebar"] {
        background: linear-gradient(to bottom, #a8d5ba, #d0f0c0);
        color: black;
    }

    /* Header sidebar - misalnya untuk tulisan "havelpav cs" */
    .st-emotion-cache-1avcm0n {
        color: black !important;  /* Warna hitam */
        font-weight: bold !important;  /* Tebal */
    }

    /* Chat bubble user */
    .stChatMessage.user {
        background-color: #e0f7da;
        border-radius: 10px;
        padding: 8px;
        color: black;
    }

    /* Chat bubble AI */
    .stChatMessage.assistant {
        background-color: #f1f8e9;
        border-radius: 10px;
        padding: 8px;
        color: black;
    }

    /* Scroll bar sidebar yang halus */
    section[data-testid="stSidebar"]::-webkit-scrollbar {
        width: 6px;
    }
    section[data-testid="stSidebar"]::-webkit-scrollbar-thumb {
        background-color: #9ccc65;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🌱 HAVELPAV AI - Customer Service Paving Block Ramah Lingkungan")

# API OpenAI (akses menggunakan st.secrets)
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "Kamu adalah HAVELPAV, AI Customer Service yang ramah, informatif, dan fokus pada isu lingkungan. "
                "Tugasmu adalah menjawab pertanyaan tentang paving block ramah lingkungan, proses produksi daur ulang, manfaat bagi lingkungan, dan produk HAVELPAV. "
                "Jawaban harus singkat, sopan, dan ramah, maksimal 3 kalimat."
            )
        }
    ]

# Sidebar untuk menampilkan chat history
with st.sidebar:
    st.header("Riwayat Chat")
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            st.write(f"🗨️ {msg['role'].capitalize()}: {msg['content'][:50]}{'...' if len(msg['content']) > 50 else ''}")

# Tampilkan riwayat chat sebelumnya
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Input pengguna
if prompt := st.chat_input("Ketik pertanyaan tentang paving ramah lingkungan..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Jawaban dari AI dengan efek mengetik
    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=st.session_state.messages,
                max_tokens=100
            )
            full_response = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": full_response})

            # Efek mengetik satu per satu huruf
            placeholder = st.empty()
            typed_text = ""
            for char in full_response:
                typed_text += char
                placeholder.markdown(typed_text)
                time.sleep(0.015)
        except Exception as e:
            st.error(f"❌ Gagal menghasilkan respons: {str(e)}")
