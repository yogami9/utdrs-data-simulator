# UTDRS Data Simulator

A data simulation service for the Unified Threat Detection and Response System (UTDRS) that generates realistic security event data and attack scenarios.

## Features

- Simulates network traffic, endpoint events, authentication logs, and cloud activity
- Generates complete attack scenarios (phishing, ransomware, data exfiltration, etc.)
- Sends events to the UTDRS API Gateway for processing
- Provides API endpoints to control simulations
- Scheduled background simulations

## Integration

This service integrates with:

- API Gateway: https://utdrs-api-gateway.onrender.com
- Core Engine: https://utdrs-core-engine.onrender.com
- Response Service: https://response-service.onrender.com

## Getting Started

### Prerequisites

- Docker and Docker Compose (for local development)
- MongoDB database

### Local Development

1. **Clone the repository**

```bash
git clone <repository-url>
cd utdrs-data-simulator
```

2. **Configure environment variables**

```bash
cp .env.example .env
# Edit .env with your settings
```

3. **Run using Docker Compose**

```bash
docker-compose up
```

The API will start running at `http://localhost:8000`, and you can access the API documentation at `http://localhost:8000/docs`.

## API Endpoints

- **GET /health** - Health check endpoint
- **GET /api/scenarios** - List available attack scenarios
- **POST /api/simulation/start** - Start a simulation
- **POST /api/simulation/stop** - Stop a simulation
- **GET /api/simulation/status** - Get simulation status

## Deployment on Render

1. Push the code to a Git repository
2. Create a new Web Service on Render
3. Connect to your Git repository
4. Select 'Docker' as the environment
5. Configure environment variables (see .env.example)
