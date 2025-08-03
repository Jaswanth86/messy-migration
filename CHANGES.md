Major Issues Identified:

SQL Injection (fixed by parameterized queries)

Plaintext Passwords (now using a password hash)

No Input Validation (added for all endpoints)

No JSON Responses (now all responses are JSON and use proper status codes)

Bad HTTP Status Codes (now correct eg. 400, 401, 404, 409, 201)

No Error Handling (now handled with try/catch and if/else on DB operations)

Global, Unscoped DB Connection (now each request opens/closes its own connection)

Poor Code Structure (now modularized with easily separable code)

No Documentation (now code, params, expectations are clear)

No Password Security (now basic PBKDF2 hashing in place)

No Unique Email Enforcement (now email is unique in DB schema and handled at creation)

No Security in Login (now compares hashed passwords, not directly)
___________________________________________________________________________________________________________________________________________________
___________________________________________________________________________________________________________________________________________________
Changes Made : 

All SQL statements are parameterized; no string interpolation with user data.

Passwords are never stored or compared in plaintext.

All endpoints validate input and return meaningful errors.

Response format is always JSON; errors return non-200 codes.

No global DB connection — each handler opens/closes its own.

App can be configured via environment variable for DB path.

Structured functions for hashing/verifying passwords.

Email field is unique in database and checked on registration.

DB initialization function seeds data properly if needed.

Logging reduced/removed for security.
___________________________________________________________________________________________________________________________________________________
___________________________________________________________________________________________________________________________________________________

Assumptions & Trade-offs:

Password hashing uses a static salt for demo; use bcrypt or argon2 in production.

The app does not introduce session controls, advanced authentication, or external logging.

No third-party dependencies (besides Flask) to keep setup simple.

Still runs as a Flask app, for maximal compatibility with initial setup/script.
________________________________________________________________________________________________________________________________________________
______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
If more time were available:

Use SQLAlchemy ORM, and separate routes/models/schemas.

Add authentication via JWT or Flask-Login.

Use better password hashing (bcrypt), and support password resets.

Add environment-based configuration.

Input validation with Marshmallow or Pydantic.

Add logging and monitoring.

Add tests (see simple samples below).
________________________________________________________________________________________________________________________________________________
______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

AI Assistance:

Used ChatGPT as a coding assistant to:

Help design the overall architecture of the URL shortener.

Generate initial code templates for endpoint implementations.

Write utility functions for URL validation and short code generation.

Draft unit tests covering core API flows and error cases.

All AI-generated code was carefully reviewed, modified, and integrated to fit project requirements and personal coding style.

No code was blindly accepted; all logic and structure decisions were validated independently.
