from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas import TransactionResponse, TransactionCreate, SelfTransactionResponse
import services


router = APIRouter(prefix="/transactions", tags=["transactions"])


# Add money
@router.post("/add-money", response_model=SelfTransactionResponse, status_code=status.HTTP_200_OK)
async def add_money(user_id: int, amount: float, db: AsyncSession = Depends(get_db)):
    return await services.add_money(db=db, user_id=user_id, amount=amount)
    
# withdrawal money
@router.post("/withdrawal", response_model=SelfTransactionResponse, status_code=status.HTTP_200_OK)
async def withdrawal_money(user_id:int, amount: float, db: AsyncSession = Depends(get_db)):
    return await services.withdrawal_money(db=db, user_id=user_id, amount=amount)


# balance check
@router.get("/balance-check/{user_id}", response_model=SelfTransactionResponse, status_code=status.HTTP_200_OK)
async def balance_check(user_id:int, db: AsyncSession = Depends(get_db)):
    res = await services.balance_check(db=db, user_id=user_id)
    if not res:
            raise HTTPException(status_code=404, detail="User not found")
    return res


# transfer
from schemas import TransferResponse

@router.post("/transfer", response_model=TransferResponse, status_code=status.HTTP_200_OK)
async def transfer(user_id:int, recipient_user_id: int, amount: float, db: AsyncSession = Depends(get_db)):
    res = await services.transfer(db=db, user_id=user_id, recipient_user_id=recipient_user_id, amount=amount)
    if not res:
        raise HTTPException(status_code=404, detail="User not found")
    return res

# POST /transactions
@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(new_trans: TransactionCreate, db: AsyncSession = Depends(get_db)):
    return await services.create_transaction(db=db, new_trans=new_trans)

# GET /transactions/{user_id}?page=1&limit=10
@router.get("/{user_id}", response_model=TransactionResponse, status_code=status.HTTP_200_OK)
async def get_user_transaction(user_id: int, skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await services.get_user_transaction(db=db, user_id=user_id, skip=skip, limit=limit)

# GET /transactions/detail/{transaction_id}
@router.get("/detail/{transaction_id}", response_model=TransactionResponse, status_code=status.HTTP_200_OK)
async def get_transaction_details(tran_id: int, db: AsyncSession = Depends(get_db)):
    return await services.get_transaction_details(db=db, tran_id=tran_id)

