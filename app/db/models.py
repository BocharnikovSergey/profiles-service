from datetime import datetime
from sqlalchemy import String, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from typing import Optional
class User(Base):
    __tablename__ = "users"
    # 1. Базовые поля (связь с Auth)
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True, nullable=False)
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    first_name: Mapped[Optional[str]] = mapped_column(String(100))
    last_name: Mapped[Optional[str]] = mapped_column(String(100))
    phone_number: Mapped[Optional[str]] = mapped_column(String(20), unique=True)
    
    avatar_url: Mapped[Optional[str]] = mapped_column(String)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<User {self.id}: {self.email}>"