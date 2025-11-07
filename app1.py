import streamlit as st
from services.chatbot import WeddingPlannerChatbot

st.set_page_config(page_title="💍 Wedding Planner Chatbot", page_icon="💬", layout="centered")

st.title("💐 Wedding Planner Chatbot")
st.caption("Chat with your personal wedding planner AI — ask questions or upload files for instant insights!")

# Initialize session state
if "chatbot" not in st.session_state:
    st.session_state.chatbot = WeddingPlannerChatbot()
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- File upload inside chat (behaves like ChatGPT file drop) ---
uploaded_file = st.file_uploader("📎 Upload a wedding-related file", type=["txt", "csv", "pdf", "docx"], label_visibility="collapsed")

if uploaded_file:
    # Show "User uploaded file" message in chat
    user_msg = f"📎 Uploaded file: **{uploaded_file.name}**"
    st.session_state.messages.append({"role": "user", "content": user_msg})
    with st.chat_message("user"):
        st.markdown(user_msg)

    # Process file instantly
    with st.chat_message("assistant"):
        with st.spinner("Analyzing your file... 💭"):
            try:
                content = uploaded_file.read().decode("utf-8", errors="ignore")
            except Exception:
                content = "⚠️ Sorry, I couldn’t read the file content properly."
            analysis = st.session_state.chatbot.analyze_file(content, uploaded_file.name)
            st.markdown(analysis)
    st.session_state.messages.append({"role": "assistant", "content": analysis})

# --- Normal text chat ---
user_input = st.chat_input("Ask me anything about your wedding 💬")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        reply = st.session_state.chatbot.chat(user_input)
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
