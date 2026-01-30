from git import Repo, GitCommandError

from settings import settings


def get_pr_diff(base_branch: str = "main") -> str:
    """
    Returns the string diff between the current HEAD and the base branch (usually main).
    Use this to see what changed.
    """
    try:
        repo = Repo(settings.github.workspace)

        try:
            origin = repo.remote(name="origin")
            origin.fetch(base_branch)
        except Exception as e:
            return f"Warning: Could not fetch origin/{base_branch}. Error: {e}"

        diff_text = repo.git.diff(f"origin/{base_branch}...HEAD")
        if not diff_text:
            return "No changes detected between branches."

        return diff_text

    except GitCommandError as e:
        return f"Git Error: {str(e)}"
    except Exception as e:
        return f"Error getting diff: {str(e)}"
