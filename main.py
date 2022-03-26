import asyncio
from os import environ
from dotenv import load_dotenv
from returns.result import Success, Failure

from src.github_client import GithubClient

load_dotenv()


async def main():
    github_token = environ.get("GITHUB_TOKEN")
    if not github_token:
        raise Exception("no github token provided")

    github_client = GithubClient(token=github_token)
    user_result = await github_client.get_user(username="kamaal111")
    match user_result:
        case Failure(error):
            print(f"what a failure {error=}")
        case Success(data):
            print(f"success {data=}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
