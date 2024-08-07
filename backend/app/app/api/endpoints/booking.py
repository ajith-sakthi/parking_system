from fastapi import APIRouter,Form,Depends
from api.deps import get_db,db_dependency
from app.core.security import current_user
from models import VehicleDetails,BookedVehicle,ParkingStation,PriceDetail, Wallet,Branch,User, VehicleType
from datetime import datetime,date, timedelta
from sqlalchemy import or_
from datetime import datetime



router = APIRouter()



# 1) book vehicle
@router.post("/book_parking_space/")
async def parkingSpaceBooking(db:db_dependency,
                              user=Depends(current_user),
                              vehicleId:int=Form(...),
                              branchId:int=Form(...),
                              vehicleTypeId:int=Form(...,description="1.Bike,2.Car"),
                              fromTime:str=Form(...,description="2024-07-05 12:00:00"),
                              toTime:str=Form(...,description="2024-07-05 12:00:00")
                              ):
    try:
        FromTime = datetime.strptime(fromTime,"%Y-%m-%d %H:%M:%S")
        ToTime= datetime.strptime(toTime,"%Y-%m-%d %H:%M:%S")
        
        if FromTime.minute !=0 or FromTime.second!=0 or ToTime.minute !=0 or ToTime.second !=0:
            return {"message":"Only give the time in hours"}
        
        # check vehicle is registered or not
        check_added_vehicle = db.query(VehicleDetails).filter(VehicleDetails.id == vehicleId,VehicleDetails.status==1,VehicleDetails.vehicle_type_id==vehicleTypeId,VehicleDetails.user_id==user.id).first()

        get_booked_details=db.query(BookedVehicle)

        # to get the minimum record for looping
        get_vehicle_details =  (get_booked_details
                        .filter(BookedVehicle.status == 1)
                        .join(VehicleDetails, VehicleDetails.id == BookedVehicle.vehicle_id))
        
        if check_added_vehicle:
            # current_time = datetime.now()
            get_approved_branch = db.query(Branch).filter(Branch.id == branchId,Branch.status==1,Branch.approved_status==1)

            if not get_approved_branch:
                return {"message":"Branch details not found, once check your branchId"}
            
            for detail in get_vehicle_details:
                difference_in_seconds = (detail.to_time - detail.from_time).total_seconds()
                
                current_difference_in_seconds = (datetime.now() - detail.from_time ).total_seconds()
                
                # vehicle parking time - completed 
                if difference_in_seconds < current_difference_in_seconds:
                    
                    detail.status = -1 

                    get_parking_station_details = db.query(ParkingStation).filter(
                        ParkingStation.branch_id==branchId, 
                        ParkingStation.vehicle_type_id == detail.vehicle_detail.vehicle_type_id
                    ).first()
                    
                    if not get_parking_station_details:
                        return {"message":"No station was added to this branch"}
                    
                    # increase current capacity count
                    if get_parking_station_details.total_parking_space > get_parking_station_details.current_parking_space:
                    
                        get_parking_station_details.current_parking_space = get_parking_station_details.current_parking_space + 1
                        
                    db.commit()

            # return "some thing"
            check_booked_or_not = (get_booked_details
                                   .filter(BookedVehicle.vehicle_id==vehicleId,
                                           BookedVehicle.user_id==user.id,
                                           BookedVehicle.status==1)
                                           .first())

            if check_booked_or_not:
                return{"message":"You already booked"}

            if FromTime > datetime.now() and ToTime > datetime.now() and ToTime > FromTime:

            # checking parking space availability 
                parking_station_detail = (db.query(ParkingStation)
                                        .filter(ParkingStation.branch_id==branchId,
                                                ParkingStation.vehicle_type_id==vehicleTypeId,
                                                ParkingStation.status==1).first())
                
                if not (parking_station_detail.current_parking_space <= 0) :

                    # FromTime = datetime.strptime(fromTime,"%Y-%m-%d %H:%M:%S").replace(minute=0,second=0)
                    # ToTime= datetime.strptime(toTime,"%Y-%m-%d %H:%M:%S").replace(minute=0,second=0)
                    
                    difference =  ToTime - FromTime

                    # get price detail
                    get_price_details = db.query(PriceDetail).filter(PriceDetail.vehicle_type_id==vehicleTypeId) 

                    # check day or hour
                    if (difference.days and difference.seconds) or (difference.days and difference.seconds==0):
                        # id = 2 ---> day
                        # print("day")
                        bike_or_car_parking_price = get_price_details.filter(PriceDetail.price_range_id==2).first()
                        
                        if difference.days and difference.seconds:
                            days_count = difference.days + 1 
                        else:
                            days_count = difference.days
                        
                        # Booked price
                        price = days_count * bike_or_car_parking_price.price
                        # print("booked price:",price)

                        # update wallet 
                        wallet= db.query(Wallet).filter(Wallet.user_id == user.id).first()
                        print(wallet.amount)
                        if not wallet:
                            return {"message":"Add a amount in your wallet before booking"}
                        
                        if not (wallet.amount >= price):
                            return {"message":"You don't have enough balance in your wallet"}
                        
                        print("wallet amount:",wallet.amount)
                        
                        wallet.amount = wallet.amount - price
                        
                        # decrease the parking space
                        parking_station_detail.current_parking_space = parking_station_detail.current_parking_space - 1
                        
                        branchDetail = db.query(Branch).filter(Branch.id==branchId).first()

                        booked_vehicle =  BookedVehicle(
                            user_id=user.id,
                            vehicle_id=vehicleId,
                            district_id = branchDetail.district_id,
                            branch_id=branchId,
                            from_time=FromTime,
                            to_time=toTime,
                            booked_price =price,
                            booked_at = datetime.now(),
                            status= 1 )

                        db.add(booked_vehicle)
                        db.commit()
                        return {"message":"Booked successfully"}
                        # return {"total_capacity":parking_station_detail.total_parking_space,
                        #         "current_capacity":parking_station_detail.current_parking_space,
                        #         "amount after reduced":wallet.amount,
                        #         "price_for_day": price
                        #         }
                            
                        
                        # print("day",difference.days)
                        # return {"hour":days_count,"price":days_count * bike_or_car_parking_price.price}

                    else:
                        # id=1---> hour
                        bike_or_car_parking_price = get_price_details.filter(PriceDetail.price_range_id==1).first()

                        #convert seconds into hour 
                        hour_count = ((difference.seconds)/60)/60

                        price = hour_count * bike_or_car_parking_price.price

                    
                        wallet= db.query(Wallet).filter(Wallet.user_id == user.id).first()
                        
                            
                        # if not wallet:
                        #     return {"message":"Wallet details not found"}
                        if wallet:
                            if wallet.amount >= price:
                                print("wallet amount:",wallet.amount)
                                wallet.amount = wallet.amount - price

                                parking_station_detail.current_parking_space = parking_station_detail.current_parking_space - 1

                                branchDetail = db.query(Branch).filter(Branch.id==branchId).first()

                                booked_vehicle =  BookedVehicle(
                                    user_id=user.id,
                                    vehicle_id=vehicleId,
                                    district_id = branchDetail.district_id,
                                    branch_id=branchId,
                                    from_time=FromTime,
                                    to_time=toTime,
                                    booked_price =price,
                                    booked_at = datetime.now(),
                                    status= 1 )

                                db.add(booked_vehicle)
                                db.commit()

                                return {"message":"Booked successfuly"}
                                # return {"total_capacity":parking_station_detail.total_parking_space,
                                #         "current_capacity":parking_station_detail.current_parking_space,
                                #         "amount after reduced":wallet.amount,
                                #         "price_for_hour": price
                                #         }

                            else:
                                return {"message":"You don't have a enough balance to book"}
                        return {"message":"Add a amount in your wallet before booking"}

                        # print("hour",((difference.seconds)/60)/60)
                        # return {"hour":hour_count,"price":hour_count * bike_or_car_parking_price.price}

                return {"message":"No space available"}
            
            return {"message":"Enter valid timing"}
        
        return {"message":"Vehicle details not found, add your vehicle before booking the parking space"}
    except ValueError:
        return {"message":"Give the date and time like example format"}
    

# 2) cancel order
@router.post("/cancel_parking_space")
async def cancelParkingSpace(db:db_dependency,
                             user=Depends(current_user),
                             bookingId:int=Form(...)):
    
    get_booking_detail = db.query(BookedVehicle).filter(BookedVehicle.id == bookingId,BookedVehicle.user_id==user.id)

    if not  get_booking_detail:
        return {"message":"You didn't book any parking space"}
    
    get_cancellation_detail = db.query(BookedVehicle).filter(BookedVehicle.id == bookingId,BookedVehicle.user_id==user.id,BookedVehicle.status==0).first()
    
    
    if get_cancellation_detail:
        return {"message":"you already cancelled this order"}
    
    # current user booking Id
    get_booking_detail = db.query(BookedVehicle).filter(BookedVehicle.id == bookingId,BookedVehicle.user_id==user.id,BookedVehicle.status==1).first()
    
    # return {"message":get_booking_detail.from_time}
    if not get_booking_detail:
        return {"message":"Booking details not found, check your bookingId"}


    #18:00:00 > 17:24:00
    if get_booking_detail.from_time < datetime.now():
        return {"message":"You have to cancel before the booking time"}
    

    get_vehicle_id = (db.query(BookedVehicle)
                      .filter(BookedVehicle.id==bookingId,BookedVehicle.user_id==user.id)
                      .join(VehicleDetails,VehicleDetails.id == BookedVehicle.vehicle_id).first())
       
    
    get_parking_station =  (db.query(ParkingStation)
                            .filter(ParkingStation.branch_id==get_booking_detail.branch_id,ParkingStation.vehicle_type_id == get_vehicle_id.vehicle_detail.vehicle_type_id).first())

    # increase the parking space 
    if get_parking_station.total_parking_space > get_parking_station.current_parking_space:
       
        get_parking_station.current_parking_space = get_parking_station.current_parking_space + 1

   

    # update wallet
    wallet = db.query(Wallet).filter(Wallet.user_id==user.id).first()

    booked_amount = get_booking_detail.booked_price

    wallet.amount = wallet.amount + booked_amount

    # update the booked vehicle status
    get_booking_detail.status = 0
    get_booking_detail.booked_price = 0
     

    db.commit()

    return {"message":"You cancelled your order"}

# # 3) filter date wise
@router.post("/booked_details_by_date")
async def listBookedDetails(db:db_dependency,
                            user=Depends(current_user),
                            fromDate:date=Form(...,description="2024-07-05"),
                            toDate:date=Form(...,description="2024-07-05"),
                            ):

    if user.user_type==1:
        toDate= toDate+timedelta(days=1)
        get_booked_details = (db.query(BookedVehicle)
                            .filter(BookedVehicle.from_time.between(fromDate,toDate),
                                    BookedVehicle.to_time.between(fromDate,toDate),or_(BookedVehicle.status==1,BookedVehicle.status==-1)
                                    ).join(User,BookedVehicle.user_id==User.id)
                                    .join(VehicleDetails,BookedVehicle.vehicle_id==VehicleDetails.id)
                                    .order_by(BookedVehicle.from_time)
                            .all())
        
        if not get_booked_details:
            return {"message":"Details not found"}
        

        bookedDetails =[]
        for detail in get_booked_details:
            
                bookedDetails.append({
                    "Username":detail.user.user_name,
                    "vehicleNo":detail.vehicle_detail.vehicle_no,
                    "fromTime":detail.from_time,
                    "toTime":detail.to_time,
                    "bookedPrice":detail.booked_price
                })
                

        return bookedDetails
    else:
        return{"message":"you are not authorized to view this detail"}

#4) view booked details
@router.get("/user_booked_history")
async def getBookingDetail(db:db_dependency,
                           user=Depends(current_user)):
    getBookedDetail = db.query(BookedVehicle).filter(BookedVehicle.user_id==user.id).all()

    for bookedDetail in getBookedDetail:
        differeneInSeconds = (bookedDetail.to_time - bookedDetail.from_time).total_seconds()

        difference_in_seconds_by_current_time = (datetime.now() - bookedDetail.from_time).total_seconds()

        if difference_in_seconds_by_current_time > differeneInSeconds:
            bookedDetail.status= -1

            db.commit()

    if not getBookedDetail:
        return {"message":"You didn't book any parking space"}
    

    bookedDetail = []


    for detail in getBookedDetail:
        status = ""
        if detail.status == 1:
            status = "current booking"
        if detail.status == -1:
            status = "previously booked"
        if detail.status == 0:
            status = "cancelled"

        
        bookedDetail.append({
            "bookedId":detail.id,
            "vehicleId":detail.vehicle_id,
            "fromTime":detail.from_time,
            "toTime":detail.to_time,
            "status":status
        })
    
    return bookedDetail
    
#5)filter time wise
# # 3) filter date wise
# @router.post("/filter_booked_details")
# async def listBookedDetails(db:db_dependency,
#                             user=Depends(current_user),
#                             fromDate:date=Form(...,description="2024-07-05"),
#                             toDate:date=Form(...,description="2024-07-05"),
#                             ):

#     if user.user_type==1:
#         toDate = toDate+timedelta(days=1)

#         get_booked_details = (db.query(BookedVehicle)
#                             .filter(BookedVehicle.booked_at >= fromDate,BookedVehicle.booked_at <= toDate
#                                     ,BookedVehicle.status !=0)
#                                     .join(User,BookedVehicle.user_id==User.id)
#                                     .join(VehicleDetails,BookedVehicle.vehicle_id==VehicleDetails.id)
                                    
#                             .all())

#         if not get_booked_details:
#             return {"message":"Details not found"}
        

#         bookedDetails =[]
#         for detail in get_booked_details:
            
#                 bookedDetails.append({
#                     "userId":detail.user.id,
#                     "Username":detail.user.user_name,
#                     "vehicleNo":detail.vehicle_detail.vehicle_no,
#                     "fromTime":detail.from_time,
#                     "toTime":detail.to_time,
#                     "bookedPrice":detail.booked_price
#                 })
                

#         return bookedDetails
#     else:
#         return{"message":"you are not authorized to view this detail"}













