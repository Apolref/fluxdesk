# FluxDesk - Help Desk Management System

**FluxDesk** is a modern and robust REST API designed for technical support automation. Built with a focus on scalability, security, and granular access control (RBAC), it simulates a real-world enterprise environment for managing support tickets.

This project followed industry best practices, implementing optimized database queries and containerized infrastructure, similar to those used by major tech companies like **Nelogica** and **Inter**.

---

## Tech Stack

* **Language:** Python 3.13+
* **Framework:** FastAPI (High performance, asynchronous support, and auto-documentation)
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy
* **Containerization:** Docker & Docker Compose
* **Migrations:** Alembic
* **Testing:** Pytest (Integration and Unit testing)
* **Security:** OAuth2 + JWT (JSON Web Tokens) & Secure password hashing with Passlib (bcrypt)

---

## Key Features

### Security & Access Control
* **RBAC (Role-Based Access Control):** Granular permissions for customer, technician, and admin roles.
* **Secure Sessions:** JWT-based authentication with configurable expiration.
* **Data Integrity:** Strict validation using Pydantic schemas.

### 🎫 Ticket Lifecycle Management
* **Automated Workflow:** Creation, technician assignment, and status transitions (Open -> In Progress -> Closed).
* **Internal Chat:** Real-time commenting system within each ticket for efficient communication.
* **Audit Logs:** Automated tracking of status changes and ownership in the ticket history.
* **Advanced Filters:** Search and list tickets by status, priority, or ownership using optimized Query Parameters.

### Intelligence & Metrics
* **Dashboard Analytics:** High-performance SQL aggregation providing real-time statistics (total tickets, workload per status, resolution rates).

---

## How to Run

### Option 1: Using Docker (Recommended)
No local installation of Python or PostgreSQL is required.

1. Clone the repository:
   git clone https://github.com/Apolref/fluxdesk.git
2. Navigate to the folder:
   cd fluxdesk
3. Spin up the entire infrastructure:
   docker-compose up --build

The API will be live at http://localhost:8000.

### Option 2: Local Setup
1. Prepare environment:
   python -m venv venv
   source venv/bin/activate (Linux/Mac) or .\venv\Scripts\activate (Windows)
   pip install -r requirements.txt
2. Run migrations and start server:
   alembic upgrade head
   uvicorn app.main:app --reload

---

## Testing

The project includes a comprehensive automated test suite to ensure system stability and security constraints.

Run the test suite:
pytest

*Current coverage: User registration, Login flows, Ticket lifecycle, Dashboard metrics, and RBAC security logic.*

---

## API Documentation

Once the server is running, you can explore the endpoints through the interactive documentation:
* Swagger UI: http://localhost:8000/docs
* ReDoc: http://localhost:8000/redoc

---

## Author

**Alexandre** - Final-year Computer Engineering Student at **USP (University of São Paulo - São Carlos)**.

[GitHub](https://github.com/Apolref) | [LinkedIn](https://www.linkedin.com/in/alelopfer/)