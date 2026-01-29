from agno.agent import Agent
from agno.models.openrouter import OpenRouter

from settings import settings


def get_agent():
    return Agent(
        model=OpenRouter(
            id=settings.openrouter.model,
            base_url=settings.openrouter.base_url,
            api_key=settings.openrouter.api_key,
        ),
        markdown=True,
    )


if __name__ == "__main__":
    agent = get_agent()
    user_query = "Test"
    agent.print_response(user_query)
