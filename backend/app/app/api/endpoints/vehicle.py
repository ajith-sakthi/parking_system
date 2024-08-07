from fastapi import APIRouter,Form,Depends
from api.deps import db_dependency,get_db
from sqlalchemy.orm import Session
from app.core.security import current_user
from models import VehicleType,VehicleDetails, User
from datetime import datetime
from utils import vehicleNumber_validation


router =  APIRouter()

# 1) add a vehicle type 
@router.post("/add_vehicle_type")
async def add_vehicle_type(db:db_dependency,
                           user=Depends(current_user),
                           vehicleType:str=Form(...),
                           ):
    if user.user_type==1:
        type_of_vehicle = VehicleType(vehicle_type=vehicleType.title(),
                                      status=1)
        db.add(type_of_vehicle)
        db.commit()
        return {"message":"vehicle type added successfully"}
    return{"message":"You are not authorized to make any changes"}


#2) add a vehicle
@router.post("/add_vehicle/")
async def add_vehicle(db:db_dependency,
                      user=Depends(current_user),
                      vehicleNo:str=Form(...,description="eg:TN 00 GH 1234 or TN 00 G 1234"),
                      vehicleTypeId:int=Form(...,description="1.Bike,2.Car"),
                      ):

    if vehicleNumber_validation(vehicleNo):
        
        get_added_vehicle = db.query(VehicleDetails)

        check_duplicate_vehicle = get_added_vehicle.filter(VehicleDetails.vehicle_no == vehicleNo,VehicleDetails.vehicle_type_id == vehicleTypeId).first()

        if check_duplicate_vehicle:
            return {"message":"This vehicle is already registered"}

        addVehicle = VehicleDetails(vehicle_no = vehicleNo,
                                    user_id = user.id,
                                    vehicle_type_id = vehicleTypeId,
                                    status=1,
                                    vehicle_added_at=datetime.now())
        db.add(addVehicle)
        db.commit()
        return {"message":"Successfully added your vehicle"}
    return {"message":"Invalid vehicle no"}


# 3)get vehicle details

@router.get("/user_vehicle_details")
async def getVehicleDetail(db:Session=Depends(get_db)
                           ,user=Depends(current_user)):

    get_vehicle_details =  (db.query(VehicleDetails)
                            .filter(VehicleDetails.user_id==user.id,VehicleDetails.status==1)
                            .join(VehicleType,VehicleDetails.vehicle_type_id == VehicleType.id )
                            .all())
    
    if not get_vehicle_details:
        return {"message":"vehicle details not found"}
    
    vehicle_details=[]

    for detail in get_vehicle_details:
        vehicle_details.append({
            "vehicleId":detail.id,
            "vehicleNo":detail.vehicle_no,
            "vehicleType":detail.vehicle_types.vehicle_type
        })


    return vehicle_details





