# TruLens RAG Evaluation with Google Gemini

This project demonstrates how to build and evaluate a **Retrieval-Augmented Generation (RAG)** pipeline using modern AI tools. It uses **LlamaIndex** to build the RAG pipeline, **Google Gemini** for generation and embeddings, and **TruLens** to evaluate the pipeline's quality.

We use Wikipedia articles as our knowledge base to answer questions about climate change and marine ecosystems.

The project includes two notebooks to demonstrate the difference between a poorly configured RAG pipeline and a highly optimized one:
1. `RAG_eval_bad.ipynb`: Intentionally uses bad chunking, missing context, and poor retrieval to show failing evaluation scores.
2. `RAG_eval_good.ipynb`: Uses optimized chunking, a Sentence Window Index, and comprehensive data to achieve high evaluation scores.

---

## 🚀 Setup Instructions for Windows

Follow these steps to set up and run the project locally on a Windows machine.

### 1. Prerequisites
- **Python 3.9 or higher**: Download and install from [python.org](https://www.python.org/downloads/windows/). Make sure to check the box that says **"Add Python to PATH"** during installation.
- **Git**: Download and install from [git-scm.com](https://git-scm.com/download/win).
- **Google Gemini API Key**: Get a free API key from [Google AI Studio](https://aistudio.google.com/).

### 2. Clone the Repository
Open your terminal (Command Prompt or PowerShell) and run:
```cmd
git clone <your-repository-url>
cd trulens-eval-demo
```

### 3. Create a Virtual Environment
It is highly recommended to use a virtual environment to manage dependencies.
```cmd
python -m venv venv
```

Activate the virtual environment:
- **Command Prompt (cmd):**
  ```cmd
  venv\Scripts\activate.bat
  ```
- **PowerShell:**
  ```powershell
  venv\Scripts\Activate.ps1
  ```
*(Note: If PowerShell gives an execution policy error, run `Set-ExecutionPolicy Unrestricted -Scope CurrentUser` first).*

### 4. Install Dependencies
With your virtual environment activated (you should see `(venv)` in your prompt), install the required Python packages:
```cmd
pip install -r requirements.txt
```

### 5. Setup the Environment Variables
1. Copy the example `.env` file to create your own configuration:
   ```cmd
   copy .env.example .env
   ```
2. Open the `.env` file in Notepad or your favorite code editor.
3. Replace `your_google_api_key_here` with your actual Google Gemini API key (it should start with `AIza...`).

### 6. Run the Project
Start Jupyter Notebook:
```cmd
jupyter notebook
```

This will open a browser window. From there:
1. Open **`RAG_eval_bad.ipynb`** and click "Run All" to see how a poorly configured pipeline fails. 
2. View the TruLens dashboard that launches at the end of the notebook.
3. Close the dashboard, then open **`RAG_eval_good.ipynb`** and click "Run All" to see how a highly optimized pipeline succeeds.

---

## 📊 Understanding the Scores (The RAG Triad)

TruLens evaluates the RAG pipeline using an LLM-as-a-judge on three core metrics:

1. **Context Relevance**: Did the retriever find the right information for the user's question?
2. **Groundedness**: Did the LLM stick to the facts found in the retrieved context without hallucinating?
3. **Answer Relevance**: Did the final answer actually address the user's question?

### Score Interpretation
| Score | Meaning |
|---|---|
| **0.0 – 0.4** | 🛑 Poor — Pipeline is broken, data is missing, or severe hallucinations. |
| **0.4 – 0.6** | 🟡 Mediocre — Needs improvement in chunking or retrieval. |
| **0.6 – 0.8** | 🟢 Good — Working reasonably well. |
| **0.8 – 1.0** | 🌟 Excellent — RAG pipeline is highly tuned and accurate. |

## 🛠️ Built With
- [LlamaIndex](https://www.llamaindex.ai/) - Data framework for building LLM applications.
- [Google Gemini API](https://ai.google.dev/) - `gemini-2.5-flash` for LLM and `gemini-embedding-001` for embeddings.
- [TruLens](https://www.trulens.org/) - Evaluation framework for LLM apps.
- [Wikipedia-API](https://pypi.org/project/Wikipedia-API/) - Sourcing ground truth document context.
