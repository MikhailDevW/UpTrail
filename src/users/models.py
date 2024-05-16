import enum

from sqlalchemy import (
    Boolean, Enum, ForeignKey, PrimaryKeyConstraint, SmallInteger,
    String, UniqueConstraint)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from .constants import (
    EMAIL_MAX_LENGTH, FIRSTNAME_MAX_LENGTH, HASHED_PASSWORD_MAX_LENGTH,
    LASTNAME_MAX_LENGTH, USERNAME_MAX_LENGTH)


class UserRole(enum.Enum):
    user = "user"
    manager = "manager"
    admin = "admin"
    owner = "owner"


class CustomUser(Base):
    __tablename__ = "customuser"

    email: Mapped[str] = mapped_column(
        String(length=EMAIL_MAX_LENGTH),
        unique=True,
        nullable=False,
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=HASHED_PASSWORD_MAX_LENGTH), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    username: Mapped[str] = mapped_column(
        String(length=USERNAME_MAX_LENGTH),
        nullable=False,
    )
    role: Mapped[str] = mapped_column(
        Enum(UserRole),
        default=UserRole.user,
        nullable=False,
    )

    profile: Mapped["Profile"] = relationship(back_populates="customuser")

    __table_args__ = (
        PrimaryKeyConstraint("id", name="user_id"),
        UniqueConstraint("email", name="uq_email"),
    )


class Profile(Base):
    __tablename__ = "uprofile"

    first_name: Mapped[str] = mapped_column(
        String(length=FIRSTNAME_MAX_LENGTH)
    )
    last_name: Mapped[str] = mapped_column(
        String(length=LASTNAME_MAX_LENGTH)
    )
    age: Mapped[int] = mapped_column(SmallInteger)

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            column='customuser.id',
            name='customuser.id',
        ),
        unique=True,
    )
    user: Mapped[CustomUser] = relationship(back_populates='profile')
