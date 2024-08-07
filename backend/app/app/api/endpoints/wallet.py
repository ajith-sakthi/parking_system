from fastapi import APIRouter,Form,Depends
from api.deps import get_db
from app.core.security import current_user
from models import Wallet
from datetime import datetime
from sqlalchemy.orm import Session


router = APIRouter()


# 1) add amount to wallet
@router.post("/add_wallet_detail")
async def addAmount(db:Session=Depends(get_db),
                    user=Depends(current_user),
                    addAmount:float=Form(...)):
    
    get_wallet_detail = db.query(Wallet).filter(Wallet.user_id == user.id).first()
    
    if get_wallet_detail:
        credit_amount = get_wallet_detail.amount
        credit_amount = credit_amount + addAmount
        get_wallet_detail.amount = credit_amount
        get_wallet_detail.money_added_at = datetime.now()
        db.commit()
        return {"message":"Money added to your wallet successfully"}
    
    wallet = Wallet(user_id = user.id,amount=addAmount,money_added_at=datetime.now())
    db.add(wallet)
    db.commit()
    return {"message":"Money added to your wallet successfully"}
    
# 2) get wallet details
@router.get("/get_wallet_details")
async def getWalletDetail(db:Session=Depends(get_db),
                          user=Depends(current_user)):
    
    getWallet =  db.query(Wallet).filter(Wallet.user_id==user.id).first()

    if not getWallet:
        return{"message":"You didn't add a wallet details"}
    
    return {
        "userId":getWallet.user_id,
        "walletId":getWallet.id,
            "currentAmount":getWallet.amount
            }

    