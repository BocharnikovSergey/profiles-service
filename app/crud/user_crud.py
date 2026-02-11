from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import User
from app.schemas.users_schemas import UserCreate,UserUpdate
from sqlalchemy import update
async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    """
    Создает нового пользователя в базе данных.
    """
    new_user = User(
        email=user_in.email,
        hashed_password= user_in.password,
        is_active=True,
        is_superuser=False
        # Здесь позже добавим хеширование пароля 
        # password=get_password_hash(user_in.password) 
    )
    
    db.add(new_user)
    
    await db.commit()
    
    await db.refresh(new_user)
    
    return new_user


async def get_user(db:AsyncSession,user_id: int) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none() 
    return user

async def delete_user(db:AsyncSession,user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user:
        await db.delete(user)
        await db.commit()
    return user

async def update_user(db:AsyncSession,user_id:int,payload:UserUpdate) -> User | None:
    update_data = payload.model_dump(exclude_unset=True)
    if not update_user:
        return await get_user(db,user_id)
    stmt = (
        update(User)
        .where(User.id == user_id)
        .values(**update_data)
        .returning(User)
    )
    result = await db.execute(stmt)
    await db.commit()
    return result.scalar_one_or_none()