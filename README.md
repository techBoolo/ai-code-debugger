# AI Code Debugger

A powerful, dual-interface (CLI & Web) tool designed to help you debug code faster using local LLMs. Built with [LangChain](https://python.langchain.com/), [Ollama](https://ollama.com/), [Streamlit](https://streamlit.io/), and [Rich](https://github.com/Textualize/rich).

![Debugger Demo](https://placehold.co/800x400?text=AI+Code+Debugger+CLI)

## Features

- **🔎 Interactive Debugging**: Paste your code and error message to get instant analysis and fixes.
- **🖥️ Dual Interface**: Choose between a Terminal-based CLI or a modern Web Dashboard.
- **💬 Conversational Sessions**: Ask follow-up questions to refine the solution without restarting context.
- **🎨 Rich UI**: Beautiful terminal output with Markdown rendering and syntax highlighting.
- **⌨️ Smart Input**: Multi-line input support (Paste friendly).
  - `Enter`: Submit
  - `Esc+Enter`: Insert new line
- **🔒 Private & Local**: Runs entirely on your machine using Ollama.

## Prerequisites

- **Python 3.12+**
- **[Ollama](https://ollama.com/)**: Must be installed and running.
  - Recommended model: `llama3` (or set your own via env).

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd langchain-basic
   ```

2. **Install dependencies:**
   This project uses `uv` for minimal and fast dependency management.

   ```bash
   # Creates virtualenv and installs dependencies
   uv sync
   ```

   *Alternatively, using standard pip:*
   ```bash
   pip install langchain langchain-ollama python-dotenv prompt_toolkit rich streamlit watchdog
   ```

3. **Configure Environment:**
   Create a `.env` file (optional if using default `llama3`):
   ```bash
   cp .env.example .env
   ```
   *Edit `.env` to change `LLM_MODEL` if needed.*

## Usage

1. **Start the Debugger:**
   ```bash
   uv run main.py
   ```
   *(Or `python main.py` if using standard pip/venv)*

2. **Debug Flow:**
   - **Paste Code**: Paste the problematic code block and press `Enter`.
   - **Paste Error**: Paste the stack trace or describe the bug and press `Enter`.
   - **Review**: Watch the AI analyze the issue with syntax-highlighted code updates.
   - **Refine**: Ask follow-up questions in the chat loop to clarify or fix secondary issues.
   - **New Session**: Press `Enter` on an empty prompt to clear context and start debugging a new file.

## Key Controls

| Action | Shortcut |
|--------|----------|
| **Submit** | `Enter` |
| **New Line** | `Esc` + `Enter` |
| **Exit** | `Ctrl+C` |

## Web Interface

Prefer a graphical interface? Launch the Streamlit app:

1. **Start the Web App:**
   ```bash
   uv run streamlit run app.py
   ```

2. **Features:**
   - 🎨 Modern, dark-mode UI.
   - ⚙️ Sidebar for Model (e.g., `llama3`) and System Persona configuration.
   - 💾 Persistent chat history during the session.

