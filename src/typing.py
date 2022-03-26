from typing import List, Literal, Optional, TypedDict


class User(TypedDict):
    login: str
    id: int
    avatar_url: str
    url: str


IssueReactions = TypedDict(
    "IssueReactions",
    {
        "url": str,
        "total_count": int,
        "+1": int,
        "-1": int,
        "laugh": int,
        "hooray": int,
        "confused": int,
        "heart": int,
        "rocket": int,
        "eyes": int,
    },
)


class IssueLabel(TypedDict):
    id: int
    url: str
    name: str
    description: str
    color: str
    default: bool


class Issue(TypedDict):
    url: str
    repository_url: str
    id: int
    number: int
    title: str
    user: "User"
    labels: "List[IssueLabel]"
    state: "Literal['open']"
    locked: bool
    assignee: "Optional[User]"
    assignees: "List[User]"
    comments: int
    created_at: str
    updated_at: str
    closed_at: "Optional[str]"
    author_association: "Literal['OWNER', 'COLLABORATOR']"
    body: "Optional[str]"
    reactions: "IssueReactions"
