import asyncio
from typing import Annotated
from genai_session.session import GenAISession
from genai_session.utils.context import GenAIContext

AGENT_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3MWRhMTU0NS00MmY0LTRmOTAtYTQwYy00YWVhYzYxNGE5MmUiLCJleHAiOjI1MzQwMjMwMDc5OSwidXNlcl9pZCI6IjI5ODMzM2QyLTFkMWQtNDNlNS04NGZlLTI5NjA4NWE2YTU4MCJ9.XucI6W9CkAvXR_RJZPVU_ajGxzKtvp3jE6QwCxIlMiU" # noqa: E501
session = GenAISession(jwt_token=AGENT_JWT)

SYSTEM_PROMPT = (
    "You are a professional grammar mentor helping users improve their language skills."
    " You will be given a transcript of a conversation between a language agent and a user."
    " The user's responses are annotated with the prefix 'user:'."
    " Your task is to identify only the user responses that are grammatically incorrect."
    " For each incorrect response, provide the following:"
    "\n\n- The original incorrect sentence (as written by the user)."
    "\n- A detailed explanation of the grammar mistake, including what rule is violated and why it's incorrect."
    "\n- Two example sentences that demonstrate the correct usage of the grammar rule."
    "\n- The corrected version of the user's sentence."
    "\n\nDo not comment on responses that are grammatically correct."
    " Only respond about incorrect responses."
    " Your feedback must be in English only, even if the original sentence is in another language."
    " Do not translate the user's sentence or write in their language."
    " Format your response clearly for each issue like this:"
    "\n\nResponse X:\n- Original: ...\n- Issue: ...\n- Examples: ...\n- Corrected: ..."
)


@session.bind(
    name="grammar_assessment_agent",
    description="Assess user's grammar from a conversation transcript."
)
async def grammar_assessment_agent(
    agent_context: GenAIContext,
    transcript: Annotated[
        str,
        "The full transcript between a language agent and the user. User responses are marked with 'user:'."
    ]
):
    """
    Returns prompt messages for AgentOS to pass to the LLM.
    """
    agent_context.logger.info("Inside grammar_assessment_agent")

    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Transcript:\n{transcript}\n\nPlease evaluate each user response for grammar as described."}
    ]


async def main():
    print(f"Grammar Assessment Agent started with JWT: {AGENT_JWT}")
    await session.process_events()

if __name__ == "__main__":
    asyncio.run(main())

