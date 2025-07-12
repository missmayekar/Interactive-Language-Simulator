import asyncio
import os
from typing import Any, Annotated

import requests
from dotenv import load_dotenv
from genai_session.session import GenAISession

load_dotenv()

BASE_URL = "http://api.weatherapi.com/v1/forecast.json"
REQUEST_KEY = os.environ.get("REQUEST_KEY")

session = GenAISession(
    jwt_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3ZjBkYjlkNi1kODQ0LTQ5YzYtYTkxYy1kOWZlMmM4YWUyYzgiLCJleHAiOjI1MzQwMjMwMDc5OSwidXNlcl9pZCI6IjI5ODMzM2QyLTFkMWQtNDNlNS04NGZlLTI5NjA4NWE2YTU4MCJ9.wUarDl1T0WMvv776M_KhqzTCozo2p__0F5eTiNpXvS8"
)


@session.bind(name="get_weather", description="Get weather forecast data")
async def get_weather(
        agent_context, city_name: Annotated[str, "City name to get weather forecast for"],
        date: Annotated[str, "Date to get forecast for in yyyy-MM-dd format"]
) -> dict[str, Any]:
    agent_context.logger.info("Inside get_translation")
    params = {"q": city_name, "dt": date, "key": REQUEST_KEY}
    response = requests.get(BASE_URL, params=params)

    return {"weather_forecast": response.json()["forecast"]["forecastday"][0]["day"]}


async def main():
    print(REQUEST_KEY)
    await session.process_events()


if __name__ == "__main__":
    asyncio.run(main())
