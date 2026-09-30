import requests
import streamlit as st

st.set_page_config(
    page_title="LegalEaseAI",
    page_icon="⚖️",
    layout="centered",
)

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
                        "question": question
                    },
                    timeout=120,
                )

            data = response.json()

            if "answer" in data:

                st.divider()

                st.markdown("### 💡 LegalEaseAI's Response")

                st.info(
                    "This response provides general legal information "
                    "and is not a substitute for professional legal advice."
                )

                st.markdown(data["answer"])

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

# ---------- FOOTER ----------
st.divider()

st.caption(
    "⚠️ LegalEaseAI provides general legal information only. "
    "Laws may vary depending on your country or state. "
    "Please consult a qualified lawyer for specific legal advice."
)