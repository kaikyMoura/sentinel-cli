import os
import zipfile
import typer
from dotenv import load_dotenv
from pathlib import Path
import git

from src.ai_analyzer import get_client, generate_ai_analysis
from src.git_utils import get_staged_diff, get_staged_files_content, get_all_tracked_files_content
from src.file_handler import process_zip_file

load_dotenv()

app = typer.Typer(
    help="CLI tool to analyze code using AI, from a Git repository or .zip file.",
    add_completion=False,
    no_args_is_help=True,
)


@app.command()
def analyze(
    task: str = typer.Argument(
        ...,
        help="Type of analysis: [improvements|documentation|commits|apply-improvements]",
    ),
    path: Path = typer.Option(
        None,
        "--path",
        "-p",
        help="Path to a project .zip file. If not provided, uses Git changes.",
    ),
    output: str = typer.Option(
        "output.md", "--output", "-o", help="Output file for the result."
    ),
    api_key: str = typer.Option(
        None, "--api-key", help="Your Gemini API key.", envvar="GEMINI_API_KEY"
    ),
    model: str = typer.Option("gemini-2.5-pro", "--model", help="Gemini model to use."),
    ci_mode: bool = typer.Option(
        False, "--ci", help="CI mode: fails if the analysis finds issues."
    ),
):
    """
    Analyze the code and perform an AI task.
    """
    if not api_key:
        print("❌ Gemini API key not found.")
        raise typer.Exit(code=1)

    try:
        client = get_client(api_key)
    except ConnectionError as e:
        print(e)
        raise typer.Exit(code=1)

    context = ""
    # The decision logic is based on the task and whether a path is provided
    if path:
        if task in ["commits", "apply-improvements"]:
            print(
                f"❌ Task '{task}' only works with Git. Do not use the --path option."
            )
            raise typer.Exit(code=1)
        try:
            context = process_zip_file(str(path))
        except (FileNotFoundError, zipfile.BadZipFile, ValueError):
            raise typer.Exit(code=1)
    else:
        try:
            repo = git.Repo(search_parent_directories=True)
        except git.InvalidGitRepositoryError:
            print("❌ Error: This does not seem to be a Git repository.")
            raise typer.Exit(code=1)
        if task == "documentation":
            print(
                "🔍 Reading all tracked files by Git to generate documentation..."
            )
            files = get_all_tracked_files_content(repo)
            if not files:
                print(
                    "❌ No files tracked by Git found in this repository."
                )
                raise typer.Exit(code=1)
            context = "\n\n".join(
                f"--- Start of file: {p} ---\n{c}\n--- End of file: {p} ---"
                for p, c in files.items()
            )
        elif task in ["improvements", "commits", "apply-improvements"]:
            print("🔍 Analyzing the 'staging area' of Git...")
            if task == "improvements":
                files = get_staged_files_content(repo)
                if not files:
                    raise typer.Exit()
                context = "\n\n".join(
                    f"--- Start of file: {p} ---\n{c}\n--- End of file: {p} ---"
                    for p, c in files.items()
                )
            else:
                context = get_staged_diff(repo)
                if not context:
                    raise typer.Exit()
        else:
            print(f"❌ Task '{task}' not supported.")
            raise typer.Exit(code=1)

    result = generate_ai_analysis(client, context, task, model)

    output_path = Path(output)
    if task == "apply-improvements":
        output_path = output_path.with_suffix(".diff")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result)

    print(f"✅ Analysis complete! Result saved to: {output_path}")

    if ci_mode and task == "improvements" and "improvements" in result.lower():
        print("\n🔥 CI mode: Improvements suggested. Returning error code.")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
