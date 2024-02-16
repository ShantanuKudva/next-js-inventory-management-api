from sqlalchemy import Column, Integer, DateTime, String, ForeignKey

from db import Base

class Orders(Base):
    __tablename__= 'orders'
    order_id= Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    product_id=Column(Integer, ForeignKey('products.product_id', ondelete='CASCADE'), nullable=False)
    quantity=Column(Integer)
    order_date=Column(DateTime)
    status=Column(String)


class Products(Base):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True, nullable=False, index=True, autoincrement=True)
    name=Column(String)
    description=Column(String)

class ProductPartAssociation(Base):
    __tablename__ ='product_part_associations'
    id=Column(Integer, autoincrement=True, index=True, primary_key=True, nullable=False)
    product_id=Column(Integer, ForeignKey('products.product_id', ondelete='CASCADE'))
    part_id=Column(Integer, ForeignKey('parts.part_id', ondelete='CASCADE'))
    quantity = Column(Integer)

class Parts(Base):
    __tablename__ = 'parts'
    part_id=Column(Integer, autoincrement=True, index=True, primary_key=True, nullable=False)
    part_name = Column(String)
    inventory_quantity = Column(Integer, default=0)  