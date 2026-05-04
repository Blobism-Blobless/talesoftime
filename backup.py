import sqlite3
import os
from datetime import datetime
from flask import current_app


def backup_sqlite_db():
    """
    Creates a timestamped backup of the SQLite database
    using the official SQLite backup API.
    """

    # 1.Define paths
    db_path = os.path.join(current_app.instance_path, 'tales_of_time.db')
    backup_dir = os.path.join(current_app.instance_path, 'backups')

    # 2.Ensure backup directory exists
    os.makedirs(backup_dir, exist_ok=True)

    #3.Create timestamped filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = os.path.join(
        backup_dir,
        f'talesoftime_backup_{timestamp}.db'
    )

    try:
        # 4.Perform the live atomic backup
        source = sqlite3.connect(db_path)
        dest = sqlite3.connect(backup_path)

        with dest:
            source.backup(dest)

        source.close()
        dest.close()

        print(f"SUCCESS: Backup created at {backup_path}")
        return backup_path

    except Exception as e:
        print(f"FAILED: Backup error: {str(e)}")
        return None


# --- SELF-EXECUTION LOGIC ---
if __name__ == "__main__":
    try:
        #Import the Flask app factory
        from app import create_app

        #Create app and run backup inside its context
        app = create_app()

        with app.app_context():
            print("Starting automated backup process...")
            result = backup_sqlite_db()

            if result:
                print("Process completed successfully.")
            else:
                print("Process failed.")

    except ImportError:
        print("ERROR: Could not find 'app.py' or 'create_app()'.")
        print("Make sure this script is in the root folder alongside app.py.")

    except Exception as e:
        print(f"CRITICAL ERROR: {str(e)}")