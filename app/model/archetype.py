from sqlalchemy import Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Archetype(Base):
    __tablename__ = 'tableIK_Archetype'
    id = Column("ID", Integer, primary_key=True)
    name = Column("ikArchetypeName", Text)
    details = Column("ikArchetypeDetails", Text)


class ArchetypeBenefit(Base):
    __tablename__ = 'tableIK_ArchetypeBenefit'
    id = Column("ID", Integer, primary_key=True)
    archetype = Column("ikArchetypeName", Text)
    name = Column("ikArchetypeBenefit", Text)
    details = Column("ikBenefitDetails", Text)
