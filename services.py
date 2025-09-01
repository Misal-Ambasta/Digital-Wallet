from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import User, Transaction
from schemas import UserCreate, UserUpdate, TransactionCreate


async def create_user(db: AsyncSession, user: UserCreate):
    new_user = User(**user.model_dump())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def update_user(db: AsyncSession, user_update: UserUpdate, user_id: int):
    print("entered")
    result = await db.execute(select(User).where(User.id == user_id))
    db_user = result.scalar_one_or_none()
    if db_user:
        update_data = user_update.model_dump(exclude_unset=True)
        print(update_data)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        await db.commit()
        await db.refresh(db_user)
    return db_user


async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_all_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()



# Transaction services

async def create_transaction(db: AsyncSession, new_trans: TransactionCreate):
    new_transaction = Transaction(**new_trans.model_dump())
    db.add(new_transaction)
    await db.commit()
    await db.refresh(new_transaction)
    return new_transaction


async def get_user_transaction(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 10):
    result = await db.execute(select(Transaction).where(User.id == user_id).offset(skip).limit(limit))
    return result.scalars().all()



async def get_transaction_details(db: AsyncSession, tran_id: int):
    result = await db.execute(select(Transaction).where(Transaction.id == tran_id))
    return result.scalar_one_or_none()

# Add money
async def add_money(db: AsyncSession, user_id: int, amount: float):
    result = await db.execute(select(User).where(User.id == user_id))
    db_user = result.scalar_one_or_none()
    if db_user:
        setattr(db_user, "balance", db_user.balance+amount)
        await db.commit()
        await db.refresh(db_user)
    return db_user


# Withdrawal money
async def withdrawal_money(db: AsyncSession, user_id: int, amount: float):
    result = await db.execute(select(User).where(User.id == user_id))
    db_user = result.scalar_one_or_none()
    if db_user:
        setattr(db_user, "balance", db_user.balance-amount)
        await db.commit()
        await db.refresh(db_user)
    return db_user


# Balance Check
async def balance_check(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    db_user = result.scalar_one_or_none()
    return db_user