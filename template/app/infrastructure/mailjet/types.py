# noqa: A005
from typing import Literal, NotRequired, TypedDict

type Primitives = str | int | float | bool | None
type JSON = dict[str, Primitives] | list[Primitives] | Primitives


class EmailUser(TypedDict):
    Email: str
    Name: NotRequired[str]


class Attachment(TypedDict):
    ContentType: str
    Filename: str
    Base64Content: str


class InlineAttachment(TypedDict):
    ContentType: str
    Filename: str
    Base64Content: str
    ContentID: str


class MailjetMessagePayload(TypedDict, total=False):
    """Mailjet payload."""

    From: EmailUser
    """Sender name and email."""
    Sender: EmailUser
    """Specifies the sender name and email address. Used when you want to send emails on behalf of a different email address."""
    To: list[EmailUser]
    """List of recipient names and emails."""
    Cc: list[EmailUser]
    """List of CC recipient names and emails."""
    Bcc: list[EmailUser]
    """List of BCC recipient names and emails."""
    ReplyTo: EmailUser
    """Reply-To email address and name."""
    Subject: str
    """Email subject."""
    TextPart: str
    """Plain text part of the email."""
    HTMLPart: str
    """HTML part of the email."""
    TemplateID: int
    """Template ID for the email."""
    TemplateLanguage: bool
    """Indicates whether the template language is used."""
    TemplateErrorReporting: EmailUser
    """Email address for template error reporting."""
    TemplateErrorDeliver: bool
    """Indicates whether to deliver the email even if there is a template error."""
    Attachments: list[Attachment]
    """List of attachments."""
    InlineAttachments: list[InlineAttachment]
    """List of inline attachments."""
    Priority: int
    """Email priority."""
    CustomCampaign: str
    """Custom campaign name."""
    DeduplicateCampaign: bool
    """Indicates whether to deduplicate the campaign."""
    TrackOpens: bool
    """Indicates whether to track email opens."""
    TrackClicks: bool
    """Indicates whether to track email clicks."""
    CustomID: str
    """Custom ID for the email."""
    EventPayload: str
    """Event payload for the email."""
    URLTags: str
    """URL tags for the email."""
    Headers: dict[str, str]
    """Custom headers for the email."""
    Variables: dict[str, JSON]
    """Custom variables for the email."""


class MailjetSendError(TypedDict):
    ErrorIdentifier: str
    ErrorCode: int
    StatusCode: int
    ErrorMessage: str
    ErrorRelatedTo: JSON
    """Indicates which part of the payload this error is related to."""


class SentEmailUser(TypedDict):
    Email: str
    MessageUUID: str
    MessageID: str
    MessageHref: str


class MailjetMessageResponse(TypedDict):
    Status: Literal["success", "error"]
    Errors: list[MailjetSendError]
    CustomID: str
    To: list[SentEmailUser]
    Cc: list[SentEmailUser]
    Bcc: list[SentEmailUser]


class MailjetSendMessagesResponse(TypedDict):
    """Mailjet send messages response."""

    Messages: list[MailjetMessageResponse]
    """List of messages with their status and ID."""
