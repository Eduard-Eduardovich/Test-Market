from sqlalchemy import BigInteger, ForeignKey, select
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase

engine = create_async_engine('sqlite+aiosqlite:///example.db', echo=True)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    user_id: Mapped[int] = mapped_column()
    purchases = relationship("Purchase", back_populates="user")


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    price: Mapped[int] = mapped_column()
    description: Mapped[str] = mapped_column()
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category = relationship("Category", back_populates="products")
    purchases = relationship("Purchase", back_populates="product")


class Color(Base):
    __tablename__ = "color"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[str] = mapped_column(ForeignKey("products.id"))
    name: Mapped[str] = mapped_column()
    purchases = relationship("Purchase", back_populates="color")


class Purchase(Base):
    __tablename__ = "purchases"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    product_id: Mapped[str] = mapped_column(ForeignKey("products.id"))
    color_id: Mapped[str] = mapped_column(ForeignKey("color.id"))
    memory_id: Mapped[str] = mapped_column(ForeignKey("memory.id"))

    user = relationship("User", back_populates="purchases")
    product = relationship("Product", back_populates="purchases")
    color = relationship("Color", back_populates="purchases")
    memory = relationship("Memory", back_populates="purchases")


class Memory(Base):
    __tablename__ = "memory"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[str] = mapped_column(ForeignKey("products.id"))
    memory: Mapped[str] = mapped_column()
    purchases = relationship("Purchase", back_populates="memory")




async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# from .models import User, Category,Product,async_session



async def add_user_and_purchases(user_id, product_id, color_id, memory_id):
    async with async_session() as session:
        new_user = User(user_id=user_id)
        session.add(new_user)
        await session.commit()

        new_purchase = Purchase(
            user_id=user_id,
            product_id=product_id,
            color_id=color_id,
            memory_id=memory_id,
        )
        session.add(new_purchase)
        await session.commit()






async def get_categories():
    async with async_session() as session:
        result = await session.scalars(select(Category))
        return result 
    

async def get_models():
    async with async_session() as session:
        result = await session.scalars(select(Product))
        return result 
    

async def get_description(desc_id):
    async with async_session() as session:
        result = await session.scalar(select(Product).where(Product.id== desc_id))
        return result 
    
async def get_color_id(color_id):
    async with async_session() as session:
        result = await session.scalar(select(Color).where(Color.id== color_id))
        return result
    

async def get_memory_id(memory_id):
    async with async_session() as session:
        result = await session.scalar(select(Memory).where(Memory.id== memory_id))
        return result



async def get_colors(product_id):
    async with async_session() as session:
        result = await session.scalars(select(Color).where(Color.product_id == product_id))
        return result
    

async def get_memory(product_id):
    async with async_session() as session:
        result = await session.scalars(select(Memory).where(Memory.product_id == product_id))
        return result



