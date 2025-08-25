# app/analytics.py
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import ModerationRequest, ModerationResult
from app.logger import logger


async def analytics_summary(session: AsyncSession, email: str) -> dict:
    """
    Generate a small analytics summary for a user (filtering by reporter email is not part of the schema,
    so this function assumes moderation requests were reported by that email in a real-world schema).
    Here we return overall summary as described in requirements, with simplifying assumptions.
    """
    # total requests:
    total_stmt = select(func.count(ModerationRequest.id))
    total_q = await session.execute(total_stmt)
    total_requests = total_q.scalar_one()

    # breakdown by classification:
    breakdown_stmt = select(ModerationResult.classification, func.count(ModerationResult.id)).group_by(ModerationResult.classification)
    breakdown_q = await session.execute(breakdown_stmt)
    rows = breakdown_q.all()
    breakdown = {r[0]: int(r[1]) for r in rows}

    unsafe_count = sum(v for k, v in breakdown.items() if k != "safe")

    logger.info("Analytics summary generated.")
    return {
        "email": email,
        "total_requests": int(total_requests),
        "unsafe_count": int(unsafe_count),
        "breakdown": breakdown,
    }
