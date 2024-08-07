from app.db.base_class import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship

class Branch(Base):
    __tablename__ = "branches"

    id = Column(Integer, primary_key=True)
    branch_name = Column(String(60))
    district_id = Column(Integer,ForeignKey("districts.id"),comment="refered districts")

    status = Column(TINYINT,comment="0.Deleted,1.Active,-1.Inactive")
    approved_status = Column(TINYINT,comment="0.Rejected, 1.Approved, -1.Pending")

    district = relationship("District",back_populates="branch")
    booked_vehicle = relationship("BookedVehicle",back_populates="branch")
    parking_station = relationship("ParkingStation",back_populates="branch")

    
    manager = relationship("Manager",back_populates="branch")

    