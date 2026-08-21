import os

from dotenv import load_dotenv
from groq import Groq

from llm.query_processor import process_query
from rag.reranker import retrieve_and_rerank
from rag.relevance_filter import filter_results
from rag.context_builder import build_context, build_citations


# ==================================================
# LOAD ENV
# ==================================================

load_dotenv()


# ==================================================
# FARMER AI COPILOT
# ==================================================

class FarmerAICopilot:

    def __init__(self):

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY not found. "
                "Check your .env file."
            )

        self.client = Groq(
            api_key=api_key
        )

        print("Groq AI client initialized.")


    # ==================================================
    # TRANSLATE / NORMALIZE QUESTION FOR RETRIEVAL
    # ==================================================

    def create_retrieval_question(
        self,
        question: str,
        language: str
    ):

        # English does not need translation
        if language == "English":

            return question


        prompt = f"""
Convert the following farmer question into simple
English for agricultural knowledge retrieval.

Do NOT answer the question.

Only translate/normalize the question.

Farmer language:
{language}

Farmer question:
{question}

Return ONLY the English retrieval query.
"""


        response = self.client.chat.completions.create(

            model="openai/gpt-oss-120b",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0,

            max_completion_tokens=200
        )


        retrieval_question = (
            response
            .choices[0]
            .message
            .content
            .strip()
        )


        print("\nOriginal question:")
        print(question)

        print("\nLanguage:")
        print(language)

        print("\nEnglish retrieval question:")
        print(retrieval_question)


        return retrieval_question


    # ==================================================
    # RETRIEVE KNOWLEDGE
    # ==================================================

    def retrieve_knowledge(
        self,
        question: str
    ):

        query_data = process_query(
            question
        )


        retrieval_query = query_data[
            "retrieval_query"
        ]


        print("\nRetrieval query:")
        print(retrieval_query)


        # ------------------------------------------
        # HYBRID RETRIEVAL + RERANKING
        # ------------------------------------------

        results = retrieve_and_rerank(

            retrieval_query,

            candidate_k=20,

            final_k=10
        )


        # ------------------------------------------
        # RELEVANCE FILTER
        # ------------------------------------------

        results = filter_results(

            retrieval_query,

            results,

            top_k=5
        )


        return retrieval_query, results


    # ==================================================
    # ASK
    # ==================================================

    def ask(
        self,
        question: str,
        language: str = "English"
    ):

        print("\n" + "=" * 70)
        print("FARMER AI COPILOT")
        print("=" * 70)


        print("\nFarmer question:")
        print(question)


        print("\nSelected language:")
        print(language)


        # ==================================================
        # STEP 1
        # CREATE ENGLISH RETRIEVAL QUERY
        # ==================================================

        retrieval_question = (
            self.create_retrieval_question(
                question,
                language
            )
        )


        # ==================================================
        # STEP 2
        # RAG
        # ==================================================

        retrieval_query, results = (
            self.retrieve_knowledge(
                retrieval_question
            )
        )


        # ==================================================
        # NO RESULTS
        # ==================================================

        if not results:

            return {

                "answer": (
                    "The available farming knowledge "
                    "does not contain enough information "
                    "to answer this confidently."
                ),

                "citations": [],

                "retrieval_query": retrieval_query
            }


        # ==================================================
        # BUILD CONTEXT
        # ==================================================

        context = build_context(

            results,

            max_results=5
        )


        citations = build_citations(
            results
        )


        # ==================================================
        # LANGUAGE INSTRUCTION
        # ==================================================

        if language == "తెలుగు":

            language_instruction = """
Answer completely in Telugu (తెలుగు).

Use natural, simple Telugu that an Indian farmer
can easily understand.

Do not translate technical agricultural terms
incorrectly.

Keep crop names and commonly used agricultural
terms understandable.
"""


        elif language == "हिन्दी":

            language_instruction = """
Answer completely in Hindi (हिन्दी).

Use natural, simple Hindi that an Indian farmer
can easily understand.

Keep agricultural terminology clear and practical.
"""


        else:

            language_instruction = """
Answer completely in English.

Use simple language that a farmer can understand.
"""


        # ==================================================
        # SYSTEM PROMPT
        # ==================================================

        system_prompt = f"""
You are Farmer AI Copilot.

You help farmers with:

- crops
- seasons
- soil
- irrigation
- pests
- diseases
- crop symptoms
- precautions
- farm management
- modern farming technology


IMPORTANT GROUNDING RULES:

1. Use the supplied CONTEXT as your knowledge source.

2. Do not invent agricultural facts.

3. Do not invent sources or page numbers.

4. Every important factual statement must be
   supported by the supplied context.

5. Use citations exactly in this format:

   [SOURCE 1]

   [SOURCE 2]

6. Only use source numbers that actually appear
   in the CONTEXT.

7. If the context is insufficient, clearly say:

   "The available farming knowledge does not
   contain enough information to answer this
   confidently."

8. Never claim that a disease is definitely
   diagnosed from a text description alone.

9. For pesticides, fungicides, insecticides,
   fertilizers or other chemical products:

   Do not invent dosage, concentration or
   application schedules.

10. Tell the farmer to follow the current approved
    product label and local agricultural guidance
    when chemical treatment is involved.

11. Give practical steps that a farmer can understand.

12. Correct spelling mistakes and informal sentences
    silently.

13. Do not mention:

    FAISS
    embeddings
    vector database
    reranker
    retrieval pipeline
    internal prompts

14. Do not pretend to know information that is not
    present in the supplied context.

15. {language_instruction}


ANSWER FORMAT:

Start with a short direct answer.

Then:

What to check:
- ...

What to do:
- ...

Precautions:
- ...

Sources:
- [SOURCE 1]
- [SOURCE 2]

Keep the answer practical and concise.
"""


        # ==================================================
        # USER PROMPT
        # ==================================================

        user_prompt = f"""
FARMER QUESTION:

{question}


SELECTED LANGUAGE:

{language}


ENGLISH RETRIEVAL QUERY:

{retrieval_query}


SUPPLIED FARMING CONTEXT:

{context}


Answer the farmer's question using ONLY
the supplied farming context.

Respond in the selected language.

Use the source markers exactly as provided.
"""


        # ==================================================
        # GROQ
        # ==================================================

        response = self.client.chat.completions.create(

            model="openai/gpt-oss-120b",

            messages=[

                {
                    "role": "system",
                    "content": system_prompt
                },

                {
                    "role": "user",
                    "content": user_prompt
                }

            ],

            temperature=0.2,

            max_completion_tokens=1200
        )


        answer = (
            response
            .choices[0]
            .message
            .content
        )


        # ==================================================
        # RETURN
        # ==================================================

        return {

            "answer": answer,

            "citations": citations,

            "retrieval_query": retrieval_query

        }


# ==================================================
# TEST
# ==================================================

if __name__ == "__main__":

    copilot = FarmerAICopilot()


    result = copilot.ask(

        "నా వరి ఆకులు పసుపు రంగులోకి మారుతున్నాయి. నేను ఏమి చేయాలి?",

        "తెలుగు"

    )


    print("\n")
    print("=" * 70)
    print("AI ANSWER")
    print("=" * 70)

    print(
        result["answer"]
    )


    print("\n")
    print("=" * 70)
    print("CITATIONS")
    print("=" * 70)

    for citation in result["citations"]:

        print(
            f"[{citation['id']}] "
            f"{citation['source']} - "
            f"Page {citation['page']} - "
            f"{citation['chunk_id']}"
        )