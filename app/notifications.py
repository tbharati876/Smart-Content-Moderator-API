# app/notifications.py
import httpx
import asyncio
from app.config import settings
from app.logger import logger
from typing import Dict, Any


async def send_slack_alert(webhook_url: str, message: str) -> Dict[str, Any]:
    if not webhook_url:
        logger.warning("No Slack webhook configured; skipping Slack alert.")
        return {"status": "skipped", "reason": "no webhook"}
    payload = {"text": message}
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(webhook_url, json=payload)
        status = "sent" if resp.status_code in (200, 201, 204) else "failed"
        logger.info(f"Slack send status: {status} ({resp.status_code})")
        return {"status": status, "http_status": resp.status_code, "response_text": resp.text}


async def send_email_stub(to_email: str, subject: str, body: str) -> Dict[str, Any]:
    """
    Placeholder for sending email. Replace with SMTP or transactional email provider.
    """
    if not settings.SMTP_HOST or not settings.SMTP_USER:
        logger.warning("SMTP not configured; skipping email send.")
        return {"status": "skipped", "reason": "no smtp config"}
      
    await asyncio.sleep(0.1)
    logger.info(f"Email (stub) sent to {to_email} with subject '{subject}'.")
    return {"status": "sent_stub"}


async def notify_channels(request_id: int, classification: str, email: str):
    """
    Notify configured channels if content is not 'safe'.
    """
    results = []
    message = f"Moderation alert for request {request_id}: classification={classification}, reporter={email}"
    # Slack
    slack_result = await send_slack_alert(settings.SLACK_WEBHOOK_URL, message)
    results.append({"channel": "slack", "result": slack_result})
    # Email
    email_result = await send_email_stub(settings.ADMIN_EMAIL or email, "Moderation alert", message)
    results.append({"channel": "email", "result": email_result})
    return results
