from fastapi import APIRouter,Form,Depends
from api.deps import get_db
from app.core.security import current_user
from models import PriceRange,VehicleType,PriceDetail
from sqlalchemy.orm import Session



router = APIRouter()

#1)add price ranges
@router.post("/add_price_range_name")
async def add_pricerangename(db:Session=Depends(get_db),
                         rangeName:str=Form(...),
                         user=Depends(current_user)):
    
    if user.user_type==1:
        range = PriceRange(range=rangeName,status=1)
        db.add(range)
        db.commit()
        return {"message":"Price range details added successfully"}
    return {"message":"You are not authorized to make any changes"}

# 2)add price details
@router.post("/add_price_details")
async def add_pricedetails(db:Session=Depends(get_db),
                           user=Depends(current_user),
                           priceRangeId:int=Form(...,description="1.Per hour,2.One day"),
                           vehicleTypeId:int=Form(...,description="1.Bike,2.Car"),
                           priceAmount:int=Form(...)):
    if user.user_type==1:
        rangeDetails = db.query(PriceRange).filter(PriceRange.id==priceRangeId).first()

        if rangeDetails:

            vehicleType = db.query(VehicleType).filter(VehicleType.id == vehicleTypeId).first()

            if vehicleType:
                priceDetails = PriceDetail(price_range_id=priceRangeId,vehicle_type_id=vehicleTypeId,price=priceAmount,status =1)
                db.add(priceDetails)
                db.commit()
                return{"message":"Price details added successfully"}
            return {"message":"Vehicle type id not found"}
        return {"message":"Price range Id not found"}
    return {"message":"Price details added successfully"}


# 3) update price details 
@router.put("/edit_pricedetails")
async def update_pricedetails(db:Session=Depends(get_db),
                           user=Depends(current_user),
                           priceRangeId:int=Form(...,description="1.Per hour,2.One day"),
                           vehicleTypeId:int=Form(...,description="1.Bike,2.Car"),
                           priceAmount:int=Form(...)):
    if user.user_type == 1 :
        rangeDetails = db.query(PriceRange).filter(PriceRange.id==priceRangeId).first()
        if rangeDetails:

            vehicleType = db.query(VehicleType).filter(VehicleType.id == vehicleTypeId).first()

            if vehicleType:
                priceDetails = db.query(PriceDetail).filter(PriceDetail.price_range_id==priceRangeId,PriceDetail.vehicle_type_id==vehicleTypeId,PriceDetail.status == 1).first()

                if priceDetails:
                    priceDetails.price = priceAmount
                    db.commit()
                    return{"message":"Updated successfully"}
                return { "message":"Price detail is not matched with your given details"}   
            return {"message":"Vehicle type id not found"} 
        return {"message":"Price range Id not found"}
    return {"message":"You are not authorized to make any changes"}
        

# 4) view price details 
# [bike : {one_hour : amt,one_day :amt },car :{one_hour : amt,one_day :amt }]
@router.get("/get_price_details")
async def get_pricedetails(db:Session = Depends(get_db),
                           user=Depends(current_user)):
    
    get_details = (db.query(PriceDetail).
                   join(PriceRange,PriceDetail.price_range_id==PriceRange.id).
                   join(VehicleType,PriceDetail.vehicle_type_id == PriceDetail.vehicle_type_id)).all()
    
    price_detail = []

    for detail in get_details:
        if detail.vehicle_types.vehicle_type == "Bike" and detail.price_range.range == "Per hour":
            bike_one_hour_price = detail.price
        if detail.vehicle_types.vehicle_type == "Bike" and detail.price_range.range == "One day":
            bike_one_day_price = detail.price
        if detail.vehicle_types.vehicle_type == "Car" and detail.price_range.range == "Per hour":
            car_one_hour_price = detail.price
        if detail.vehicle_types.vehicle_type == "Car" and detail.price_range.range == "One day":
            car_one_day_price = detail.price
        

    price_detail_in_dict = {
        "Bike":{
            "Per hour":bike_one_hour_price,
            "One day":bike_one_day_price
        },
        "Car":{
            "Per hour":car_one_hour_price,
            "One day" :car_one_day_price
        }
    }

    price_detail.append(price_detail_in_dict)

    return price_detail














    # return get_details.vehicle_types.vehicle_type
    # price_details = []
    # for detail in get_details:
    #     if detail.price_range_id == 1 and detail.vehicle_type_id==1:
    #         bike_one_hour_price = detail.price
    #     if detail.price_range_id == 2 and detail.vehicle_type_id == 1:
    #         bike_one_day_price = detail.price
    #     if detail.price_range_id==1 and detail.vehicle_type_id ==2:
    #         car_one_hour_price = detail.price
    #     if detail.price_range_id==2 and detail.vehicle_type_id ==2:
    #         car_one_day_price = detail.price
            

    # price_details_in_dict = {
    #     "bike":{
    #         "one_hour": bike_one_hour_price,
    #         "one_day":bike_one_day_price
    #     },
    #     "car":{
    #         "one_hour":car_one_hour_price,
    #         "one_day":car_one_day_price
    #     }
    # }
    # price_details.append(price_details_in_dict)


    # return price_details





