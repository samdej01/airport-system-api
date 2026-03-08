from datetime import date
from pydantic import BaseModel


class SiteCreate(BaseModel):
    name: str
    code: str


class SiteResponse(BaseModel):
    id: int
    name: str
    code: str

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: str
    password: str
    site_id: int


class UserResponse(BaseModel):
    id: int
    email: str
    site_id: int

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class AssetCreate(BaseModel):
    facility_number: str
    serial_number: str
    device_type: str
    manufacturer: str
    model: str
    production_year: int
    location: str
    operational_status: str
    site_id: int


class AssetResponse(BaseModel):
    id: int
    facility_number: str
    serial_number: str
    device_type: str
    manufacturer: str
    model: str
    production_year: int
    location: str
    operational_status: str
    site_id: int

    class Config:
        from_attributes = True


class DailyCheckCreate(BaseModel):
    asset_id: int
    site_id: int
    check_date: date
    status: str
    remarks: str | None = None


class DailyCheckResponse(BaseModel):
    id: int
    asset_id: int
    site_id: int
    check_date: date
    status: str
    remarks: str | None = None

    class Config:
        from_attributes = True


class MaintenanceCreate(BaseModel):
    asset_id: int
    site_id: int
    maintenance_type: str
    maintenance_date: date
    description: str
    technician_id: int


class MaintenanceResponse(BaseModel):
    id: int
    asset_id: int
    site_id: int
    maintenance_type: str
    maintenance_date: date
    description: str
    technician_id: int

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: str
    password: str


class AssetHistoryResponse(BaseModel):
    asset: AssetResponse
    daily_checks: list[DailyCheckResponse]
    maintenance_logs: list[MaintenanceResponse]


class AssetSummaryReport(BaseModel):
    site_id: int
    total_assets: int
    operating: int
    not_ready: int
    decommissioned: int


class MaintenanceHistoryReport(BaseModel):
    asset_id: int
    maintenance_count: int
    maintenance_logs: list[MaintenanceResponse]


class DailyCheckSummaryReport(BaseModel):
    site_id: int
    total_checks: int
    operating: int
    not_ready: int
    decommissioned: int

class AssetUpdate(BaseModel):
    operational_status: str | None = None
    location: str | None = None