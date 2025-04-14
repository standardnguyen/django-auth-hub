# Django Auth Hub - Database Schema Documentation

## Overview
This document details the database schema for the Django Authentication Hub system. The schema consists of three primary models designed to handle user authentication, invite-based registration, and JWT token management.

## Database Models

### 1. User Model
This model extends Django's AbstractUser model to manage user accounts.

| Field | Type | Description | Constraints |
|-------|------|-------------|------------|
| id | AutoField | Primary key | Primary Key, Auto-increment |
| username | CharField | Unique username | Unique, Max length: 150 |
| email | EmailField | User's email address | Unique |
| password | CharField | Hashed password | - |
| first_name | CharField | User's first name | Optional, Max length: 150 |
| last_name | CharField | User's last name | Optional, Max length: 150 |
| date_joined | DateTimeField | Account creation timestamp | Auto-created |
| last_login | DateTimeField | Last login timestamp | Nullable |
| is_active | BooleanField | Account active status | Default: True |
| is_staff | BooleanField | Staff status for admin site | Default: False |
| is_admin | BooleanField | Admin privileges for operations | Default: False |

**Indexes:**
- Username (B-tree, unique)
- Email (B-tree, unique)

### 2. Invite Code Model
This model manages invite codes for new user registration.

| Field | Type | Description | Constraints |
|-------|------|-------------|------------|
| id | AutoField | Primary key | Primary Key, Auto-increment |
| code | CharField | Unique invite code string | Unique, Max length: 64 |
| created_by | ForeignKey | Reference to user who created the code | References User.id, CASCADE on delete |
| used_by | ForeignKey | Reference to user who used the code | References User.id, SET_NULL on delete, Nullable |
| created_at | DateTimeField | Creation timestamp | Auto-created |
| used_at | DateTimeField | Usage timestamp | Nullable |
| expires_at | DateTimeField | Expiration timestamp | - |
| is_valid | BooleanField | Validity status | Default: True |

**Indexes:**
- Code (B-tree, unique)
- Created_by (B-tree)
- Used_by (B-tree)
- Is_valid + Expires_at (Composite, for querying valid codes)

### 3. Token Record Model
This model tracks JWT tokens for potential invalidation.

| Field | Type | Description | Constraints |
|-------|------|-------------|------------|
| id | AutoField | Primary key | Primary Key, Auto-increment |
| user | ForeignKey | Associated user | References User.id, CASCADE on delete |
| jti | CharField | JWT token identifier | Max length: 255 |
| created_at | DateTimeField | Token creation timestamp | Auto-created |
| expires_at | DateTimeField | Token expiration timestamp | - |
| is_valid | BooleanField | Token validity status | Default: True |

**Indexes:**
- User + Is_valid (Composite, for user token validation)
- JTI (B-tree, for specific token lookup)

## Relationships

1. **User to Invite Codes (created):**
   - One-to-many relationship
   - A user can create multiple invite codes
   - Each invite code is created by exactly one user

2. **User to Invite Codes (used):**
   - One-to-one relationship
   - A user account is created using exactly one invite code
   - Each invite code can be used by at most one user

3. **User to Token Records:**
   - One-to-many relationship
   - A user can have multiple token records
   - Each token record belongs to exactly one user

## Database Configuration
- **Engine:** PostgreSQL 17
- **Character Set:** UTF-8
- **Collation:** UTF-8, case-insensitive

## Schema Migration
The initial schema will be created using Django's migration system:
```
python manage.py makemigrations authentication
python manage.py migrate
```

## Constraints and Validations
- Email addresses must be valid format
- Passwords must meet Django's default password validation requirements
- Invite codes must be unique
- Token JTIs must be unique per user