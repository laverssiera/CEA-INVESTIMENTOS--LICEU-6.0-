from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Project


class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_projects(self) -> list[Project]:
        return list(self.db.scalars(select(Project).order_by(Project.id)).all())
