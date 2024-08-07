from fastapi import APIRouter,Depends,UploadFile,File
from utils import phoneNo_validation
from sqlalchemy.orm import Session
from api.deps import get_db
from app.core.config import settings
from app.core.security import current_user
from models import TestUser
from schemas import Feedback


router = APIRouter()

@router.post("/upload_user_detail")
async def uploadUserDetail(db:Session= Depends(get_db),
                           file:UploadFile=File(...,description="xlsx"),
                           user=Depends(current_user)):
    
    
    
    if user.user_type == 1:
        check_file_extension = file.filename.split(".")[1]
        

        if check_file_extension != "xlsx":
            return {"message":"File format should be in xlsx format"}
        
        readData = await file.read()
        
        # setting a path
        base_dir =  settings.BASE_UPLOAD_FOLDER
        
        file_path =  f"{base_dir}{file.filename}"
        
        f= open(file_path,"wb")
        f.write(readData)

        import pandas as pd

        excel_data = pd.read_excel(file_path)

        testUser = []
        for index,row in excel_data.iterrows():
            firstName = row["first_name"]if not pd.isna(row["first_name"]) else None
            lastName =  row["last_name"]if not pd.isna(row["last_name"]) else None
            userName = row["user_name"]if not pd.isna(row["user_name"]) else None
            e_mail = row["email"]if not pd.isna(row["email"]) else None
            contactNo = str(row["contact_no"])if not pd.isna(row["contact_no"]) else None

            testUser.append({
                "firstName":firstName,
                "lastName":lastName,
                "userName":userName,
                "e_mail":e_mail,
                "contactNo":contactNo
            })


        for userData in testUser:

            check_duplicate_user =  db.query(TestUser).filter(TestUser.user_name==userData["userName"]).first()
            
            if not check_duplicate_user:

                if not phoneNo_validation(userData["contactNo"]):
                    return {"message":f"{userData['contactNo']} : Phone number is invalid "}
                
                addUserData = TestUser(
                    first_name = userData["firstName"],
                    last_name=userData["lastName"],
                    user_name =  userData["userName"],
                    email = userData["e_mail"],
                    contact_no = userData["contactNo"]
                )
                
                db.add(addUserData)
                db.commit()
            else:
                return {"message":f"{userData['userName']} is already exist"}
                
    
        return {"message":"Test user created successfully"}



@router.post("/feedback")
async def feedback(fd_back:Feedback):
    return fd_back

    
