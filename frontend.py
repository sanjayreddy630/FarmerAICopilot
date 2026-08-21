import streamlit as st
import requests

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Farmer AI Copilot",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

.stApp {
    background: #f5f7f2;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #123524;
}

[data-testid="stSidebar"] * {
    color: white;
}

/* Main container */
.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Header */
.hero {
    background: linear-gradient(
        135deg,
        #123524 0%,
        #1f6b45 100%
    );
    padding: 35px 40px;
    border-radius: 24px;
    color: white;
    margin-bottom: 25px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
}

.hero-title {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 8px;
}

.hero-subtitle {
    font-size: 17px;
    opacity: 0.9;
}

/* Cards */
.info-card {
    background: white;
    padding: 22px;
    border-radius: 18px;
    border: 1px solid #e1e8df;
    box-shadow: 0 5px 20px rgba(0,0,0,0.04);
    height: 100%;
}

.info-icon {
    font-size: 28px;
}

.info-title {
    font-size: 17px;
    font-weight: 700;
    color: #173b28;
    margin-top: 8px;
}

.info-text {
    font-size: 14px;
    color: #66736a;
    margin-top: 5px;
}

/* Chat answer */
.answer-card {
    background: white;
    border-radius: 20px;
    padding: 28px;
    margin-top: 20px;
    border: 1px solid #dce7dc;
    box-shadow: 0 8px 25px rgba(0,0,0,0.05);
}

.answer-title {
    color: #173b28;
    font-size: 20px;
    font-weight: 750;
    margin-bottom: 15px;
}

/* Citation */
.citation-card {
    background: #f1f7f0;
    border-left: 4px solid #2e7d4f;
    padding: 12px 16px;
    border-radius: 10px;
    margin-top: 8px;
    font-size: 14px;
}

/* Disclaimer */
.disclaimer {
    background: #fff8e6;
    border: 1px solid #f0dfad;
    padding: 15px 18px;
    border-radius: 12px;
    color: #6d5b28;
    font-size: 13px;
    margin-top: 25px;
}

/* Buttons */
.stButton > button {
    border-radius: 12px;
    border: 1px solid #d5e1d5;
    background: white;
    color: #173b28;
    font-weight: 600;
}

.stButton > button:hover {
    border-color: #2e7d4f;
    color: #2e7d4f;
}

/* Chat input */
[data-testid="stChatInput"] {
    border-radius: 15px;
}

/* Hide streamlit decoration */
[data-testid="stDecoration"] {
    display: none;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "question" not in st.session_state:
    st.session_state.question = ""


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="text-align:center; padding:20px 5px;">
            <div style="font-size:52px;">🌾</div>
            <div style="
                font-size:24px;
                font-weight:800;
                margin-top:5px;
            ">
                Farmer AI
            </div>
            <div style="
                font-size:13px;
                opacity:0.75;
            ">
                Intelligent Farming Assistant
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### 💡 Try asking")

    example_questions = [
        "My rice leaves are turning yellow. What should I do?",
        "What precautions should I take during Kharif season?",
        "How can I detect crop diseases early?",
        "What are the benefits of drip irrigation?",
        "What should I do for leaf spot disease?"
    ]

    for question in example_questions:

        if st.button(
            question,
            key=f"example_{question}",
            use_container_width=True
        ):
            st.session_state.question = question

    st.divider()

    if st.button(
        "🗑️ Clear conversation",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()

    st.markdown(
        """
        <div style="
            margin-top:30px;
            font-size:12px;
            opacity:0.75;
            line-height:1.6;
        ">
        <b>Powered by:</b><br>
        Hybrid RAG • FAISS • Reranking • Groq AI
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-title">
            🌾 Farmer AI Copilot
        </div>

        <div class="hero-subtitle">
            Ask farming questions in natural language and get
            source-grounded recommendations from your agricultural
            knowledge base.
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# FEATURE CARDS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        """
        <div class="info-card">
            <div class="info-icon">🧠</div>
            <div class="info-title">AI Powered</div>
            <div class="info-text">
                Understands natural-language farmer questions.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="info-card">
            <div class="info-icon">🔎</div>
            <div class="info-title">RAG Retrieval</div>
            <div class="info-text">
                Retrieves relevant information from the farming dataset.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div class="info-card">
            <div class="info-icon">📚</div>
            <div class="info-title">Citations</div>
            <div class="info-text">
                Answers are connected to source pages from the dataset.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        """
        <div class="info-card">
            <div class="info-icon">🌱</div>
            <div class="info-title">Farmer Friendly</div>
            <div class="info-text">
                Ask questions naturally without technical terminology.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    if message["role"] == "user":

        with st.chat_message("user", avatar="👨‍🌾"):
            st.markdown(message["content"])

    else:

        with st.chat_message("assistant", avatar="🌾"):

            st.markdown(
                '<div class="answer-title">🌾 Farmer AI Recommendation</div>',
                unsafe_allow_html=True
            )

            st.markdown(message["content"])

            citations = message.get("citations", [])

            if citations:

                st.markdown("### 📚 Sources")

                for citation in citations:

                    st.markdown(
                        f"""
                        <div class="citation-card">
                            <b>[{citation.get("id", "")}]</b>
                            {citation.get("source", "Farming Dataset")}
                            — Page {citation.get("page", "Unknown")}
                            — {citation.get("chunk_id", "")}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )


# ============================================================
# QUESTION INPUT
# ============================================================

question = st.chat_input(
    "Ask your farming question..."
)

if st.session_state.question:

    question = st.session_state.question
    st.session_state.question = ""


# ============================================================
# SEND QUESTION
# ============================================================

if question:

    # Show user question
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user", avatar="👨‍🌾"):
        st.markdown(question)

    # Call backend
    with st.chat_message("assistant", avatar="🌾"):

        with st.spinner(
            "🌱 Analyzing your question and searching farming knowledge..."
        ):

            try:

                response = requests.post(
                    "http://127.0.0.1:5000/api/ask",
                    json={
                        "question": question
                    },
                    timeout=180
                )

                if response.status_code == 200:

                    data = response.json()

                    answer = data.get(
                        "answer",
                        "I could not generate an answer."
                    )

                    citations = data.get(
                        "citations",
                        []
                    )

                    st.markdown(
                        '<div class="answer-title">🌾 Farmer AI Recommendation</div>',
                        unsafe_allow_html=True
                    )

                    st.markdown(answer)

                    if citations:

                        st.markdown("### 📚 Sources")

                        for citation in citations:

                            st.markdown(
                                f"""
                                <div class="citation-card">
                                    <b>[{citation.get("id", "")}]</b>
                                    {citation.get("source", "Farming Dataset")}
                                    — Page {citation.get("page", "Unknown")}
                                    — {citation.get("chunk_id", "")}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "citations": citations
                    })

                else:

                    error_message = (
                        f"Backend returned HTTP {response.status_code}."
                    )

                    st.error(error_message)

            except requests.exceptions.ConnectionError:

                st.error(
                    "❌ Cannot connect to the Farmer AI backend. "
                    "Please start app.py first."
                )

            except requests.exceptions.Timeout:

                st.error(
                    "⏳ The AI service took too long to respond. "
                    "Please try again."
                )

            except Exception as e:

                st.error(
                    f"❌ Something went wrong: {str(e)}"
                )


# ============================================================
# DISCLAIMER
# ============================================================

st.markdown(
    """
    <div class="disclaimer">
        ⚠️ <b>Important:</b>
        Farmer AI Copilot provides decision-support information based on
        its available knowledge sources. Crop calendars, disease conditions,
        chemical labels and management recommendations can vary by
        location and current conditions. Verify important recommendations
        with current local agricultural advisories before field use.
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div style="
        text-align:center;
        margin-top:35px;
        color:#7b877f;
        font-size:12px;
    ">
        🌾 Farmer AI Copilot &nbsp;•&nbsp;
        Hybrid RAG &nbsp;•&nbsp;
        Source-Grounded AI
    </div>
    """,
    unsafe_allow_html=True
)