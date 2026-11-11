import streamlit as st
from rag import answer_question

st.set_page_config(
    page_title="OS Study Assistant",
    page_icon="📚",
    layout="centered",
)

st.title("📚 OS Study Assistant")
st.caption(
    "Ask an Operating Systems question. "
    "Answers are based on our course materials."
)

with st.form("question_form"):
    question = st.text_area(
        "Your question",
        placeholder="What is virtual memory?",
    )
    submitted = st.form_submit_button("Ask")

if submitted:
    question = question.strip()

    if not question:
        st.warning("Please enter a question first.")
    else:
        try:
            with st.spinner("Searching course materials..."):
                result = answer_question(question)
        except Exception:
            st.error(
                "Could not generate an answer. "
                "Check your internet connection and API configuration, "
                "then try again."
            )
        else:
            st.subheader("Answer")
            st.markdown(result["answer"])

            sources = result.get("sources", [])

            if sources:
                st.subheader("Sources")

                for source in sources:
                    st.write(
                        f"- {source['document']} "
                        f"— page {source['page']}"
                    )