import git
from typing import Dict, List

# This represents the empty tree SHA
EMPTY_TREE_SHA = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"

def get_staged_files_content(repo: git.Repo) -> Dict[str, str]:
    """
    Gets the content of files in the Git staging area by reading from the index.
    
    For an initial commit (when there is no HEAD), this function reads from the
    filesystem. Otherwise, it reads from the Git index.
    
    Returns a mapping of file paths to their contents.
    """
    if not repo.head.is_valid():
        staged_files = {}
        for item in repo.index.iter_blobs():
            path, blob = item
            try:
                staged_files[path] = blob.data_stream.read().decode('utf-8')
            except (IOError, UnicodeDecodeError) as e:
                print(f"Warning: Unable to read file {path}: {e}")
        return staged_files

    staged_files = {}
    for item in repo.index.diff("HEAD"):
        if item.a_path and item.change_type in ('A', 'M'):
            try:
                with open(item.a_path, 'r', encoding='utf-8') as f:
                    staged_files[item.a_path] = f.read()
            except (IOError, UnicodeDecodeError) as e:
                print(f"Warning: Unable to read file {item.a_path}: {e}")
    return staged_files

def get_staged_diff(repo: git.Repo) -> str:
    """
    Gets a unified diff of the staged changes.
    
    If the repository has no HEAD (i.e., this is the initial commit), this function
    returns the full contents of all files in the staging area.
    
    Returns a string containing the unified diff.
    """
    if not repo.head.is_valid():
        return repo.git.diff('--staged', '--no-color', EMPTY_TREE_SHA)
    
    return repo.git.diff('--staged', '--no-color')

def has_unstaged_changes(repo: git.Repo) -> bool:
    """
    Checks if there are any unstaged changes in the repository.

    Args:
        repo: A GitPython Repo object representing the Git repository.

    Returns:
        bool: True if there are unstaged changes, False otherwise.
    """

    return bool(repo.index.diff(None))

def get_all_tracked_files_content(repo: git.Repo) -> Dict[str, str]:
    """
    Retrieves the content of all files tracked by Git in the current repository.

    This function iterates over each file path obtained from the Git index and
    reads the file content from the filesystem. The content is stored in a dictionary
    with the file paths as keys.

    Args:
        repo: A GitPython Repo object representing the Git repository.

    Returns:
        Dict[str, str]: A dictionary where keys are file paths and values are the
        corresponding file contents.

    Warnings:
        Prints a warning message if a file cannot be read due to an IOError or
        UnicodeDecodeError.
    """
    tracked_files = {}
    for file_path in repo.git.ls_files().splitlines():
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tracked_files[file_path] = f.read()
        except (IOError, UnicodeDecodeError) as e:
            print(f"Warning: Unable to read tracked file {file_path}: {e}")
    return tracked_files

