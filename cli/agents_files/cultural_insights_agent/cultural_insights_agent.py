import asyncio
from typing import Annotated
from genai_session.session import GenAISession
from genai_session.utils.context import GenAIContext

AGENT_JWT = "<your JWT Token>"

session = GenAISession(jwt_token=AGENT_JWT)


SYSTEM_PROMPT = (
    "You are an expert on cultural etiquette and cross-cultural communication who is helping learn the language with Native Fluency."
    "You are here to make the new Language more Fun to learn."
    "You will be given a user's conversation text, which may be in any language. "
    "Your task is to analyze the conversation for potential cultural idioms, references, or etiquette insights. "
    "ALWAYS write your feedback in ENGLISH ONLY, even if the conversation itself is in another language. "
    "Do not translate the conversation. Do not respond in the conversation's language. "
    "Your feedback must be titled 'Insights:' and include only 2–3 concise bullet points starting with '-'. "
    "Each bullet should suggest fun facts, culturally appropriate alternatives, or short practical use cases. "
    "Keep your response professional, clear, and limited to those 2–3 bullet-pointed insights in ENGLISH ONLY."
)




@session.bind(
    name="cultural_insights_agent",
    description="Provide Cultural Insights based on conversation text."
)
async def cultural_insights_agent(
    agent_context: GenAIContext,
    conversation_text: Annotated[
        str,
        "The conversation text the user wants analyzed for cultural etiquette and appropriateness."
    ]
):
    """
    Instead of calling the LLM locally, return the prompt messages for AgentOS
    to pass to the configured model.
    """

    agent_context.logger.info("Inside cultural_insights_agent")

    # Return the prompt as message list for AgentOS to use
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Conversation Text: {conversation_text}\nPlease provide cultural feedback and suggestions."}
    ]


async def main():
    print(f"Cultural Insights Agent started with JWT: {AGENT_JWT}")
    await session.process_events()

if __name__ == "__main__":
    asyncio.run(main())