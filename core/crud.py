from sqlalchemy.orm import Session

from core import schemas, models
from core import models


def get_role(db: Session, role_id: int):
    return db.query(models.Role).filter(models.Role.id == role_id).first()


def create_role(db: Session, role: schemas.Role):
    db_role = models.Role(name=role.name)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


def get_permission(db: Session, permission_id: int):
    return db.query(models.Permission).filter(models.Permission.id == permission_id).first()


def create_permission(db: Session, permission: schemas.Permission):
    db_permission = models.Permission(name=permission.name)
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission
