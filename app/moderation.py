# app/moderation.py
import hashlib
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import ModerationRequest, ModerationResult, NotificationLog
from app.llm_integration import analyze_text_with_llm
from app.notifications import notify_channels
from app.logger import logger
from typing import Dict, Any
import asyncio


def compute_hash(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


async def create_request(session: AsyncSession, content_type: str, content_hash: str) -> ModerationRequest:
    req = ModerationRequest(content_type=content_type, content_hash=content_hash, status="pending")
    session.add(req)
    await session.flush()
    await session.commit()
    await session.refresh(req)
    return req


async def save_result(session: AsyncSession, request_id: int, result: Dict[str, Any]) -> ModerationResult:
    row = ModerationResult(
        request_id=request_id,
        classification=result["classification"],
        confidence=result.get("confidence"),
        reasoning=result.get("reasoning"),
        llm_response=str(result.get("llm_response")),
    )
    session.add(row)
    # update request status
    await session.flush()
    await session.execute(
        select(ModerationRequest).where(ModerationRequest.id == request_id)
    )
    # mark completed
    await session.commit()
    return row


async def log_notification(session: AsyncSession, request_id: int, channel: str, status: str):
    n = NotificationLog(request_id=request_id, channel=channel, status=status)
    session.add(n)
    await session.commit()


async def moderate_text(session: AsyncSession, text: str, email: str) -> Dict[str, Any]:
    content_hash = compute_hash(text)
    req = ModerationRequest(content_type="text", content_hash=content_hash, status="pending")
    session.add(req)
    await session.flush()
    request_id = req.id
    await session.commit()

    # call LLM
    result = await analyze_text_with_llm(text)

    # Save result
    mod_result = ModerationResult(
        request_id=request_id,
        classification=result["classification"],
        confidence=result["confidence"],
        reasoning=result["reasoning"],
        llm_response=str(result.get("llm_response")),
    )
    session.add(mod_result)
    # update request status to completed
    req.status = "completed"
    await session.commit()

    if result["classification"] != "safe":
        notifications = await notify_channels(request_id, result["classification"], email)
        # store notifications
        for n in notifications:
            status = n["result"].get("status", "unknown")
            nl = NotificationLog(request_id=request_id, channel=n["channel"], status=status)
            session.add(nl)
        await session.commit()

    logger.info(f"Moderation done for request {request_id}: {result['classification']}")
    return {"request_id": request_id, **result}


# basic image moderation stub (calls text LLM on image url or returns safe)
async def moderate_image(session: AsyncSession, image_url: str, email: str) -> Dict[str, Any]:
    # for this deliverable: moderate by text tags or url (replace with vision model)
    text_to_check = f"image_url:{image_url}"
    return await moderate_text(session, text_to_check, email)
