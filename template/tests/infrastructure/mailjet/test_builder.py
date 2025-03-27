"""Tests for Mailjet payload builder."""

import pytest

from app.infrastructure.mailjet.builder import (
    MailjetPayloadBuilder,
)
from app.infrastructure.mailjet.types import JSON, EmailUser


def test_initialization() -> None:
    """Test builder initialization."""
    builder = MailjetPayloadBuilder()
    assert isinstance(builder.build(), dict)
    assert not builder.build()


@pytest.mark.parametrize(
    ("email", "name", "expected"),
    [
        ("test@example.com", None, {"Email": "test@example.com"}),
        (
            "test@example.com",
            "Test User",
            {"Email": "test@example.com", "Name": "Test User"},
        ),
    ],
)
def test_build_email_user(email: str, name: str | None, expected: EmailUser) -> None:
    """Test _build_email_user method."""
    builder = MailjetPayloadBuilder()
    result = builder._build_email_user(email, name)  # noqa: SLF001
    assert result == expected


def test_set_from() -> None:
    """Test set_from method."""
    builder = MailjetPayloadBuilder()
    result = builder.set_from("test@example.com", "Test User")
    assert result is builder
    payload = builder.build()
    assert "From" in payload
    assert payload["From"] == {"Email": "test@example.com", "Name": "Test User"}


def test_set_sender() -> None:
    """Test set_sender method."""
    builder = MailjetPayloadBuilder()
    result = builder.set_sender("test@example.com", "Test User")
    assert result is builder
    payload = builder.build()
    assert "Sender" in payload
    assert payload["Sender"] == {"Email": "test@example.com", "Name": "Test User"}


def test_add_to() -> None:
    """Test add_to method."""
    builder = MailjetPayloadBuilder()
    result = builder.add_to("test1@example.com", "User 1").add_to("test2@example.com")
    assert result is builder
    payload = builder.build()
    assert "To" in payload
    assert payload["To"] == [
        {"Email": "test1@example.com", "Name": "User 1"},
        {"Email": "test2@example.com"},
    ]


def test_add_cc() -> None:
    """Test add_cc method."""
    builder = MailjetPayloadBuilder()
    result = builder.add_cc("test1@example.com", "User 1").add_cc("test2@example.com")
    assert result is builder
    payload = builder.build()
    assert "Cc" in payload
    assert payload["Cc"] == [
        {"Email": "test1@example.com", "Name": "User 1"},
        {"Email": "test2@example.com"},
    ]


def test_add_bcc() -> None:
    """Test add_bcc method."""
    builder = MailjetPayloadBuilder()
    result = builder.add_bcc("test1@example.com", "User 1").add_bcc("test2@example.com")
    assert result is builder
    payload = builder.build()
    assert "Bcc" in payload
    assert payload["Bcc"] == [
        {"Email": "test1@example.com", "Name": "User 1"},
        {"Email": "test2@example.com"},
    ]


def test_set_reply_to() -> None:
    """Test set_reply_to method."""
    builder = MailjetPayloadBuilder()
    result = builder.set_reply_to("test@example.com", "Test User")
    assert result is builder
    payload = builder.build()
    assert "ReplyTo" in payload
    assert payload["ReplyTo"] == {"Email": "test@example.com", "Name": "Test User"}


def test_set_subject() -> None:
    """Test set_subject method."""
    builder = MailjetPayloadBuilder()
    result = builder.set_subject("Test Subject")
    assert result is builder
    payload = builder.build()
    assert "Subject" in payload
    assert payload["Subject"] == "Test Subject"


def test_set_text_part() -> None:
    """Test set_text_part method."""
    builder = MailjetPayloadBuilder()
    result = builder.set_text_part("Test plain text content")
    assert result is builder
    payload = builder.build()
    assert "TextPart" in payload
    assert payload["TextPart"] == "Test plain text content"


def test_set_html_part() -> None:
    """Test set_html_part method."""
    builder = MailjetPayloadBuilder()
    result = builder.set_html_part("<p>Test HTML content</p>")
    assert result is builder
    payload = builder.build()
    assert "HTMLPart" in payload
    assert payload["HTMLPart"] == "<p>Test HTML content</p>"


def test_set_template_id() -> None:
    """Test set_template_id method."""
    builder = MailjetPayloadBuilder()
    template_id = 12345
    result = builder.set_template_id(template_id)
    assert result is builder
    payload = builder.build()
    assert "TemplateID" in payload
    assert payload["TemplateID"] == template_id


@pytest.mark.parametrize("use", [True, False])
def test_set_template_language(use: bool) -> None:
    """Test set_template_language method."""
    builder = MailjetPayloadBuilder()
    result = builder.set_template_language(use=use)
    assert result is builder
    payload = builder.build()
    assert "TemplateLanguage" in payload
    assert payload["TemplateLanguage"] == use


def test_set_template_error_reporting() -> None:
    """Test set_template_error_reporting method."""
    builder = MailjetPayloadBuilder()
    result = builder.set_template_error_reporting("test@example.com", "Test User")
    assert result is builder
    payload = builder.build()
    assert "TemplateErrorReporting" in payload
    assert payload["TemplateErrorReporting"] == {
        "Email": "test@example.com",
        "Name": "Test User",
    }


@pytest.mark.parametrize("use", [True, False])
def test_set_template_error_deliver(use: bool) -> None:
    """Test set_template_error_deliver method."""
    builder = MailjetPayloadBuilder()
    result = builder.set_template_error_deliver(use=use)
    assert result is builder
    payload = builder.build()
    assert "TemplateErrorDeliver" in payload
    assert payload["TemplateErrorDeliver"] == use


def test_add_attachment() -> None:
    """Test add_attachment method."""
    builder = MailjetPayloadBuilder()
    result = builder.add_attachment(
        content_type="text/plain",
        filename="test.txt",
        base64_content="dGVzdCBjb250ZW50",
    )
    assert result is builder
    payload = builder.build()
    assert "Attachments" in payload
    assert payload["Attachments"] == [
        {
            "ContentType": "text/plain",
            "Filename": "test.txt",
            "Base64Content": "dGVzdCBjb250ZW50",
        },
    ]


def test_add_inline_attachment() -> None:
    """Test add_inline_attachment method."""
    builder = MailjetPayloadBuilder()
    result = builder.add_inline_attachment(
        content_type="image/png",
        filename="test.png",
        base64_content="aW1hZ2UgY29udGVudA==",
        content_id="test_id",
    )
    assert result is builder
    payload = builder.build()
    assert "InlineAttachments" in payload
    assert payload["InlineAttachments"] == [
        {
            "ContentType": "image/png",
            "Filename": "test.png",
            "Base64Content": "aW1hZ2UgY29udGVudA==",
            "ContentID": "test_id",
        },
    ]


def test_set_priority() -> None:
    """Test set_priority method."""
    builder = MailjetPayloadBuilder()
    priority = 2
    result = builder.set_priority(priority)
    assert result is builder
    payload = builder.build()
    assert "Priority" in payload
    assert payload["Priority"] == priority


def test_set_custom_campaign() -> None:
    """Test set_custom_campaign method."""
    builder = MailjetPayloadBuilder()
    result = builder.set_custom_campaign("test_campaign")
    assert result is builder
    payload = builder.build()
    assert "CustomCampaign" in payload
    assert payload["CustomCampaign"] == "test_campaign"


@pytest.mark.parametrize("use", [True, False])
def test_set_deduplicate_campaign(use: bool) -> None:
    """Test set_deduplicate_campaign method."""
    builder = MailjetPayloadBuilder()
    result = builder.set_deduplicate_campaign(use=use)
    assert result is builder
    payload = builder.build()
    assert "DeduplicateCampaign" in payload
    assert payload["DeduplicateCampaign"] == use


@pytest.mark.parametrize("use", [True, False])
def test_set_track_opens(use: bool) -> None:
    """Test set_track_opens method."""
    builder = MailjetPayloadBuilder()
    result = builder.set_track_opens(use=use)
    assert result is builder
    payload = builder.build()
    assert "TrackOpens" in payload
    assert payload["TrackOpens"] == use


@pytest.mark.parametrize("use", [True, False])
def test_set_track_clicks(use: bool) -> None:
    """Test set_track_clicks method."""
    builder = MailjetPayloadBuilder()
    result = builder.set_track_clicks(use=use)
    assert result is builder
    payload = builder.build()
    assert "TrackClicks" in payload
    assert payload["TrackClicks"] == use


def test_set_custom_id() -> None:
    """Test set_custom_id method."""
    builder = MailjetPayloadBuilder()
    result = builder.set_custom_id("test_id")
    assert result is builder
    payload = builder.build()
    assert "CustomID" in payload
    assert payload["CustomID"] == "test_id"


def test_set_event_payload() -> None:
    """Test set_event_payload method."""
    builder = MailjetPayloadBuilder()
    result = builder.set_event_payload("test_payload")
    assert result is builder
    payload = builder.build()
    assert "EventPayload" in payload
    assert payload["EventPayload"] == "test_payload"


def test_set_url_tags() -> None:
    """Test set_url_tags method."""
    builder = MailjetPayloadBuilder()
    result = builder.set_url_tags("test_tags")
    assert result is builder
    payload = builder.build()
    assert "URLTags" in payload
    assert payload["URLTags"] == "test_tags"


def test_set_headers() -> None:
    """Test set_headers method."""
    headers = {"X-Custom-Header": "value"}
    builder = MailjetPayloadBuilder()
    result = builder.set_headers(headers)
    assert result is builder
    payload = builder.build()
    assert "Headers" in payload
    assert payload["Headers"] == headers


def test_set_variables() -> None:
    """Test set_variables method."""
    variables: dict[str, JSON] = {
        "var1": "value1",
        "var2": 123,
        "var3": True,
        "var4": None,
        "var5": ["a", 1, True, None],
        "var6": {"key": "value"},
    }
    builder = MailjetPayloadBuilder()
    result = builder.set_variables(variables)
    assert result is builder
    payload = builder.build()
    assert "Variables" in payload
    assert payload["Variables"] == variables


def test_method_chaining() -> None:
    """Test method chaining."""
    builder = MailjetPayloadBuilder()
    result = (
        builder.set_from("from@example.com", "From User")
        .add_to("to@example.com", "To User")
        .set_subject("Test Subject")
        .set_text_part("Test Content")
        .set_custom_id("test_id")
        .set_track_opens(use=True)
    )

    assert result is builder
    payload = builder.build()
    assert "From" in payload
    assert "To" in payload
    assert "Subject" in payload
    assert "TextPart" in payload
    assert "CustomID" in payload
    assert "TrackOpens" in payload

    assert payload["From"] == {"Email": "from@example.com", "Name": "From User"}
    assert payload["To"] == [{"Email": "to@example.com", "Name": "To User"}]
    assert payload["Subject"] == "Test Subject"
    assert payload["TextPart"] == "Test Content"
    assert payload["CustomID"] == "test_id"
    assert payload["TrackOpens"] is True
