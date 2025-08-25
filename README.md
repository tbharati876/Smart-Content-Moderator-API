# Smart Content Moderator API

**Project:** Smart Content Moderator API (FastAPI)  
**Purpose:** Analyze user-submitted text/images for inappropriate content, store results, send notifications, and provide analytics.

---

## What this repo contains
- `app/` — FastAPI application code
- `tests/` — simple unit tests (pytest + httpx)
- `outputs/` — example JSON outputs (samples)
- `requirements.txt` — Python dependencies

---

## Design & Notes (assumptions)
- **Framework:** FastAPI (async-first).
- **DB:** SQLite (async via `aiosqlite`). Schema follows the assignment:
  - `moderation_requests` (id, content_type, content_hash, status, created_at)
  - `moderation_results` (request_id, classification, confidence, reasoning, llm_response)
  - `notification_logs` (request_id, channel, status, sent_at)
- **LLM:** Module includes a **heuristic stub** (`analyze_text_with_llm`) for deterministic behavior in this take-home. Replace with real OpenAI/Gemini calls (function `call_openai_real` placeholder).
- **Notifications:** Slack webhook + email stub implemented. Replace email stub with SMTP or transactional provider (Brevo, SendGrid) as needed.
- **Analytics:** Simple aggregation by classification. In real system, tie requests to reporter email or user ID.

---

## Files to upload to GitHub
Copy the `app/`, `tests/`, `requirements.txt`, `README.md`, and `outputs/` directories/files into your repository root as-is.

---

## How the endpoints behave (documentation)
- `POST /api/v1/moderate/text`
  - Body: `{ "email": "...", "text": "..." }`
  - Returns 201 with moderation result including classification, confidence, reasoning.

- `POST /api/v1/moderate/image`
  - Body: `{ "email": "...", "image_url": "..." }` OR `{ "image_base64": "..." }`
  - Returns 201 with moderation result (image moderation is currently delegated to text-stub).

- `GET /api/v1/analytics/summary?user=<email>`
  - Returns analytics summary (total_requests, unsafe_count, breakdown).

---

## Production notes & next steps
- Replace `llm_integration.analyze_text_with_llm` with an actual LLM API client.
- Implement secure webhook validation and retry/backoff for notification delivery.
- Add authentication, rate-limiting, and request auditing.
- For scale: use PostgreSQL, background worker (Celery/RQ) for LLM calls, and object storage for images.
- Add migrations (Alembic) for production DB schema changes.

---

## Example outputs
See `/outputs` for sample JSON responses that you can include in your GitHub repo.

---

## Contact & assumptions
- The heuristic LLM stub is used for deterministic unit testing and should be replaced before production.
- If any environment variables are required (e.g., `OPENAI_API_KEY`, `SLACK_WEBHOOK_URL`, `SMTP_...`), populate them in `.env` or your deployment environment.

