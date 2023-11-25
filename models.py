from sqlalchemy import BigInteger,ForeignKey,select
from sqlalchemy.ext.asyncio import AsyncAttrs,async_sessionmaker,create_async_engine
from sqlalchemy.orm import relationship,Mapped,mapped_column,DeclarativeBase

engine = create_async_engine('sqlite+aiosqlite:///example.db', echo=True)

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs,DeclarativeBase):
    pass

class User(Base):
    __tablename__='users'

    id: Mapped[int] = mapped_column(primary_key=True)
    th_id = mapped_column(BigInteger)

class Category(Base):
    __tablename__='categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()

    products = relationship('Product',back_populates='category')

    
class Product(Base):
    __tablename__='products'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    price: Mapped[int] = mapped_column()
    description: Mapped[str] = mapped_column()
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))

    category = relationship('Category',back_populates='products')   



async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# from .models import User, Category,Product,async_session


async def get_categories():
    async with async_session() as session:
        result = await session.scalars(select(Category))
        return result 
    

