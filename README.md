# Project Apex: Development Roadmap

This document outlines the detailed steps and instructions to build Project Apex, an agentic AI companion for empowering women in Indian Science & Technology.

## 1. Project Overview

Project Apex is an agentic AI solution designed to serve as a confidential, 24/7 "pocket friend" for women scientists in India's premier government organizations. It provides instant, actionable support by interpreting policies, automating documentation, guiding users through official procedures, and offering a safe space for wellness support.

## 2. Technology Stack

*   **Frontend**: Next.js (React)
*   **Backend**: Python with CrewAI & FastAPI
*   **Database**: PostgreSQL
*   **Deployment**: Docker (recommended)

## 3. Project Setup & Prerequisites

Ensure you have the following installed on your system:
*   Node.js (v18 or later)
*   Python (v3.9 or later)
*   PostgreSQL
*   Docker and Docker Compose (optional, but recommended for easier setup)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd apex
```

### Step 2: Database Setup

1.  **Start PostgreSQL**: Ensure your PostgreSQL server is running.
2.  **Create Database**: Create a new database for the project.
    ```sql
    CREATE DATABASE apex_db;
    ```
3.  **Environment Variables**: Create a `.env` file in the `backend` directory and add the database connection details.
    ```
    DATABASE_URL="postgresql://user:password@localhost/apex_db"
    ```

### Step 3: Backend Setup (Python/CrewAI)

1.  **Navigate to Backend Directory**:
    ```bash
    cd backend
    ```
2.  **Create a Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install Dependencies**: Create a `requirements.txt` file with the following content and install it.
    ```txt
    crewai
    fastapi
    uvicorn
    psycopg2-binary
    python-dotenv
    # Add other necessary packages
    ```
    ```bash
    pip install -r requirements.txt
    ```

### Step 4: Frontend Setup (Next.js)

1.  **Navigate to Frontend Directory**:
    ```bash
    cd ../frontend
    ```
2.  **Install Dependencies**:
    ```bash
    npm install
    ```
3.  **Environment Variables**: Create a `.env.local` file in the `frontend` directory to store the backend API URL.
    ```
    NEXT_PUBLIC_API_URL=http://localhost:8000/api
    ```

## 4. Development Phases

### Phase 1: Backend - Agents & API

1.  **Agent Development (`backend/agents`)**:
    *   **Policy Agent (`athena.py`)**: Develop the agent trained on the knowledge base of HR policies, POSH Act, etc.
    *   **Workflow Agent (`scribe.py`)**: Develop the agent with tools for form generation and process guidance.
    *   **Wellness Agent (`asha.py`)**: Develop the agent fine-tuned for empathetic conversations.
    *   **Orchestrator (`main_crew.py`)**: Create the main CrewAI crew that orchestrates the other agents based on user intent.
2.  **API Development (`backend/main.py`)**:
    *   Use FastAPI to create API endpoints.
    *   Create an endpoint (e.g., `/api/chat`) that takes a user query and passes it to the Orchestrator agent.
    *   The endpoint should return the agent's response to the frontend.

### Phase 2: Database Schema & Models

1.  **Define Schema**: Design the SQL schema for:
    *   `users` (secure login information)
    *   `cases` (grievances, requests, with status and history)
    *   `documents` (generated forms and uploads)
    *   `conversations` (chat logs, especially for anonymous mode)
2.  **Implement Models**: Use an ORM like SQLAlchemy (optional) to interact with the database from the Python backend.

### Phase 3: Frontend - UI/UX

1.  **Component Development (`frontend/components`)**:
    *   Build reusable React components for the UI elements described in the `UI_README.md` (e.g., ChatWindow, DashboardCard, CaseTracker).
2.  **Page Development (`frontend/app`)**:
    *   Create pages for Login, Dashboard, Chat, Case Center, and the Resource Hub.
3.  **API Integration**:
    *   Use a library like `axios` or `fetch` to connect the frontend to the backend FastAPI endpoints.
    *   Implement state management (e.g., React Context or Zustand) to handle application state.

### Phase 4: Integration & Testing

1.  **End-to-End Testing**: Test the full user flow, from a user asking a question on the frontend to getting a response from the backend agents.
2.  **Security Audit**: Ensure all data, especially sensitive user information, is handled securely.
3.  **User Acceptance Testing (UAT)**: Get feedback from potential users.

## 5. Running the Project

1.  **Start the Backend Server**:
    ```bash
    cd backend
    uvicorn main:app --reload
    ```
    The backend will be available at `http://localhost:8000`.

2.  **Start the Frontend Server**:
    ```bash
    cd frontend
    npm run dev
    ```
    The frontend will be available at `http://localhost:3000`.

## 6. Proposed Folder Structure

```
apex/
├── backend/
│   ├── agents/
│   │   ├── athena.py
│   │   ├── scribe.py
│   │   └── asha.py
│   ├── knowledge_base/
│   │   └── (policy documents, etc.)
│   ├── main.py             # FastAPI app
│   ├── main_crew.py        # CrewAI setup
│   ├── requirements.txt
│   └── venv/
├── frontend/
│   ├── app/
│   │   ├── dashboard/
│   │   ├── chat/
│   │   └── layout.js
│   ├── components/
│   │   ├── ui/
│   │   └── ChatWindow.js
│   ├── public/
│   └── package.json
├── .gitignore
└── README.md
```
