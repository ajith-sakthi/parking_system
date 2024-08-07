from fastapi import APIRouter
from .endpoints import   district, masters, users,login, vehicle, parkingstation, booking, pricedetails, wallet,branch,reports,testuser

api_router = APIRouter()

api_router.include_router(users.router,tags=["Users"],prefix="/user")

api_router.include_router(login.router,tags=["Login"],prefix="/login")

api_router.include_router(district.router,tags=["District"],prefix="/district")

api_router.include_router(branch.router,tags=["Branch"],prefix="/branch")

api_router.include_router(vehicle.router,tags=["Vehicle Details"],prefix="/vehicle")

api_router.include_router(parkingstation.router,tags=["Parking station"],prefix="/parking_station")

api_router.include_router(booking.router,tags=["Booking"],prefix="/booking")

api_router.include_router(pricedetails.router,tags=["Price Details"],prefix="/pricedetails")

api_router.include_router(wallet.router,tags=["Wallet"],prefix="/wallet")

api_router.include_router(masters.router,tags=["Master"],prefix="/masters")

api_router.include_router(reports.router,tags=["Reports"],prefix="/report")

api_router.include_router(testuser.router,tags=["Import"],prefix="/import")
