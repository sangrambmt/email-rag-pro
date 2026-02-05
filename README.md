# Email Knowledge Intelligence System (RAG)

A local Retrieval Augmented Generation system.
Documents and email attachments placed in a folder are automatically extracted, chunked, embedded and indexed.
You can query them through a FastAPI API. Answers are grounded in retrieved content and include source files.

---

## Project Structure

email-rag-pro/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application
│   ├── config.py         # Environment configuration
│   ├── embed.py          # Vector DB setup
│   ├── retrieve.py       # Retrieval logic
│   ├── prompt.py         # Prompt engineering
│   ├── llm.py            # LLM client
│   ├── chunk.py          # Text chunking
│   ├── schemas.py        # API models
│   └── extractors.py     # Multi-format text extraction
├── data/
│   ├── emails/           # Document storage (auto-created)
│   └── index/            # Vector DB + state (auto-created)
├── test/
│   ├── test_api.py
│   ├── test_full_pipeline.py
│   ├── test_document_formats.py
│   ├── test_chunking.py
│   ├── test_edge_cases.py
│   ├── load_sample_data.py
│   └── run_all_tests.py
├── fetch_email.py        # IMAP email fetcher
├── watcher.py            # File watcher and indexer
├── requirements.txt      # Python dependencies
├── .env.example          # Environment template
└── README.md             # This file

---

## Environment Configuration

Create a file named `.env` in the project root by copying `.env.example` and filling the values.

The following settings are supported.

OpenAI and models:

OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx
EMBEDDING_MODEL=text-embedding-3-large
LLM_MODEL=gpt-4o-mini

Email IMAP settings (optional, only needed if you use email fetching):

IMAP_HOST=imap.gmail.com
IMAP_USER=[your-email@gmail.com](mailto:your-email@gmail.com)
IMAP_PASSWORD=your-app-password
IMAP_FOLDER=INBOX

If you do not want to fetch emails, you can leave the IMAP fields empty and just copy files manually into the folder.

---

## How to Run the System (Step by Step)

### 1. Open the Project Folder

Open the folder named `email-rag-pro`.
This folder contains `watcher.py`, the `app` directory, `requirements.txt` and `.env.example`.

---

### 2. Install Dependencies

1. Open a terminal or PowerShell inside the `email-rag-pro` folder.
2. Install the required Python packages by running:
   python -m pip install -r requirements.txt
3. Wait until the installation completes.

---

### 3. Configure Environment Variables

1. Copy `.env.example` and rename it to `.env`.
2. Open `.env` in a text editor.
3. Set at least the following:

OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx

You may also change the models if needed:

EMBEDDING_MODEL=text-embedding-3-large
LLM_MODEL=gpt-4o-mini

If you want to fetch emails, also set:

IMAP_HOST=imap.gmail.com
IMAP_USER=[your-email@gmail.com]
IMAP_PASSWORD=your-app-password
IMAP_FOLDER=INBOX

4. Save the file.

---

### 4. Start the Folder Watcher (Indexer)

1. Open a terminal in the `email-rag-pro` folder.
2. Run:
   python watcher.py
3. Keep this terminal open.

This process will:

* Create the folder `data/emails/` if it does not exist
* Watch this folder for new files
* Automatically index any new document added to this folder

---

### 5. Start the API Server

1. Open a second terminal in the same `email-rag-pro` folder.
2. Run:
   uvicorn app.main:app --reload
3. The API will be available at:
   [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

### 6. Add Documents to the Folder

1. Copy any document into:
   data/emails/

2. Supported formats:

* .txt
* .pdf
* .docx
* .pptx

3. As soon as a file is copied:

* The watcher detects it
* Text is extracted
* The text is chunked
* Chunks are embedded
* Embeddings are stored in the vector database

You will see a confirmation message in the watcher terminal.

---

### 7. Optional: Fetch Emails

If you configured IMAP settings in `.env`:

1. Open a terminal in the project root.
2. Run:
   python fetch_email.py
3. Emails will be saved into `data/emails/` and indexed automatically by the watcher.

---

### 8. Ask Questions

1. Open this URL in your browser:
   [http://127.0.0.1:8000/docs]

2. Select POST /ask and click Try it out.

3. Enter a question, for example:
   What does the contract say about pricing?

4. Set top_k to a number like 5.

5. Click Execute.

The response will include:

* The generated answer
* The source files used

---

### 9. Stop the System

* Go to both terminals.
* Press Ctrl + C in each terminal to stop:

  * The folder watcher
  * The API server

---

## End to End Flow (From Email or File to Answer)

1. An email is fetched or a file is copied into `data/emails/`.
2. `watcher.py` detects the new file.
3. The system extracts text using `extractors.py`.
4. The text is split into overlapping chunks using `chunk.py`.
5. Each chunk is converted into an embedding using the configured embedding model.
6. Embeddings are stored in the persistent vector database under `data/index/`.
7. A user sends a question to the `/ask` API.
8. The question is embedded using the same embedding model.
9. The system retrieves the most relevant chunks from the vector database.
10. A prompt is built using only these chunks.
11. The language model generates an answer from this context using the configured LLM.
12. The API returns the answer along with the source file names.





