from sqlalchemy import Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Spell(Base):
    __tablename__ = 'tableIK_Spells'
    id = Column("ID", Integer, primary_key=True)
    name = Column("ikSpellName", Text)
    details = Column("ikSpellDescription", Text)
    spell_cost = Column("ikSpellCost", Text)
    range = Column("ikSpellRange", Text)
    aoe = Column("ikSpellAOE", Text)
    pow = Column("ikSpellPow", Text)
    upkeep = Column("ikSpellUp", Text)
    offense = Column("ikSpellOff", Text)
