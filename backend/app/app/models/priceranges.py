from app.db.base_class import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship

class PriceRange(Base):
    __tablename__ =  "priceranges"

    id = Column(Integer,primary_key=True)
    range = Column(String(15))
    status = Column(TINYINT)

    price_detail = relationship("PriceDetail",back_populates="price_range")
    
