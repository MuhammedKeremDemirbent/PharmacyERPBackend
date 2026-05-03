# 🏥 Pharmacy ERP (Enterprise Resource Planning) - Backend

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Django REST](https://img.shields.io/badge/Django_REST-ff1709?style=for-the-badge&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=celery&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

A high-performance, enterprise-grade backend project specifically developed for pharmacies. It provides a centralized system to manage inventory tracking, patient records, sales operations, and procurement processes.

## 🚀 Key Features

- **Modular Architecture:** The project is divided into 5 main modules (`accounts`, `inventory`, `sales`, `patients`, `procurement`) to enhance maintainability and code readability.
- **Asynchronous Task Processing:** Heavy operations such as generating PDF receipts and sending emails are offloaded to background tasks using **Celery** and **Redis** to prevent slowing down the user experience.
- **Scheduled Tasks (CRON Jobs):** Powered by **Celery Beat**, periodic tasks like sending daily/weekly reports, low-stock alert emails, and managing campaigns are fully automated.
- **Idempotency (Duplicate Request Protection):** Critical operations like sales (checkout) and email dispatching are protected by an idempotency layer. This prevents the same request from being accidentally processed twice (e.g., deducting stock twice or sending duplicate emails) in case of network failures or double-clicks.
- **Secure Authentication:** User login and authorization flows are secured using **JWT (JSON Web Tokens)**. Password reset and verification flows also utilize secure token mechanisms.
- **Advanced Reporting:** Integrates `reportlab` and `Pillow` libraries to dynamically generate receipts and invoices in PDF format on the fly.

## 🛠️ Technology Stack

- **Programming Language:** Python
- **Web Framework:** Django & Django REST Framework (DRF)
- **Database:** PostgreSQL
- **Cache & Message Broker:** Redis
- **Task Queue:** Celery & Celery Beat
- **Email Testing Environment:** Mailpit
- **Containerization:** Docker & Docker Compose
- **Reverse Proxy:** Nginx

---

## 🐳 Installation & Setup (via Docker)

The project is fully **Dockerized** to eliminate dependency issues and ensure stable execution across different operating systems. You do not need to install Python or a database locally.

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) and **Docker Compose** must be installed and running on your machine.

### 1. Clone the Repository
```bash
git clone https://github.com/MuhammedKeremDemirbent/PharmacyERPBackend.git
cd PharmacyERPBackend
```

### 2. Configure Environment Variables
Create a `.env` file in the root directory by copying the provided `.env.template`:

**Windows PowerShell:**
```powershell
Copy-Item .env.template -Destination .env
```
**Linux / Mac / Git Bash:**
```bash
cp .env.template .env
```

Open the newly created `.env` file and fill in the necessary variables. The default values are generally sufficient for local testing, but you can update the `SECRET_KEY`, JWT settings, and email configurations as needed.

### 3. Build and Start the Containers
The following command builds and starts the PostgreSQL database, Redis, Django backend, Celery worker/beat, PgAdmin, and Nginx simultaneously in detached mode:
```bash
docker-compose up -d --build
```

### 4. Setup the Database and Create an Admin Account
Once the containers are successfully running, execute the migrate command to create the database tables:
```bash
docker-compose exec backend python manage.py migrate
```
To access the Django Admin panel, create a superuser account:
```bash
docker-compose exec backend python manage.py createsuperuser
```
*(You will be prompted to set a username, email, and password. For security reasons, the password characters will not be displayed as you type; just type it and press Enter.)*

### 5. Accessing the Services
Once the entire system is up and running, you can access the various platforms at the following URLs:

- **Main API Endpoints (Backend):** `http://localhost:8000/` (or `http://localhost/` if routed via Nginx)
- **Django Admin Panel:** `http://localhost:8000/admin`
- **Mailpit (View Sent Test Emails):** `http://localhost:8025`
- **PgAdmin (Database Management UI):** `http://localhost:8080` *(Login credentials are the `PGADMIN_EMAIL` and `PGADMIN_PASSWORD` from your `.env` file)*

---

## 💻 Frequently Used Docker Commands

Essential commands for development and testing:

**Stop and Shut Down the System:**
```bash
docker-compose down
```
> [!WARNING]  
> If you want to **completely wipe** all data stored in the database, append the `-v` flag (`docker-compose down -v`). Proceed with caution!

**Live Tailing of Logs:**
```bash
# To view only the Django API (backend) logs:
docker-compose logs -f backend

# To check for errors in background tasks (Celery):
docker-compose logs -f celery_worker
```

**Run Commands Inside the Container (Tests, Shell, etc.):**
```bash
docker-compose exec backend python manage.py test
docker-compose exec backend python manage.py shell
```
