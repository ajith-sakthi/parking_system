from fastapi import APIRouter,Form,Depends
from api.deps import get_db
from sqlalchemy.orm import Session
from app.core.security import current_user,oauth_scheme
from models import District,Branch,Admin,User
router =  APIRouter()

# 1) add district 
@router.post("/add_district")
async def add_district(db:Session=Depends(get_db),
                       user=Depends(current_user),
                       districtName:str=Form(...)):
    if user.user_type == 1 :
        district = District(district_name = districtName.title(),status = 1)
        db.add(district)
        db.commit()
        return {"message":"New district added successfully"}
    else:
        return {"message":"You are not authorized to add the district"}

# 2) update district
@router.put("/update_district")
async def update_district(db:Session=Depends(get_db),
                       user=Depends(current_user),
                       district_id:int = Form(...),
                       newChanges:str=Form(...)):
    
    if user.user_type == 1:
        district = db.query(District).filter(District.id==district_id).first()
        if district:
            district.district_name = newChanges.title()
            db.commit()
        return {"message":"Updated successfully"}
        
    return {"message":"You are not authorized to update district"}

# 3) delete district
@router.post("/delete_district")
async def delete_district(db:Session=Depends(get_db),
                       user=Depends(current_user),
                       district_id:int = Form(...),
                       ):
    
    if user.user_type == 1:
        district = db.query(District).filter(District.id==district_id).first()
        if district:
            district.status = 0
            db.commit()
        return {"message":"Deleted successfully"}
        
    return {"message":"You are not authorized to delete the district"}


#4) get district detail
@router.get("/get_district")
async def getDistrict(db:Session=Depends(get_db),
                      user=Depends(current_user),
                      no_of_data_per_page:int=5,
                      page_no:int=1):
    
    start = (page_no * no_of_data_per_page)-no_of_data_per_page
    end =  no_of_data_per_page

    getDistrictDetail = db.query(District).filter(District.status==1)

    totalRow = getDistrictDetail.count()

    if start < 0 or start >= totalRow:
        start = 0

    get_detail = getDistrictDetail.offset(start).limit(end).all()

    districtDetail = []

    for detail in get_detail:
        districtDetail.append({
            "districtId":detail.id,
            "districtName":detail.district_name
        })

    return districtDetail

    

    





