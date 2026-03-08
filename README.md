# ✈️ Airport Security Management & Maintenance System

## Project Overview

This project is a backend API system designed to manage security screening devices across multiple airports. The system supports a *multi-site architecture*, meaning that each airport operates independently and users can only access data belonging to their assigned site.

---

### Asset Management

Each security screening device is registered as an Asset within the system and the device's information is stored.


### Daily Inspection Tracking

The system records information for each inspection.


### Maintenance Management

The system tracks maintenance activities performed on devices, preventive maintenance and corrective maintenance.

### Reporting

The system includes endpoints that generate operational reports that support monitoring.

### Authentication & Authorization

The system implements secure authentication using JWT (JSON Web Tokens).

#### Key Security Features
- Secure login endpoint
- Password hashing using bcrypt
- JWT token generation
- Protected API endpoints
	
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

### This project demonstrates several backend development concepts
- REST API design using FastAPI
- Secure authentication using JWT
- Password hashing and verification
- Relational database design using SQLAlchemy
- Multi-site data isolation
- Backend architecture organization
- API documentation using Swagger

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
