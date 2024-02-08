# TODO APP
Develop a Secure Flask API with SQLAlchemy, JWT Authentication, and CRUD Operations

Objective:
Create a Flask API that utilizes SQLAlchemy for database operations, implements JWT authentication for user management, provides CRUD endpoints for users and todos, ensures endpoint protection, and runs the API with HTTPS using TLS encryption.

### Steps:

**Setup Environment:**
- [x] Set up a virtual environment for the project.
- [x] Install Flask, SQLAlchemy, Flask-JWT-Extended, and other necessary dependencies.

**Define Models with SQLAlchemy:**
- [x] Create SQLAlchemy models for User and Todo entities.
- [x] Define relationships between User and Todo models if necessary.

**Implement User Authentication with JWT:**
- [x] Create routes for user registration, login, and user profile retrieval.
- [x] Implement JWT token generation upon successful login.
- [x] Hash user passwords securely before storing them in the database.

**User CRUD Operations:**
- [x] Create endpoints for creating, reading, updating, and deleting users.
- [x] Ensure that only authenticated users can access these endpoints.
- [] Implement authorization checks to allow only users to modify their own information.

**Implement Todo CRUD Operations:**
- [x] Create endpoints for creating, reading, updating, and deleting todos.
- [x] Ensure that only authenticated users can access these endpoints.
- [] Implement authorization checks to allow only users to modify their own todos.

**Protect Endpoints:**
- [] Implement middleware or decorators to protect endpoints from unauthorized access.
- [x] Use JWT tokens to authenticate and authorize users accessing protected endpoints. 

**Run Flask API with HTTPS using TLS:**
- [x] Obtain an SSL certificate for your domain or use a self-signed certificate for testing purposes.
- [x] Configure Flask to run with HTTPS using TLS encryption.
- [x] Ensure that the API runs securely over HTTPS protocol.
- [x] Utilize openssl or devcerts or any tool to generate a certificate.
