from app.db.base_class import Base
from sqlalchemy import Column, Integer, String, ForeignKey,DateTime
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship


class Manager(Base):
    __tablename__ = "managers"

    id = Column(Integer,primary_key=True)

    branch_id = Column(Integer,ForeignKey("branches.id"))

    user_id = Column(Integer, ForeignKey("users.id"))

    status = Column(TINYINT,comment="1-Active, -1-Inactive")

    created_at = Column(DateTime)


    branch = relationship("Branch",back_populates="manager")
    user = relationship("User",back_populates="manager")

