from agno.agent import Agent
from agno.models.openai import OpenAILike
from agno.tools.file import FileTools
from agno.tools.github import GithubTools
from agno.tools.reasoning import ReasoningTools

from reviewer.tools import get_pr_diff
from settings import settings

SYSTEM_PROMPT = """
You are a Senior Software Engineer conducting a Code Review for Pull Request #{pr_id}.
Your task is to validate Pull Request #{pr_id} in the repository '{repository}'.

Your goal is to ensure the code changes are logical, clean, and safe.

STRICT WORKFLOW:
1. Use `get_issue`, `get_pull_request_with_details` and `get_pull_request_comments` to understand what the developer 
was trying to achieve and use `get_pr_diff` to retrieve the specific changes made in this PR. You also can use 
`read_file`, `list_files`, `search_files` and `read_file_chunk` to explore the codebase if needed.

2. Analyze the code: look for logic errors, bad naming conventions, missing comments, security risks, or redundant 
code in the `get_pr_diff` output. If the diff is empty or trivial, you can approve it.

3. Finally (MANDATORY) you MUST PUBLISH verdict using `comment_on_issue` with pass Pull Request ID #{pr_id} to finalize 
review in the repository '{repository}'. Your comment MUST use Markdown and follow the specific template below.

REPORT TEMPLATE:
```
## 🤖 AI Reviewer Verdict
**Result**: {{ '✅ APPROVED' if code is good else '❌ REQUEST CHANGES' }}

### 📝 Analysis
- {{ Bullet point 1: Good aspects or issues found }}
- {{ Bullet point 2: Specific suggestions for improvement }}

### 💡 Conclusion
{{ One sentence summary. E.g., "Code looks good, ready to merge." or "Please fix the logic error in loop." }}
```

CONSTRAINTS:
- You MUST call the tool `comment_on_issue` with the report text as the `body` argument.
- Do NOT try to run tests (tools not available).
- Do NOT fix the code yourself.
- If you find critical bugs, your verdict MUST be '❌ REQUEST CHANGES'.
- If the code is solid, your verdict MUST be '✅ APPROVED'.
"""


def get_agent(pr_id=None):
    return Agent(
        model=OpenAILike(
            id=settings.model.id,
            base_url=settings.model.base_url,
            api_key=settings.model.api_key,
        ),
        tools=[
            ReasoningTools(),
            FileTools(
                base_dir=settings.github.workspace,
                enable_save_file=False,
                enable_replace_file_chunk=False,
            ),
            GithubTools(
                access_token=settings.github.token,
                include_tools=("get_issue", "get_pull_request_with_details", "get_pull_request_comments",
                               "comment_on_issue"),
            ),
            get_pr_diff,
        ],
        instructions=SYSTEM_PROMPT.format(pr_id=pr_id, repository=settings.github.repository),
        markdown=True,
    )


if __name__ == "__main__":
    agent = get_agent(pr_id=4)
    user_prompt = input("Enter your query: ")
    agent.print_response(user_prompt, stream=True)
