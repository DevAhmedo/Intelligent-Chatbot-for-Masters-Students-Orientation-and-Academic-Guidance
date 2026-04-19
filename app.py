import streamlit as st

from query_data import query_rag


st.set_page_config(page_title="Masters Students Guidance Chatbot", page_icon="💬", layout="centered")

# Simple custom style for a clean, modern single-page layout.
st.markdown(
    """
    <style>
    .main {
        background: linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%);
    }
    .block-container {
        max-width: 860px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .hero {
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .hero h1 {
        margin-bottom: 0.35rem;
        color: #0f172a;
        font-size: 2.2rem;
    }
    .hero p {
        color: #334155;
        margin-top: 0;
        margin-bottom: 0;
        font-size: 1rem;
    }
    .input-shell {
        margin-top: 0.9rem;
        padding: 0.7rem;
        border: 1px solid rgba(148, 163, 184, 0.25);
        border-radius: 12px;
        background: rgba(15, 23, 42, 0.68);
        box-shadow: 0 6px 20px rgba(2, 6, 23, 0.35);
    }
    .stChatMessage {
        border-radius: 12px;
        border: 1px solid rgba(148, 163, 184, 0.2);
        background: rgba(2, 6, 23, 0.35);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown(
    """'
    <div class="hero">
        <h1>Masters Students Guidance Chatbot</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="chat-shell">', unsafe_allow_html=True)

if not st.session_state.messages:
    st.info("Start by typing a question below.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="input-shell">', unsafe_allow_html=True)
with st.form("chat_form", clear_on_submit=True):
    question = st.text_input("", placeholder="Ask a question...", label_visibility="collapsed")
    submitted = st.form_submit_button("Send", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

if submitted:
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        st.session_state.messages.append({"role": "user", "content": question.strip()})
        with st.spinner("Processing your question..."):
            try:
                response = query_rag(question.strip(), st.session_state.messages)
            except Exception as exc:
                response = f"Sorry, I could not process that request.\n\nDetails: {exc}"
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
