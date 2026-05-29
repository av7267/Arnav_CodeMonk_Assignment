# Codemonk Backend Intern Assignment

A robust backend service for managing users and processing large blocks of text to find word frequencies, built with Django, Django REST Framework, PostgreSQL, Redis, and Celery.

## Prerequisites

- Docker
- Docker Compose

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd codemonk-backend
   ```

2. **Setup Environment Variables:**
   Copy the example environment file to `.env`:
   ```bash
   cp .env.example .env
   ```
   *Note: In a production environment, you would fill out the `.env` file with secure, real secrets.*

3. **Run the Services:**
   Use Docker Compose to build and start all containers:
   ```bash
   docker compose up --build
   ```
   *This will start the `web` (Django), `db` (Postgres), `redis`, and `celery` worker services.*

4. **Run Database Migrations:**
   In a new terminal window, execute the following command to apply database migrations:
   ```bash
   docker compose exec web python manage.py migrate
   ```

5. **Access the Application & API Docs:**
   - **API Base URL:** `http://localhost:8000/api/v1/`
   - **Swagger UI Documentation:** `http://localhost:8000/api/schema/swagger-ui/`

## Architecture Overview

- **Web (Django + DRF):** Handles incoming HTTP requests, user authentication (JWT), and API routing.
- **Database (PostgreSQL):** Persistently stores user accounts, paragraphs, and word frequency counts.
- **Message Broker (Redis):** Acts as the queue for background tasks to be picked up.
- **Worker (Celery):** Processes text in the background (counting word frequencies) so the main web server isn't blocked by slow operations.

## Available Endpoints

Check the Swagger UI (`/api/schema/swagger-ui/`) for detailed interactive documentation.

### Authentication
- `POST /api/v1/auth/register/` - Register a new user account (returns user info).
- `POST /api/v1/auth/login/` - Login with email/password (returns JWT access/refresh tokens).
- `POST /api/v1/auth/token/refresh/` - Refresh an expired access token.

### Paragraphs (Requires Auth Token)
- `POST /api/v1/paragraphs/` - Submit a large block of text. It is split into paragraphs and processed asynchronously in the background. (Returns 202 Accepted).
- `GET /api/v1/paragraphs/search/?word=<word>` - Find the top 10 paragraphs where the specific word appears the most.

## Testing Guide (Swagger UI)

Testing the API through the Swagger UI (`/api/schema/swagger-ui/`) is the easiest way to interact with the system. Follow these steps:

### 1. Register a New User
1. Click on **`POST /api/v1/auth/register/`** to expand it.
2. Click **"Try it out"**.
3. Fill in the JSON body with your details (e.g., `name`, `email`, `date_of_birth`, and a strong `password`).
4. Click **"Execute"**. You should receive a `201` status code with your user profile data.

### 2. Log In & Get Your Token
1. Click on **`POST /api/v1/auth/login/`** to expand it, and click **"Try it out"**.
2. Enter the `email` and `password` you just created.
3. Click **"Execute"**. The response will contain an `"access"` token and a `"refresh"` token.
4. **Copy the `"access"` token string** (without quotes).

### 3. Authenticate the UI
1. Scroll to the top of the page and click the green **"Authorize"** button.
2. In the `Value` field, type `Bearer ` followed by your access token (e.g., `Bearer eyJhbGci...`).
3. Click **"Authorize"** and then **"Close"**. The padlock icons on the endpoints should now be locked.

### 4. Submit Text
1. Expand **`POST /api/v1/paragraphs/`** and click **"Try it out"**.
2. In the `text` field, paste a large block of text. Ensure paragraphs are separated by a double newline (`\n\n`).
3. Click **"Execute"**. You will receive a `202 Accepted` response. Celery is now counting word frequencies in the background!

### 5. Search for Words
1. Expand **`GET /api/v1/paragraphs/search/`** and click **"Try it out"**.
2. In the `word` parameter field, type a word that exists in the text you submitted.
3. Click **"Execute"**. You will receive a ranked list of the top 10 paragraphs where the word appears the most!
# Arnav_CodeMonk_Assignment
