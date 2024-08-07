from fastapi import APIRouter,Form,Depends
from api.deps import get_db
from sqlalchemy.orm import Session
from app.core.security import current_user
from models import District,Branch,Admin,User,Manager
from datetime import datetime
router =  APIRouter()


#1) add branch
@router.post("/add_branch")
async def add_branch(db:Session=Depends(get_db),
                       user=Depends(current_user),
                       districtId:int=Form(...),
                       branchName:str=Form(...),
                    #    managerId:int=Form(...)
                       ):
    if user.user_type == 1 or user.user_type == 2 :


        # get_manager= db.query(User).filter(User.id==managerId,User.user_type == 4).all()


        # if not get_manager:
        #     return {"message":"Manager Details not found, once check your manager id"}
        


        district = db.query(District).filter(District.id==districtId,District.status==1).first()
        if not district:
            return {"message":"District id not found"}
        
        if user.user_type == 1:
            branch = Branch(branch_name = branchName.title(),
                            district_id=districtId,
                            status = 1, approved_status = 1)
            
        get_admin = db.query(Admin).filter(Admin.user_id ==user.id,Admin.district_id==districtId).first()

        if user.user_type == 2:
            if not get_admin:
                return {"message":"You are not authorized to add a branch to this district"}
            
            branch = Branch(branch_name = branchName.title(),
                            district_id=districtId,
                            status = -1, approved_status = -1)
        db.add(branch)
        db.commit()

        return {"message":"New branch added successfully"}
    else:
        return {"message":"You are not authorized to create the branch"}
    

# 2) get pending status 
@router.get("/pending_status_branch")
async def getPendingStatusBranch(db:Session=Depends(get_db),
                                 user=Depends(current_user)):
    
    if user.user_type == 1 or user.user_type == 2:

        get_pending_status = db.query(Branch).filter(Branch.approved_status == -1)

        if not get_pending_status:
            return {"message":"There is no branch with pending status"}
        
        branch_details=[]
        for branch in get_pending_status:
            branches = {
                "branchID" : branch.id,
                "branchName":branch.branch_name
            }
            branch_details.append(branches)

        return branch_details
    return {"message":"You are not authorized to view this details"}
  

#3) approved branch api
@router.post("/approve")
async def approved(db:Session=Depends(get_db),
                   user=Depends(current_user),
                   branchId:int=Form(...),
                   approvedStatus:int=Form(...,description="0.Rejected, 1.Approved")  ):
    
    if user.user_type ==1:
        get_branch_detail = db.query(Branch).filter(Branch.id==branchId ,
                                                    Branch.status == -1,
                                                    Branch.approved_status==-1).first()
        
        if not get_branch_detail:
            return {"message":"No details found, check your branchId once"}
        
        
        if not (approvedStatus == 0 or approvedStatus ==1):
            return {"message":"Give the value '0' or '1'"}

        if approvedStatus == 0:
            get_branch_detail.approved_status = approvedStatus
            db.commit()
            return {"message":"You rejected this branch"}
        

        get_branch_detail.approved_status = approvedStatus
        get_branch_detail.status = 1
        db.commit()
        return {"message":"You successfully approved the branch"}
    
    return {"message":"You are not authorized to approve"}
 

#4) list the branch in specific district
@router.post("/specific_district_branchName")
async def listBranchName(db:Session=Depends(get_db),
                         user=Depends(current_user),
                         districtId:int=Form(...)   
                         ):
            
        get_branchName = db.query(Branch).filter(Branch.district_id==districtId,Branch.approved_status==1).all()

        if not get_branchName:
            return {"message":"Branch details not found"}
        
        branchName = []

        for name in get_branchName:
            branchName.append({
                "branchId":name.id,
                "branchName":name.branch_name
            })

        return branchName
    
   
#5) delete branch
@router.post("/delete_branch")
async def deleteBranch(db:Session=Depends(get_db),
                       user=Depends(current_user),
                       branchId:int = Form(...)
                       ):
    if user.user_type ==1 :

        getBranchDetails =  db.query(Branch).filter(Branch.id==branchId,Branch.status==1).first()

        if not getBranchDetails:
            return {"message":"Branch details not found, once check your branch id"}
        
        getBranchDetails.status = 0

        db.commit()
        return{"message":"Branch deleted"}




