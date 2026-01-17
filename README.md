# gas-control-backend
Backend of Gas Asset Management System

Create .env

```
# Database Credentials
DB_HOST="localhost"
DB_USER="user"
DB_PASSWORD="password"
DB_PORT="5401"
DB_NAME="gas_control_database"
```

## Tests
To run tests:

```
docker compose exec -w /app gas-control-api pytest -v
```