<h1 align="center">Sentinel - CLI</h1>

## 1. Project Overview

The Sentinel is a command-line interface (CLI) tool designed to leverage the power of Google's Gemini large language models for automated code analysis. It provides developers with AI-driven insights to improve code quality, generate documentation, create conventional commit messages, and automatically refactor code.

The tool is built with Python using the Typer framework for a robust and user-friendly CLI experience. It can operate in two primary modes:
1.  **Git Integration**: Analyzes changes in the Git staging area or all tracked files in the repository.
2.  **Archive Analysis**: Processes an entire codebase provided as a `.zip` archive.

This flexibility makes it a valuable asset for local development workflows and continuous integration (CI) pipelines.

## 2. File Structure

The project is organized into a modular structure to separate concerns, promoting maintainability and scalability.

```
.
├── .env.example            # Example environment variable file
├── .gitignore              # Specifies files and directories to be ignored by Git
├── main.py                 # Main application entry point and CLI command definitions
├── project.bat             # Optional Windows batch script to zip the project for testing
├── requirements.txt        # Lists the project's Python dependencies
└── src/
    ├── __init__.py         # Initializes the 'src' directory as a Python package
    ├── ai_analyzer.py      # Handles all interactions with the Google Gemini API
    ├── file_handler.py     # Manages file system operations, including reading and processing ZIP archives
    └── git_utils.py        # Contains utility functions for interacting with a Git repository
```

## 3. Key Components & Responsibilities

### `main.py`
-   **Role**: Application Entry Point & CLI Controller.
-   **Responsibilities**:
    -   Defines the CLI commands and arguments/options (`task`, `--path`, `--output`, etc.) using **Typer**.
    -   Handles the primary application logic and orchestrates the workflow.
    -   Determines the context source (Git staged changes, all tracked files, or a `.zip` file) based on user input.
    -   Invokes the appropriate functions from `git_utils.py` or `file_handler.py` to gather the code context.
    -   Passes the collected context to the `ai_analyzer.py` module for processing.
    -   Writes the AI-generated output to the specified file.
    -   Implements CI mode (`--ci`), which exits with a non-zero status code if improvements are found.

### `src/ai_analyzer.py`
-   **Role**: AI Interaction Layer.
-   **Responsibilities**:
    -   `get_client()`: Securely initializes the Google Gemini client using the provided API key.
    -   `generate_ai_analysis()`:
        -   Contains the core **prompt engineering** logic. It dynamically selects a system prompt tailored to the specific `task` (e.g., "generate documentation", "suggest improvements").
        -   Constructs the final prompt by combining the system prompt with the provided code context.
        -   Sends the request to the specified Gemini model and returns the text response.
        -   Handles potential errors during the API call.

### `src/git_utils.py`
-   **Role**: Git Repository Interface.
-   **Responsibilities**:
    -   Uses the **GitPython** library to interact with the local repository.
    -   `get_staged_diff()`: Fetches the `diff` of staged changes, used for generating commit messages and applying improvements.
    -   `get_staged_files_content()`: Reads the full content of files that are currently in the staging area.
    -   `get_all_tracked_files_content()`: Reads the content of every file tracked by Git, used for generating whole-project documentation.

### `src/file_handler.py`
-   **Role**: File System and Archive Processor.
-   **Responsibilities**:
    -   `process_zip_file()`:
        -   Validates the existence of the `.zip` file.
        -   Extracts the archive's contents into a temporary directory for safe processing.
        -   Calls `read_project_files_from_dir` to read the extracted project code.
    -   `read_project_files_from_dir()`:
        -   Recursively traverses a project directory.
        -   Filters files based on a predefined list of allowed extensions (e.g., `.py`, `.js`, `.md`).
        -   Skips common non-source directories (e.g., `node_modules`, `.git`, `__pycache__`).
        -   Concatenates the content of all valid files into a single string to be used as context for the AI.

## 4. Setup & Usage Instructions

### Prerequisites
-   Python 3.8+
-   Git

### Installation
1.  **Clone the repository:**
    ```sh
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```sh
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

### Configuration
1.  **Get a Gemini API Key:**
    -   Visit [Google AI Studio](https://aistudio.google.com/) to generate your free API key.

2.  **Set up the environment variable:**
    -   Create a file named `.env` in the project root by copying `.env.example`.
    -   Add your API key to the `.env` file:
        ```env
        GEMINI_API_KEY="YOUR_API_KEY_HERE"
        ```
    -   The application uses `python-dotenv` to load this key automatically. Alternatively, you can pass the key directly via the `--api-key` option.

### Usage
The tool is invoked via the command, followed by a specific task and optional parameters.

**General Syntax:**
`python main.py <TASK> [OPTIONS]`

**Available Tasks:**
-   `improvements`: Reviews staged code and suggests improvements.
-   `documentation`: Generates technical documentation for all tracked files.
-   `commits`: Creates a Conventional Commit message from staged changes.
-   `apply-improvements`: Generates a diff/patch file with suggested improvements.

**Examples:**

1.  **Generate a commit message for staged changes:**
    ```sh
    # Stage your changes first
    git add .
    # Run the command
    python main.py commits --output commit_message.txt
    ```

2.  **Get improvement suggestions for staged files:**
    ```sh
    git add src/main.py
    python main.py improvements --output suggestions.md
    ```

3.  **Generate documentation for the entire project:**
    ```sh
    python main.py documentation -o project_docs.md
    ```

4.  **Analyze a project from a `.zip` archive:**
    ```sh
    python main.py improvements --path /path/to/my-project.zip
    ```
    *Note: The `commits` and `apply-improvements` tasks are not compatible with `.zip` analysis.*

5.  **Generate a patch file to apply improvements:**
    ```sh
    git add .
    python main.py apply-improvements --output changes.diff
    # You can then apply the patch
    # git apply changes.diff
    ```

6.  **Use in a CI/CD Pipeline:**
    The `--ci` flag causes the script to exit with code 1 if the `improvements` task finds any issues, which will fail the pipeline step.
    ```sh
    git add .
    python main.py improvements --ci
    ```
