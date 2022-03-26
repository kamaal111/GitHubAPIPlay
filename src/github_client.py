import json
import requests
from typing import TYPE_CHECKING
from requests.exceptions import HTTPError
from os import path
from returns.result import Success, Failure

if TYPE_CHECKING:
    from typing import Any, Dict
    from returns.result import Result


_BASE_URL = "https://api.github.com/"


class BaseGithubClient:
    path = ""

    def __init__(self, *, token: str):
        self.token = token

    def url(self, rest: str = ""):
        return path.join(_BASE_URL, self.path, rest)


class GithubUsersClient(BaseGithubClient):
    path = "users"

    def get_user(self, *, username: str) -> "Result[Dict[str, Any], HTTPError]":
        url = self.url(username)
        response = requests.get(url)
        try:
            response.raise_for_status()
        except HTTPError as error:
            return Failure(error)

        data = json.loads(response.content)
        return Success(data)


class GithubClient:
    def __init__(self, *, token: str):
        self._users_client = GithubUsersClient(token=token)

    def get_user(self, *, username: str):
        return self._users_client.get_user(username=username)
