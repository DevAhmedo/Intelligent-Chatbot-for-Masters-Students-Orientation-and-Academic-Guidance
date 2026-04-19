import argparse
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama

from get_embedding_function import get_embedding_function

CHROMA_PATH = "./chroma_db"

PROMPT_TEMPLATE = """
You are a chatbot for the University of Sharjah.

Your task is to answer ONLY questions related to the University of Sharjah, especially matters concerning master's students.

STRICT RULES:
1. Use ONLY the provided context to answer.
2. Do NOT use any external knowledge.
3. If the question is NOT about the University of Sharjah, reply exactly:
   "I can only answer questions related to Masters students at the University of Sharjah. Please ask a relevant question."
4. If the question is about the University of Sharjah but the answer is NOT clearly found in the context, reply exactly:
   "I could not find this information in the available University of Sharjah master's student documents."
5. Do NOT guess, assume, or provide partial/related information.
6. Do NOT mix information from different programs (e.g., PhD, undergraduate) unless explicitly relevant.
7. Keep the answer short, clear, and direct.
8. Do NOT say phrases like "according to the provided context".

Conversation history (for reference only):
{chat_history}

Context:
{context}

---

User question: {question}

Answer:
"""

STANDALONE_QUESTION_TEMPLATE = """
Rewrite the follow-up question into a standalone question using the conversation history.
Preserve the original meaning.
Do not answer the question.
If the question is already standalone, return it unchanged.
Return only the standalone question.

Conversation history:
{chat_history}

Follow-up question: {question}

Standalone question:
"""


def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    query_rag(query_text, [])


def _format_chat_history(chat_history: list[dict], max_messages: int = 6) -> str:
    if not chat_history:
        return ""

    recent_messages = chat_history[-max_messages:]
    formatted_messages = []
    for message in recent_messages:
        role = "User" if message.get("role") == "user" else "Assistant"
        content = (message.get("content") or "").strip()
        if content:
            formatted_messages.append(f"{role}: {content}")

    return "\n".join(formatted_messages)


def query_rag(query_text: str, chat_history: list[dict] | None = None):
    # Prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
    model = Ollama(model="llama3")

    history_text = _format_chat_history(chat_history or [])
    standalone_query = query_text
    if history_text:
        standalone_prompt = ChatPromptTemplate.from_template(STANDALONE_QUESTION_TEMPLATE)
        rewrite_prompt = standalone_prompt.format(chat_history=history_text, question=query_text)
        rewritten_query = model.invoke(rewrite_prompt)
        standalone_query = (rewritten_query or "").strip() or query_text

    # Search the DB.
    results = db.similarity_search_with_score(standalone_query, k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(
        context=context_text,
        chat_history=history_text or "(no previous messages)",
        question=query_text,
    )
    response_text = model.invoke(prompt)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)
    return response_text


if __name__ == "__main__":
    main()
