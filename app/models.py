from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Site(Base):
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    code = Column(String, unique=True, nullable=False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    site_id = Column(Integer, ForeignKey("sites.id"), nullable=False)

    site = relationship("Site")


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    facility_number = Column(String, unique=True, nullable=False)
    serial_number = Column(String, unique=True, nullable=False)
    device_type = Column(String, nullable=False)
    manufacturer = Column(String, nullable=False)
    model = Column(String, nullable=False)
    production_year = Column(Integer, nullable=False)
    location = Column(String, nullable=False)
    operational_status = Column(String, nullable=False)
    site_id = Column(Integer, ForeignKey("sites.id"), nullable=False)

    site = relationship("Site")


class DailyCheck(Base):
    __tablename__ = "daily_checks"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    site_id = Column(Integer, ForeignKey("sites.id"), nullable=False)
    check_date = Column(String, nullable=False)
    status = Column(String, nullable=False)
    remarks = Column(String, nullable=True)

    asset = relationship("Asset")
    site = relationship("Site")


class MaintenanceLog(Base):
    __tablename__ = "maintenance_logs"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    site_id = Column(Integer, ForeignKey("sites.id"), nullable=False)
    maintenance_type = Column(String, nullable=False)
    maintenance_date = Column(String, nullable=False)
    description = Column(String, nullable=False)
    technician_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    asset = relationship("Asset")
    site = relationship("Site")
    technician = relationship("User")