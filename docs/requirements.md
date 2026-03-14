# Requirements documentation
This documentation lists and describes all dependencies used by this microservice, explaining their purpose, functionality, and the impact in case of failure.

-----

## 1. Runtime dependencies
### **FastAPI & HTTP**

#### `fastapi==0.128.0`
Main framework used to build the API.  
**Impact:** critical.

#### `uvicorn==0.40.0`
ASGI server required to run FastAPI applications.  
**Impact:** critical.

#### `httpx==0.27.2`
Asynchronous HTTP client used to communicate with external services.  
**Impact:** mid.

-----

### **Validation, security and authentication**
#### `pydantic==2.12.5`
Structured data validation (for API schemas).  
**Impact:** critical.

#### `pydantic_core==2.41.5`
Internal Pydantic engine responsible for efficient parsing.  
**Impact:** critical.

#### `pydantic-settings==2.13.1`
Typed management of environment variables.  
**Impact:** high.

#### `typing_extensions==4.15.0`
Typing extensions required by Pydantic and FastAPI.  
**Impact:** low.

#### `typing-inspection==0.4.2`
Utility for advanced type inspection.  
**Impact:** low.

#### `email-validator==2.3.0`
Robust email validation.  
**Impact:** low.

#### `PyJWT==2.11.0`
Generate and validate JWT tokens.  
**Impact:** high.

#### `passlib==1.7.4`
Library used for secure password hashing.  
**Impact:** high.

#### `argon2-cffi==25.1.0`
Secure Argon2 hashing algorithm.  
**Impact:** high.

#### `argon2-cffi-bindings==25.1.0`
Bindings required for Argon2 to work.  
**Impact:** high.

-----

### **Database and ORM**
#### `SQLAlchemy==2.0.46`
Main ORM used to model and interact with the database.  
**Impact:** critical.

#### `SQLAlchemy-Utils==0.42.1`
Additional utilities for SQLAlchemy.  
**Impact:** mid.

#### `mysql-connector-python==9.6.0`
Native MySQL driver.  
**Impact:** critical.

#### `alembic==1.18.3`
Database migration tool (migrations).  
**Impact:** high.

-----

### **Configuration and Environment**
#### `python-dotenv==1.2.1`
Loads environment variables defined in the `.env` file.  
**Impact:** mid.

#### `python-dateutil==2.9.0.post0`
Advanced operations with dates and timezones.  
**Impact:** mid.

#### `async-timeout==4.0.3`
Configurable timeout for asynchronous operations.  
**Impact:** mid.

-----

### **Utilities**
#### `propcache==0.4.1`
Cache for computed properties, improving performance.  
**Impact:** low.

-----

## 2. Test dependencies
#### `pytest==8.3.3`
Main testing framework.  
**Impact:** high.asyncpg

#### `pytest-asyncio==0.24.0`
Support for asynchronous tests using asyncio.  
**Impact:** high.

#### `pytest-cov==5.0.0`
Measures test coverage.  
**Impact:** mid.

#### `faker==26.0.0`
Generates fake data for testing scenarios.  
**Impact:** low.

-----

## 3. How to install dependencies
pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org --cert false