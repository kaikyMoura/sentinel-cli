feat(cli): introduce AI-powered code analysis tool

This initial commit introduces a new command-line interface (CLI) tool for performing AI-driven code analysis using the Google Gemini API.

The tool is built with Typer and provides several analysis capabilities based on the user's input. It can process code either from the Git staging area or from a supplied `.zip` project archive.

Key Features:
- **Multiple Analysis Tasks**: Supports generating documentation, suggesting code improvements, creating conventional commit messages, and applying improvements directly as a patch.
- **Flexible Input**: Analyzes code from `git diff --staged` or by reading the contents of a `.zip` file.
- **Modular Structure**: The application is organized into modules for handling Git interactions (`git_utils`), file/zip processing (`file_handler`), and communication with the AI model (`ai_analyzer`).
- **Configuration**: The tool can be configured via command-line arguments and environment variables (e.g., for the API key).
- **CI Mode**: Includes a `--ci` flag that can be used in continuous integration pipelines to fail a job if the analysis suggests improvements.