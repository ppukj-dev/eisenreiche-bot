from sqlalchemy import Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Ability(Base):
    __tablename__ = 'tableIK_Ability'
    id = Column("ID", Integer, primary_key=True)
    name = Column("ikAbilityName", Text)
    prerequisites = Column("ikAbilityPrereq", Text)
    details = Column("ikAbilityDetails", Text)