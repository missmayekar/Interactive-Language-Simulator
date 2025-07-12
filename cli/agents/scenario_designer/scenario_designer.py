import asyncio
from typing import Annotated
from genai_session.session import GenAISession
from genai_session.utils.context import GenAIContext
AGENT_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyODY0ZGQ4MC01NGM3LTQ5YTQtOWI5NS01NWIyYzkzZDM3MWQiLCJleHAiOjI1MzQwMjMwMDc5OSwidXNlcl9pZCI6IjI5ODMzM2QyLTFkMWQtNDNlNS04NGZlLTI5NjA4NWE2YTU4MCJ9.g3076zTzV5Lcb-3FBo_Zo_tdn2GZypy-dkz18LdvL6Y" # noqa: E501

session = GenAISession(jwt_token=AGENT_JWT)
SYSTEM_PROMPT = (
    "You are a language training assistant. Generate short, practical, and realistic dialogues "
    "between two people for language learners to practice speaking in everyday scenarios. "
    "Each dialogue must be clearly structured as a conversation with alternating lines between "
    "'User:' (the learner) and 'Native Speaker:' (a native speaker or conversation partner). "
    "Keep the user's lines simple and slightly imperfect to reflect common learner mistakes at the given fluency level, "
    "so they can be evaluated and corrected later by a grammar mentor. "
    "Do not label or number the dialogue lines. Avoid long or complex sentences. "
    "Ensure the overall conversation is polite, relevant to the scenario, and natural-sounding."
)

@session.bind(
    name="scenario_designer_agent",
    description="Creates language learning dialogue scripts based on user-defined scenario, language, and level."
)
async def scenario_designer_agent(
    agent_context: GenAIContext,
    scenario: Annotated[str, "Scenario for the conversation (e.g., 'buying flowers')"],
    language: Annotated[str, "Target language (e.g., 'English')"],
    level: Annotated[str, "User level (e.g., 'beginner')"]
):
    agent_context.logger.info(f"Generating scenario script: {scenario} - {language} - {level}")

    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"""Create a short dialogue between two people based on the following:
- Scenario: {scenario}
- Language: {language}
- Level: {level}

Instructions:
- Keep it 4–6 exchanges long
- Define roles of the user
- Use language appropriate to the level
- Avoid political/cultural bias
- Output in plain text only"""},
    ]

async def main():
    print("Scenario Designer Agent started...")
    await session.process_events()

if __name__ == "__main__":
    asyncio.run(main())
