import logging
from time import perf_counter

import streamlit as st

from rag import answer_question
from retrieve import get_vector_db

logger = logging.getLogger(__name__)

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


@st.cache_resource(show_spinner=False)
def prepare_search():
    """Load the local search model once, before accepting questions."""
    return get_vector_db()


try:
    with st.spinner(
        "Preparing local search (once per app start)...",
        show_time=True,
    ):
        prepare_search()
except Exception as error:
    logger.error("Search initialization failed (%s)", type(error).__name__)
    st.error(
        "Could not load local search. Make sure ingestion completed on this "
        "computer. If the model cache is missing, run src/ingest.py again."
    )
    st.stop()

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
        progress = st.empty()
        started = perf_counter()
        try:
            with st.spinner("Preparing your answer...", show_time=True):
                result = answer_question(
                    question,
                    on_progress=lambda message: progress.info(message),
                )
        except Exception as error:
            progress.empty()
            logger.error("Answer generation failed (%s)", type(error).__name__)
            detail = str(error).lower()
            if "429" in detail or "resource_exhausted" in detail:
                st.error("The API quota was reached. Wait a moment and try again.")
            elif "503" in detail or "unavailable" in detail:
                st.error("Groq is currently busy. Please try again shortly.")
            elif "timeout" in detail or "timed out" in detail:
                st.error("The answer service took too long. Please try again.")
            else:
                st.error(
                    "Could not generate an answer. Check your internet "
                    "connection and API configuration, then try again."
                )
        else:
            progress.empty()
            st.caption(f"Answered in {perf_counter() - started:.1f} seconds")
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
