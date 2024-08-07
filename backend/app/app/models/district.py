from app.db.base_class import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship

class District(Base):
    __tablename__ = "districts"

    id = Column(Integer, primary_key=True)
    district_name = Column(String(60))
    status = Column(TINYINT, comment="0.Delete,1.Active,-1.Inactive")

    
    branch = relationship('Branch',back_populates="district")

    admin = relationship("Admin",back_populates="district")

    booked_vehicle = relationship("BookedVehicle",back_populates="district")