from typing import Any

from flask_sqlalchemy import SQLAlchemy  # pyright: ignore[reportMissingImports]
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


db: Any = SQLAlchemy(model_class=Base)  # pyright: ignore[reportUnknownVariableType]

class User(db.Model):  # pyright: ignore[reportUntypedBaseClass]
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

class PhotoJob(db.Model):  # pyright: ignore[reportUntypedBaseClass]
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    filename: Mapped[str] = mapped_column(String(200), nullable=False)
    result: Mapped[str | None] = mapped_column(String(20))  # BEST, REJECTED, NO_FACE
    emotion: Mapped[str | None] = mapped_column(String(30), nullable=True)
    processed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
