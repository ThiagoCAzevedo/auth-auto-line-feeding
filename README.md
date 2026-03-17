
# Auth Microservice

The Auth Microservice is a core component of the CIAL ecosystem, responsible for delivering secure, scalable, and centralized authentication and authorization services. It ensures that all users and internal systems interact with the platform through a consistent and robust security layer.

This service manages credential validation, token lifecycle, session control, and access enforcement across the entire CIAL architecture. By abstracting authentication concerns into a dedicated module, it enhances maintainability, security, and interoperability between distributed services.

#### Key Responsibilities
- Manage user registration and authentication flows  
- Issue and validate JWT access and refresh tokens  
- Handle password hashing and credential storage  
- Provide middleware/hooks for protecting internal services  
- Integrate with the CIAL User database  
- Support role-based and/or permission-based authorization  
- Offer secure endpoints for login, logout, token refresh, and session validation
## 🟢 API Reference 

### Get Logged User (*Access API*)

```http
    GET /access/me
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| _None_ | — | Requires authentication (Bearer Token) |

**Description:** Returns the profile information of the currently authenticated user.


### Login User (*Access API*)

```http
    POST /access/login
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| email     | string | Required. User email |
| password     | string | Required. User password |
| remember_me     | boolean | Extends refresh token expiration (30 days vs 1 day) |

**Description:** Authenticates a user and returns access + refresh tokens.


### Logout User (*Access API*)

```http
    POST /access/logout
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| _None_     | — | Requires authentication (Bearer Token) |

**Description:** Invalidates the user’s refresh token, effectively logging them out.


### Register New User (*Register API*)

```http
    POST /register
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| first_name     | string | Required. User first name |
| last_name     | string | Required. User last name |
| email     | string | Required. User email |
| password     | string | Required. User password |

**Description:** Creates a new user in "pending approval" state.

### Permanently Delete User (*Delete API*)

```http
    POST /register
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| user_id     | integer | Required. ID of the user to delete |

**Description:** Permanently deletes a user.  
**_Requires admin privileges._**


### List All Users (*List API*)

```http
    GET /list/list-all
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| page     | integer | Page number (>= 1) |
| page_size     | integer | Page size (1-100) |
| q   | string | Optional search by email or name |
| status     | boolean | Filter by status (true/false) |

**Description:** Returns paginated, searchable and filterable list of users.  
**_Requires admin privileges._**


### List All Users (*List API*)

```http
    GET /list/list/{user_id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| user_id     | integer | Required. ID of the user to fetch |

**Description:** Retrieves a single user by ID.  
**_Requires admin privileges._**


### Update User (*Update API*)

```http
    PUT /update/{user_id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| user_id     | integer | Required. ID of the user to fetch |
| body     | object | Partial or full fields to update |

**Description:** Updates user information.  
**_Requires admin privileges._**


### Health Check

```http
    GET /health
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| *None*     | — | Simple service health check |

**Description:** Verifies if the service is healthy and returns basic metadata.
## 🟢 Run Locally

Clone the project

```bash
  git clone https://github.com/ThiagoCAzevedo/auth-cial.git
```

Go to the project directory

```bash
  cd auth-cial
```

Install dependencies

```bash
  pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org 
```

Start the server

```bash
  python main.py
```

or

```bash
  python -m uvicorn main:app --reload --port <PORT TO RUN>
```

***Observation:** Use Python 3.10.0*


## 🟢 Running Tests

To run tests, run the following command

```bash
  npm run test
```


## 🟢 Authors

- [@ThiagoCAzevedo](https://www.github.com/thiagocazevedo)
- [@ThiagoCanatoAzevedo](https://www.github.com/thiagocanatoazevedo)


## 🟢 Support

For support, email nata.silva@gruposese.com or contact Sesé IT support.

