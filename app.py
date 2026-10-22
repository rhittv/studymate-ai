import os
from typing import List, Dict

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader

load_dotenv()

st.set_page_config(
    page_title="StudyMate AI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
:root { color-scheme: light; }
.block-container { max-width: 1180px; padding-top: 2rem; padding-bottom: 3rem; }
.hero { padding: 1.5rem 1.6rem; border: 1px solid rgba(120,120,140,.22);
        border-radius: 20px; background: linear-gradient(135deg, #f7f8ff, #f2fbf8); }
.hero h1 { margin: 0 0 .35rem 0; letter-spacing: -0.04em; }
.hero p { margin: 0; color: #525b6b; font-size: 1.03rem; }
.small-muted { color: #707888; font-size: .88rem; }
[data-testid="stChatMessage"] { border-radius: 14px; }
</style>
""", unsafe_allow_html=True)


def extract_pdf(uploaded_file) -> List[Dict]:
    """Extract text page by page and preserve page numbers."""
    reader = PdfReader(uploaded_file)
    pages = []

    for page_num, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        if text:
            pages.append({
                "page_number": page_num,
                "text": text,
            })

    return pages


def split_into_chunks(
    pages: List[Dict],
    chunk_size: int = 1100,
    overlap: int = 180,
) -> List[Dict]:
    """Split each page separately and retain its page number."""
    chunks = []

    for page in pages:
        text = page["text"]
        start = 0

        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append({
                    "text": chunk_text,
                    "chunk_id": len(chunks) + 1,
                    "page_number": page["page_number"],
                })

            if end == len(text):
                break

            start = end - overlap

    return chunks


def retrieve_chunks(question: str, chunks: List[Dict], limit: int = 4) -> List[Dict]:
    # Lightweight baseline retrieval: rank chunks by keyword overlap.
    stop_words = {"the", "and", "for", "that", "this", "with", "what", "when",
                  "where", "which", "from", "into", "are", "was", "were", "you",
                  "your", "can", "could", "does", "about", "have", "has", "how"}
    terms = {w.lower().strip(".,!?():;[]{}\"'") for w in question.split()}
    terms = {w for w in terms if len(w) > 2 and w not in stop_words}
    ranked = []
    for chunk in chunks:
        haystack = chunk["text"].lower()
        score = sum(haystack.count(term) for term in terms)
        if score:
            ranked.append((score, chunk))
    ranked.sort(key=lambda item: item[0], reverse=True)
    return [chunk for _, chunk in ranked[:limit]]

def ask_model(question: str, context_chunks: List[Dict], history: List[Dict]) -> str:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is missing. Add it to your .env file and restart the app.")
    client = OpenAI(api_key=api_key)
    context = "\n\n---\n\n".join(
        f"Source chunk {chunk['chunk_id']}:\n{chunk['text']}" for chunk in context_chunks
    )
    messages = [{
        "role": "system",
        "content": (
            "You are StudyMate, a careful study assistant. Answer using the provided document "
            "context whenever possible. Do not invent facts or citations. If the context does "
            "not contain the answer, say so clearly and suggest what the student could search for. "
            "When using context, cite it as [Chunk N]. Context:\n\n" + context
        )
    }]
    # Include recent conversation for follow-up questions, but keep the prompt compact.
    messages.extend(history[-6:])
    messages.append({"role": "user", "content": question})
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        messages=messages,

    )
    return response.choices[0].message.content or "I couldn't generate an answer. Please try again."

if "documents" not in st.session_state:
    st.session_state.documents = []
if "chunks" not in st.session_state:
    st.session_state.chunks = []
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.markdown("## 📚 StudyMate AI")
    st.caption("Your documents, explained.")
    st.divider()
    st.markdown("### Your library")
    uploaded_files = st.file_uploader(
        "Upload PDF notes or textbooks",
        type=["pdf"],
        accept_multiple_files=True,
        help="This starter version extracts selectable text from PDFs. Scanned image-only PDFs need OCR, which we'll add later.",
    )
    if st.button("Process documents", type="primary", use_container_width=True):
        if not uploaded_files:
            st.warning("Upload at least one PDF first.")
        else:
            all_chunks, document_names = [], []
            with st.spinner("Reading and preparing your documents..."):
                for file in uploaded_files:
                    try:
                        
                        pages = extract_pdf(file)

                        if not pages:
                            st.warning(
                                f"No selectable text found in {file.name}. "
                                "It may be a scanned PDF."
                            )
                            continue

                        chunks = split_into_chunks(pages)

                        for chunk in chunks:
                            chunk["source"] = file.name
                            chunk["chunk_id"] = len(all_chunks) + 1
                            all_chunks.append(chunk)

                        document_names.append(file.name)

                    except Exception as exc:
                        st.error(f"Couldn't read {file.name}: {exc}")
            st.session_state.chunks = all_chunks
            st.session_state.documents = document_names
            st.session_state.messages = []
            if all_chunks:
                st.success(f"Processed {len(document_names)} document(s).")
    if st.session_state.documents:
        st.markdown("**Ready to use**")
        for name in st.session_state.documents:
            st.markdown(f"📄 {name}")
        st.caption(f"{len(st.session_state.chunks)} text chunks prepared")
    st.divider()
    st.markdown("### How it works")
    st.markdown(
        "1. Extract text from PDFs\n"
        "2. Find relevant passages\n"
        "3. Ask an LLM to answer from those passages\n"
        "4. Show source chunk references"
    )
    st.markdown('<p class="small-muted">Starter build · RAG foundations</p>', unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <h1>Study smarter with your own materials.</h1>
  <p>Upload your notes, ask questions, and get answers grounded in your documents.</p>
</div>
""", unsafe_allow_html=True)
st.write("")

left, right = st.columns([1.55, 1], gap="large")
with left:
    st.markdown("### 💬 Ask your documents")
    if not st.session_state.chunks:
        st.info("Start by uploading one or more text-based PDFs in the left sidebar, then select **Process documents**.")
        st.markdown("**Try asking:**")
        st.markdown("- What are the main ideas in this material?\n- Explain a difficult concept in simple terms.\n- What should I remember for an exam?")
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    prompt = st.chat_input(
        "Ask a question about your PDFs...",
        disabled=not bool(st.session_state.chunks),
    )
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Searching your documents and drafting an answer..."):
                recent_history = [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages[:-1]
                    if m["role"] in ("user", "assistant")
                ]
                matches = retrieve_chunks(prompt, st.session_state.chunks)
                if not matches:
                    st.warning("I couldn't find a strong keyword match. Try using terms from the document.")
                    answer = "I couldn't find a relevant passage in the uploaded text for that question. Try rephrasing it using keywords from your material."
                else:
                    try:
                        answer = ask_model(prompt, matches, recent_history)
                    except Exception as exc:
                        answer = f"**Couldn't contact the AI model:** {exc}"
                st.markdown(answer)
                
                if matches:
                    with st.expander("View retrieved source passages"):
                        for chunk in matches:
                            st.markdown(
                                f"**{chunk['source']} · Page {chunk.get('page_number', 'Unknown')} "
                                f"· Chunk {chunk['chunk_id']}**"
                            )
                            st.caption(
                                chunk["text"][:900]
                                + ("…" if len(chunk["text"]) > 900 else "")
                            )

                st.session_state.messages.append({"role": "assistant", "content": answer})

with right:
    st.markdown("### ✨ What you can do")
    st.markdown("""
    **Understand**

    Turn dense notes into clear explanations.

    **Revise**

    Ask for summaries, key terms, and exam questions.

    **Explore**

    Ask follow-up questions across your uploaded material.
    """)
    st.divider()
    st.markdown("### 🧱 Under the hood")
    st.markdown("""
    - **Python + Streamlit** — app and interface
    - **pypdf** — PDF text extraction
    - **Retrieval** — selects potentially relevant passages
    - **OpenAI API** — generates answers from context
    """)
    st.caption("This first version uses keyword-based retrieval. Semantic embeddings, better citations, persistent storage, and deployment are planned improvements.")
