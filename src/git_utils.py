import git
from typing import Dict

def get_staged_files_content() -> Dict[str, str]:
    """
    Returns a dictionary with the paths of the staged files as keys and their
    content as values. If the file is binary or can't be read, it will be
    skipped.

    Returns:
        Dict[str, str]: A dictionary mapping the paths of the staged files to
            their content.
    """
    repo = git.Repo(search_parent_directories=True)
    staged_files = {}
    for item in repo.index.diff("HEAD"):
        if item.a_path and item.change_type in ('A', 'M'):
            try:
                with open(item.a_path, 'r', encoding='utf-8') as f:
                    staged_files[item.a_path] = f.read()
            except (IOError, UnicodeDecodeError) as e:
                print(f"Warning: Failed to read the file {item.a_path}: {e}")
    return staged_files

def get_staged_diff() -> str:
    """
    Returns the staged diff as a string.

    Returns:
        str: The staged diff.
    """
    repo = git.Repo(search_parent_directories=True)
    return repo.git.diff('--staged')
