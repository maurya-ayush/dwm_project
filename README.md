# Data Quality Monitoring Project

This project sets up a data quality monitoring system using Apache Airflow, Great Expectations, PostgreSQL, and Streamlit.

## Prerequisites

- Docker and Docker Compose installed
- At least 4GB of RAM available
- At least 2 CPUs available
- At least 10GB of disk space available

## Project Structure

```
.
├── airflow/
│   ├── dags/          # Airflow DAG files
│   ├── logs/          # Airflow logs
│   ├── config/        # Airflow configuration
│   └── plugins/       # Airflow plugins
├── great_expectations/ # Great Expectations configuration and expectations
├── postgres-init/     # PostgreSQL initialization scripts
├── streamlit/        # Streamlit application
└── docker-compose.yml # Docker Compose configuration
```

## Setup Instructions

1. Create a `.env` file in the project root with the following content:
```bash
AIRFLOW_UID=50000
_AIRFLOW_WWW_USER_USERNAME=admin
_AIRFLOW_WWW_USER_PASSWORD=admin
```

2. Create required directories:
```bash
mkdir -p airflow/{dags,logs,config,plugins}
```

3. Set proper permissions:
```bash
chmod -R 775 airflow
```

## Running the Project

1. Start all services:
```bash
docker-compose up -d
```

2. Monitor the logs:
```bash
docker-compose logs -f
```

## Accessing the Services

- **Airflow UI**: http://localhost:8080
  - Username: admin
  - Password: admin

- **Flower (Celery Monitoring)**: http://localhost:5555

- **Streamlit App**: http://localhost:8501

- **PgAdmin**: http://localhost:5050
  - Email: admin@dq.com
  - Password: admin123

## Service Details

### Airflow
- Uses CeleryExecutor for distributed task execution
- Includes Great Expectations integration
- Configured with PostgreSQL as metadata database
- Redis as Celery broker

### PostgreSQL
- Database name: airflow
- Username: airflow
- Password: airflow
- Port: 5432

### Streamlit
- Python 3.9 based application
- Includes plotly for visualizations
- Connected to PostgreSQL database

## Troubleshooting

1. If services fail to start, check the logs:
```bash
docker-compose logs [service_name]
```

2. To restart a specific service:
```bash
docker-compose restart [service_name]
```

3. To rebuild and restart all services:
```bash
docker-compose down
docker-compose up -d --build
```

4. If you encounter permission issues:
```bash
sudo chown -R 50000:0 airflow/
```

## Development

- The project uses a local version of Great Expectations mounted into the Airflow container
- Any changes to the great_expectations directory will be immediately reflected in the container
- DAGs can be added to the `airflow/dags` directory and will be automatically loaded

## Notes

- The setup uses CeleryExecutor for better scalability and reliability
- All services have health checks configured
- Services are configured to restart automatically on failure
- PostgreSQL data is persisted using Docker volumes