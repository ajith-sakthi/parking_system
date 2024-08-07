from fastapi import APIRouter,Form,Depends
from api.deps import db_dependency
from pydantic import EmailStr
from models import User
from sqlalchemy.orm import Session
from utils import get_user_by_userName,get_user_by_phNo,get_user_by_email,phoneNo_validation
from api.deps import get_db
from core.security import get_hash_password,current_user
from datetime import datetime

router = APIRouter()

# 1) sign up
@router.post('/')
async def sign_up(db:Session =Depends(get_db),
                  firstName:str=Form(...),
                  lastName:str=Form(...),
                  userName:str=Form(...),
                  eMail:EmailStr=Form(...),
                  password:str=Form(...),
                  phNo:str=Form(...),
                  ):
    

    
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
                user_type = 3,
                status = 1,
                created_at = datetime.now())

    db.add(users)
    db.commit()
    return {"message":"Sign Up successfully"}

# 2) forgot password
@router.put("/forgot_password")
async def change_password(db:Session=Depends(get_db),
                          userName:str=Form(...),
                          eMail:str=Form(...),
                          newPassword:str=Form(...)):
    
    if not get_user_by_userName(db,userName):
        return {"message":"Username is not found"}
    if not get_user_by_email(db,eMail):
        return {"message":"Email id not found"}
    
    user = get_user_by_userName(db,userName)

    if user:
        new_password = get_hash_password(newPassword)
        user.pass_word = new_password
        db.commit()
        return{"message":"Password changed successfully"}


# 3) current_userDetail
# {
#     "userId":1,
#     "user_name":"some_name",
#     "user_typeid":3
# }
@router.get("/current_user_detail")
async def get_current_user(db:Session=Depends(get_db),
                           user=Depends(current_user)):
    getUserDetail = db.query(User).filter(User.id == user.id).first()

    return {
        "userId":getUserDetail.id,
        "user_name":getUserDetail.user_name,
        "user_type":getUserDetail.user_type
    }