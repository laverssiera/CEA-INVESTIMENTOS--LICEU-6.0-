from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from backend.app.db.base import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)

# Tabela associativa para membros de comitê
committee_members = Table(
    'committee_members',
    Base.metadata,
    Column('committee_id', Integer, ForeignKey('governance_committees.id')),
    Column('user_id', String) # ID do usuário no ecossistema
)

class GovernanceCommittee(Base):
    __tablename__ = "governance_committees"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String) # 'CREDITO', 'RISCO', 'ESG', 'INVESTIMENTOS'
    description = Column(String)
    min_quorum = Column(Integer, default=3)
    created_at = Column(DateTime, default=utc_now)

class GovernanceProposal(Base):
    __tablename__ = "governance_proposals"
    
    id = Column(Integer, primary_key=True, index=True)
    committee_id = Column(Integer, ForeignKey("governance_committees.id"))
    title = Column(String)
    description = Column(String)
    proposal_data = Column(JSON) # Ex: { "type": "credit_approval", "amount": 5000000 }
    status = Column(String, default="pending") # 'pending', 'approved', 'rejected', 'executed'
    created_at = Column(DateTime, default=utc_now)
    expires_at = Column(DateTime)

class GovernanceVote(Base):
    __tablename__ = "governance_votes"
    
    id = Column(Integer, primary_key=True, index=True)
    proposal_id = Column(Integer, ForeignKey("governance_proposals.id"))
    user_id = Column(String)
    vote = Column(String) # 'yes', 'no', 'abstain'
    justification = Column(String, nullable=True)
    timestamp = Column(DateTime, default=utc_now)
