import uuid
from datetime import datetime, timezone
from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
def uid(): return uuid.uuid4()
def now(): return datetime.now(timezone.utc)
class Tenant(Base):
    __tablename__="tenants"
    id: Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uid)
    name: Mapped[str]=mapped_column(String(160),nullable=False)
    code: Mapped[str]=mapped_column(String(60),unique=True,index=True,nullable=False)
    status: Mapped[str]=mapped_column(String(30),default="ACTIVE",nullable=False)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now,nullable=False)
class Campus(Base):
    __tablename__="campuses"; __table_args__=(UniqueConstraint("tenant_id","code"),)
    id: Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uid)
    tenant_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("tenants.id"),index=True,nullable=False)
    name: Mapped[str]=mapped_column(String(160),nullable=False)
    code: Mapped[str]=mapped_column(String(60),nullable=False)
    status: Mapped[str]=mapped_column(String(30),default="ACTIVE",nullable=False)
class User(Base):
    __tablename__="users"; __table_args__=(UniqueConstraint("tenant_id","email"),)
    id: Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uid)
    tenant_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("tenants.id"),index=True,nullable=False)
    email: Mapped[str]=mapped_column(String(320),index=True,nullable=False)
    password_hash: Mapped[str]=mapped_column(Text,nullable=False)
    is_active: Mapped[bool]=mapped_column(Boolean,default=True,nullable=False)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now,nullable=False)
class Role(Base):
    __tablename__="roles"; __table_args__=(UniqueConstraint("tenant_id","code"),)
    id: Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uid)
    tenant_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("tenants.id"),index=True,nullable=False)
    code: Mapped[str]=mapped_column(String(80),nullable=False)
    name: Mapped[str]=mapped_column(String(120),nullable=False)
class Permission(Base):
    __tablename__="permissions"
    id: Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uid)
    code: Mapped[str]=mapped_column(String(160),unique=True,index=True,nullable=False)
class UserRole(Base):
    __tablename__="user_roles"; __table_args__=(UniqueConstraint("tenant_id","user_id","role_id"),)
    id: Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uid)
    tenant_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("tenants.id"),index=True,nullable=False)
    user_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("users.id"),index=True,nullable=False)
    role_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("roles.id"),index=True,nullable=False)
    scope_type: Mapped[str]=mapped_column(String(40),default="TENANT",nullable=False)
    scope_id: Mapped[str|None]=mapped_column(String(80),nullable=True)
class RolePermission(Base):
    __tablename__="role_permissions"; __table_args__=(UniqueConstraint("role_id","permission_id"),)
    id: Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uid)
    role_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("roles.id"),index=True,nullable=False)
    permission_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("permissions.id"),index=True,nullable=False)
class AuditEvent(Base):
    __tablename__="audit_events"
    id: Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uid)
    tenant_id: Mapped[uuid.UUID|None]=mapped_column(UUID(as_uuid=True),index=True,nullable=True)
    user_id: Mapped[uuid.UUID|None]=mapped_column(UUID(as_uuid=True),index=True,nullable=True)
    action: Mapped[str]=mapped_column(String(160),index=True,nullable=False)
    resource_type: Mapped[str]=mapped_column(String(100),nullable=False)
    resource_id: Mapped[str|None]=mapped_column(String(100),nullable=True)
    request_id: Mapped[str|None]=mapped_column(String(80),index=True,nullable=True)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now,nullable=False)
