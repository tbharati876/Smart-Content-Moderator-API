# app/main.py
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session, engine, Base
from app import models
from app.schemas import TextModerationRequest, ImageModerationRequest, ModerationResultOut, AnalyticsSummary
from app.moderation import moderate_text, moderate_image
from app.analytics import analytics_summary
from app.logger import logger
import asyncio

app = FastAPI(title="Smart Content Moderator API", version="0.1.0")


@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables ensured.")


@app.post("/api/v1/moderate/text", response_model=ModerationResultOut)
async def post_moderate_text(payload: TextModerationRequest, session: AsyncSession = Depends(get_session)):
    try:
        result = await moderate_text(session, payload.text, payload.email)
        return JSONResponse(status_code=201, content={
            "request_id": result["request_id"],
            "classification": result["classification"],
            "confidence": result.get("confidence"),
            "reasoning": result.get("reasoning"),
            "llm_response": result.get("llm_response"),
        })
    except Exception as e:
        logger.exception("Error moderating text")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/moderate/image", response_model=ModerationResultOut)
async def post_moderate_image(payload: ImageModerationRequest, session: AsyncSession = Depends(get_session)):
    # minimal validation
    if not payload.image_url and not payload.image_base64:
        raise HTTPException(status_code=400, detail="image_url or image_base64 required")
    source = payload.image_url or "base64-data"
    try:
        result = await moderate_image(session, source, payload.email)
        return JSONResponse(status_code=201, content={
            "request_id": result["request_id"],
            "classification": result["classification"],
            "confidence": result.get("confidence"),
            "reasoning": result.get("reasoning"),
            "llm_response": result.get("llm_response"),
        })
    except Exception as e:
        logger.exception("Error moderating image")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/analytics/summary", response_model=AnalyticsSummary)
async def get_analytics_summary(user: str, session: AsyncSession = Depends(get_session)):
    try:
        summary = await analytics_summary(session, user)
        return JSONResponse(status_code=200, content=summary)
    except Exception as e:
        logger.exception("Error getting analytics")
        raise HTTPException(status_code=500, detail=str(e))


# Allow running with python -m app.main
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
