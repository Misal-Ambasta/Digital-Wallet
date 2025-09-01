from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from database import get_db
from schemas import UserResponse, UserCreate, UserUpdate
import services


router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await services.create_user(user=user, db=db)


@router.put("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user_update: UserUpdate, db: AsyncSession = Depends(get_db)):
    return await services.update_user(db=db, user_update=user_update, user_id=user_id)


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    res = await services.get_user(user_id=user_id, db=db)
    if not res:
        raise HTTPException(status_code=404, detail="User not found")
    return res

@router.get("/all", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
async def get_all_users(db:AsyncSession = Depends(get_db)):
    return await services.get_all_users(db=db)


