from fastapi import APIRouter
from fastapi import APIRouter,Form,Depends,Query
from pydantic import EmailStr
from api.deps import get_db
from sqlalchemy.orm import Session
from app.core.security import current_user
from utils import get_user_by_userName,get_user_by_phNo,get_user_by_email,phoneNo_validation
from core.security import get_hash_password
from models import User,Admin,District, BookedVehicle, Branch, Manager,VehicleDetails, PriceDetail
from datetime import datetime,date, timedelta
from sqlalchemy import func,or_,desc
from fpdf import FPDF

router = APIRouter()


#1) create a admin
@router.post("/create_admin")
async def createAdmin(db:Session =Depends(get_db),
                     user=Depends(current_user),
                  firstName:str=Form(...),
                  lastName:str=Form(...),
                  userName:str=Form(...),
                  eMail:EmailStr=Form(...),
                  password:str=Form(...),
                  phNo:str=Form(...)):
    
    if user.user_type == 1 :
        if get_user_by_userName(db,userName):
            return {"message":"This username is already exist"}
        if get_user_by_email(db,eMail):
            return {"message":"This emailId is already exist"}
        if get_user_by_phNo(db,phNo):
            return {"message":"This Phone Number is already exist"}
        if " " in phNo:
            return{"message":"Don't give space between the phone Number"}
        if not phoneNo_validation(phNo):
            return {"message":"Give a valid phone number"}
    
        hashed_password =  get_hash_password(password)
        
        
        users = User(first_name=firstName,
                    last_name=lastName,
                    user_name= userName,
                    e_mail=eMail,
                    pass_word = hashed_password,
                    ph_no=phNo,
                    user_type = 2,
                    status = 1,
                    created_at = datetime.now())
        db.add(users)
        db.commit()
        return {"message":"User created successfully"}
    else:
        return {"message":"You are not allowed to create a admin"}



#2) add admin
@router.post("/add_admin")
async def addAdmin(db:Session=Depends(get_db),
                   user=Depends(current_user),
                   userId:int=Form(...),
                   districtId:int=Form(...)
                   ):
    
    if user.user_type !=1 :
        return {"message":"Only super-admin can add the admin"}
    
    get_user = db.query(User).filter(User.id==userId,User.user_type==2).first()
    get_district = db.query(District).filter(District.id==districtId).first()

    if not get_user:
        return {"message":"Given userID is not a admin"}
    
    if not get_district:
        return {"message":"District details not found, once check your district Id"}
    
    get_admin_detail = db.query(Admin).filter(Admin.user_id==userId,Admin.status==1).first()

    if get_admin_detail:
        return {"Giver user id is already a admin in another district"}
    
    admin = Admin(user_id =userId,district_id=districtId,status=1)

    db.add(admin)
    db.commit()
    return{"message":"Admin added successfully"}
    

#3) create a manager
@router.post("/create_manager")
async def createManager(db:Session =Depends(get_db),
                     user=Depends(current_user),
                  firstName:str=Form(...),
                  lastName:str=Form(...),
                  userName:str=Form(...),
                  eMail:EmailStr=Form(...),
                  password:str=Form(...),
                  phNo:str=Form(...)):
    
    if user.user_type == 1 or user.user_type==2:
        if get_user_by_userName(db,userName):
            return {"message":"This username is already exist"}
        if get_user_by_email(db,eMail):
            return {"message":"This emailId is already exist"}
        if get_user_by_phNo(db,phNo):
            return {"message":"This Phone Number is already exist"}
        if " " in phNo:
            return{"message":"Don't give space between the phone Number"}
        if not phoneNo_validation(phNo):
            return {"message":"Give a valid phone number"}
    
        hashed_password =  get_hash_password(password)
        
        
        users = User(first_name=firstName,
                    last_name=lastName,
                    user_name= userName,
                    e_mail=eMail,
                    pass_word = hashed_password,
                    ph_no=phNo,
                    user_type = 4,
                    status = 1,
                    created_at = datetime.now())
        db.add(users)
        db.commit()
        return {"message":"User created successfully"}
    else:
        return {"message":"You are not allowed to create a admin"}

#4) add a manager
@router.post("/add_manager")
async def addManager(db:Session=Depends(get_db),
                     user=Depends(current_user),
                     districtId:int=Form(...),
                     userId:int=Form(...),
                     branchId:int=Form(...),
                    ):
    
    if user.user_type == 1 or user.user_type==2:

        get_branch_details = db.query(Branch).filter(Branch.id==branchId,Branch.district_id==districtId,Branch.status==1,Branch.approved_status==1).first()

        if not get_branch_details:
            return {"message":"Branch details not found"}

        if user.user_type==2:
            get_admin = (db.query(Admin)
                         .filter(Admin.user_id==user.id,Admin.district_id==districtId,Admin.status == 1)
                         .all())
            
            if not get_admin:
                return {"message":"You are not able to add manager in another district"}
            
            
        get_user = db.query(User).filter(User.id==userId,User.user_type==4).first()
       

        if not get_user:
            return {"message":"The given User id is not a manager"}
        
        checkManager = db.query(Manager).filter(or_(Manager.user_id == userId,Manager.branch_id==branchId),Manager.status == 1).first()

        
        
        if checkManager:
            return {"message":"Given branch already had a manager or given user id is already a manager"}
        
        

        add_manager = Manager(branch_id = branchId,user_id = userId,status=1,created_at = datetime.now())

        db.add(add_manager)
        db.commit()

        return {"message":"Manager Successfully added"}
            
    else:
        return {"message":"you are not allowed to add a manager"}


#5) total amount - branch
@router.post("/branch_wise_income")
async def branchWiseAmount(db:Session=Depends(get_db),
                           user=Depends(current_user),
                           branchId:int=Form(None),
                           no_of_data_per_page:int=5,
                           page_no:int=1):


    start = (page_no * no_of_data_per_page) - no_of_data_per_page # 1 * 5 - 5 == 0 
    end = no_of_data_per_page # 5

    if user.user_type == 1 or user.user_type == 2:

        if user.user_type ==1:
            
            if branchId:

                getBranch = db.query(Branch).filter(Branch.id==branchId).first()

                if not getBranch:
                    return {"message":"BranchId not found"}
                
                getAmount = (db.query(func.sum(BookedVehicle.booked_price))
                            .filter(BookedVehicle.branch_id==branchId,or_(BookedVehicle.status==1,BookedVehicle.status == -1))
                            .scalar())
                
                if not getAmount:
                    return {"message":"No booking in this branch"}
                
                return {
                    "branchId":branchId,
                    "TotalAmount":getAmount
                }
            else:
                
                # getamt = (db.query(BookedVehicle.branch_id,func.sum(BookedVehicle.booked_price))
                #             .filter(or_(BookedVehicle.status==1,BookedVehicle.status == -1))
                #             .group_by(BookedVehicle.branch_id)
                #             )
                getamt = (db.query(BookedVehicle.branch_id,func.sum(BookedVehicle.booked_price))
                            .filter((BookedVehicle.status!=0))
                            .group_by(BookedVehicle.branch_id)
                            )
                totalRow= getamt.count()
                
                if start < 0 or start >= totalRow:
                    start = 0
            

                getamount = getamt.offset(start).limit(end).all()

            
                branchWiseAmount = []
                
                for branchid,amount in getamount:
                    branchWiseAmount.append({
                        "branchId":branchid,
                        "Total amount":amount

                    })
                
                return branchWiseAmount
            
        if user.user_type == 2:
            
            getAdmin = db.query(Admin).filter(Admin.user_id==user.id).first()
            
            if not branchId:
               
                getBookedDetails = (db.query(BookedVehicle.branch_id,func.sum(BookedVehicle.booked_price))
                                .filter(BookedVehicle.district_id == getAdmin.district_id,or_(BookedVehicle.status==1,BookedVehicle.status == -1))
                                .group_by(BookedVehicle.branch_id))
                
                totalRow= getBookedDetails.count()
                
                if start < 0 or start >= totalRow:
                    start = 0

                getBookedDetail =getBookedDetails.offset(start).limit(end).all()

                branchWiseAmount = []

                for branchid,amount in getBookedDetail:
                    branchWiseAmount.append({
                        "branchId":branchid,
                        "Total amount":amount
                    })
                return branchWiseAmount
            
            # filter branch detail by login admin's districtId
            getBranchDetail =  db.query(Branch).filter(Branch.district_id==getAdmin.district_id).all()

            getBranchId=[]
            for detail in getBranchDetail:
                getBranchId.append(detail.id)

            
            if branchId not in getBranchId:
                return {"message":"You view only your allocated branches"}
            
            # check branch is available
            getBranch = db.query(Branch).filter(Branch.id==branchId).first()

            if not getBranch:
                return {"message":"BranchId not found"}

            getAmount = (db.query(func.sum(BookedVehicle.booked_price))
                            .filter(BookedVehicle.branch_id==branchId,or_(BookedVehicle.status==1,BookedVehicle.status == -1))
                            .scalar())
            if not getAmount:
                    return {"message":"No booking in this branch"}
                
            return {
                "branchId":branchId,
                "TotalAmount":getAmount
            }

    else:
        return {"message":"You are not allowed to view this detail"}

#6) list admin details
@router.get("/listAdminDetails")
async def getAdmin(db:Session=Depends(get_db),
                    user=Depends(current_user),
                    no_of_data_per_page:int=5,
                    page_no:int=1
                      ):
    start = (page_no * no_of_data_per_page)-no_of_data_per_page
    end =  no_of_data_per_page

    if not (user.user_type == 1 or user.user_type == 2  ):
        return {"message":"You are not authorized to view this detail"}
    
    get_details = (db.query(User.user_name,District.id,District.district_name)
                .join(Admin,User.id == Admin.user_id)
                .join(District, Admin.district_id==District.id)
                )
    
    totalRow = get_details.count()

    if start < 0 or start >= totalRow:
            start = 0

    get_detail = get_details.offset(start).limit(end).all()

    districtDetail = []

    for userName, id,districtName in get_detail:
        districtDetail.append({
            
            "districtId":id,
            "adminName":userName,
            "districtName":districtName
        })

    return districtDetail
    
#7) list manager details
@router.get("/listManagerDetails")
async def getManager(db:Session=Depends(get_db),
                      user=Depends(current_user),
                      no_of_data_per_page:int=5,
                      page_no:int=1):
    
    start = (page_no * no_of_data_per_page)-no_of_data_per_page
    end =  no_of_data_per_page
    
    if not (user.user_type == 1 or user.user_type == 2  ):
        return {"message":"You are not authorized to view this detail"}
    
    if user.user_type ==1 or user.user_type==2:
        if user.user_type ==1 :
            
            get_details = (db.query(User.user_name,Branch.id,Branch.branch_name,Manager.status)
                        .join(Manager,User.id == Manager.user_id)
                        .join(Branch, Branch.id==Manager.branch_id)
                        .filter(Manager.status==1)
                        .order_by(Branch.id)
                        )

            totalRow = get_details.count()
            
            if start < 0 or start >= totalRow:
                start = 0

            get_detail = get_details.offset(start).limit(end).all()

            branchDetail = []

            for userName, id,branchName,status in get_detail:
                if status == 1:
                    branchDetail.append({
                        
                        "branchId":id,
                        "managerName":userName,
                        "branchName":branchName
                    })  

            return branchDetail
        
        if user.user_type == 2 :
            getAdmin = db.query(Admin).filter(Admin.user_id==user.id).first()

            
            get_branch_details = (db.query(User.user_name,Branch.id,Branch.branch_name)
                                .filter(Branch.district_id == getAdmin.district_id)
                                .join(Manager,User.id == Manager.user_id)
                                .join(Branch, Manager.branch_id==Branch.id)
                                .filter(Manager.status==1)
                                )
            
            totalRow = get_branch_details.count()
            print(totalRow)
            if start < 0 or start >= totalRow:
                start = 0

            get_branch_detail = get_branch_details.offset(start).limit(end).all()

            manager_details = []

            for username,branchId,branchname in get_branch_detail:
                manager_details.append({
                    "branchId":branchId,
                    "managerName":username,
                    "branchName":branchname
                })


            return manager_details

#8) frequent branch booking
@router.get("/frequently_booking_branch")
async def frequentlyBookingBranch(db:Session=Depends(get_db),
                                  user=Depends(current_user)):
    if user.user_type == 1:
        getData = (db.query(BookedVehicle.branch_id,func.count(BookedVehicle.branch_id)
                            .label("frequently_booked_branch_count"))
                            .group_by(BookedVehicle.branch_id)
                            .filter(BookedVehicle.status!=0)
                            .order_by(desc("frequently_booked_branch_count")).first())
       

        getBranchDetail = db.query(Branch).filter(Branch.id==getData[0]).first()

        return {"branchId":getData[0],
                "branchName":getBranchDetail.branch_name,
                
                }

    return {"message":"You are not authorized to view this detail"}


#9) highest income branch
@router.get("/high_income_branch")
async def highIncomeBranch(db:Session=Depends(get_db),
                           user=Depends(current_user)):
    
    if user.user_type == 1 :
        getIncomeData = (db.query(BookedVehicle.branch_id,func.sum(BookedVehicle.booked_price)
                                  .label("Income"))
                         .group_by(BookedVehicle.branch_id)
                         .filter(BookedVehicle.status!=0)
                         .order_by(desc("Income"))
                         .first()
                         )

        getBranchDetail = db.query(Branch).filter(Branch.id==getIncomeData[0]).first()

        return {"branchId":getIncomeData[0],
                "branchName":getBranchDetail.branch_name,
                "income":getIncomeData[1]
                }
    if user.user_type == 2:
        getAdmin = db.query(Admin).filter(Admin.user_id==user.id).first()
        getIncomeData = (db.query(BookedVehicle.branch_id,func.sum(BookedVehicle.booked_price)
                                  .label("Income"))
                         .group_by(BookedVehicle.branch_id)
                         .filter(BookedVehicle.status!=0,BookedVehicle.district_id==getAdmin.district_id)
                         .order_by(desc("Income"))
                         .first()
                         )
        
        getBranchDetail = db.query(Branch).filter(Branch.id==getIncomeData[0]).first()

        return {"branchId":getIncomeData[0],
                "branchName":getBranchDetail.branch_name,
                "Income":getIncomeData[1]
                }

    return {"message":"You are not authorized to view this detail"}


  









# # invoice= []
#     invoiceNew = {
#             "BookedId":getBookingDetails.id,
#             "Name":getBookingDetails.user.user_name,
#             "BranchName":getBookingDetails.branch.branch_name,
#             "BookedDate":getBookingDetails.booked_at,
#             "FromTime":getBookingDetails.from_time,
#             "ToTime":getBookingDetails.to_time,
#             "Amount":getBookingDetails.booked_price

#         }

    # for bookedDetail in getBookingDetails:
    #     invoice.append({
    #         "BookedId":bookedDetail.id,
    #         "Name":bookedDetail.user.user_name,
    #         "BranchName":bookedDetail.branch.branch_name,
    #         "BookedDate":bookedDetail.booked_at,
    #         "FromTime":bookedDetail.from_time,
    #         "ToTime":bookedDetail.to_time,
    #         "Amount":bookedDetail.booked_price

    #     })

    # return invoiceNew

    # bookingDetails =[]

    # for booked in getBookingDetails:
        
    #     bookingDetails.append(booked)
    
    # return bookingDetails




            
        





# {
#     "booking_id": 5,
#     "userName": "some name",
#     "vehicleNo": "TN 02 GH 4568",
#     "branchName": "saravanampatti",
#     "description":hourly/day,
#     "unitprice":hourrate / day rate
#     "bookedPrice":15,
# }