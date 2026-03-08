# ✈️ Airport Security Management & Maintenance System

## Project Overview

Airport Security Management & Maintenance System is a backend system designed to manage security screening devices across multiple airports.

The system provides a centralized API that allows technicians and operators to:
	-	Register and manage screening devices
	-	Record daily inspections
	-	Track preventive and corrective maintenance
	-	Maintain a full historical record for each device
	-	Generate operational reports

The system supports a multi-site architecture, meaning that each airport operates independently and users can only access data belonging to their assigned site.

---

## Multi-Site System Architecture

The system is designed to support multiple airports such as:
	-	King Khalid International Airport — Riyadh
	-	King Abdulaziz International Airport — Jeddah
	-	King Fahd International Airport — Dammam

Each airport is treated as a separate site within the system.

This ensures:
	-	Users are assigned to a specific airport
	-	Technicians only access devices at their own site
	-	Data from different airports remains isolated

This approach allows the system to scale easily to 20+ airports in the future.

---

## Asset Management

Each security screening device is registered as an Asset within the system.

### Device Information Stored
	-	Facility Number
	-	Serial Number
	-	Device Type
	-	Manufacturer
	-	Model
	-	Production Year
	-	Site (Airport)
	-	Location inside the airport (Terminal / Gate)
	-	Operational Status

This allows the system to maintain a complete inventory of security devices across all airports.

---

## Daily Inspection Tracking

Each device must be inspected daily.

The system records the following information for each inspection:
	-	Asset ID
	-	Inspection Date
	-	Operational Status
	-	Operating
	-	Not Ready
	-	Decommissioned
	-	Optional technician remarks

This enables the system to track the daily operational status of all devices.

---

## Maintenance Management

The system tracks maintenance activities performed on devices.

Two types of maintenance are supported.

### Preventive Maintenance

Routine maintenance such as:
	-	Cleaning devices
	-	Inspecting sensors
	-	Checking filters
	-	Performing system checks

### Corrective Maintenance

Maintenance performed to resolve faults such as:
	-	Replacing components
	-	Repairing hardware
	-	Fixing malfunctions

Each maintenance log includes:
	-	Asset ID
	-	Maintenance Type
	-	Date
	-	Description
	-	Technician responsible

This allows the system to maintain a complete maintenance history for each device.

---

## Authentication & Authorization

The system implements secure authentication using JWT (JSON Web Tokens).

### Key Security Features
	-	Secure login endpoint
	-	Password hashing using bcrypt
	-	JWT token generation
	-	Protected API endpoints

After login, users receive an access token which must be included in requests.

Example:

```
Authorization: Bearer <access_token>
```

The token ensures that users can only access data belonging to their assigned site.

---

## Reporting

The system includes endpoints that generate operational reports.

Examples include:
	-	Asset operational status summary
	-	Maintenance history for a specific device
	-	Daily inspection summaries for a site

These reports help support operational monitoring and decision making.

---

## Technologies Used

### Backend Framework
	-	FastAPI

### Programming Language
	-	Python

### Database
	-	SQLite

### ORM
	-	SQLAlchemy

### Authentication
	-	JWT (JSON Web Tokens)

### Password Security
	-	Passlib + bcrypt

### API Documentation
	-	Swagger / OpenAPI

---

## 📂 Project Structure

```
airport-system-api
│
├── app
│   ├── auth.py        # Authentication logic (JWT + password hashing)
│   ├── database.py    # Database connection and session management
│   ├── models.py      # SQLAlchemy database models
│   └── schemas.py     # Pydantic request and response schemas
│
├── main.py            # FastAPI application and API endpoints
├── requirements.txt
└── README.md
```

---

### API Endpoints

Assets

```
GET    /assets
POST   /assets
PATCH  /assets/{asset_id}
GET    /assets/{asset_id}
```

Daily Checks

```
POST /daily-checks
GET  /daily-checks
```

Maintenance

```
POST /maintenance
GET  /maintenance
```

Reports

```
GET /reports/assets-summary
GET /reports/maintenance-history
GET /reports/daily-checks-summary
```

---

## What This Project Demonstrates

This project demonstrates several backend development concepts:
	-	REST API design using FastAPI
	-	Secure authentication using JWT
	-	Password hashing and verification
	-	Relational database design using SQLAlchemy
	-	Multi-site data isolation
	-	Backend architecture organization
	-	API documentation using Swagger

---

## Running the Project

1️⃣ Clone the repository
```
git clone https://github.com/samdej01/airport-system-api.git
```

2️⃣ Navigate to the project directory
```
cd airport-system-api
```

3️⃣ Create a virtual environment
```
python -m venv venv
```

4️⃣ Activate the virtual environment

Mac / Linux:
```
source venv/bin/activate
```

5️⃣ Install dependencies
```
pip install -r requirements.txt
```

6️⃣ Run the server
```
uvicorn main:app --reload
```

7️⃣ Open the API documentation
```
http://127.0.0.1:8000/docs
```
