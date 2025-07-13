import asyncio
from typing import Annotated
from genai_session.session import GenAISession
from genai_session.utils.context import GenAIContext

AGENT_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmMDYwYmU3Ny00MWFjLTQyYmYtODNjMi1kNzFkZmJjMTdjMjgiLCJleHAiOjI1MzQwMjMwMDc5OSwidXNlcl9pZCI6IjdjYTY1MjZiLTVmMTktNDBmYy1hZmIyLTU1NWUzYTdiZjJkOCJ9.M2j8xGTi-0mGNt1qUqCWYJ5uuQkHX5L1_yTZjjvk5kU" # noqa: E501
session = GenAISession(jwt_token=AGENT_JWT)


@session.bind(
    name="speech_mentor",
    description="analyses grammar and provides feedback"
)
async def speech_mentor(
    agent_context: GenAIContext,
    test_arg: Annotated[
        str,
        "This is a test argument. Your agent can have as many parameters as you want. Feel free to rename or adjust it to your needs.",  # noqa: E501
    ],
):
    """analyses grammar and provides feedback"""
    return "Hello, World!"


async def main():
    print(f"Agent with token '{AGENT_JWT}' started")
    await session.process_events()

if __name__ == "__main__":
    asyncio.run(main())
