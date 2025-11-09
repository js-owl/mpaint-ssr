from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from database import Base


class Profile(Base):
    __tablename__ = "profiles"
    __table_args__ = (UniqueConstraint("user_id", name="uq_profiles_user_id"),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    username = Column(String, nullable=False)
    first_name = Column(String, nullable=True)

    user = relationship("User", back_populates="profile", uselist=False)

