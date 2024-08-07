from fastapi import APIRouter
from fastapi import APIRouter,Form,Depends,Query
from pydantic import EmailStr
from api.deps import get_db
from sqlalchemy.orm import Session
from app.core.security import current_user
from utils import getBranchReport,invoiceDetail
from models import User,Admin,District, BookedVehicle, Branch, Manager,VehicleDetails, PriceDetail
from datetime import datetime,date, timedelta
from sqlalchemy import func,or_,desc
from fpdf import FPDF

router = APIRouter()    


#1) getInvoice
@router.post("/get_invoice")
async def getInvoice(db:Session=Depends(get_db),
                           user=Depends(current_user),
                           bookedId:int = Form(...),
                           type:int=Form(...,description="1.pdf,2.xlsx")):
    
    
    getBookingDetails =( db.query(BookedVehicle)
                        .join(User,BookedVehicle.user_id == user.id)
                        .join(VehicleDetails,BookedVehicle.vehicle_id == VehicleDetails.id)
                        .join(Branch,BookedVehicle.branch_id == Branch.id)
                        .filter(BookedVehicle.id == bookedId,BookedVehicle.user_id==user.id,BookedVehicle.status!=0)
                        .first()
                        )
    
    if not getBookingDetails:
        return {"message":"Details not found"}
    
    bookedDate = str(getBookingDetails.booked_at.date())
    
    time_difference =  getBookingDetails.to_time - getBookingDetails.from_time

    # get price detail
    get_price_details = db.query(PriceDetail).filter(PriceDetail.vehicle_type_id==getBookingDetails.vehicle_detail.vehicle_type_id)

    if (time_difference.days and time_difference.seconds) or (time_difference.days and time_difference.seconds==0):
        # id = 2 ---> day
        # print("day")
        bike_or_car_parking_price = get_price_details.filter(PriceDetail.price_range_id==2).first()
        
        if time_difference.days and time_difference.seconds:
            days_count = time_difference.days + 1 
        else:
            days_count = time_difference.days
        
        # Booked price
        price = days_count * bike_or_car_parking_price.price

        invoiceNew = {
            "BookedId":getBookingDetails.id,
            "Name":getBookingDetails.user.user_name,
            "BranchName":getBookingDetails.branch.branch_name,
            "Description":"Day Rate",
            "Unit Price":int(bike_or_car_parking_price.price),
            "Quantity":int(days_count),
            "Amount":getBookingDetails.booked_price
        }

       
        invoiceDetail(invoiceNew,bookedDate,type)

        return {"message":"Invoice generated successfully"}
    else:
        # id=1---> hour
        bike_or_car_parking_price = get_price_details.filter(PriceDetail.price_range_id==1).first()

        #convert seconds into hour 
        hour_count = ((time_difference.seconds)/60)/60


        # price = hour_count * bike_or_car_parking_price.price

        invoiceNew = {
            "BookedId":getBookingDetails.id,
            "Name":getBookingDetails.user.user_name,
            "BranchName":getBookingDetails.branch.branch_name,
            "Description":"Hourly Rate",
            "Unit Price":bike_or_car_parking_price.price,
            "Quantity":int(hour_count),
            "Amount":getBookingDetails.booked_price
        }


        invoiceDetail(invoiceNew,bookedDate,type)


        return {"message":"Invoice generated successfully"}


#2) list branch with income details
@router.post("/branches_income_detail")
async def getBranchIncomeDetails(db:Session=Depends(get_db),
                           user=Depends(current_user),
                           type:int=Form(...,description="1.pdf,2.xlsx"),
                           fromDate :date =Form(None),
                           toDate:date=Form(None)):
    if not (user.user_type == 1 or user.user_type == 2):
        return {"message":"You are not authorized to view this detail"}
    
    if fromDate and toDate:
        
        endDate = toDate + timedelta(days=1) 

        if user.user_type==1:
            
            getIncomeData = (db.query(BookedVehicle.branch_id,func.sum(BookedVehicle.booked_price)
                                    .label("Income"))
                                    .filter(BookedVehicle.from_time.between(fromDate,endDate),
                                            BookedVehicle.to_time.between(fromDate,endDate))
                            .group_by(BookedVehicle.branch_id)
                            .filter(BookedVehicle.status!=0)
                            .order_by(desc("Income"))
                            .all()
                            )
            incomeDetails = []
            total = 0 
            for incomeDetail in getIncomeData:
                count = 0 
                branchName = db.query(Branch).filter(Branch.id ==  incomeDetail[0]).first()

                incomeDetails.append(
                    {
                        "Branch ID": incomeDetail[0],
                        "BranchName":branchName.branch_name,
                        "Income": incomeDetail[1]

                    }
                )
            
                total = total + incomeDetail[1]
                count += 1
            
            getBranchReport(incomeDetails,total,type)

            return incomeDetails
        if user.user_type == 2:
            getAdmin = db.query(Admin).filter(Admin.user_id==user.id).first()
            getIncomeData = (db.query(BookedVehicle.branch_id,func.sum(BookedVehicle.booked_price)
                                    .label("Income"))
                                    .filter(BookedVehicle.from_time.between(fromDate,endDate),
                                            BookedVehicle.to_time.between(fromDate,endDate))
                            .group_by(BookedVehicle.branch_id)
                            .filter(BookedVehicle.status!=0,BookedVehicle.district_id==getAdmin.district_id)
                            .order_by(desc("Income"))
                            .all()
                            )
            

            incomeDetails = []
            total = 0

            for incomeDetail in getIncomeData:
                branchName = db.query(Branch).filter(Branch.id ==  incomeDetail[0]).first()

                incomeDetails.append(
                    {
                        "Branch ID": incomeDetail[0],
                        "BranchName":branchName.branch_name,
                        "Income": incomeDetail[1]

                    }
                )
                total = total + incomeDetail[1]

            getBranchReport(incomeDetails,total,type)
            return incomeDetails
        
    else:
        if user.user_type==1:
            getIncomeData = (db.query(BookedVehicle.branch_id,func.sum(BookedVehicle.booked_price)
                                    .label("Income"))
                            .group_by(BookedVehicle.branch_id)
                            .filter(BookedVehicle.status!=0)
                            .order_by(desc("Income"))
                            .all()
                            )
            
            incomeDetails = []
            total = 0
            count= 0
            for incomeDetail in getIncomeData:
                
                branchName = db.query(Branch).filter(Branch.id ==  incomeDetail[0]).first()

                incomeDetails.append(
                    {
                        "Branch ID": incomeDetail[0],
                        "BranchName":branchName.branch_name,
                        "Income": incomeDetail[1]

                    }
                )

                total = total + incomeDetail[1]
                count += 1
            print(count)
            
            getBranchReport(incomeDetails,total,type)
            


            return incomeDetails
        if user.user_type == 2:
            getAdmin = db.query(Admin).filter(Admin.user_id==user.id).first()
            getIncomeData = (db.query(BookedVehicle.branch_id,func.sum(BookedVehicle.booked_price)
                                    .label("Income"))
                            .group_by(BookedVehicle.branch_id)
                            .filter(BookedVehicle.status!=0,BookedVehicle.district_id==getAdmin.district_id)
                            .order_by(desc("Income"))
                            .all()
                            )
            

            incomeDetails = []
            total = 0

            for incomeDetail in getIncomeData:
                branchName = db.query(Branch).filter(Branch.id ==  incomeDetail[0]).first()

                incomeDetails.append(
                    {
                        "Branch ID": incomeDetail[0],
                        "BranchName":branchName.branch_name,
                        "Income": incomeDetail[1]

                    }
                )
                total = total + incomeDetail[1]

            getBranchReport(incomeDetails,total,type)

            return incomeDetails


