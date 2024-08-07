from app.db.base_class import Base
from sqlalchemy import Column, Integer, String, ForeignKey,DateTime
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship

class VehicleDetails(Base):
    __tablename__ = "vehicle_details"

    id = Column(Integer, primary_key=True)
    vehicle_no = Column(String(15))
    user_id = Column(Integer,ForeignKey("users.id"))
    vehicle_type_id = Column(Integer,ForeignKey("vehicle_types.id"))
    status = Column(TINYINT)
    vehicle_added_at = Column(DateTime)
    user = relationship("User",back_populates="vehicle_detail")
    vehicle_types = relationship("VehicleType",back_populates="vehicle_detail")
    booked_vehicle = relationship("BookedVehicle",back_populates="vehicle_detail")

    
    