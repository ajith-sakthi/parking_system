from fastapi import APIRouter,Form,Depends
from api.deps import get_db,db_dependency
# from sqlalchemy.orm import Session
from app.core.security import current_user
from models import ParkingStation,Branch, VehicleType
from datetime import datetime
router =  APIRouter()

# 1) add parking station details
@router.post("/add_parking_station")
async def addParkingStation(db:db_dependency,
                            user=Depends(current_user),
                            branchId:int=Form(...),
                            vehicleTypeId:int=Form(...,description="1.Bike,2.Car"),
                            parkingCapacity:int=Form(...),
                            ):
    if user.user_type == 1:
        branch = db.query(Branch).filter(Branch.id==branchId,Branch.status==1,Branch.approved_status==1).first()

        vehcile_type = db.query(VehicleType).filter(VehicleType.id==vehicleTypeId).first()

        
        if not branch:
            return {"message":"Branch id not found"}
        if not vehcile_type:
            return {"message":"Vehicle type id not found"}

        check_already_add_or_not = (db.query(ParkingStation)
                                    .filter(ParkingStation.branch_id==branchId,
                                            ParkingStation.vehicle_type_id==vehicleTypeId,
                                            ParkingStation.status==1)
                                            .first())
        if check_already_add_or_not:
            return {"message":"The given details are already added"}
        
        parking_station = ParkingStation(branch_id = branchId,
                                        vehicle_type_id=vehicleTypeId,
                                        total_parking_space=parkingCapacity,
                                        current_parking_space=parkingCapacity,
                                        created_at = datetime.now(),
                                        status =1)
        db.add(parking_station)
        db.commit()
        
        return {"message":"Parking station details added successfully"}
        
    return {"message":"you are not authorized to make any changes"}


# 2) update the parking staion details
@router.put("/update_parking_station_details")
async def updateParkingStationDetails(db:db_dependency,
                                      user=Depends(current_user),
                                      branchId:int=Form(...),
                                      vehicleTypeId:int=Form(...,description="1.Bike,2.Car"),
                                      totalParkingSpace:int=Form(...)
                                      ):
    if user.user_type==1:

        get_parking_station_detail = (db.query(ParkingStation)
                                      .filter(ParkingStation.branch_id==branchId,
                                              ParkingStation.vehicle_type_id==vehicleTypeId,
                                              ParkingStation.status==1)
                                              ).first()
        if get_parking_station_detail:
            get_parking_station_detail.total_parking_space=totalParkingSpace
            get_parking_station_detail.current_parking_space = totalParkingSpace
            db.commit()
            return{"message":"Changes made successfully"}
            
        return {"message":"Details not found"}
    return {"message":"You are not authorized to update district"}


