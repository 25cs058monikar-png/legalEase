import requests
import streamlit as st

st.set_page_config(
    page_title="LegalEaseAI",
    page_icon="⚖️",
    layout="centered",
)

# ---------- CHAT HISTORY ----------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------- HEADER ----------
st.markdown(
    """
    <div style="text-align:center; padding:20px 0;">
        <h1 style="font-size:42px; margin-bottom:5px;">
            ⚖️ LegalEaseAI
        </h1>
        <p style="font-size:18px; color:#666;">
            AI-Powered Legal Information Assistant
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

# ---------- QUESTION ----------
st.markdown("### 📝 Ask Your Legal Question")


country = st.selectbox(
    "🌍 Select your country",
    ["India", "United States", "United Kingdom", "Canada", "Australia", "Other"],
)

state = st.text_input(
    "📍 State / Province",
    placeholder="Example: Tamil Nadu",
)
question = st.text_area(
    "Enter your question below:",
    placeholder="Example: What are my rights as a tenant?",
    height=150,
)

# ---------- ASK BUTTON ----------
if st.button(
    "⚖️ ASK LEGAL QUESTION",
    type="primary",
    use_container_width=True,
):

    if not question.strip():

        st.warning("Please enter a legal question.")

    else:

        try:

            with st.spinner("LegalEaseAI is thinking..."):

                response = requests.post(
                    "http://127.0.0.1:8000/api/ask",
                    json={
                        "question": question,
                        "country": country,
                        "state": state,
                    },
                    timeout=120,
                )

            data = response.json()

            if "answer" in data:

                # Save question and answer
                st.session_state.chat_history.append(
                    {
                        "question": question,
                        "answer": data["answer"],
                    }
                )

            else:

                st.error(
                    data.get(
                        "error",
                        "Something went wrong."
                    )
                )

        except requests.RequestException as e:

            st.error(
                f"Could not connect to the backend: {e}"
            )

# ---------- CURRENT ANSWER / HISTORY ----------
if st.session_state.chat_history:

    st.divider()
    st.markdown("### 💬 LegalEaseAI Conversation")

    for chat in reversed(st.session_state.chat_history):

        st.markdown(
            f"**🧑 Your Question:** {chat['question']}"
        )

        st.markdown("**⚖️ LegalEaseAI:**")
        st.markdown(chat["answer"])

        st.divider()

# ---------- CLEAR HISTORY ----------
if st.session_state.chat_history:

    if st.button("🗑️ Clear Chat History"):

        st.session_state.chat_history = []
        st.rerun()

# ---------- FOOTER ----------
st.caption(
    "⚠️ LegalEaseAI provides general legal information only. "
    "Laws may vary depending on your country or state. "
    "Please consult a qualified lawyer for specific legal advice."
)
