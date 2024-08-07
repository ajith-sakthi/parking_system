from app.db.base_class import Base
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship

class ParkingStation(Base):
    __tablename__ ="parking_stations"

    id = Column(Integer,primary_key=True)
    branch_id = Column(Integer,ForeignKey("branches.id"))
    vehicle_type_id = Column(Integer,ForeignKey("vehicle_types.id"))
    total_parking_space = Column(Integer)
    current_parking_space = Column(Integer)
    status = Column(TINYINT,comment="0.Delete,1.Active,2.Inactive")
    created_at = Column(DateTime)
    branch = relationship("Branch",back_populates="parking_station")
    vehicle_types = relationship("VehicleType",back_populates="parking_station")



