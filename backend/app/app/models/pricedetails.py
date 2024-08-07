from app.db.base_class import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship

class PriceDetail(Base):
    __tablename__ = "price_details"

    id = Column(Integer,primary_key=True)

    price_range_id = Column(Integer,ForeignKey("priceranges.id"))
    vehicle_type_id = Column(Integer, ForeignKey("vehicle_types.id"))
    price = Column(Float)
    status = Column(TINYINT)    

    vehicle_types = relationship("VehicleType",back_populates="price_detail")
    price_range = relationship("PriceRange",back_populates="price_detail")


