<!-- START doctoc generated TOC please keep comment here to allow auto update -->

<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

Table of Contents
Credit Approval System

Overview

Features

Setup and Initialization

Requirements

Installation

Data Ingestion

API Endpoints

1. Register Customer

2. Check Eligibility

3. Create Loan

4. View Loan Details

5. View Loans by Customer

General Guidelines

License

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

Credit Approval System
Overview
The Credit Approval System is a backend application built using Django and Django Rest Framework. It is designed to manage customer data and loan processing based on historical data and future transactions. The system assesses loan eligibility and manages loan approvals based on customer credit scores derived from their loan history.

Features
Register new customers with an approved credit limit based on their monthly salary.

Check loan eligibility based on customer credit scores calculated from historical loan data.

Process new loans and provide details about approved loans.

View customer and loan details through API endpoints.

Setup and Initialization
Requirements
Python 3.11 or higher

Django 4.2+

Django Rest Framework

PostgreSQL

Docker

Installation
Clone the repository:

git clone https://github.com/ashishmor-17/credit_approval_system.git
cd credit_approval_system

Build and run the Docker containers:

docker-compose up --build

Access the application at http://localhost:8000.

Data Ingestion
The application requires initial data to be ingested from the provided Excel files:

customer_data.xlsx: Contains existing customer data.

loan_data.xlsx: Contains historical loan data.

Background tasks will handle the ingestion of this data into the PostgreSQL database.

API Endpoints
1. Register Customer
Endpoint: /register

Method: POST

Request Body:

first_name: First Name of customer (string)

last_name: Last Name of customer (string)

age: Age of customer (int)

monthly_income: Monthly income of individual (int)

phone_number: Phone number (int)

Response: Customer details including customer_id and approved_limit.

2. Check Eligibility
Endpoint: /check-eligibility

Method: POST

Request Body:

customer_id: Id of customer (int)

loan_amount: Requested loan amount (float)

interest_rate: Interest rate on loan (float)

tenure: Tenure of loan (int)

Response: Loan approval status and corrected interest rate if applicable.

3. Create Loan
Endpoint: /create-loan

Method: POST

Request Body:

customer_id: Id of customer (int)

loan_amount: Requested loan amount (float)

interest_rate: Interest rate on loan (float)

tenure: Tenure of loan (int)

Response: Loan approval status and details.

4. View Loan Details
Endpoint: /view-loan/<loan_id>

Method: GET

Response: Details of the specified loan and associated customer information.

5. View Loans by Customer
Endpoint: /view-loans/<customer_id>

Method: GET

Response: List of all loans associated with the specified customer.

General Guidelines
Ensure code quality and organization.

Unit tests are encouraged for bonus points.

The application should be fully dockerized and run from a single command.

License
This project is licensed under the MIT License.