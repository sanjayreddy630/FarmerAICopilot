import streamlit as st
from llm.answer_engine import FarmerAICopilot


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="Farmer AI Copilot",
    page_icon="🌾",
    layout="wide"
)


# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    .main {
        background-color: #f7faf7;
    }

    .title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 0px;
    }

    .subtitle {
        font-size: 18px;
        color: #667766;
        margin-bottom: 30px;
    }

    .answer-box {
        padding: 25px;
        border-radius: 15px;
        background-color: #ffffff;
        border: 1px solid #dce8dc;
        margin-top: 20px;
    }

    .citation-box {
        padding: 15px;
        border-radius: 10px;
        background-color: #f0f6f0;
        border: 1px solid #d7e5d7;
        margin-bottom: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.markdown(
    '<div class="title">🌾 Farmer AI Copilot</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-powered farming assistance using '
    'Retrieval-Augmented Generation (RAG)'
    '</div>',
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.header("🌱 Farmer Assistant")

    language = st.selectbox(
        "Language",
        [
            "English",
            "Telugu",
            "Hindi"
        ]
    )

    st.divider()

    st.markdown("### 🔎 How it works")

    st.markdown(
        """
        **1.** Understand farmer question

        **2.** Retrieve relevant farming knowledge

        **3.** Rerank the results

        **4.** Build grounded context

        **5.** Generate AI answer

        **6.** Show source citations
        """
    )

    st.divider()

    st.caption(
        "Answers are generated from the "
        "farming knowledge base."
    )


# ---------------------------------------------------------
# QUESTION
# ---------------------------------------------------------

st.subheader("🌾 Ask your farming question")

question = st.text_area(
    "Describe your farming problem",
    placeholder=(
        "Example: rice leaf yelow what do\n"
        "Example: What precautions should I take "
        "during Kharif season?"
    ),
    height=120
)


ask = st.button(
    "🌾 Ask Farmer Copilot",
    type="primary",
    use_container_width=True
)


# ---------------------------------------------------------
# COPILOT
# ---------------------------------------------------------

if ask:

    if not question.strip():

        st.warning(
            "Please enter a farming question."
        )

    else:

        with st.spinner(
            "🌱 Analyzing your question..."
        ):

            try:

                copilot = FarmerAICopilot()

                result = copilot.ask(
                    question.strip()
                )

                # -----------------------------------------
                # ANSWER
                # -----------------------------------------

                st.markdown(
                    "## 🤖 AI Advisory"
                )

                answer = result.get(
                    "answer",
                    "No answer was generated."
                )

                st.markdown(
                    f"""
                    <div class="answer-box">
                    {answer}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # -----------------------------------------
                # CITATIONS
                # -----------------------------------------

                citations = result.get(
                    "citations",
                    []
                )

                if citations:

                    st.markdown(
                        "## 📚 Sources"
                    )

                    for citation in citations:

                        source = citation.get(
                            "source",
                            "Farming Dataset"
                        )

                        page = citation.get(
                            "page",
                            "Unknown"
                        )

                        chunk = citation.get(
                            "chunk_id",
                            "Unknown"
                        )

                        st.markdown(
                            f"""
                            <div class="citation-box">

                            📄 <b>{source}</b><br>

                            Page: <b>{page}</b><br>

                            Chunk: <b>{chunk}</b>

                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                # -----------------------------------------
                # RETRIEVAL QUERY
                # -----------------------------------------

                with st.expander(
                    "🔍 View retrieval information"
                ):

                    st.write(
                        "Original question:"
                    )

                    st.code(
                        result.get(
                            "original_query",
                            question
                        )
                    )

                    st.write(
                        "Retrieval query:"
                    )

                    st.code(
                        result.get(
                            "retrieval_query",
                            ""
                        )
                    )

            except Exception as e:

                st.error(
                    "Something went wrong while "
                    "processing the question."
                )

                st.exception(e)