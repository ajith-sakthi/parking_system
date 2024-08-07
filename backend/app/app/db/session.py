from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# db_url = "mysql+pymysql://Ajith:Ajith123@localhost/ParkingSystem"


engine = create_engine(settings.DATA_BASE,pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)


