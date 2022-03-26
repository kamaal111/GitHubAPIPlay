from os import path
from typing import TYPE_CHECKING

from .utils.requests import HTTPMethods, Requests

if TYPE_CHECKING:
    from typing import Optional, List, Any, Dict
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
            method=HTTPMethods.GET,
            url=url,
            headers=self.default_headers,
            auth=self.default_auth,
        )
        return request.execute()

    def get_issue(self, *, username: str, repo_name: str, issue_number: int):
        url = self.url(f"{username}/{repo_name}/issues/{issue_number}")

        request: "Requests[Issue]" = Requests(
            method=HTTPMethods.GET,
            url=url,
            headers=self.default_headers,
            auth=self.default_auth,
        )
        return request.execute()

    def create_issue(
        self,
        *,
        username: str,
        repo_name: str,
        title: str,
        description: "Optional[str]" = None,
        assignee: "Optional[str]" = None,
        labels: "Optional[List[str]]" = None,
    ):
        url = self.url(f"{username}/{repo_name}/issues")
        payload: "Dict[str, Any]" = {"title": title}
        if description:
            payload["body"] = description
        if assignee:
            payload["assignee"] = assignee
        if labels:
            payload["labels"] = labels

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

    def get_issues(self, *, username: str, repo_name: str):
        return self._repos_client.get_issues(username=username, repo_name=repo_name)

    def get_issue(self, *, username: str, repo_name: str, issue_number: int):
        return self._repos_client.get_issue(
            username=username, repo_name=repo_name, issue_number=issue_number
        )

    def create_issue(
        self,
        *,
        username: str,
        repo_name: str,
        title: str,
        description: "Optional[str]" = None,
        assignee: "Optional[str]" = None,
        labels: "Optional[List[str]]" = None,
    ):
        return self._repos_client.create_issue(
            username=username,
            repo_name=repo_name,
            title=title,
            description=description,
            assignee=assignee,
            labels=labels,
        )
