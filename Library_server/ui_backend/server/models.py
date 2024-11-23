from typing import List, Optional
from sqlalchemy import (
    ForeignKey,
    Integer,
    String,
)
from flask_login import UserMixin # type: ignore
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    pass


metadata = Base.metadata  # exposing metadata for migrations or querying


class User(Base, UserMixin):
    __tablename__ = 'user'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    nick: Mapped[str] = mapped_column(String(12))
    name: Mapped[str] = mapped_column(String(20))
    surname: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(30))
    password: Mapped[str] = mapped_column(String)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    latest: Mapped[List["RecentRead"]] = relationship(
        back_populates='user', cascade='all, delete-orphan'
    )
    library: Mapped['Library'] = relationship(back_populates='user', cascade='all, delete-orphan')
    
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, nick={self.nick!r}, name={self.name!r},"\
                " surname={self.surname!r}, email={self.email!r})"


class RecentRead(Base):
    __tablename__ = 'recently_read'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    book_name: Mapped[str] = mapped_column(String(40))
    book_genre: Mapped[str] = mapped_column(String(40))
    current_page: Mapped[int] = mapped_column(Integer, default=1)
    user: Mapped['User'] = relationship(back_populates='latest')
    
    def __repr__(self) -> str:
        return f"Reading(id={self.id!r}, book_name={self.book_name!r})"


class Library(Base):
    __tablename__ = 'library'
    id: Mapped[int] = mapped_column(primary_key=True)
    book_name: Mapped[str] = mapped_column(String(60))
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    current_page: Mapped[int] = mapped_column(Integer)
    user: Mapped['User'] = relationship(back_populates='library')
    ...
    
    def __repr__(self) -> str:
        return f'Library(id={self.id!r}, book_name={self.book_name!r})'
    