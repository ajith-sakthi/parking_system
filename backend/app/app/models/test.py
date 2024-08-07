from app.db.base_class import Base
from sqlalchemy import Column, Integer, String

class TestUser(Base):
    __tablename__ = "testusers"


    id = Column(Integer, primary_key=True)
    first_name = Column(String(20))
    last_name= Column(String(20))
    user_name = Column(String(20))
    email = Column(String(30))
    contact_no = Column(String(14))