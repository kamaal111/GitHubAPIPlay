import asyncio
import requests
from typing import TYPE_CHECKING
from requests.exceptions import HTTPError
from enum import Enum
from returns.result import Success, Failure

if TYPE_CHECKING:
    from typing import Any, Dict, Optional
    from requests import Response
    from returns.result import Result


class HTTPMethods(str, Enum):
    GET = "GET"


class RequestException(Exception):
    def __init__(
        self, *, status_code: "Optional[int]" = None, data: "Dict[str, Any]"
    ) -> None:
        self.status_code = status_code
        self.data = data
        super().__init__(data.get("message"))


async def make_requests(
    *, method: HTTPMethods, url: str, headers: "Optional[Dict[str, Any]]" = None
) -> "Result[Dict[str, Any], RequestException]":
    request_method = None
    match method:
        case HTTPMethods.GET:
            request_method = requests.get
        case _:
            return Failure(RequestException(data={"message": "Invalid HTTP method"}))

    def do_request():
        return request_method(url, headers=headers)

    event_loop = asyncio.get_event_loop()
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
