# app/models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Text
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy.orm import relationship

class ModerationRequest(Base):
    __tablename__ = "moderation_requests"
    id = Column(Integer, primary_key=True, index=True)
    content_type = Column(String(20), nullable=False)
    content_hash = Column(String(128), nullable=True)
    status = Column(String(20), nullable=False, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    results = relationship("ModerationResult", back_populates="request", uselist=False)
    notifications = relationship("NotificationLog", back_populates="request")


class ModerationResult(Base):
    __tablename__ = "moderation_results"
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("moderation_requests.id"), nullable=False)
    classification = Column(String(50), nullable=False)
    confidence = Column(Float, nullable=True)
    reasoning = Column(Text, nullable=True)
    llm_response = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    request = relationship("ModerationRequest", back_populates="results")


class NotificationLog(Base):
    __tablename__ = "notification_logs"
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("moderation_requests.id"), nullable=False)
    channel = Column(String(20), nullable=False)  # slack / email
    status = Column(String(20), nullable=False)
    sent_at = Column(DateTime(timezone=True), server_default=func.now())

    request = relationship("ModerationRequest", back_populates="notifications")
