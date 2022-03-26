from os import path
from typing import TYPE_CHECKING

from .utils.requests import HTTPMethods, Requests

if TYPE_CHECKING:
    from typing import Any, Dict


_BASE_URL = "https://api.github.com/"


class BaseGithubClient:
    path = ""

    def __init__(self, *, token: str):
        self.token = token

    @property
    def default_headers(self):
        return {"Authorization": f"token: {self.token}"}

    def url(self, rest: str = ""):
        return path.join(_BASE_URL, self.path, rest)


class GithubUsersClient(BaseGithubClient):
    path = "users"

    def get_user(self, *, username: str):
        url = self.url(username)
        request: "Requests[Dict[str, Any]]" = Requests(
            method=HTTPMethods.GET, url=url, headers=self.default_headers
        )
        return request.execute()


class GithubIssuesClient(BaseGithubClient):
    path = "issues"

    def get_issues(self):
        url = self.url()
        request: "Requests[Dict[str, Any]]" = Requests(
            method=HTTPMethods.GET, url=url, headers=self.default_headers
        )
        return request.execute()


class GithubClient:
    def __init__(self, *, token: str):
        self._users_client = GithubUsersClient(token=token)
        self._issues_client = GithubIssuesClient(token=token)

    def get_user(self, *, username: str):
        return self._users_client.get_user(username=username)

    def get_issues(self):
        return self._issues_client.get_issues()
