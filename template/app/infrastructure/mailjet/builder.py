from typing import Self

from app.infrastructure.mailjet.types import (
    JSON,
    Attachment,
    EmailUser,
    InlineAttachment,
    MailjetMessagePayload,
)


class MailjetPayloadBuilder:  # noqa: WPS214 allowed for builder pattern
    """Builder for Mailjet payload.

    See https://dev.mailjet.com/email/reference/send-emails#v3_1_post_send
    """

    def __init__(self) -> None:
        self._payload: MailjetMessagePayload = {}

    def build(self) -> MailjetMessagePayload:
        """Build the payload."""
        return self._payload

    def set_from(self, email: str, name: str | None = None) -> Self:
        """Set the sender email and name."""
        self._payload["From"] = self._build_email_user(email, name)
        return self

    def set_sender(self, email: str, name: str | None = None) -> Self:
        """Set the sender email and name."""
        self._payload["Sender"] = self._build_email_user(email, name)
        return self

    def add_to(self, email: str, name: str | None = None) -> Self:
        """Add a recipient email and name."""
        if "To" not in self._payload:
            self._payload["To"] = []
        self._payload["To"].append(self._build_email_user(email, name))
        return self

    def add_cc(self, email: str, name: str | None = None) -> Self:
        """Add a CC recipient email and name."""
        if "Cc" not in self._payload:
            self._payload["Cc"] = []
        self._payload["Cc"].append(self._build_email_user(email, name))
        return self

    def add_bcc(self, email: str, name: str | None = None) -> Self:
        """Add a BCC recipient email and name."""
        if "Bcc" not in self._payload:
            self._payload["Bcc"] = []
        self._payload["Bcc"].append(self._build_email_user(email, name))
        return self

    def set_reply_to(self, email: str, name: str | None = None) -> Self:
        """Set the Reply-To email and name."""
        self._payload["ReplyTo"] = self._build_email_user(email, name)
        return self

    def set_subject(self, subject: str) -> Self:
        """Set the email subject."""
        self._payload["Subject"] = subject
        return self

    def set_text_part(self, text: str) -> Self:
        """Set the plain text part of the email."""
        self._payload["TextPart"] = text
        return self

    def set_html_part(self, html: str) -> Self:
        """Set the HTML part of the email."""
        self._payload["HTMLPart"] = html
        return self

    def set_template_id(self, template_id: int) -> Self:
        """Set the template ID for the email."""
        self._payload["TemplateID"] = template_id
        return self

    def set_template_language(self, *, use: bool = True) -> Self:
        """Set whether the template language is used."""
        self._payload["TemplateLanguage"] = use
        return self

    def set_template_error_reporting(
        self,
        email: str,
        name: str | None = None,
    ) -> Self:
        """Set the email address for template error reporting."""
        self._payload["TemplateErrorReporting"] = self._build_email_user(email, name)
        return self

    def set_template_error_deliver(self, *, use: bool = True) -> Self:
        """Set whether to deliver the email even if there is a template error."""
        self._payload["TemplateErrorDeliver"] = use
        return self

    def add_attachment(
        self,
        content_type: str,
        filename: str,
        base64_content: str,
    ) -> Self:
        """Add an attachment to the email."""
        if "Attachments" not in self._payload:
            self._payload["Attachments"] = []
        attachment: Attachment = {
            "ContentType": content_type,
            "Filename": filename,
            "Base64Content": base64_content,
        }
        self._payload["Attachments"].append(attachment)
        return self

    def add_inline_attachment(
        self,
        content_type: str,
        filename: str,
        base64_content: str,
        content_id: str,
    ) -> Self:
        """Add an inline attachment to the email."""
        if "InlineAttachments" not in self._payload:
            self._payload["InlineAttachments"] = []
        inline_attachment: InlineAttachment = {
            "ContentType": content_type,
            "Filename": filename,
            "Base64Content": base64_content,
            "ContentID": content_id,
        }
        self._payload["InlineAttachments"].append(inline_attachment)
        return self

    def set_priority(self, priority: int) -> Self:
        """Set the email priority."""
        self._payload["Priority"] = priority
        return self

    def set_custom_campaign(self, campaign: str) -> Self:
        """Set the custom campaign name."""
        self._payload["CustomCampaign"] = campaign
        return self

    def set_deduplicate_campaign(self, *, use: bool = True) -> Self:
        """Set whether to deduplicate the campaign."""
        self._payload["DeduplicateCampaign"] = use
        return self

    def set_track_opens(self, *, use: bool = True) -> Self:
        """Set whether to track email opens."""
        self._payload["TrackOpens"] = use
        return self

    def set_track_clicks(self, *, use: bool = True) -> Self:
        """Set whether to track email clicks."""
        self._payload["TrackClicks"] = use
        return self

    def set_custom_id(self, custom_id: str) -> Self:
        """Set the custom ID for the email."""
        self._payload["CustomID"] = custom_id
        return self

    def set_event_payload(self, payload: str) -> Self:
        """Set the event payload for the email."""
        self._payload["EventPayload"] = payload
        return self

    def set_url_tags(self, tags: str) -> Self:
        """Set the URL tags for the email."""
        self._payload["URLTags"] = tags
        return self

    def set_headers(self, headers: dict[str, str]) -> Self:
        """Set custom headers for the email."""
        self._payload["Headers"] = headers
        return self

    def set_variables(self, variables: dict[str, JSON]) -> Self:
        """Set custom variables for the email."""
        self._payload["Variables"] = variables
        return self

    def _build_email_user(
        self,
        email: str,
        name: str | None = None,
    ) -> EmailUser:
        """Build an email user dictionary."""
        user: EmailUser = {"Email": email}
        if name:
            user["Name"] = name
        return user
