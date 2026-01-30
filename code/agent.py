from agno.agent import Agent
from agno.models.openai import OpenAILike
from agno.tools.file import FileTools
from agno.tools.github import GithubTools
from agno.tools.reasoning import ReasoningTools

from settings import settings


def get_agent():
    return Agent(
        model=OpenAILike(
            id=settings.model.id,
            base_url=settings.model.base_url,
            api_key=settings.model.api_key,
        ),
        tools=[
            ReasoningTools(),
            FileTools(),  # TODO: probably add enable_delete_file=True
            GithubTools(
                access_token=settings.github.token,
                include_tools=("get_issue", "create_pull_request"),
            ),
        ],
        markdown=True,
    )


if __name__ == "__main__":
    agent = get_agent()
    user_prompt = input("Enter your query: ")
    agent.print_response(user_prompt, stream=True)
