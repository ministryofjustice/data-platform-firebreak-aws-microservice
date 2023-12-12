from sqlalchemy.orm import Session

from app.core import models, schemas


def get_roles(db: Session):
    return db.query(models.Role).all()


def get_role(db: Session, role_username: str):
    return db.query(models.Role).filter(models.Role.username == role_username).first()


def create_role(db: Session, role: schemas.RoleCreate):
    db_role = models.Role(**role.dict())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


def get_permission(db: Session, permission_id: int):
    return db.query(models.Permission).filter(models.Permission.id == permission_id).first()


def create_permission(db: Session, permission: schemas.PermissionCreate):
    db_permission = models.Permission(name=permission.name)
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission
