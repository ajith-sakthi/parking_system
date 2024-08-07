from app.db.base_class import Base
from sqlalchemy import Column, Integer, String,ForeignKey
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship

class Admin(Base):
    __tablename__="admins"


    id = Column(Integer,primary_key=True)
    user_id =  Column(Integer, ForeignKey("users.id"))
    district_id = Column(Integer, ForeignKey("districts.id"))
    status = Column(TINYINT)

    user = relationship("User",back_populates="admin")
    district = relationship("District",back_populates="admin")