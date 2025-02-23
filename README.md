# Voting App
                                         ![image](https://github.com/user-attachments/assets/91bb6bf3-1271-45a3-be53-5c97d0d7f948)

A full-stack voting application built with FastAPI for the backend and React for the frontend, containerized using Docker and managed with Docker Compose.

## 📁 Project Structure

```
VotingApp/
├── app/                   # Backend application
│   ├── main.py            # FastAPI backend logic
│   ├── requirements.txt   # Backend dependencies
│   ├── unit_tests.py      # Backend unit tests
├── frontend/              # Frontend application
│   ├── public/
│   │   ├── index.html     # Root HTML file
│   ├── src/
│   │   ├── api.js         # API integration
│   │   ├── App.js         # Main React component
│   │   ├── config.js      # Configurations (API URL, etc.)
│   │   ├── index.css      # Global styles
│   │   ├── index.js       # Entry point for React app
│   ├── Dockerfile        # Dockerfile for frontend
│   ├── package.json      # Frontend dependencies
│   ├── package-lock.json # Lock file for dependencies
│
├── integration_test.py    # Integration tests
│
├── docker-compose.yml    # Docker Compose configuration
├── Dockerfile            # Main Dockerfile for the application
├── README.md             # Documentation
```

## 🚀 Getting Started

### Clone the Repository
```bash
git clone https://github.com/EASS-HIT-PART-A-2024-CLASS-VI/Voting-App---Guy-Bloch.git
cd voting-app
```

### Environment Setup

#### Backend
```bash
cd app
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Frontend
```bash
cd frontend
npm install
```

### Run with Docker Compose
```bash
docker-compose up --build
```

### Access the Application
- **Frontend:** `http://localhost:3000
- **Backend API:** `http://localhost:8000/docs

## 🧪 Testing

### Unit Tests
- **Purpose:** Test individual components of the backend (e.g., API routes, services).
- **File:** `app/unit_tests.py`
- **Run Command (Bash):**
  ```bash
  pytest app/unit_tests.py
  ```
- **Run Command (Docker):**
  ```bash
     docker-compose run unit_tests
  ```

### Integration Tests
- **Purpose:** Test the interaction between components to ensure they work together.
- **File:** `integration_tests/integration_test.py`
- **Run Command (Bash):**
  ```bash
  pytest integration_test.py
  ```
- **Run Command (Docker):**
  ```bash
  docker-compose run integration_test
  ```

## 📜 API Endpoints
- **POST /candidates/** - Add a new candidate
- **GET /candidates/** - List all candidates
- **POST /vote/** - Cast a vote
- **DELETE /candidates/{id}** - Delete a candidate
- **GET /results/** - Get voting results

## 📦 Deployment
Make sure to adjust the environment variables and run:
```bash
docker-compose -f docker-compose.prod.yml up --build
```

## 🛠️ Built With
- **FastAPI:** Backend
- **React:** Frontend
- **mongoDB:** Data-Base
- **Docker:** Containerization
- **Pytest:** Testing Framework

## 🤝 Contributing
Feel free to fork this repository, make changes, and submit a pull request!

## 👤 Author
- **Guy Bloch**

