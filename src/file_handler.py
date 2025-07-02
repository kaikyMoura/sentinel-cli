import os
import zipfile
import tempfile
from pathlib import Path
from typing import List, Set

# The list of directories to ignore
IGNORED_DIRS: Set[str] = {"node_modules", ".git", ".next", "__pycache__", "dist"}

# The list of allowed file extensions
ALLOWED_EXTENSIONS: List[str] = [
    ".js", ".ts", ".tsx", ".json", ".css", ".html",
    ".md", ".py", ".go", ".rs",
]

# The maximum character limit
MAX_CHAR_LIMIT: int = 2_000_000

def read_project_files_from_dir(project_path: str) -> str:
    """
    Reads all project files from the specified directory, concatenating their
    content into a single string while respecting certain filters.

    This function walks through the directory tree of the given project path,
    skipping directories defined in IGNORED_DIRS and processing only files with
    extensions listed in ALLOWED_EXTENSIONS. Each file's content is encapsulated
    with markers indicating the start and end of the file, along with its relative path.

    Args:
        project_path (str): The root directory path of the project to read.

    Returns:
        str: The concatenated content of all readable files with allowed extensions,
             formatted with start and end markers. If the total content exceeds
             MAX_CHAR_LIMIT, it returns early with a partial content warning.
    """
    full_content = ""
    print(f"📂 Reading files from: {project_path}")

    for root, _, files in os.walk(project_path):
        # Check if the current directory should be ignored
        if any(ignored_dir in root.split(os.sep) for ignored_dir in IGNORED_DIRS):
            continue

        for file in files:
            file_path = Path(root) / file
            # Check if the file extension is allowed
            if file_path.suffix in ALLOWED_EXTENSIONS:
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        relative_path = os.path.relpath(file_path, project_path)
                        full_content += f"\n\n--- Start of file: {relative_path} ---\n"
                        full_content += content
                        full_content += f"\n--- End of file: {relative_path} ---\n"

                        if len(full_content) > MAX_CHAR_LIMIT:
                            print("⚠️ Project too large. The analysis may be partial.")
                            return full_content
                except Exception as e:
                    print(f"Warning: Could not read file {file_path}. Error: {e}")
                    pass
    return full_content

def process_zip_file(zip_path: str) -> str:
    """
    Processes a ZIP file containing a project directory, extracting and reading
    its files.

    This function checks for the existence of the specified ZIP file and attempts
    to extract its contents into a temporary directory. It reads all valid source
    code files from the extracted directory, as defined by allowed extensions and 
    ignoring certain directories, and concatenates their content.

    Args:
        zip_path (str): The file path to the ZIP archive to be processed.

    Returns:
        str: The concatenated content of all readable files within the ZIP archive.

    Raises:
        FileNotFoundError: If the ZIP file does not exist at the specified path.
        BadZipFile: If the ZIP file is invalid or corrupted.
        ValueError: If no valid source code files are found in the ZIP archive.
    """
    if not os.path.exists(zip_path):
        print(f"❌ File not found: {zip_path}")
        raise FileNotFoundError

    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Unzipping '{zip_path}'...")
        try:
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(temp_dir)
        except zipfile.BadZipFile:
            print("❌ Invalid or corrupted ZIP file.")
            raise
        
        project_code = read_project_files_from_dir(temp_dir)

        if not project_code:
            print("❌ No valid source code files found in the .zip.")
            raise ValueError("No valid files found.")
            
        return project_code
