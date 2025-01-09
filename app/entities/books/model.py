from sqlalchemy import Integer, String, Column, Text

from database.connect import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(30), index=True, nullable=False)
    author = Column(String(30), index=True, nullable=False)
    description = Column(Text, nullable=True)
    year = Column(Integer, index=True, nullable=False)