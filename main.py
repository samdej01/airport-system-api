from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import models, schemas
from app.auth import create_access_token, get_current_user, hash_password, verify_password
from app.database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Security Management & Maintenance System API is running"}


# Site Endpoints

@app.post("/sites", response_model=schemas.SiteResponse, status_code=status.HTTP_201_CREATED)
def create_site(site: schemas.SiteCreate, db: Session = Depends(get_db)):
    existing_site = db.query(models.Site).filter(
        (models.Site.name == site.name) | (models.Site.code == site.code)
    ).first()

    if existing_site:
        raise HTTPException(status_code=400, detail="Site name or code already exists")

    new_site = models.Site(name=site.name, code=site.code)
    db.add(new_site)
    db.commit()
    db.refresh(new_site)
    return new_site


@app.get("/sites", response_model=list[schemas.SiteResponse])
def get_sites(db: Session = Depends(get_db)):
    sites = db.query(models.Site).all()
    return sites


# User Endpoints

@app.post("/users", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    site = db.query(models.Site).filter(models.Site.id == user.site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")

    hashed_password = hash_password(user.password)

    new_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        site_id=user.site_id
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/users", response_model=list[schemas.UserResponse])
def get_users(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    users = db.query(models.User).filter(models.User.site_id == current_user.site_id).all()
    return users


# Login Endpoint

@app.post("/login", response_model=schemas.TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token({
        "sub": user.email,
        "user_id": user.id,
        "site_id": user.site_id
    })

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# Daily Check Endpoints

@app.post("/daily-checks", response_model=schemas.DailyCheckResponse, status_code=status.HTTP_201_CREATED)
def create_daily_check(daily_check: schemas.DailyCheckCreate, db: Session = Depends(get_db)):
    site = db.query(models.Site).filter(models.Site.id == daily_check.site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")

    asset = db.query(models.Asset).filter(models.Asset.id == daily_check.asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    if asset.site_id != daily_check.site_id:
        raise HTTPException(
            status_code=400,
            detail="Asset does not belong to the provided site"
        )

    new_daily_check = models.DailyCheck(
        asset_id=daily_check.asset_id,
        site_id=daily_check.site_id,
        check_date=str(daily_check.check_date),
        status=daily_check.status,
        remarks=daily_check.remarks
    )

    db.add(new_daily_check)
    db.commit()
    db.refresh(new_daily_check)
    return new_daily_check


@app.get("/daily-checks", response_model=list[schemas.DailyCheckResponse])
def get_daily_checks(
    asset_id: int | None = Query(default=None),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(models.DailyCheck).filter(models.DailyCheck.site_id == current_user.site_id)

    if asset_id is not None:
        query = query.filter(models.DailyCheck.asset_id == asset_id)

    daily_checks = query.all()
    return daily_checks


# Maintenance Endpoints

@app.post("/maintenance", response_model=schemas.MaintenanceResponse, status_code=status.HTTP_201_CREATED)
def create_maintenance(maintenance: schemas.MaintenanceCreate, db: Session = Depends(get_db)):
    site = db.query(models.Site).filter(models.Site.id == maintenance.site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")

    asset = db.query(models.Asset).filter(models.Asset.id == maintenance.asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    technician = db.query(models.User).filter(models.User.id == maintenance.technician_id).first()
    if not technician:
        raise HTTPException(status_code=404, detail="Technician not found")

    if asset.site_id != maintenance.site_id:
        raise HTTPException(
            status_code=400,
            detail="Asset does not belong to the provided site"
        )

    if technician.site_id != maintenance.site_id:
        raise HTTPException(
            status_code=400,
            detail="Technician does not belong to the provided site"
        )

    new_maintenance = models.MaintenanceLog(
        asset_id=maintenance.asset_id,
        site_id=maintenance.site_id,
        maintenance_type=maintenance.maintenance_type,
        maintenance_date=str(maintenance.maintenance_date),
        description=maintenance.description,
        technician_id=maintenance.technician_id
    )

    db.add(new_maintenance)
    db.commit()
    db.refresh(new_maintenance)
    return new_maintenance


@app.get("/maintenance", response_model=list[schemas.MaintenanceResponse])
def get_maintenance(
    asset_id: int | None = Query(default=None),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(models.MaintenanceLog).filter(
        models.MaintenanceLog.site_id == current_user.site_id
    )

    if asset_id is not None:
        query = query.filter(models.MaintenanceLog.asset_id == asset_id)

    maintenance_logs = query.all()
    return maintenance_logs


# Asset Endpoints

@app.post("/assets", response_model=schemas.AssetResponse, status_code=status.HTTP_201_CREATED)
def create_asset(asset: schemas.AssetCreate, db: Session = Depends(get_db)):
    site = db.query(models.Site).filter(models.Site.id == asset.site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")

    existing_asset = db.query(models.Asset).filter(
        (models.Asset.facility_number == asset.facility_number) |
        (models.Asset.serial_number == asset.serial_number)
    ).first()

    if existing_asset:
        raise HTTPException(
            status_code=400,
            detail="Facility number or serial number already exists"
        )

    new_asset = models.Asset(
        facility_number=asset.facility_number,
        serial_number=asset.serial_number,
        device_type=asset.device_type,
        manufacturer=asset.manufacturer,
        model=asset.model,
        production_year=asset.production_year,
        location=asset.location,
        operational_status=asset.operational_status,
        site_id=asset.site_id
    )

    db.add(new_asset)
    db.commit()
    db.refresh(new_asset)
    return new_asset


@app.get("/assets", response_model=list[schemas.AssetResponse])
def get_assets(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    assets = db.query(models.Asset).filter(models.Asset.site_id == current_user.site_id).all()
    return assets


@app.patch("/assets/{asset_id}", response_model=schemas.AssetResponse)
def update_asset(
    asset_id: int,
    asset_update: schemas.AssetUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()

    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    if asset.site_id != current_user.site_id:
        raise HTTPException(status_code=403, detail="Not allowed to modify this asset")

    if asset_update.operational_status is not None:
        asset.operational_status = asset_update.operational_status

    if asset_update.location is not None:
        asset.location = asset_update.location

    db.commit()
    db.refresh(asset)

    return asset


# Asset History Endpoint

@app.get("/assets/{asset_id}", response_model=schemas.AssetHistoryResponse)
def get_asset_history(
    asset_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()

    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    if asset.site_id != current_user.site_id:
        raise HTTPException(status_code=403, detail="Not allowed to access this asset")

    daily_checks = (
        db.query(models.DailyCheck)
        .filter(models.DailyCheck.asset_id == asset_id)
        .all()
    )

    maintenance_logs = (
        db.query(models.MaintenanceLog)
        .filter(models.MaintenanceLog.asset_id == asset_id)
        .all()
    )

    return {
        "asset": asset,
        "daily_checks": daily_checks,
        "maintenance_logs": maintenance_logs
    }


# Reports Endpoint

# Asset Summary Endpoint

@app.get("/reports/assets-summary", response_model=schemas.AssetSummaryReport)
def get_assets_summary(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    assets = db.query(models.Asset).filter(models.Asset.site_id == current_user.site_id).all()

    total_assets = len(assets)
    operating = len([asset for asset in assets if asset.operational_status == "Operating"])
    not_ready = len([asset for asset in assets if asset.operational_status == "Not Ready"])
    decommissioned = len([asset for asset in assets if asset.operational_status == "Decommissioned"])

    return {
        "site_id": current_user.site_id,
        "total_assets": total_assets,
        "operating": operating,
        "not_ready": not_ready,
        "decommissioned": decommissioned
    }


# Maintenance History Endpoint

@app.get("/reports/maintenance-history", response_model=schemas.MaintenanceHistoryReport)
def get_maintenance_history(
    asset_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()

    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    if asset.site_id != current_user.site_id:
        raise HTTPException(status_code=403, detail="Not allowed to access this asset")

    maintenance_logs = (
        db.query(models.MaintenanceLog)
        .filter(models.MaintenanceLog.asset_id == asset_id)
        .all()
    )

    maintenance_count = len(maintenance_logs)

    return {
        "asset_id": asset_id,
        "maintenance_count": maintenance_count,
        "maintenance_logs": maintenance_logs
    }


# Daily Check Summary Endpoint

@app.get("/reports/daily-checks-summary", response_model=schemas.DailyCheckSummaryReport)
def get_daily_checks_summary(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    daily_checks = (
        db.query(models.DailyCheck)
        .filter(models.DailyCheck.site_id == current_user.site_id)
        .all()
    )

    total_checks = len(daily_checks)
    operating = len([check for check in daily_checks if check.status == "Operating"])
    not_ready = len([check for check in daily_checks if check.status == "Not Ready"])
    decommissioned = len([check for check in daily_checks if check.status == "Decommissioned"])

    return {
        "site_id": current_user.site_id,
        "total_checks": total_checks,
        "operating": operating,
        "not_ready": not_ready,
        "decommissioned": decommissioned
    }