from sqlalchemy import Column, Integer, String, Float, BigInteger, DateTime, ForeignKey, Boolean, Numeric, Index
from sqlalchemy.orm import relationship, declarative_base
from __init__ import engine

#create table and declare keys
base = declarative_base()


class Customers(base):
    __tablename__ = 'customers'
    id = Column(String, primary_key = True)
    name = Column(String)

    __table_args__ = (
        Index('customers_id_index', 'id'),
    )


class Tweets(base):
    __tablename__ = 'tweets'
    id = Column(String, primary_key = True)
    tweeted_at = Column(DateTime)
    content = Column(String(length=500))
    customerid = Column(String, ForeignKey('customers.id'))
    customers = relationship("Customers", backref = 'tweets')

    __table_args__ = (
        Index('tweets_id_index','id'),
        Index('tweets_tweeted_at_index','tweeted_at'),
        Index('tweets_customerid_index','customerid'),
    )


class Supplies(base):
    __tablename__ = 'supplies'
    id = Column(String, primary_key = True)
    name = Column(String)
    cost = Column(Integer)
    perishable = Column(Boolean)

    __table_args__ = (
        Index('supplies_id_index','id'),
    )
    

class TypesOfProducts(base):
    __tablename__ = 'types_of_products'
    id = Column(BigInteger, primary_key = True)
    product_type = Column(String)

    __table_args__ =(
        Index('producttype_id_index','id'),
    )

    

class Products(base):
    __tablename__ = 'products'
    id = Column(String, primary_key = True)
    name = Column(String)
    price = Column(Numeric(10,2))
    description = Column(String(length=255))

    __table_args__ =(
        Index('products_id_index','id'),
    )


class ProductTypes(base):
    __tablename__ = 'product_types'
    id = Column(BigInteger, primary_key = True)
    productid = Column(String, ForeignKey('products.id'))
    types_of_productsid = Column(BigInteger,ForeignKey('types_of_products.id'))
    products = relationship("Products", backref = 'product_types')
    types_of_products = relationship("TypesOfProducts", backref = 'product_types')

    __table_args__ =(
        Index('product_types_productid_index','productid'),
        Index('product_types_types_of_productsid_index','types_of_productsid'),
    )


class ProductSupplies(base):
    __tablename__ = 'product_supplies'
    id = Column(BigInteger, primary_key = True)
    productid = Column(String, ForeignKey('products.id'))
    supplyid = Column(String, ForeignKey('supplies.id'))
    products = relationship("Products", backref = 'product_supplies')
    supplies = relationship("Supplies", backref = 'product_supplies')

    __table_args__ =(
        Index('productsupplies_productid_index','productid'),
        Index('productsupplies_supplyid_index','supplyid'),
    )


class Stores(base):
    __tablename__ = 'stores'
    id = Column(String, primary_key = True)
    name = Column(String)
    opened_at = Column(DateTime)
    tax_rate = Column(Float(53))

    __table_args__ =(
        Index('stores_id_index','id'),
        Index('stores_opened_at_index','opened_at'),
    )


class Orders(base):
    __tablename__ = 'orders'
    id = Column(String, primary_key = True)
    ordered_at = Column(DateTime)
    subtotal = Column(Numeric(10,2))
    customerid = Column(String, ForeignKey('customers.id'))
    storeid = Column(String, ForeignKey('stores.id'))
    customers = relationship("Customers", backref = 'orders')
    stores = relationship("Stores", backref = 'orders')

    __table_args__ =(
        Index('orders_id_index','id'),
        Index('orders_ordered_at_index','ordered_at'),
        Index('orders_customerid_index','customerid'),
        Index('orders_storeid_index','storeid'),
    )


class OrderItems(base):
    __tablename__ = 'order_items'
    id = Column(String, primary_key = True)
    orderid = Column(String, ForeignKey('orders.id'))
    productid = Column(String, ForeignKey('products.id'))
    orders = relationship("Orders", backref = 'product_supplies')
    products = relationship("Products", backref = 'product_supplies')

    __table_args__ =(
        Index('orderitems_orderid_index','orderid'),
        Index('orderitems_productid_index','productid'),
    )

base.metadata.drop_all(engine)
base.metadata.create_all(engine)
print('tables created')

