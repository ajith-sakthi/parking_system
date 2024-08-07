from app.db.base_class import Base
from sqlalchemy import Column, Integer,ForeignKey,Float, DateTime
from sqlalchemy.orm import relationship

class Wallet(Base):
    __tablename__= "wallet_details"

    id = Column(Integer,primary_key=True)

    user_id = Column(Integer,ForeignKey("users.id") )
    amount = Column(Float)
    money_added_at = Column(DateTime)

    user = relationship("User",back_populates="wallet")
