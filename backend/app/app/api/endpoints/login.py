from fastapi import APIRouter,Form,Depends,HTTPException
from utils import get_user_by_userName,phoneNo_validation
from sqlalchemy.orm import Session
from api.deps import get_db
from app.core.security import verify_password
from datetime import timedelta
from app.core.config import settings
from app.core.security import create_access_token,current_user
from models import User
from pydantic import EmailStr

router =  APIRouter()

# 1) create a token
@router.post("/token")
async def createAccessToken(db:Session=Depends(get_db),
                 username=Form(...),
                 password=Form(...)):


    user = get_user_by_userName(db,username.strip())

    if user is None:
        raise HTTPException(
        status_code=404,
        detail="Username is not found"
    )
    else:
        verified_user = verify_password(password.strip(),user.pass_word)

        if not verified_user:
            raise HTTPException(
                status_code=403,
                detail="Username and password is not matched"
            )
        
        token_expire_time = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        access_token =  create_access_token(data={"sub":user.user_name},expires_delta=token_expire_time)

        return {"access_token":access_token,"token_type":"bearer"}

# 2) update a user
@router.put("/update_user")
async def update_user(db:Session=Depends(get_db),
                      user=Depends(current_user),
                      userName:str=Form(None),
                      firstName:str=Form(None),
                      lastName:str=Form(None),
                      eMail:EmailStr=Form(None),
                      phNo:str=Form(None)
                      ):
    
    # user_in_db = db.query(User).filter(User.id == user.id).first()

    if user:
        if userName:
            user.user_name = userName
        if firstName:
            user.first_name = firstName
        if lastName:
            user.last_name = lastName
        if eMail:
            user.e_mail = eMail
        if phNo:
            if phoneNo_validation(phNo):
                user.ph_no = phNo
            else:
                return {"message":"Give valid Phone Number"}
        db.commit()
        return{"message":"User details updated successfully"}






        
