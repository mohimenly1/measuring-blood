#!/usr/bin/env python3
"""
Migration script helper
Run this script to initialize Alembic and create migrations
"""

import sys
import os
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

def init_alembic():
    """Initialize Alembic if not already initialized"""
    alembic_dir = backend_dir / "alembic"
    versions_dir = alembic_dir / "versions"
    
    if not alembic_dir.exists():
        print("Initializing Alembic...")
        os.system(f"cd {backend_dir} && alembic init alembic")
        print("Alembic initialized!")
    else:
        print("Alembic already initialized")

def create_migration(message: str = None):
    """Create a new migration"""
    if message:
        os.system(f"cd {backend_dir} && alembic revision --autogenerate -m '{message}'")
    else:
        os.system(f"cd {backend_dir} && alembic revision --autogenerate")

def upgrade_db(revision: str = "head"):
    """Upgrade database to a specific revision"""
    os.system(f"cd {backend_dir} && alembic upgrade {revision}")

def downgrade_db(revision: str = "-1"):
    """Downgrade database by one revision"""
    os.system(f"cd {backend_dir} && alembic downgrade {revision}")

def show_current_revision():
    """Show current database revision"""
    os.system(f"cd {backend_dir} && alembic current")

def show_history():
    """Show migration history"""
    os.system(f"cd {backend_dir} && alembic history")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("""
Usage:
    python migrate.py init              - Initialize Alembic
    python migrate.py create [message]  - Create a new migration
    python migrate.py upgrade [rev]     - Upgrade database (default: head)
    python migrate.py downgrade [rev]   - Downgrade database (default: -1)
    python migrate.py current           - Show current revision
    python migrate.py history           - Show migration history
        """)
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "init":
        init_alembic()
    elif command == "create":
        message = sys.argv[2] if len(sys.argv) > 2 else "Auto migration"
        create_migration(message)
    elif command == "upgrade":
        revision = sys.argv[2] if len(sys.argv) > 2 else "head"
        upgrade_db(revision)
    elif command == "downgrade":
        revision = sys.argv[2] if len(sys.argv) > 2 else "-1"
        downgrade_db(revision)
    elif command == "current":
        show_current_revision()
    elif command == "history":
        show_history()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

