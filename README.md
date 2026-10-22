# StudyMate AI 📚
<img width="1433" height="810" alt="Screenshot 2026-10-22 at 23 54 29" src="https://github.com/user-attachments/assets/1a9d8a79-dc17-4b51-93be-28312044be4a" />


**An AI-powered PDF question-answering assistant built with Python, Streamlit, and the OpenAI API.**

StudyMate AI allows users to upload a PDF document and ask questions about its contents. The application extracts text from the document, splits it into smaller chunks, retrieves relevant passages, and uses an OpenAI language model to generate answers grounded in the retrieved context.

This project was built to develop practical skills in LLM application development, document processing, retrieval, API integration, and automated testing.

## ✨ Features

- **PDF text extraction:** Extracts text from uploaded PDF documents using `pypdf`.
- **Text chunking:** Splits extracted text into smaller, overlapping chunks to provide manageable context to the language model.
- **Source tracking:** Preserves page numbers and displays source information so users can inspect where retrieved information came from.
- **Question answering:** Uses the OpenAI API to answer questions using retrieved document passages.
- **Context-aware responses:** Provides the model with relevant document text instead of relying only on its general knowledge.
- **Missing-information handling:** Tested behavior for questions that cannot be answered from the uploaded document.
- **Automated tests:** Uses `pytest` to test chunk metadata, relevant passage retrieval, and queries with no matching passages.

## 🛠️ Tech Stack

- **Python** — application logic and document processing
- **Streamlit** — interactive web interface
- **OpenAI API** — LLM-powered answer generation
- **pypdf** — PDF text extraction
- **python-dotenv** — local environment-variable configuration
- **pytest** — automated testing
- **Git and GitHub** — version control and project hosting

## ⚙️ How It Works

1. **Upload:** The user uploads a PDF through the Streamlit interface.
2. **Extract:** The application extracts text from each page and retains page-number metadata.
3. **Chunk:** Page text is split into overlapping chunks to preserve useful context.
4. **Retrieve:** A keyword-overlap retrieval function selects relevant chunks for the user's question.
5. **Generate:** The retrieved passages are sent to an OpenAI model, which generates an answer based on the provided context.
6. **Inspect:** The interface displays source information, including the relevant page and text, so the user can verify the answer.

## 🚀 Getting Started

### Prerequisites

- Python 3
- An OpenAI API key

### 1. Clone the repository

```bash
git clone https://github.com/rhittv/studymate-ai.git
cd studymate-ai
```

### 2. Create and activate a virtual environment

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your API key

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_api_key_here
```

Replace the placeholder with your own API key. Never commit your `.env` file or expose your API key publicly.

### 5. Run the application

```bash
streamlit run app.py
```

Streamlit will provide a local URL where you can open the app in your browser.

## 🧪 Run Tests

Run the automated test suite with:

```bash
pytest -v
```

The current tests cover:

- Preservation of page numbers and chunk metadata during chunking.
- Retrieval of a relevant passage for a matching question.
- Returning no results when no chunks match the query.

## 🧠 Engineering Decisions and Learnings

Building this project provided hands-on practice with:

- Designing a document-processing pipeline.
- Preserving metadata across extraction and chunking stages.
- Connecting a Python application to an external LLM API.
- Managing API credentials through environment variables.
- Testing retrieval logic independently of the language model.
- Handling questions for which the retrieval stage finds no matching passages.
- Using Git and GitHub to manage and publish a project.

## 🔭 Current Limitations and Future Improvements

StudyMate AI is a learning prototype. Its current retrieval system uses keyword overlap rather than embeddings or semantic search, so it may miss relevant passages when a question uses different wording from the source document.

Potential next improvements include:

- Semantic retrieval using embeddings and a vector index.
- More comprehensive automated tests, including API mocking and end-to-end cases.
- Improved handling of scanned PDFs and documents with complex layouts.
- More robust evaluation of answer accuracy and source attribution.
- Deployment so others can try the application online.

## 👨‍💻 Author

**Rhittv**

GitHub: [@rhittv](https://github.com/rhittv)

---

*StudyMate AI is an educational project exploring practical LLM application development and document-based question answering.*
