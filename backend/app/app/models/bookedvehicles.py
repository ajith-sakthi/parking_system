from app.db.base_class import Base
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship


class BookedVehicle(Base):
    __tablename__= 'booked_vehicles'

    id = Column(Integer,primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    district_id = Column(Integer,ForeignKey("districts.id"))
    branch_id = Column(Integer,ForeignKey("branches.id"))
    vehicle_id = Column(Integer,ForeignKey("vehicle_details.id"))
    from_time = Column(DateTime)
    to_time = Column(DateTime)
    booked_price = Column(Float)
    booked_at = Column(DateTime)
    status = Column(TINYINT,comment="0.Cancelled, 1.Active, -1.Inactive")
    

    vehicle_detail = relationship("VehicleDetails",back_populates="booked_vehicle")
    user = relationship("User",back_populates="booked_vehicle")
    district = relationship("District",back_populates="booked_vehicle")
    branch = relationship("Branch",back_populates="booked_vehicle")
    