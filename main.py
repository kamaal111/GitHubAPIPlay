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
    issues_result = await github_client.create_issue(
        username="kamaal111", repo_name="GitHubAPIPlay", title="Test", body="Testing"
    )
    match issues_result:
        case Failure(error):
            print(f"{error.status_code}: what a failure {error}")
        case Success(data):
            print(f"success {data=}")


if __name__ == "__main__":
    asyncio.run(main())
