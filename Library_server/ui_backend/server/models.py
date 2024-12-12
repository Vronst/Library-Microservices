from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import ForeignKey, Integer, String, Boolean, func, DateTime
from flask_login import UserMixin  # type: ignore
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    """Base model for SQLAlchemy ORM."""
    pass


metadata = Base.metadata  # exposing metadata for migrations or querying


class User(Base, UserMixin):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    admin: Mapped[bool] = mapped_column(Boolean, default=False, server_default='0')
    nick: Mapped[str] = mapped_column(String(12))
    name: Mapped[str] = mapped_column(String(20))
    surname: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(30))
    password: Mapped[str] = mapped_column(String)
    family_id: Mapped[Optional[int]] = mapped_column(ForeignKey('families.id'), nullable=True)

    latest: Mapped[List["RecentRead"]] = relationship(
        "RecentRead", back_populates="user", cascade="all, delete-orphan"
    )
    library: Mapped[List["Library"]] = relationship(
        "Library", back_populates="user", cascade="all, delete-orphan"
    )
    family: Mapped[Optional["Family"]] = relationship("Family", back_populates="users")

    @property
    def is_admin(self) -> bool:
        return self.admin

    def __repr__(self) -> str:
        return (
            f"User(id={self.id!r}, nick={self.nick!r}, name={self.name!r}, "
            f"surname={self.surname!r}, email={self.email!r})"
        )


class Family(Base):
    __tablename__ = 'families'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))

    users: Mapped[List["User"]] = relationship("User", back_populates="family")
    libraries: Mapped[List["Library"]] = relationship("Library", back_populates="family")

    def __repr__(self) -> str:
        return f"Family(id={self.id!r}, name={self.name!r})"


class RecentRead(Base):
    __tablename__ = 'recent_reads'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    book_id: Mapped[int] = mapped_column(ForeignKey('libraries.id'))
    time_stamp: Mapped[datetime] = mapped_column(default=func.now())

    user: Mapped["User"] = relationship("User", back_populates="latest")
    library: Mapped["Library"] = relationship("Library", back_populates="recent_reads")

    def __repr__(self) -> str:
        return f"RecentRead(id={self.id!r}, user_id={self.user_id!r}, book_id={self.book_id!r})"


class Library(Base):
    __tablename__ = 'libraries'

    id: Mapped[int] = mapped_column(primary_key=True)
    book_name: Mapped[str] = mapped_column(String(60))
    book_id: Mapped[int] = mapped_column(Integer, nullable=False)
    book_author: Mapped[str] = mapped_column(String(60))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    current_page: Mapped[int] = mapped_column(Integer, default=1)
    pages: Mapped[int] = mapped_column(Integer)
    family_id: Mapped[Optional[int]] = mapped_column(ForeignKey('families.id'), nullable=True)
    img: Mapped[Optional[str]] = mapped_column(String(), nullable=True)
    genre: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="library")
    family: Mapped[Optional["Family"]] = relationship("Family", back_populates="libraries")
    recent_reads: Mapped[List["RecentRead"]] = relationship(
        "RecentRead", back_populates="library", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Library(id={self.id!r}, book_name={self.book_name!r})"
