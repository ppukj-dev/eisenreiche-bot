from sqlalchemy import Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Skill(Base):
    __tablename__ = 'tableIK_Skill'
    id = Column("ID", Integer, primary_key=True)
    name = Column("ikSkillName", Text)
    stats = Column("ikSkillStats", Text)
    details = Column("ikSkillDetails", Text)
