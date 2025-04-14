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

1. Install [pyenv](https://github.com/pyenv/pyenv).

2. Install Python 3.13.2 if it isn't the default version
   ```
   pyenv install 3.13.2
   ```

3. Install PostgreSQL development libraries first:
   ```
   # Ubuntu/Debian
   sudo apt install -y postgresql-common
   sudo /usr/share/postgresql-common/pgdg/apt.postgresql.org.sh
   sudo apt install postgresql-17 postgresql-server-dev-17
   ```

4. Clone the repository:
   ```bash
   git clone https://github.com/standardnguyen/django-auth-hub.git
   cd django-auth-hub
   ```

5. Set your Python environment:
   ```
   pyenv local 3.13.2
   python -m venv venv
   ```

6. Activate the environment:
   ```
   source venv/bin/activate  # on macOS/Linux
   # or
   venv\Scripts\activate  # on Windows
   
   # Now just use 'python' and 'pip'
   python --version  # Should show 3.13.0
   pip install -r requirements.txt
   ```


todo:

starting a postgresql database on local

getting the initial migrations... not sure how to do that