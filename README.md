<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
## Table of Contents

- [Credit Approval System](#credit-approval-system)
  - [Overview](#overview)
  - [Features](#features)
  - [Setup and Initialization](#setup-and-initialization)
    - [Requirements](#requirements)
    - [Installation](#installation)
  - [Data Ingestion](#data-ingestion)
  - [API Endpoints](#api-endpoints)
    - [1. Register Customer](#1-register-customer)
    - [2. Check Eligibility](#2-check-eligibility)
    - [3. Create Loan](#3-create-loan)
    - [4. View Loan Details](#4-view-loan-details)
    - [5. View Loans by Customer](#5-view-loans-by-customer)
  - [General Guidelines](#general-guidelines)
  - [License](#license)
<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Credit Approval System

## Overview

The Credit Approval System is a backend application built using Django and Django Rest Framework. It is designed to manage customer data and loan processing based on historical data and future transactions. The system assesses loan eligibility and manages loan approvals based on customer credit scores derived from their loan history.

## Features

- Register new customers with an approved credit limit based on their monthly salary.
- Check loan eligibility based on customer credit scores calculated from historical loan data.
- Process new loans and provide details about approved loans.
- View customer and loan details through API endpoints.

## Setup and Initialization

### Requirements

- Python 3.11 or higher  
- Django 4.2+  
- Django Rest Framework  
- PostgreSQL  
- Docker  

### Installation

```{=html}
<!-- START doctoc generated TOC please keep comment here to allow auto update -->
```
```{=html}
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
```
## Table of Contents

-   [Credit Approval System](#credit-approval-system)
    -   [Overview](#overview)
    -   [Features](#features)
    -   [Setup and Initialization](#setup-and-initialization)
        -   [Requirements](#requirements)
        -   [Installation](#installation)
    -   [Data Ingestion](#data-ingestion)
    -   [API Endpoints](#api-endpoints)
        -   [1. Register Customer](#1-register-customer)
        -   [2. Check Eligibility](#2-check-eligibility)
        -   [3. Create Loan](#3-create-loan)
        -   [4. View Loan Details](#4-view-loan-details)
        -   [5. View Loans by Customer](#5-view-loans-by-customer)
    -   [General Guidelines](#general-guidelines)
    -   [License](#license)
        `<!-- END doctoc generated TOC please keep comment here to allow auto update -->`{=html}

# Credit Approval System

## Overview

The Credit Approval System is a backend application built using Django
and Django Rest Framework. It is designed to manage customer data and
loan processing based on historical data and future transactions. The
system assesses loan eligibility and manages loan approvals based on
customer credit scores derived from their loan history.

## Features

-   Register new customers with an approved credit limit based on their
    monthly salary.
-   Check loan eligibility based on customer credit scores calculated
    from historical loan data.
-   Process new loans and provide details about approved loans.
-   View customer and loan details through API endpoints.

## Setup and Initialization

### Requirements

-   Python 3.11 or higher\
-   Django 4.2+\
-   Django Rest Framework\
-   PostgreSQL\
-   Docker

### Installation

1.  **Clone the repository:**

\`\`\`bash git clone https://github.com/ashishmor-17/credit-system cd
credit-system

Build and run the Docker containers: docker-compose up --build

Data Ingestion The application requires initial data to be ingested from
the provided Excel files inside the data/ folder:

data/customer_data.xlsx: Contains existing customer data.

data/loan_data.xlsx: Contains historical loan data.

These files are processed using background Celery tasks once the app
starts.

API Endpoints 1. Register Customer Endpoint: /register

Method: POST

Request Body:

json Copy Edit { "first_name": "John", "last_name": "Doe", "age": 30,
"monthly_income": 60000, "phone_number": 9876543210 } Response:

json Copy Edit { "customer_id": 1, "approved_limit": 240000 } 2. Check
Eligibility Endpoint: /check-eligibility

Method: POST

Request Body:

json Copy Edit { "customer_id": 1, "loan_amount": 50000,
"interest_rate": 10.5, "tenure": 12 } Response:

json Copy Edit { "customer_id": 1, "loan_approved": true,
"interest_rate": 10.5, "tenure": 12, "monthly_installment": 4395.79 } 3.
Create Loan Endpoint: /create-loan

Method: POST

Request Body:

json Copy Edit { "customer_id": 1, "loan_amount": 50000,
"interest_rate": 10.5, "tenure": 12 } Response:

json Copy Edit { "loan_id": 101, "loan_approved": true,
"monthly_installment": 4395.79, "tenure": 12 } 4. View Loan Details
Endpoint: /view-loan/`<loan_id>`{=html}

Method: GET

Response:

json Copy Edit { "loan_id": 101, "customer": { "id": 1, "first_name":
"John", "last_name": "Doe" }, "loan_amount": 50000, "tenure": 12,
"interest_rate": 10.5, "monthly_installment": 4395.79, "start_date":
"2025-08-01", "end_date": "2026-08-01" } 5. View Loans by Customer
Endpoint: /view-loans/`<customer_id>`{=html}

Method: GET

Response:

json Copy Edit \[ { "loan_id": 101, "loan_amount": 50000, "tenure": 12,
"interest_rate": 10.5, "monthly_installment": 4395.79 }, ...\] General
Guidelines Ensure code quality and modularity. Unit tests are
encouraged. The app is fully dockerized and can be run with a single
command. Use background workers (Celery + Redis) for ingesting large
Excel datasets asynchronously.
