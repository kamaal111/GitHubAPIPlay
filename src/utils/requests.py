import asyncio
import json
import requests
from typing import TYPE_CHECKING, Generic, TypeVar
from requests.exceptions import HTTPError
from enum import Enum, auto
from returns.result import Success, Failure

if TYPE_CHECKING:
    from typing import Any, Dict, Optional, Tuple
    from requests import Response
    from returns.result import Result


class AutoName(Enum):
    def _generate_next_value_(self, start, count, last_values):
        return self


class HTTPMethods(str, AutoName):
    GET = auto()
    POST = auto()


class RequestException(Exception):
    def __init__(
        self, *, status_code: "Optional[int]" = None, data: "Dict[str, Any]"
    ) -> None:
        self.status_code = status_code
        self.data = data
        super().__init__(data.get("message"))


REQUEST_TYPEVAR = TypeVar("REQUEST_TYPEVAR")


class Requests(Generic[REQUEST_TYPEVAR]):
    def __init__(
        self,
        *,
        method: "HTTPMethods",
        url: str,
        headers: "Optional[Dict[str, Any]]" = None,
        body: "Optional[Dict[str, Any]]" = None,
        auth: "Optional[Tuple[str, str]]" = None
    ) -> None:
        self.method = method
        self.url = url
        self.headers = headers
        self.body = body
        self.auth = auth

    async def execute(self) -> "Result[REQUEST_TYPEVAR, RequestException]":
        request_method = None
        match self.method:
            case HTTPMethods.GET:
                request_method = requests.get
            case HTTPMethods.POST:
                request_method = requests.post
            case _:
                return Failure(
                    RequestException(data={"message": "Invalid HTTP method"})
                )

        def do_request():
            data = json.dumps(self.body)
            return request_method(
                self.url, headers=self.headers, data=data, auth=self.auth
            )

        event_loop = asyncio.get_running_loop()
        response = await event_loop.run_in_executor(None, do_request)
        try:
            response.raise_for_status()
        except HTTPError as error:
            error_response: "Response" = error.response
            return Failure(
                RequestException(
                    status_code=response.status_code, data=error_response.json()
                )
            )

        return Success(response.json())
