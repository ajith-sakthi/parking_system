import sys
sys.path.append("../")
from api.api import api_router
from fastapi import FastAPI
 
#  start from here
app = FastAPI()

app.include_router(api_router)