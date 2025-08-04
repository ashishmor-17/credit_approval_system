<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
## Table of Contents

- [For Mac/Linux: source venv/bin/activate](#for-maclinux-source-venvbinactivate)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

Credit Approval System
This project presents a robust and scalable Django-based Credit Approval System, designed to efficiently manage customer credit and loan data. It leverages a modern tech stack to ensure high performance, reliability, and ease of deployment, making it ideal for financial institutions needing a streamlined credit assessment process.

🚀 Key Features
Customer & Loan Data Ingestion: Seamlessly import customer and loan information from CSV files.

RESTful APIs: Comprehensive APIs for managing customer profiles and loan applications.

Asynchronous Processing: Utilizes Celery workers for background tasks, ensuring the main application remains responsive during heavy data processing.

Reliable Data Storage: Powered by PostgreSQL for secure and scalable relational data management.

Efficient Messaging: Employs Redis as a high-performance message broker for Celery.

Containerized Deployment: Fully Dockerized for consistent and straightforward deployment across various environments.

📦 Technologies Under the Hood
Python 3.11: The core programming language.

Django 4.2+: High-level Python web framework for rapid development.

Django REST Framework: Toolkit for building powerful Web APIs.

Celery: Distributed task queue for asynchronous operations.

Redis: In-memory data structure store, used as Celery's message broker.

PostgreSQL: Open-source relational database system.

Docker & Docker Compose: For containerization and orchestration.

Pytest: A flexible and scalable testing framework.

🧪 Running Locally
To get the Credit Approval System up and running on your local machine, follow these steps:

Prerequisites
Setup Steps
Clone the Repository:

git clone https://github.com/ashishmor-17/credit_approval_system.git
cd credit-system

Set up Python Environment:

python -m venv venv
source venv/bin/activate  # On Windows
# For Mac/Linux: source venv/bin/activate
pip install -r requirements.txt

Run Migrations:

python manage.py migrate

Start Services with Docker Compose:
This will build and start the Django application, Celery workers, Redis, and PostgreSQL containers.

docker-compose up --build

Wait for all services to be healthy before proceeding.

Ingest Sample Data:
This command processes sample CSV files to populate the database with initial customer and loan data.

python manage.py ingest_data

Access the Application:
Once all services are running, you can access the Django development server (if not using Docker for the Django app directly) or the Dockerized application.

👨‍💻 Author
Ashish Mor
GitHub: @ashishmor-17

📝 License
This project is open-source and available under the MIT License.
