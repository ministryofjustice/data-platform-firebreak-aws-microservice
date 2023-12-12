from sqlalchemy import Column, Integer, String

from app.core.databases import Base


class Permission(Base):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    # roles = relationship("Role", back_populates="permissions")


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    username = Column(String, unique=True, index=True)
    # permissions = relationship("Permission", back_populates="roles")
