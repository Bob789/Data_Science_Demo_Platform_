# Scripts Directory

Utility scripts for managing and maintaining the ML Model Training Platform.

---

## Available Scripts

### setup_admin.py

**Purpose:** Interactive command-line tool for managing admin privileges.

**When to Use:**
- Initial platform setup to create the first admin user
- Grant admin privileges to existing users
- Revoke admin privileges from users

**Usage:**
```bash
python scripts/setup_admin.py
```

**Requirements:**
- Database must be running and accessible
- Environment variables must be configured in `.env`
- At least one user account must exist (create via web signup)

**Features:**
- Lists all users with their current admin status
- Displays token balances
- Interactive username input
- Confirmation prompts for safety
- Works with existing database schema

**Example Session:**
```
============================================================
  ML PLATFORM - ADMIN SETUP TOOL
============================================================

============================================================
CURRENT USERS
============================================================
ID    Username             Tokens     Admin     
------------------------------------------------------------
1     john_doe             45         NO        
2     jane_smith           100        NO        
3     admin_user           50         YES       
============================================================

Enter the username you want to grant admin privileges to:
(or type 'exit' to quit)
Username: john_doe

You are about to grant admin privileges to user: john_doe
Admin users will have access to:
  - View all users and their token balances
  - View system activity logs
  - View all trained models
  - Access sensitive system statistics

Are you sure? (yes/no): yes

Admin privileges granted to 'john_doe' successfully!

User 'john_doe' can now access the Admin Panel!
They will need to logout and login again for changes to take effect.

============================================================
Setup complete. Press Enter to exit...
```

**Admin Capabilities:**
Once a user has admin privileges, they can:
- View all users and their details
- Create, update, and delete user accounts
- View complete system activity logs
- Manage token balances for any user
- Access token distribution analytics
- Delete any trained model

---

## Environment Variables

Scripts require the following environment variables (set in `.env`):

| Variable | Description | Example |
|----------|-------------|---------|
| DB_HOST | PostgreSQL host | localhost |
| DB_PORT | PostgreSQL port | 5432 |
| DB_NAME | Database name | ml_platform |
| DB_USER | Database username | postgres |
| DB_PASSWORD | Database password | your_password |

---

## Adding New Scripts

When adding new utility scripts:

1. Place in the `scripts/` directory
2. Add comprehensive docstring at the top
3. Include error handling for database operations
4. Add usage documentation to this README
5. Follow existing code patterns

**Template:**
```python
# File: scripts/your_script.py
"""
Script Name

Brief description of what the script does.

Usage:
    python scripts/your_script.py [options]

Environment Variables Required:
    - DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app_fastapi import database_manager as db

def main():
    """Main entry point."""
    try:
        # Ensure database connection
        db.create_database_if_not_exists()
        
        # Your script logic here
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

---

## Future Scripts (Planned)

- `backup_database.py` - Automated database backup
- `export_models.py` - Export trained models with metadata
- `cleanup_logs.py` - Archive old usage logs
- `reset_tokens.py` - Bulk token reset utility

---

*Last Updated: 2025-11-27*
