# File: scripts/setup_admin.py
"""
Admin Setup Script for ML Model Training Platform

This script provides an interactive command-line interface for managing
admin privileges in the ML Platform. It allows granting or revoking
admin access to existing user accounts.

Usage:
    python scripts/setup_admin.py

Environment Variables Required:
    - DB_HOST: PostgreSQL server hostname (e.g., localhost)
    - DB_PORT: PostgreSQL server port (e.g., 5432)
    - DB_USER: Database username
    - DB_PASSWORD: Database password
    - DB_NAME: Target database name

Prerequisites:
    - PostgreSQL database must be running and accessible
    - At least one user account must exist (create via web signup)
    - Environment variables must be configured in .env file

What This Script Does:
    1. Connects to the PostgreSQL database
    2. Creates required tables if they don't exist
    3. Displays all registered users with their current status
    4. Prompts for username to grant/revoke admin privileges
    5. Confirms action before making changes

Admin Privileges Include:
    - View all users and their token balances
    - Create, update, and delete user accounts
    - View complete system activity logs
    - Access token distribution analytics
    - Delete any trained model

Security Notes:
    - Admin users can modify any user's data
    - Admin users can view sensitive system information
    - Grant admin access only to trusted users
    - Users must logout and login for changes to take effect
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app_fastapi import database_manager as db

def list_users():
    """Display all users in the database."""
    users = db.select_all_users()

    if not users:
        print("No users found in the database.")
        print("Please create a user account first by signing up in the web interface.")
        return []

    print("\n" + "="*60)
    print("CURRENT USERS")
    print("="*60)
    print(f"{'ID':<5} {'Username':<20} {'Tokens':<10} {'Admin':<10}")
    print("-"*60)

    for user in users:
        # user structure: (user_id, user_name, user_password, tokens, created_at, is_admin)
        user_id = user[0]
        username = user[1]
        tokens = user[3]
        is_admin = user[5] if len(user) > 5 else False
        admin_status = "YES" if is_admin else "NO"

        print(f"{user_id:<5} {username:<20} {tokens:<10} {admin_status:<10}")

    print("="*60 + "\n")
    return users

def set_admin():
    """Interactive function to set admin privileges."""
    print("\nADMIN SETUP TOOL")
    print("="*60)

    # List all users
    users = list_users()

    if not users:
        return

    # Get username input
    print("Enter the username you want to grant admin privileges to:")
    print("(or type 'exit' to quit)")
    username = input("Username: ").strip()

    if username.lower() == 'exit':
        print("Exiting...")
        return

    # Check if user exists
    user_exists = any(user[1] == username for user in users)

    if not user_exists:
        print(f"\nUser '{username}' not found in the database.")
        print("Please check the spelling or create the user account first.")
        return

    # Check current admin status
    is_currently_admin = db.check_user_is_admin(username)

    if is_currently_admin:
        print(f"\nUser '{username}' is already an admin!")
        response = input("Do you want to REVOKE admin privileges? (yes/no): ").strip().lower()

        if response == 'yes':
            result = db.set_user_admin(username, False)
            print(f"\n{result}")
        else:
            print("\nOperation cancelled.")
    else:
        print(f"\nYou are about to grant admin privileges to user: {username}")
        print("Admin users will have access to:")
        print("  - View all users and their token balances")
        print("  - View system activity logs")
        print("  - View all trained models")
        print("  - Access sensitive system statistics")

        response = input("\nAre you sure? (yes/no): ").strip().lower()

        if response == 'yes':
            result = db.set_user_admin(username, True)
            print(f"\n{result}")
            print(f"\nUser '{username}' can now access the Admin Panel!")
            print("They will need to logout and login again for changes to take effect.")
        else:
            print("\nOperation cancelled.")

def main():
    """Main function."""
    print("\n" + "="*60)
    print("  ML PLATFORM - ADMIN SETUP TOOL")
    print("="*60)

    try:
        # Ensure database exists
        db.create_database_if_not_exists()
        db.create_users_table()

        # Run setup
        set_admin()

    except Exception as e:
        print(f"\nError: {e}")
        print("Please make sure the database is running and configured correctly.")

    print("\n" + "="*60)
    print("Setup complete. Press Enter to exit...")
    input()

if __name__ == "__main__":
    main()