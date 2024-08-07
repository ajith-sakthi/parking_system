from app.db.base_class import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    user_name = Column(String(50))
    pass_word = Column(String(100))
    e_mail = Column(String(50)) 
    ph_no = Column(String(10))
    user_type = Column(TINYINT,comment="1.super_admin,2.admin,3.customer,4.manager")
    status = Column(TINYINT,comment="0.Delete,1.Active,-1.Inactive")
    created_at = Column(DateTime)

    vehicle_detail = relationship("VehicleDetails",back_populates="user")
    booked_vehicle = relationship("BookedVehicle",back_populates="user")
    wallet = relationship("Wallet",back_populates="user")

    admin = relationship("Admin",back_populates="user")
    manager = relationship("Manager",back_populates="user")    


    