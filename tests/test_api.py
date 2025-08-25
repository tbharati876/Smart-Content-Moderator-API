# tests/test_api.py
import asyncio
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_text_moderation_safe():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {"email": "tester@example.com", "text": "Hello how are you?"}
        r = await ac.post("/api/v1/moderate/text", json=payload)
        assert r.status_code == 201
        data = r.json()
        assert "classification" in data
        assert data["classification"] in ["safe", "spam", "toxic", "harassment"]

@pytest.mark.asyncio
async def test_image_moderation_missing():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {"email": "tester@example.com"}
        r = await ac.post("/api/v1/moderate/image", json=payload)
        assert r.status_code == 400
