from os import path

from .utils.make_request import HTTPMethods, make_requests


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
        response_result = make_requests(
            method=HTTPMethods.GET, url=url, headers=self.default_headers
        )
        return response_result


class GithubIssuesClient(BaseGithubClient):
    path = "issues"

    def get_issues(self):
        url = self.url()
        response_result = make_requests(
            method=HTTPMethods.GET, url=url, headers=self.default_headers
        )
        return response_result


class GithubClient:
    def __init__(self, *, token: str):
        self._users_client = GithubUsersClient(token=token)
        self._issues_client = GithubIssuesClient(token=token)

    def get_user(self, *, username: str):
        return self._users_client.get_user(username=username)

    def get_issues(self):
        return self._issues_client.get_issues()
