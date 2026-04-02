# Gas Asset Management System (Backend)
This repository contains the backend service for the __Gas Asset Management System__ (GAMS), developed using __FastAPI__ and __PostgreSQL__.

The frontend application for this project is located in a separate repository: [click](https://github.com/OleksandrPro/gas-control-frontend)

## About the Project

GAMS is an internal corporate system designed for tracking and managing gas pipeline infrastructure, built to replace massive legacy Excel spreadsheets. The backend provides a reliable, normalized database architecture and an API for complex data processing and filtering.

## Core Features

* __Inventory Cards__: Full lifecycle management (create, read, update, delete) for gas infrastructure inventory cards.

* __Equipment__: Detailed tracking of equipment (pipes, valves, etc.) linked to the cards, with support for data separation across "Balance", "Fact", and "In Cut" contexts.

* __Dictionaries__: Management of system-wide reference data (pipe materials, pressure types, ownership types, districts, etc.) to ensure data purity and integrity.

* __Advanced Filtering__: A flexible search system that allows infrastructure filtering by both general card parameters and specific nested equipment characteristics.

* __Dynamic Calculations__: Automated, real-time computation of total pipe lengths and other aggregated metrics based on applied filters.

## Development Setup

### 1. Create .env


Add the following variables to a `.env` file in your project root:

```
# Database Credentials
DB_HOST="localhost"
DB_USER="user"
DB_PASSWORD="password"
DB_PORT="5401"
DB_NAME="gas_control_database"
```

### 2. Build and Run the Application


Use Docker Compose to build the backend image (installing all Python dependencies) and start the services:

```
docker compose up --build
```
(The `--build` flag ensures that Docker installs any new dependencies specified in the requirements file before starting).

### 3. Run app
```
docker compose up
```

## Tests
To run the automated test suite within the running Docker container, use the following command:

```
docker compose exec -w /app gas-control-api pytest -v
```

## Roadmap

The roadmap is regularly updated based on emerging business requirements to ensure GAMS remains a cutting-edge asset management tool.

### Phase 1: Core MVP (Completed)

 - [x] Inventory Cards: Full CRUD operations.

 - [x] Equipment Management: Tracking pipes, valves, etc., with complex column separation (Balance / Fact / Cut).

 - [x] Dictionaries: Centralized management for reference data (materials, districts, pressures).

 - [x] Pagination: Optimized data fetching for large datasets.

 - [x] Advanced Filtering: Querying by high-level card attributes.

 - [x] Deep Filtering: Querying by nested equipment parameters (e.g., pipe diameters, materials).

 - [x] Equipment Migration Logic: Data migration when changing a card's "Cut Type".

### Phase 2: Data & Security (Upcoming)

 - [] Legacy Data Import: Automated pipeline to populate the database directly from historical Excel spreadsheets (50k+ rows).

 - [] Authentication & Authorization: Secure login system.

 - [] Role-Based Access Control (RBAC): Differentiating permissions between Administrators, Editors, and Viewers.

### Phase 3: Analytics & Reporting (Planned)

 - [] Data Export: Generating downloadable Excel/CSV reports based on active filters.

 - [] Audit Logging: Tracking the history of changes (who modified which card and when).

 - [] Analytics Dashboard: Visualizing aggregate infrastructure metrics (charts and graphs).