from os import path
from typing import TYPE_CHECKING

from .utils.requests import HTTPMethods, Requests

if TYPE_CHECKING:
    from typing import Optional, List
    from .typing import Issue


_BASE_URL = "https://api.github.com/"


class BaseGithubClient:
    path = ""

    def __init__(self, *, username: str, token: str):
        self.username = username
        self.token = token

    @property
    def default_headers(self):
        return {"accept": "application/vnd.github.v3+json"}

    @property
    def default_auth(self):
        return (self.username, self.token)

    def url(self, rest: str = ""):
        return path.join(_BASE_URL, self.path, rest)


class GitHubReposClient(BaseGithubClient):
    path = "repos"

    def get_issues(self, *, username: str, repo_name: str):
        url = self.url(f"{username}/{repo_name}/issues")

        request: "Requests[List[Issue]]" = Requests(
            method=HTTPMethods.POST,
            url=url,
            headers=self.default_headers,
            auth=self.default_auth,
        )
        return request.execute()

    def create_issue(
        self, *, username: str, repo_name: str, title: str, body: "Optional[str]" = None
    ):
        url = self.url(f"{username}/{repo_name}/issues")
        payload = {"title": title}
        if body:
            payload["body"] = body

        request: "Requests[Issue]" = Requests(
            method=HTTPMethods.POST,
            url=url,
            headers=self.default_headers,
            body=payload,
            auth=self.default_auth,
        )
        return request.execute()


class GithubClient:
    def __init__(self, *, username: str, token: str):
        self._repos_client = GitHubReposClient(username=username, token=token)

    def create_issue(
        self, *, username: str, repo_name: str, title: str, body: "Optional[str]" = None
    ):
        return self._repos_client.create_issue(
            username=username, repo_name=repo_name, title=title, body=body
        )
