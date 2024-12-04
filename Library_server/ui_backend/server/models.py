from typing import List, Optional
from sqlalchemy import (
    ForeignKey,
    Integer,
    String,
    Boolean,
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
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    admin: Mapped[bool] = mapped_column(Boolean, default=False, server_default='0')
    nick: Mapped[str] = mapped_column(String(12))
    name: Mapped[str] = mapped_column(String(20))
    surname: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(30))
    password: Mapped[str] = mapped_column(String)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    family_id: Mapped[int] = mapped_column(Integer, ForeignKey('families.id'), nullable=True)

    latest: Mapped[List["RecentRead"]] = relationship(
        back_populates='user', cascade='all, delete-orphan'
    )
    library: Mapped['Library'] = relationship(back_populates='user', cascade='all, delete-orphan')
    family: Mapped[Optional['Family']] = relationship('Family', back_populates='users')
    
    @property
    def is_admin(self) -> bool | None:
        return self.admin

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, nick={self.nick!r}, name={self.name!r},"\
                " surname={self.surname!r}, email={self.email!r})"


class Family(Base):
    __tablename__ = 'families'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    
    users: Mapped[list['User']] = relationship('User', back_populates='family')
    libraries: Mapped[list['Library']] = relationship('Library', back_populates='family')
    
    def __repr__(self) -> str:
        return f'Family(id={self.id!r}, name={self.name!r})'


class RecentRead(Base):
    __tablename__ = 'recently_read'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    book_name: Mapped[str] = mapped_column(String(40))
    book_genre: Mapped[str] = mapped_column(String(40))
    current_page: Mapped[int] = mapped_column(Integer, default=1)
    number_of_pages: Mapped[int] = mapped_column(Integer)

    user: Mapped['User'] = relationship(back_populates='latest')
    
    def __repr__(self) -> str:
        return f"Reading(id={self.id!r}, book_name={self.book_name!r}, book_genre={self.book_genre!r}, current_page={self.current_page!r})"


class Library(Base):
    __tablename__ = 'libraries'
    id: Mapped[int] = mapped_column(primary_key=True)
    book_name: Mapped[str] = mapped_column(String(60))
    book_author: Mapped[str] = mapped_column(String(60))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    current_page: Mapped[int] = mapped_column(Integer, default=1)
    pages: Mapped[int] = mapped_column(Integer)
    family_id: Mapped[int] = mapped_column(ForeignKey('families.id'), nullable=True)

    user: Mapped['User'] = relationship(back_populates='library')
    family: Mapped[Optional['Family']] = relationship(back_populates='libraries')
    
    def __repr__(self) -> str:
        return f'Library(id={self.id!r}, book_name={self.book_name!r})'
    