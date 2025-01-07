Voting App

A full-stack voting application built with FastAPI for the backend and React for the frontend, containerized using Docker and managed with Docker Compose.

📁 Project Structure

pythonProject4/
├── app/                   # Backend application
│   ├── main.py            # FastAPI backend logic
│   ├── requirements.txt   # Backend dependencies
│   ├── unit_tests.py      # Backend unit tests
│
├── frontend/              # Frontend application
│   ├── public/
│   │   ├── index.html     # Root HTML file
│   ├── src/
│   │   ├── api.js         # API integration
│   │   ├── App.js         # Main React component
│   │   ├── config.js      # Configurations (API URL, etc.)
│   │   ├── index.css      # Global styles
│   │   ├── index.js       # Entry point for React app
│   ├── .env              # Environment variables for frontend
│   ├── Dockerfile        # Dockerfile for frontend
│   ├── package.json      # Frontend dependencies
│   ├── package-lock.json # Lock file for dependencies
│
├── integration_test     # Integration tests
│
├── venv/                 # Python virtual environment
│
├── conf/                 # Configuration files (e.g., Nginx, environment configs)
│
├── docker-compose.yml    # Docker Compose configuration
├── Dockerfile            # Main Dockerfile for the application
├── nginx.conf            # Nginx configuration for reverse proxy
├── README.md             # Documentation

🚀 Getting Started

Clone the Repository

git clone https://github.com/EASS-HIT-PART-A-2024-CLASS-VI/Voting-App---Guy-Bloch.git
cd voting-app

Environment Setup

Backend

cd app
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

Frontend

cd frontend
npm install

Run with Docker Compose

docker-compose up --build

Access the Application

Frontend: http://localhost:3000

Backend API: http://localhost:8000

🧪 Testing

Unit Tests

Purpose: Test individual components of the backend (e.g., API routes, services).

File: app/unit_tests.py

Run Command (Bash):

pytest app/unit_tests.py

Run Command (Docker):

docker-compose run unit_tests

Integration Tests

Purpose: Test the interaction between components to ensure they work together.

File: integration_test.py

Run Command (Bash):

pytest integration_test.py

Run Command (Docker):

docker-compose run integration_test

Run both tests : 

docker-compose up unit_tests integration_tests


📜 API Endpoints

POST /candidates/ - Add a new candidate

GET /candidates/ - List all candidates

POST /vote/ - Cast a vote

DELETE /candidates/{id} - Delete a candidate

GET /results/ - Get voting results

📦 Deployment

Make sure to adjust the environment variables and run:

docker-compose -f docker-compose.prod.yml up --build

🛠️ Built With

FastAPI: Backend

React: Frontend

Docker: Containerization

Nginx: Reverse Proxy

Pytest: Testing Framework

🤝 Contributing

Feel free to fork this repository, make changes, and submit a pull request!

👤 Author

Guy Bloch
