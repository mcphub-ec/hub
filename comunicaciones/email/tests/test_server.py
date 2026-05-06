import base64
import importlib
import os
import sys
from email.message import EmailMessage
from pathlib import Path
from unittest.mock import Mock

import pytest


SERVER_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SERVER_DIR))


def load_server(monkeypatch):
    monkeypatch.setenv("EMAIL_ACCOUNTS", "personal")
    monkeypatch.setenv("EMAIL_PERSONAL_IMAP_HOST", "imap.example.com")
    monkeypatch.setenv("EMAIL_PERSONAL_IMAP_PORT", "993")
    monkeypatch.setenv("EMAIL_PERSONAL_IMAP_USER", "reader@example.com")
    monkeypatch.setenv("EMAIL_PERSONAL_IMAP_PASSWORD", "imap-secret")
    monkeypatch.setenv("EMAIL_PERSONAL_SMTP_HOST", "smtp.example.com")
    monkeypatch.setenv("EMAIL_PERSONAL_SMTP_PORT", "587")
    monkeypatch.setenv("EMAIL_PERSONAL_SMTP_USER", "sender@example.com")
    monkeypatch.setenv("EMAIL_PERSONAL_SMTP_PASSWORD", "smtp-secret")
    monkeypatch.setenv("EMAIL_PERSONAL_FROM", "sender@example.com")
    monkeypatch.setenv("EMAIL_PERSONAL_TLS_MODE", "starttls")
    monkeypatch.setenv("MCP_MASTER_KEY", "test-master-key")
    if "server" in sys.modules:
        return importlib.reload(sys.modules["server"])
    return importlib.import_module("server")


def sample_message() -> EmailMessage:
    message = EmailMessage()
    message["Subject"] = "=?utf-8?q?Factura_=C3=A9xito?="
    message["From"] = "Alice <alice@example.com>"
    message["To"] = "Bob <bob@example.com>"
    message["Date"] = "Wed, 06 May 2026 12:00:00 +0000"
    message.set_content("Hola mundo")
    message.add_alternative("<html><body><script>bad()</script><p onclick=\"bad()\">Hola</p></body></html>", subtype="html")
    message.add_attachment(b"PDF", maintype="application", subtype="pdf", filename="factura.pdf")
    return message


class FakeIMAP:
    def __init__(self, message_bytes: bytes):
        self.message_bytes = message_bytes
        self.selected = []
        self.uid_calls = []
        self.logged_out = False

    def login(self, user, password):
        self.user = user
        self.password = password

    def select(self, mailbox, readonly=True):
        self.selected.append((mailbox, readonly))
        return "OK", [b"1"]

    def list(self):
        return "OK", [b'(\\HasNoChildren) "/" "INBOX"', b'(\\HasNoChildren) "/" "Archive"']

    def uid(self, command, *args):
        self.uid_calls.append((command, args))
        if command == "search":
            return "OK", [b"101 102"]
        if command == "fetch":
            return "OK", [(b"102 (RFC822 {1}", self.message_bytes)]
        return "NO", []

    def logout(self):
        self.logged_out = True


class FakeSMTP:
    sent = []

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def starttls(self, context=None):
        self.started_tls = True

    def login(self, user, password):
        self.user = user
        self.password = password

    def send_message(self, message, from_addr=None, to_addrs=None):
        FakeSMTP.sent.append((message, from_addr, to_addrs))

    def quit(self):
        self.closed = True


def test_load_account_and_list_accounts_never_expose_secrets(monkeypatch):
    server = load_server(monkeypatch)

    account = server._load_account("personal")
    listed = server.list_accounts()
    serialized = str(listed)

    assert account.imap_password == "imap-secret"
    assert listed["accounts"][0]["account_id"] == "personal"
    assert listed["accounts"][0]["can_send"] is True
    assert "imap-secret" not in serialized
    assert "smtp-secret" not in serialized


def test_parse_mime_message_decodes_headers_sanitizes_html_and_lists_attachments(monkeypatch):
    server = load_server(monkeypatch)

    parsed = server._extract_message(sample_message(), include_body=True)

    assert parsed["subject"] == "Factura éxito"
    assert parsed["from"] == ["alice@example.com"]
    assert parsed["body_text"] == "Hola mundo"
    assert "<script>" not in parsed["body_html"]
    assert "onclick" not in parsed["body_html"]
    assert parsed["attachments"][0]["filename"] == "factura.pdf"
    assert parsed["attachments"][0]["downloadable"] is True


def test_prepare_and_send_token_rejects_modified_payload(monkeypatch):
    server = load_server(monkeypatch)
    FakeSMTP.sent = []
    monkeypatch.setattr(server.smtplib, "SMTP", FakeSMTP)

    prepared = server.prepare_email(
        account_id="personal",
        to=["client@example.com"],
        subject="Hola",
        body_text="Texto original",
    )

    with pytest.raises(ValueError, match="Invalid send_token"):
        server.send_prepared_email(
            account_id="personal",
            to=["client@example.com"],
            subject="Hola",
            body_text="Texto cambiado",
            send_token=prepared["send_token"],
        )

    result = server.send_prepared_email(
        account_id="personal",
        to=["client@example.com"],
        subject="Hola",
        body_text="Texto original",
        send_token=prepared["send_token"],
    )

    assert result["success"] is True
    assert FakeSMTP.sent[0][1] == "sender@example.com"
    assert FakeSMTP.sent[0][2] == ["client@example.com"]


def test_imap_search_and_attachment_fetch_use_readonly_and_size_limit(monkeypatch):
    server = load_server(monkeypatch)
    fake = FakeIMAP(sample_message().as_bytes())
    monkeypatch.setattr(server, "_connect_imap", Mock(return_value=fake))

    search = server.search_emails("personal", mailbox="INBOX", limit=999)
    attachment_part_id = search["messages"][0]["attachments"][0]["part_id"]
    attachment = server.get_attachment("personal", "INBOX", "102", attachment_part_id)

    assert search["limit"] == server.MAX_SEARCH_LIMIT
    assert search["messages"][0]["uid"] == "102"
    assert fake.selected[0] == ("INBOX", True)
    assert ("fetch", ("102", "(BODY.PEEK[])")) in fake.uid_calls
    assert attachment["filename"] == "factura.pdf"
    assert base64.b64decode(attachment["content_base64"]) == b"PDF"


def test_missing_master_key_blocks_prepare_email(monkeypatch):
    server = load_server(monkeypatch)
    monkeypatch.delenv("MCP_MASTER_KEY", raising=False)

    with pytest.raises(ValueError, match="MCP_MASTER_KEY"):
        server.prepare_email(
            account_id="personal",
            to="client@example.com",
            subject="Hola",
            body_text="Texto",
        )
