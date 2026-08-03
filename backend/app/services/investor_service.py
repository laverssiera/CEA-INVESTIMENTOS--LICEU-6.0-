from sqlalchemy.orm import Session

from app.repositories.investor_repository import InvestorRepository
from app.repositories.user_repository import UserRepository


class InvestorService:
    def __init__(self, db: Session):
        self.db = db
        self.users = UserRepository(db)
        self.investors = InvestorRepository(db)

    def onboard_signup(self, username: str, full_name: str, email: str, password_hash: str, profile: str):
        user = self.users.create(username=username, name=full_name, email=email, password_hash=password_hash, role=profile)
        investor = self.investors.create(user_id=user.id, profile_type=profile)
        self.db.commit()
        return user, investor
