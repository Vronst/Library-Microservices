from typing import List, Optional
from sqlalchemy import (
    ForeignKey,
    String
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    nick: Mapped[str] = mapped_column(String(12))
    name: Mapped[str] = mapped_column(String(20))
    surname: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(30))
    age: Mapped[Optional[int]] = mapped_column()
    latest: Mapped[List["Reading"]] = relationship(
        back_populates='user', cascade='all, delete-orphan'
    )
    
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, nick={self.nick!r}, name={self.name!r},"\
                " surname={self.surname!r}, email={self.email!r})"

class Reading(Base):
    __tablename__ = 'latest_reading'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    book_name: Mapped[str] = mapped_column(String(40))
    user: Mapped['User'] = relationship(back_populates='latest')
    
    def __repr__(self) -> str:
        return f"Reading(id={self.id!r}, book_name={self.book_name!r})"
    