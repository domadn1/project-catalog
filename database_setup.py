#!/usr/bin/env python3

''' Creates a database catalog which allows to maintain Products
for making catalog to display on web
'''

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    ''' Stores User detail for acess and authorization purposes '''
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

    @property
    def serialize(self):
        ''' Return object data in easily serializeable format '''
        return {
            'id' : self.id,
            'name': self.name,
            'email': self.email,
            'picture': self.picture
        }


class Category(Base):
    ''' Stores Category for Product '''
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        ''' Return object data in easily serializeable format '''
        return {
            'name': self.name,
            'id': self.id
        }


class ProductItem(Base):
    ''' Store Products with price, description and categories'''
    __tablename__ = 'product_item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)


    @property
    def serialize(self):
        ''' Return object data in easily serializeable format '''
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
        }


ENGINE = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(ENGINE)
print('Database catalog successfully created!')
