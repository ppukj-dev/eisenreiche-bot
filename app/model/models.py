from sqlalchemy import Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Ability(Base):
    __tablename__ = 'tableIK_Ability'
    id = Column("ID", Integer, primary_key=True)
    name = Column("ikAbilityName", Text)
    prerequisites = Column("ikAbilityPrereq", Text)
    details = Column("ikAbilityDetails", Text)


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


class Skill(Base):
    __tablename__ = 'tableIK_Skill'
    id = Column("ID", Integer, primary_key=True)
    name = Column("ikSkillName", Text)
    stats = Column("ikSkillStats", Text)
    details = Column("ikSkillDetails", Text)


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
