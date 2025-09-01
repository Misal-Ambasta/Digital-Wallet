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
        # Check if username is being updated and is unique
        if "username" in update_data:
            username_check = await db.execute(select(User).where(User.username == update_data["username"]).where(User.id != user_id))
            existing_user = username_check.scalar_one_or_none()
            if existing_user:
                from fastapi import HTTPException
                raise HTTPException(status_code=400, detail="Username already exists")
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

# Transfer

async def transfer(db: AsyncSession, user_id: int, recipient_user_id: int, amount: float):
    result1 = await db.execute(select(User).where(User.id == user_id))
    result2 = await db.execute(select(User).where(User.id == recipient_user_id))
    db_user = result1.scalar_one_or_none()
    recipient_user = result2.scalar_one_or_none()
    if not db_user or not recipient_user:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="User(s) not found")
    if db_user.balance < amount:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Insufficient balance")
    # Deduct and add balance
    db_user.balance -= amount
    recipient_user.balance += amount
    await db.commit()
    await db.refresh(db_user)
    await db.refresh(recipient_user)
    # Create transaction for sender
    sender_transaction = Transaction(
        transaction_type="transfer",
        amount=amount,
        description=f"Transfer to user {recipient_user_id}",
        user_id=user_id,
        recipient_user_id=recipient_user_id
    )
    db.add(sender_transaction)
    await db.commit()
    await db.refresh(sender_transaction)
    # Create transaction for recipient
    recipient_transaction = Transaction(
        transaction_type="receive",
        amount=amount,
        description=f"Received from user {user_id}",
        user_id=recipient_user_id,
        recipient_user_id=user_id
    )
    db.add(recipient_transaction)
    await db.commit()
    await db.refresh(recipient_transaction)
    return {"sender_transaction_id": sender_transaction.id, "recipient_transaction_id": recipient_transaction.id}
        