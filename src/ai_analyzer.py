import os
from google import genai

def get_client(api_key: str):
    """
    Initializes and returns a GenAI client using the provided API key.

    Args:
        api_key (str): The API key for authenticating with the GenAI service.

    Returns:
        The initialized GenAI client.

    Raises:
        ConnectionError: If the API client configuration fails.
    """
    try:
        return genai.Client(api_key=api_key)
        return genai
    except Exception as e:
        raise ConnectionError(f"The API client configuration failed: {e}") from e

def generate_ai_analysis(client: genai.Client, code_context: str, task: str, model_name: str) -> str:
    """
    Sends the given code context to the specified GenAI model with a task prompt and
    returns the generated Markdown content.

    Args:
        client: The GenAI client to use.
        code_context (str): The full content of the codebase.
        task (str): The task to perform, either "documentation", "improvements", "commits", or "apply-improvements".
        model_name (str): The name of the GenAI model to use.

    Returns:
        str: The generated content.

    Raises:
        Exception: If the AI model generation fails.
    """
    print(f"🤖 Sendind text to the model {model_name}...")

    prompts = {
        "documentation": """
          Act as a senior software engineer and generate a professional, clear, and concise technical documentation in Markdown.
          Include: 1. Project Overview 2. File Structure 3. Key Components & Responsibilities 4. Setup & Usage Instructions.
        """,
        "improvements": """
          Act as a senior software engineer and review the code.
          Provide detailed improvement suggestions in Markdown, categorized by:
          1. Code Quality 2. Bug Risks 3. Performance Enhancements 4. Security Best Practices.
        """,
        "commits": """
          Act as an experienced software engineer. Based on the following 'git diff', generate a clear and concise commit message following Conventional Commits specification.
          The message should have a header, an optional body, and an optional footer.
          Example: feat(api): add new endpoint for users
        """,
        "apply-improvements": """
          Act as a senior software engineer. Based on the provided code, rewrite it by applying best practices for quality, performance, and security.
          Your response should ONLY be the modified code, with no explanations, so I can apply it directly as a patch.
          If there are multiple files, format the output as a .diff file.
        """
    }

    if task not in prompts:
        return "❌ Unknown task. The available tasks are: documentation, improvements, commits, apply-improvements."

    prompt = f"{prompts[task]}\n\n--- Context/Diff ---\n{code_context}"

    try:
        response = client.models.generate_content(model=model_name, contents=prompt)
        return response.text or "⚠️ The ai model did not return any content."
    except Exception as e:
        return f"❌ Error generating AI analysis: {e}"
