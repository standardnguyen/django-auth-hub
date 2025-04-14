# Django Auth Hub

A lightweight authentication hub built with Django and JWT for managing access across small business applications and side projects. Features invite-code registration, token invalidation, and Docker deployment configuration.

## Features

- **Centralized Authentication**: Single sign-on for multiple web applications
- **Invite-Only Registration**: Control user access with unique invite codes
- **JWT-Based Auth**: Secure token-based authentication with invalidation capabilities
- **PostgreSQL Backend**: Robust data storage with PostgreSQL 17
- **Docker Deployment**: Easy deployment via Docker containers

## Requirements

- Docker and Docker Compose
- PostgreSQL 17
- Python 3.13+
- Django 5.2+

## Quick Start

### Local Environment Setup

1. install [pyenv]( if 3.13 isn't your default python version)

pyenv install 3.13.2


1. Clone the repository:
   ```bash
   git clone https://github.com/standardnguyen/django-auth-hub.git
   cd django-auth-hub
   ```

2. Set your python environment
   ```
   pyenv local 3.13.2
   python -m venv venv
   ```

# Everything after this needs to be vetted, it was written by AI


2. Create a `.env` file in the project root with the following variables:
   ```
   SECRET_KEY=your_django_secret_key
   DEBUG=False
   ALLOWED_HOSTS=yourdomain.com,localhost,127.0.0.1
   
   # PostgreSQL Settings
   DB_NAME=auth_hub
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=your_host_address
   DB_PORT=5432
   
   # JWT Settings
   JWT_SECRET_KEY=your_jwt_secret_key
   JWT_ACCESS_TOKEN_LIFETIME=24h
   JWT_REFRESH_TOKEN_LIFETIME=7d
   
   # CORS Settings
   CORS_ALLOWED_ORIGINS=https://app1.yourdomain.com,https://app2.yourdomain.com
   ```

### Local Development

1. Build and run the Docker containers:
   ```bash
   docker-compose up -d
   ```

2. Create a superuser for initial setup:
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

3. Access the admin panel at `http://localhost:8000/admin` to generate your first invite code.

### Production Deployment on DigitalOcean

1. Provision a DigitalOcean Droplet (recommended: Ubuntu 22.04 with Docker pre-installed)

2. Configure your PostgreSQL connection settings in the `.env` file to connect to your DigitalOcean PostgreSQL 17 cluster

3. Deploy using Docker Compose:
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

4. Configure Nginx as a reverse proxy (see `nginx/nginx.conf` for example configuration)

## API Documentation

### Authentication Endpoints

- `POST /api/auth/register/` - Register a new user with invite code
  ```json
  {
    "username": "newuser",
    "email": "user@example.com",
    "password": "securepassword",
    "invite_code": "ABC123XYZ"
  }
  ```

- `POST /api/auth/login/` - Obtain JWT tokens
  ```json
  {
    "username": "existinguser",
    "password": "userpassword"
  }
  ```

- `POST /api/auth/refresh/` - Refresh access token
  ```json
  {
    "refresh": "your_refresh_token"
  }
  ```

- `POST /api/auth/logout/` - Invalidate tokens
  ```json
  {
    "refresh": "your_refresh_token"
  }
  ```

### Invite Management Endpoints

- `POST /api/invites/create/` - Generate new invite code (admin only)
  ```json
  {
    "expiration_days": 7
  }
  ```

- `GET /api/invites/list/` - List all invite codes (admin only)

### User Management Endpoints

- `GET /api/users/me/` - Get current user profile
- `GET /api/users/` - List all users (admin only)

## Client Integration

To integrate with client applications, include the JWT token in the Authorization header:

```javascript
// Example using fetch API
fetch('https://your-app-api.com/some-protected-endpoint', {
  headers: {
    'Authorization': 'Bearer ' + jwtToken,
    'Content-Type': 'application/json'
  }
})
```

## Security Considerations

- All communication must use HTTPS in production
- JWT tokens are set to expire after 24 hours by default
- Tokens can be invalidated from the admin interface or via the logout endpoint
- Password changes automatically invalidate all existing tokens for that user

## Development

### Database Migrations

```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

### Running Tests

```bash
docker-compose exec web python manage.py test
```
