# Database Schema

This document describes the PostgreSQL database schema for the ML Model Training Platform.

---

## Overview

The platform uses PostgreSQL for persistent data storage, managing:
- User accounts and authentication
- Token balances for the payment system
- Usage activity logging

**Database Name:** Configured via `DB_NAME` environment variable

---

## Tables

### users

Stores user account information.

```sql
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    user_name VARCHAR(100) UNIQUE NOT NULL,
    user_password TEXT NOT NULL,
    tokens INT DEFAULT 10,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| user_id | SERIAL | PRIMARY KEY | Auto-incrementing user identifier |
| user_name | VARCHAR(100) | UNIQUE, NOT NULL | Username for login |
| user_password | TEXT | NOT NULL | bcrypt-hashed password |
| tokens | INT | DEFAULT 10 | Token balance for operations |
| is_admin | BOOLEAN | DEFAULT FALSE | Admin privilege flag |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Account creation time |

**Indexes:**
- Primary key on `user_id`
- Unique constraint on `user_name` (implicit index)

---

### usage_logs

Tracks all system activity for auditing and analytics.

```sql
CREATE TABLE IF NOT EXISTS usage_logs (
    log_id SERIAL PRIMARY KEY,
    user_name VARCHAR(100) NOT NULL,
    action VARCHAR(50) NOT NULL,
    tokens_changed INT DEFAULT 0,
    status VARCHAR(20) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    details TEXT
);
```

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| log_id | SERIAL | PRIMARY KEY | Auto-incrementing log identifier |
| user_name | VARCHAR(100) | NOT NULL | Username who performed action |
| action | VARCHAR(50) | NOT NULL | Action type (see action types below) |
| tokens_changed | INT | DEFAULT 0 | Token delta (negative = spent) |
| status | VARCHAR(20) | NOT NULL | SUCCESS or FAILED |
| timestamp | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | When action occurred |
| details | TEXT | | Additional information |

**Action Types:**
- `MODEL_TRAINING` - User trained a model (-1 token)
- `PREDICTION` - User made a prediction (-5 tokens)
- `TOKEN_PURCHASE` - User purchased tokens (+N tokens)
- `MODEL_DELETION` - User deleted a model (0 tokens)
- `TOKEN_REFUND` - System refunded tokens after failure (+N tokens)

---

## Entity Relationship Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                          users                               │
├──────────────────────────────────────────────────────────────┤
│ PK │ user_id        │ SERIAL                                │
│    │ user_name      │ VARCHAR(100) UNIQUE NOT NULL          │
│    │ user_password  │ TEXT NOT NULL                         │
│    │ tokens         │ INT DEFAULT 10                        │
│    │ is_admin       │ BOOLEAN DEFAULT FALSE                 │
│    │ created_at     │ TIMESTAMP DEFAULT CURRENT_TIMESTAMP   │
└──────────────────────────────────────────────────────────────┘
         │
         │ user_name (logical reference)
         ▼
┌──────────────────────────────────────────────────────────────┐
│                       usage_logs                             │
├──────────────────────────────────────────────────────────────┤
│ PK │ log_id         │ SERIAL                                │
│    │ user_name      │ VARCHAR(100) NOT NULL                 │
│    │ action         │ VARCHAR(50) NOT NULL                  │
│    │ tokens_changed │ INT DEFAULT 0                         │
│    │ status         │ VARCHAR(20) NOT NULL                  │
│    │ timestamp      │ TIMESTAMP DEFAULT CURRENT_TIMESTAMP   │
│    │ details        │ TEXT                                  │
└──────────────────────────────────────────────────────────────┘
```

**Note:** There is a logical relationship between `usage_logs.user_name` and `users.user_name`, but no foreign key constraint is enforced to allow log retention when users are deleted.

---

## Connection Configuration

Database connection is configured via environment variables:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ml_platform
DB_USER=postgres
DB_PASSWORD=your_password
```

**Connection Management:**
- Uses `psycopg2` for PostgreSQL connections
- Context manager (`get_connection()`) ensures proper cleanup
- Automatic database creation if not exists

---

## Common Queries

### Get User by Username
```sql
SELECT user_id, user_name, user_password, tokens, is_admin
FROM users
WHERE user_name = %s;
```

### Update Token Balance
```sql
UPDATE users
SET tokens = tokens + %s
WHERE user_name = %s AND tokens + %s >= 0;
```

### Get User Activity
```sql
SELECT * FROM usage_logs
WHERE user_name = %s
ORDER BY timestamp DESC
LIMIT %s;
```

### Get All Users (Admin)
```sql
SELECT * FROM users
ORDER BY user_id;
```

---

## Data Integrity

### Password Storage
- Passwords are hashed using bcrypt via `passlib`
- Never stored in plain text
- Verification uses constant-time comparison

### Token Balance Protection
- Balance cannot go negative (enforced in UPDATE query)
- Failed operations trigger automatic refunds
- All token changes are logged

### Audit Trail
- All significant actions are logged to `usage_logs`
- Logs include success/failure status
- Timestamp allows activity analysis

---

## Migration Notes

### Initial Setup
Tables are created automatically on first run:
```python
from app_fastapi import database_manager as db

db.create_database_if_not_exists()
db.create_users_table()
db.create_usage_logs_table()
```

### Schema Changes
No automated migration system is currently implemented. For schema changes:
1. Back up existing data
2. Apply changes manually via SQL
3. Update corresponding Python code

### Recommended Production Improvements
- Add foreign key constraint from `usage_logs` to `users`
- Add index on `usage_logs.user_name` for query performance
- Add index on `usage_logs.timestamp` for time-based queries
- Consider table partitioning for logs at scale

---

## Backup and Recovery

### Backup Command
```bash
pg_dump -U $DB_USER -h $DB_HOST -d $DB_NAME > backup.sql
```

### Restore Command
```bash
psql -U $DB_USER -h $DB_HOST -d $DB_NAME < backup.sql
```

---

*Last Updated: 2025-11-27*
