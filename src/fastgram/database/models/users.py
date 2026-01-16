from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime
from sqlalchemy.sql import func

from ..base import FastAPIBase


class Users(FastAPIBase):
    username: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(
        String(100), unique=True, index=True, nullable=True)
    first_name: Mapped[str] = mapped_column(
        String(50), nullable=True)
    last_name: Mapped[str] = mapped_column(
        String(50), nullable=True)
    bio: Mapped[str] = mapped_column(
        String(500), nullable=True)
    avatar_url: Mapped[str] = mapped_column(
        String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(
        default=True)
    is_verified: Mapped[bool] = mapped_column(
        default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True)
    last_login: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True)
