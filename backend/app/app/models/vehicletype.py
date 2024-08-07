from app.db.base_class import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship

class VehicleType(Base):
    __tablename__ = "vehicle_types"

    id = Column(Integer, primary_key=True)
    vehicle_type = Column(String(15))
    status = Column(TINYINT)
    
    vehicle_detail = relationship('VehicleDetails',back_populates="vehicle_types")
    price_detail = relationship("PriceDetail",back_populates="vehicle_types")
    parking_station = relationship("ParkingStation",back_populates="vehicle_types")